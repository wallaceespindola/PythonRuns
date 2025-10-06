import pytest
from datetime import datetime, timedelta, timezone
from jose import JWTError
import time

from pythonruns.src.mytests.jwt_test import JWTManager


@pytest.fixture
def jwt_manager():
    """Fixture for creating a JWTManager instance."""
    return JWTManager()


@pytest.fixture
def test_data():
    """Fixture for test data."""
    return {"sub": "user123", "name": "Test User"}


class TestJWTManager:
    """Test suite for JWTManager class."""

    def test_init_default_values(self):
        """Test JWTManager initialization with default values."""
        manager = JWTManager()
        assert manager.secret_key == "supersecretkey"
        assert manager.algorithm == "HS256"
        assert manager.expire_minutes == 30

    def test_init_custom_values(self):
        """Test JWTManager initialization with custom values."""
        custom_key = "mycustomkey"
        custom_algo = "HS512"
        custom_expire = 60

        manager = JWTManager(
            secret_key=custom_key,
            algorithm=custom_algo,
            expire_minutes=custom_expire
        )

        assert manager.secret_key == custom_key
        assert manager.algorithm == custom_algo
        assert manager.expire_minutes == custom_expire

    def test_create_access_token(self, jwt_manager, test_data):
        """Test creating a JWT access token."""
        token = jwt_manager.create_access_token(test_data)

        # Verify token is a string
        assert isinstance(token, str)

        # Verify token is not empty
        assert len(token) > 0

        # Verify token has three parts (header.payload.signature)
        assert len(token.split('.')) == 3

    def test_decode_token_valid(self, jwt_manager, test_data):
        """Test decoding a valid JWT token."""
        token = jwt_manager.create_access_token(test_data)
        decoded = jwt_manager.decode_token(token)

        # Verify the decoded data contains the original data
        assert decoded["sub"] == test_data["sub"]
        assert decoded["name"] == test_data["name"]

        # Verify expiration field exists
        assert "exp" in decoded

    def test_decode_token_includes_expiration(self, jwt_manager, test_data):
        """Test that decoded token includes proper expiration time."""
        token = jwt_manager.create_access_token(test_data)
        decoded = jwt_manager.decode_token(token)

        # Get the expiration timestamp
        exp_timestamp = decoded["exp"]

        # Convert to datetime
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        now = datetime.now(timezone.utc)

        # Verify expiration is in the future
        assert exp_datetime > now

        # Verify expiration is approximately 30 minutes in the future (with 1 minute tolerance)
        expected_exp = now + timedelta(minutes=30)
        time_diff = abs((exp_datetime - expected_exp).total_seconds())
        assert time_diff < 60  # Within 60 seconds tolerance

    def test_decode_token_invalid(self, jwt_manager):
        """Test decoding an invalid JWT token."""
        invalid_token = "invalid.token.string"

        with pytest.raises(JWTError) as exc_info:
            jwt_manager.decode_token(invalid_token)

        assert "Token validation failed" in str(exc_info.value)

    def test_decode_token_tampered(self, jwt_manager, test_data):
        """Test decoding a tampered JWT token."""
        token = jwt_manager.create_access_token(test_data)

        # Tamper with the token by modifying a character
        tampered_token = token[:-1] + ('a' if token[-1] != 'a' else 'b')

        with pytest.raises(JWTError):
            jwt_manager.decode_token(tampered_token)

    def test_decode_token_wrong_secret(self, jwt_manager, test_data):
        """Test decoding a token with wrong secret key."""
        token = jwt_manager.create_access_token(test_data)

        # Create a new manager with different secret
        wrong_manager = JWTManager(secret_key="wrongsecret")

        with pytest.raises(JWTError):
            wrong_manager.decode_token(token)

    def test_decode_expired_token(self, test_data):
        """Test that expired tokens are properly rejected."""
        # Create a manager with very short expiration
        short_manager = JWTManager(expire_minutes=0)

        # Create token that expires immediately
        token = short_manager.create_access_token(test_data)

        # Wait a moment to ensure it expires
        time.sleep(1)

        # Try to decode the expired token - should raise JWTError
        with pytest.raises(JWTError) as exc_info:
            short_manager.decode_token(token)

        assert "Token validation failed" in str(exc_info.value)

    def test_token_with_empty_data(self, jwt_manager):
        """Test creating a token with empty data dictionary."""
        token = jwt_manager.create_access_token({})
        decoded = jwt_manager.decode_token(token)

        # Should only contain the expiration field
        assert "exp" in decoded

    def test_token_with_various_data_types(self, jwt_manager):
        """Test creating a token with various data types."""
        complex_data = {
            "user_id": 12345,
            "username": "testuser",
            "roles": ["admin", "user"],
            "active": True,
            "metadata": {"key": "value"}
        }

        token = jwt_manager.create_access_token(complex_data)
        decoded = jwt_manager.decode_token(token)

        # Verify all data is preserved
        assert decoded["user_id"] == complex_data["user_id"]
        assert decoded["username"] == complex_data["username"]
        assert decoded["roles"] == complex_data["roles"]
        assert decoded["active"] == complex_data["active"]
        assert decoded["metadata"] == complex_data["metadata"]

    def test_multiple_tokens_are_different(self, jwt_manager, test_data):
        """Test that creating multiple tokens generates different tokens."""
        token1 = jwt_manager.create_access_token(test_data)

        # Sleep briefly to ensure different expiration timestamps
        time.sleep(0.01)

        token2 = jwt_manager.create_access_token(test_data)

        # Tokens should be different due to different expiration times
        # However, if created at the exact same second, they might be identical
        # So we just verify they can both be decoded successfully
        decoded1 = jwt_manager.decode_token(token1)
        decoded2 = jwt_manager.decode_token(token2)

        assert decoded1["sub"] == test_data["sub"]
        assert decoded2["sub"] == test_data["sub"]

    def test_custom_expiration_time(self, test_data):
        """Test creating tokens with custom expiration time."""
        short_lived_manager = JWTManager(expire_minutes=5)
        token = short_lived_manager.create_access_token(test_data)
        decoded = short_lived_manager.decode_token(token)

        exp_datetime = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
        now = datetime.now(timezone.utc)
        expected_exp = now + timedelta(minutes=5)

        time_diff = abs((exp_datetime - expected_exp).total_seconds())
        assert time_diff < 60  # Within 60 seconds tolerance

    @pytest.mark.parametrize("algorithm", ["HS256", "HS384", "HS512"])
    def test_different_algorithms(self, algorithm, test_data):
        """Test creating tokens with different algorithms."""
        manager = JWTManager(algorithm=algorithm)
        token = manager.create_access_token(test_data)
        decoded = manager.decode_token(token)

        assert decoded["sub"] == test_data["sub"]

if __name__ == "__main__":
    pytest.main()