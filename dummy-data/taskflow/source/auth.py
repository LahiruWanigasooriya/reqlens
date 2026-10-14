from datetime import datetime, timedelta


users = []


def register_user(
    full_name: str,
    email: str,
    password: str,
):
    if len(password) < 8:
        raise ValueError(
            "Password must contain at least 8 characters"
        )

    for user in users:
        if user["email"] == email:
            raise ValueError(
                "Email already registered"
            )

    user = {
        "id": len(users) + 1,
        "full_name": full_name,
        "email": email,
        "password": password,
    }

    users.append(user)

    return user


def login_user(
    email: str,
    password: str,
):
    for user in users:

        if (
            user["email"] == email
            and user["password"] == password
        ):
            return {
                "message": "Login successful",
                "user_id": user["id"],
            }

    raise ValueError(
        "Invalid credentials"
    )


def request_password_reset(
    email: str,
):
    user = next(
        (
            user
            for user in users
            if user["email"] == email
        ),
        None,
    )

    if not user:
        raise ValueError(
            "User not found"
        )

    expires_at = (
        datetime.utcnow()
        + timedelta(minutes=30)
    )

    return {
        "email": email,
        "reset_link":
            "https://taskflow.dev/reset/example-token",
        "expires_at": expires_at,
    }
    