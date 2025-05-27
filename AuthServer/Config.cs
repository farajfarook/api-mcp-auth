using Duende.IdentityServer.Models;

namespace AuthServer;

public static class Config
{
    public static IEnumerable<IdentityResource> IdentityResources =>
        new IdentityResource[]
        {
            new IdentityResources.OpenId(),
            new IdentityResources.Profile(),
        };

    public static IEnumerable<ApiScope> ApiScopes =>
        new ApiScope[]
        {
            new ApiScope("api", "My API"),
            new ApiScope("weatherget", "Get weather data")
        };

    public static IEnumerable<ApiResource> ApiResources =>
        new ApiResource[]
        {
            new ApiResource("api", "My API")
            {
                Scopes = { "api", "weatherget" }
            }
        };

    public static IEnumerable<Client> Clients =>
        new Client[]
        {
            // m2m client credentials flow client
            new Client
            {
                ClientId = "m2m.client",
                ClientName = "Client Credentials Client",

                AllowedGrantTypes = GrantTypes.ClientCredentials,
                ClientSecrets = { new Secret("511536EF-F270-4058-80CA-1C89C192F69A".Sha256()) },

                AllowedScopes = { "api" }
            },

            new Client
            {
                ClientId = "m2m.client",
                ClientName = "Client Credentials Client",

                AllowedGrantTypes = GrantTypes.ClientCredentials,
                ClientSecrets = { new Secret("511536EF-F270-4058-80CA-1C89C192F69A".Sha256()) },

                AllowedScopes = { "api" }
            },

            // interactive client using code flow + pkce
            new Client
            {
                ClientId = "interactive",
                RequireClientSecret = false, // SPA should not require a client secret

                AllowedGrantTypes = GrantTypes.Code,

                RedirectUris = {
                    "http://localhost:5173/signin-oidc"
                },
                FrontChannelLogoutUri = "http://localhost:5173/signout-oidc",
                PostLogoutRedirectUris = {
                    "http://localhost:5173/signout-callback-oidc"
                },

                AllowOfflineAccess = true,
                AllowedScopes = { "openid", "profile", "api" , "weatherget" }
            },
        };
}
