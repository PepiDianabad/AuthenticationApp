import Keycloak from 'keycloak-js';

const keycloak = new Keycloak({
  url: 'http://localhost:8080/auth',
  realm: 'master2',
  clientId: 'react',
});

export default keycloak;
