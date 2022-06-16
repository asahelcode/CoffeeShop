/* @DONE replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dabolinux.us', // the auth0 domain prefix
    audience: 'CoffeeShopNew', // the audience set for the auth0 app
    // audience: 'http://localhost:5000', // the audience set for the auth0 app
    clientId: '0qFP6YXf2hS20ERx8TQJDmrTK1EmZ17q', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
