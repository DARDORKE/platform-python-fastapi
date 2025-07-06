"""
WebSocket endpoints for real-time communication.
"""
import json
import asyncio
from typing import Dict, List, Optional, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.core.database import get_session
from app.core.redis import redis_client
from app.core.security import verify_token
from app.models.user import User
from app.services.user_service import UserService


router = APIRouter()


class ConnectionManager:
    """
    Gestionnaire de connexions WebSocket avancé.
    
    Fonctionnalités:
    - Gestion des connexions multiples
    - Groupes de connexions
    - Diffusion ciblée
    - Authentification WebSocket
    """
    
    def __init__(self):
        # Connexions actives: {user_id: {connection_id: websocket}}
        self.active_connections: Dict[int, Dict[str, WebSocket]] = {}
        
        # Groupes de connexions: {group_name: {user_id: connection_id}}
        self.groups: Dict[str, Dict[int, str]] = {}
        
        # Métadonnées des connexions
        self.connection_metadata: Dict[str, Dict] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int, connection_id: str):
        """Accepter une nouvelle connexion."""
        await websocket.accept()
        
        # Ajouter à la liste des connexions actives
        if user_id not in self.active_connections:
            self.active_connections[user_id] = {}
        
        self.active_connections[user_id][connection_id] = websocket
        
        # Stocker les métadonnées
        self.connection_metadata[connection_id] = {
            "user_id": user_id,
            "connected_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
        }
        
        # Notifier Redis de la nouvelle connexion
        await redis_client.sadd("online_users", user_id)
        await redis_client.publish("user_events", json.dumps({
            "type": "user_connected",
            "user_id": user_id,
            "connection_id": connection_id,
            "timestamp": datetime.now().isoformat()
        }))
    
    async def disconnect(self, user_id: int, connection_id: str):
        """Supprimer une connexion."""
        if user_id in self.active_connections:
            if connection_id in self.active_connections[user_id]:
                del self.active_connections[user_id][connection_id]
            
            # Supprimer l'utilisateur s'il n'a plus de connexions
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
                await redis_client.srem("online_users", user_id)
        
        # Supprimer des groupes
        for group_name, group_members in self.groups.items():
            if user_id in group_members and group_members[user_id] == connection_id:
                del group_members[user_id]
        
        # Supprimer les métadonnées
        if connection_id in self.connection_metadata:
            del self.connection_metadata[connection_id]
        
        # Notifier Redis de la déconnexion
        await redis_client.publish("user_events", json.dumps({
            "type": "user_disconnected",
            "user_id": user_id,
            "connection_id": connection_id,
            "timestamp": datetime.now().isoformat()
        }))
    
    async def send_personal_message(self, message: str, user_id: int):
        """Envoyer un message à un utilisateur spécifique."""
        if user_id in self.active_connections:
            # Envoyer à toutes les connexions de l'utilisateur
            for connection_id, websocket in self.active_connections[user_id].items():
                try:
                    await websocket.send_text(message)
                    # Mettre à jour l'activité
                    if connection_id in self.connection_metadata:
                        self.connection_metadata[connection_id]["last_activity"] = datetime.now().isoformat()
                except:
                    # Connexion fermée, la nettoyer
                    await self.disconnect(user_id, connection_id)
    
    async def broadcast_to_group(self, message: str, group_name: str):
        """Diffuser un message à un groupe."""
        if group_name in self.groups:
            for user_id, connection_id in self.groups[group_name].items():
                if user_id in self.active_connections:
                    if connection_id in self.active_connections[user_id]:
                        try:
                            await self.active_connections[user_id][connection_id].send_text(message)
                        except:
                            # Connexion fermée, la nettoyer
                            await self.disconnect(user_id, connection_id)
    
    async def broadcast_to_all(self, message: str):
        """Diffuser un message à toutes les connexions."""
        for user_id, connections in self.active_connections.items():
            for connection_id, websocket in connections.items():
                try:
                    await websocket.send_text(message)
                except:
                    # Connexion fermée, la nettoyer
                    await self.disconnect(user_id, connection_id)
    
    async def join_group(self, user_id: int, connection_id: str, group_name: str):
        """Rejoindre un groupe."""
        if group_name not in self.groups:
            self.groups[group_name] = {}
        
        self.groups[group_name][user_id] = connection_id
        
        # Notifier le groupe
        await self.broadcast_to_group(json.dumps({
            "type": "user_joined_group",
            "user_id": user_id,
            "group_name": group_name,
            "timestamp": datetime.now().isoformat()
        }), group_name)
    
    async def leave_group(self, user_id: int, group_name: str):
        """Quitter un groupe."""
        if group_name in self.groups and user_id in self.groups[group_name]:
            del self.groups[group_name][user_id]
            
            # Notifier le groupe
            await self.broadcast_to_group(json.dumps({
                "type": "user_left_group",
                "user_id": user_id,
                "group_name": group_name,
                "timestamp": datetime.now().isoformat()
            }), group_name)
    
    def get_online_users(self) -> List[int]:
        """Obtenir la liste des utilisateurs en ligne."""
        return list(self.active_connections.keys())
    
    def get_group_members(self, group_name: str) -> List[int]:
        """Obtenir les membres d'un groupe."""
        if group_name in self.groups:
            return list(self.groups[group_name].keys())
        return []
    
    def get_connection_count(self) -> int:
        """Obtenir le nombre total de connexions."""
        return sum(len(connections) for connections in self.active_connections.values())


# Instance globale du gestionnaire de connexions
manager = ConnectionManager()


async def get_current_user_from_token(token: str, session: AsyncSession) -> User:
    """Obtenir l'utilisateur depuis le token WebSocket."""
    try:
        user_id = verify_token(token)
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Token invalide")
        
        user_service = UserService(session)
        user = await user_service.get_by_id(int(user_id))
        
        if not user:
            raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
        
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Authentification échouée")


@router.websocket("/ws/notifications/{token}")
async def websocket_notifications(
    websocket: WebSocket,
    token: str,
    session: AsyncSession = Depends(get_session)
):
    """
    WebSocket pour les notifications en temps réel.
    
    Fonctionnalités:
    - Authentification par token
    - Notifications personnalisées
    - Gestion des déconnexions
    """
    
    try:
        # Authentifier l'utilisateur
        user = await get_current_user_from_token(token, session)
        
        # Générer un ID de connexion unique
        import uuid
        connection_id = str(uuid.uuid4())
        
        # Connecter l'utilisateur
        await manager.connect(websocket, user.id, connection_id)
        
        # Envoyer un message de bienvenue
        await websocket.send_text(json.dumps({
            "type": "welcome",
            "message": f"Bienvenue {user.first_name}!",
            "connection_id": connection_id,
            "timestamp": datetime.now().isoformat()
        }))
        
        # Envoyer les notifications en attente
        await send_pending_notifications(user.id, websocket)
        
        # Boucle de traitement des messages
        while True:
            try:
                # Recevoir les messages du client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Traiter selon le type de message
                await handle_websocket_message(message, user.id, connection_id)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Erreur: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }))
    
    except Exception as e:
        await websocket.close(code=4000, reason=str(e))
    finally:
        # Déconnecter l'utilisateur
        if 'user' in locals() and 'connection_id' in locals():
            await manager.disconnect(user.id, connection_id)


@router.websocket("/ws/chat/{room_id}/{token}")
async def websocket_chat(
    websocket: WebSocket,
    room_id: str,
    token: str,
    session: AsyncSession = Depends(get_session)
):
    """
    WebSocket pour le chat en temps réel.
    
    Fonctionnalités:
    - Salles de chat
    - Messages en temps réel
    - Historique des messages
    """
    
    try:
        # Authentifier l'utilisateur
        user = await get_current_user_from_token(token, session)
        
        # Générer un ID de connexion unique
        import uuid
        connection_id = str(uuid.uuid4())
        
        # Connecter l'utilisateur
        await manager.connect(websocket, user.id, connection_id)
        
        # Rejoindre la salle de chat
        await manager.join_group(user.id, connection_id, f"chat_{room_id}")
        
        # Envoyer l'historique des messages
        await send_chat_history(room_id, websocket)
        
        # Boucle de traitement des messages
        while True:
            try:
                # Recevoir les messages du client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Traiter le message de chat
                await handle_chat_message(message, room_id, user)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Erreur: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }))
    
    except Exception as e:
        await websocket.close(code=4000, reason=str(e))
    finally:
        # Déconnecter l'utilisateur
        if 'user' in locals() and 'connection_id' in locals():
            await manager.disconnect(user.id, connection_id)
            await manager.leave_group(user.id, f"chat_{room_id}")


async def handle_websocket_message(message: dict, user_id: int, connection_id: str):
    """Traiter les messages WebSocket."""
    
    message_type = message.get("type")
    
    if message_type == "ping":
        # Répondre au ping
        await manager.send_personal_message(json.dumps({
            "type": "pong",
            "timestamp": datetime.now().isoformat()
        }), user_id)
    
    elif message_type == "join_group":
        # Rejoindre un groupe
        group_name = message.get("group_name")
        if group_name:
            await manager.join_group(user_id, connection_id, group_name)
    
    elif message_type == "leave_group":
        # Quitter un groupe
        group_name = message.get("group_name")
        if group_name:
            await manager.leave_group(user_id, group_name)
    
    elif message_type == "broadcast":
        # Diffuser un message (admin seulement)
        # Vérifier les permissions ici
        await manager.broadcast_to_all(json.dumps({
            "type": "broadcast",
            "message": message.get("message"),
            "from_user": user_id,
            "timestamp": datetime.now().isoformat()
        }))


async def handle_chat_message(message: dict, room_id: str, user: User):
    """Traiter les messages de chat."""
    
    if message.get("type") == "message":
        # Message de chat
        chat_message = {
            "type": "message",
            "room_id": room_id,
            "user_id": user.id,
            "username": f"{user.first_name} {user.last_name}",
            "message": message.get("content"),
            "timestamp": datetime.now().isoformat()
        }
        
        # Sauvegarder dans Redis
        await redis_client.lpush(f"chat_history:{room_id}", json.dumps(chat_message))
        await redis_client.ltrim(f"chat_history:{room_id}", 0, 99)  # Garder les 100 derniers
        
        # Diffuser à la salle
        await manager.broadcast_to_group(json.dumps(chat_message), f"chat_{room_id}")
    
    elif message.get("type") == "typing":
        # Indicateur de frappe
        typing_message = {
            "type": "typing",
            "room_id": room_id,
            "user_id": user.id,
            "username": f"{user.first_name} {user.last_name}",
            "typing": message.get("typing", False),
            "timestamp": datetime.now().isoformat()
        }
        
        # Diffuser à la salle
        await manager.broadcast_to_group(json.dumps(typing_message), f"chat_{room_id}")


async def send_pending_notifications(user_id: int, websocket: WebSocket):
    """Envoyer les notifications en attente."""
    try:
        # Récupérer les notifications depuis Redis
        notifications = await redis_client.lrange(f"notifications:{user_id}", 0, -1)
        
        for notification in notifications:
            await websocket.send_text(notification)
        
        # Supprimer les notifications envoyées
        await redis_client.delete(f"notifications:{user_id}")
    
    except Exception:
        pass  # Ignorer les erreurs de notification


async def send_chat_history(room_id: str, websocket: WebSocket):
    """Envoyer l'historique du chat."""
    try:
        # Récupérer l'historique depuis Redis
        history = await redis_client.lrange(f"chat_history:{room_id}", 0, 49)  # 50 derniers messages
        
        for message in reversed(history):  # Ordre chronologique
            await websocket.send_text(message)
    
    except Exception:
        pass  # Ignorer les erreurs d'historique


# Fonctions utilitaires pour envoyer des notifications
async def send_notification_to_user(user_id: int, notification: dict):
    """Envoyer une notification à un utilisateur."""
    notification_json = json.dumps(notification)
    
    # Envoyer via WebSocket si connecté
    await manager.send_personal_message(notification_json, user_id)
    
    # Sinon, stocker dans Redis pour plus tard
    await redis_client.lpush(f"notifications:{user_id}", notification_json)
    await redis_client.ltrim(f"notifications:{user_id}", 0, 99)  # Garder les 100 dernières


async def send_notification_to_group(group_name: str, notification: dict):
    """Envoyer une notification à un groupe."""
    notification_json = json.dumps(notification)
    await manager.broadcast_to_group(notification_json, group_name)


# Endpoint pour obtenir les statistiques WebSocket
@router.get("/ws/stats")
async def get_websocket_stats():
    """Obtenir les statistiques des connexions WebSocket."""
    return {
        "online_users": manager.get_online_users(),
        "total_connections": manager.get_connection_count(),
        "active_groups": list(manager.groups.keys()),
        "connection_metadata": manager.connection_metadata
    }