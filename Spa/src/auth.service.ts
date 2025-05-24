import { UserManager, WebStorageStateStore } from 'oidc-client-ts';

const oidcConfig = {
  authority: 'http://localhost:5001', // AuthServer URL (HTTP)
  client_id: 'interactive',
  redirect_uri: 'http://localhost:5173/signin-oidc',
  post_logout_redirect_uri: 'http://localhost:5173/signout-callback-oidc',
  response_type: 'code',
  scope: 'openid profile api',
  userStore: new WebStorageStateStore({ store: window.localStorage }),
};

export const userManager = new UserManager(oidcConfig);
