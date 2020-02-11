/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'gwillig.eu', // the auth0 domain prefix
    audience: 'coffee_shop_api', // the audience set for the auth0 app
    clientId: 'f58iONpRgvVedQQXalwNyo2i8w2EL8uz', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200', // the base url of the running ionic application.
  }
};
