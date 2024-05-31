import requests

KEYCLOAK_URL = "http://localhost:8080/auth/realms/master2/protocol/openid-connect/userinfo"

def validate_token(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(KEYCLOAK_URL, headers=headers)
    if response.status_code == 200:
        return True, response.json()
    return False, None
