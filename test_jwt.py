from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "80f42ad38ba618fc60dfa0d283f87e8a"
ALGORITHM = "HS256"

# Create a test token
payload = {
    "sub": 1,
    "exp": datetime.utcnow() + timedelta(minutes=30)
}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
print(f"Token: {token}")

# Try to decode it
try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"Decoded: {decoded}")
except Exception as e:
    print(f"Error: {e}")

# Test with the token from the frontend
frontend_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImV4cCI6MTc1MTgyNzEzN30.PSh9DRHWdY0HjV86u1xqw9Ys1x6UIF1pnulwboJbA34"
try:
    decoded_frontend = jwt.decode(frontend_token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"Frontend token decoded: {decoded_frontend}")
except Exception as e:
    print(f"Frontend token error: {e}")