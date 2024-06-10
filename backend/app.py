from flask import Flask, request, jsonify
from flask_oidc import OpenIDConnect
from keycloak import KeycloakOpenID
from functools import wraps

app = Flask(__name__)

app.config.update({
    'SECRET_KEY': '0X6Gi6oaFu6Y2nDysARXops5tkdOuEz4',
    'TESTING': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_RESOURCE_SERVER_ONLY': True,
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
})

oidc = OpenIDConnect(app)

keycloak_openid = KeycloakOpenID(
    server_url='http://localhost:8080/auth/',
    client_id='flask-app',
    realm_name='master2',
    client_secret_key='0X6Gi6oaFu6Y2nDysARXops5tkdOuEz4'
)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            token = token.split(" ")[1]
            options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}
            keycloak_openid.userinfo(token, options=options)
        except Exception as e:
            return jsonify({'message': str(e)}), 403

        return f(*args, **kwargs)
    return decorated

@app.route('/protected')
@token_required
def protected():
    return jsonify(message="This is a protected route.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
