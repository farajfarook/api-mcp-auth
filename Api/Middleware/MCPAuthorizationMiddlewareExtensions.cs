using Microsoft.AspNetCore.Builder;

namespace Api.Middleware
{
    public static class MCPAuthorizationMiddlewareExtensions
    {
        public static IApplicationBuilder UseMCPAuthorization(
            this IApplicationBuilder builder)
        {
            return builder.UseMiddleware<MCPAuthorizationMiddleware>();
        }
    }
}
