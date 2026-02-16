import pytest
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from jose import jwt

def test_password_hashing():
    #Arrange
    password = "test_password"
    #Act
    hashed = get_password_hash(password)
    #Assert
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)

def test_create_access_token_payload():
    #Arrange
    test_email = "test@example.com"
    test_role = "admin"
    payload = {
        "sub": test_email,
        "role": test_role
    }
    #Act
    token = create_access_token(payload)
    #Assert
    assert token is not None
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded["sub"] == test_email  
    assert decoded["role"] == test_role
    assert "exp" in decoded