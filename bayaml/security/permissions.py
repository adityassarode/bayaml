from .roles import Role


def can(role: Role, action: str) -> bool:
    if role == Role.ADMIN:
        return True
    return action in {"read", "run"}
