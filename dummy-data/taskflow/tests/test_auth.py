from source.auth import (
    login_user,
    register_user,
)


def test_registration():
    user = register_user(
        "Test User",
        "test@example.com",
        "password123",
    )

    assert user["email"] == (
        "test@example.com"
    )


def test_login():
    register_user(
        "Login User",
        "login@example.com",
        "password123",
    )

    result = login_user(
        "login@example.com",
        "password123",
    )

    assert result["message"] == (
        "Login successful"
    )