def check_roles(roles: list, rolesToFind: list) -> bool:
    for role in roles:
        if role.name in rolesToFind:
            return True
    return False