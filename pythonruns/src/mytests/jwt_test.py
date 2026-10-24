import os
import secrets
from datetime import UTC, datetime, timedelta

import jwt
from jwt import PyJWTError as JWTError


class JWTManager:
    """Manager class for creating and handling JWT tokens."""

    def __init__(self, secret_key: str | None = None, algorithm: str = "HS256", expire_minutes: int = 30):
        """
        Initialize JWT Manager.

        :param secret_key: Secret key for encoding JWT (defaults to $JWT_SECRET_KEY, else a random 64-byte key)
        :param algorithm: Algorithm to use for JWT encoding
        :param expire_minutes: Token expiration time in minutes
        """
        self.secret_key = secret_key or os.getenv("JWT_SECRET_KEY") or secrets.token_urlsafe(64)
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def create_access_token(self, data: dict) -> str:
        """
        Create a JWT access token.

        :param data: Dictionary containing the data to encode in the token
        :return: Encoded JWT token as string
        """
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(minutes=self.expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> dict:
        """
        Decode and verify a JWT token.

        :param token: JWT token to decode
        :return: Dictionary containing the decoded payload
        :raises JWTError: If the token is invalid or expired
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            raise JWTError(f"Token validation failed: {e!s}")


if __name__ == "__main__":
    # Example usage
    jwt_manager = JWTManager()

    # Create a token
    token = jwt_manager.create_access_token({"sub": "user123"})
    print(f"Generated Token: {token}")

    # Decode the token
    try:
        decoded = jwt_manager.decode_token(token)
        print(f"Decoded Token: {decoded}")
    except JWTError as e:
        print(f"Error decoding token: {e}")
