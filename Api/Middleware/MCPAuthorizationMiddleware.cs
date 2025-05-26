using Microsoft.AspNetCore.Http;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace Api.Middleware
{
    public class MCPAuthorizationMiddleware // Renamed from CustomAuthorizationMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<MCPAuthorizationMiddleware> _logger; // Updated logger type

        public MCPAuthorizationMiddleware(RequestDelegate next, ILogger<MCPAuthorizationMiddleware> logger) // Renamed constructor
        {
            _next = next;
            _logger = logger;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            if (context.User.Identity != null && context.User.Identity.IsAuthenticated)
            {
                _logger.LogInformation($"User {context.User.Identity.Name} is authenticated. Applying custom authorization logic.");

                // Example: Deny access if a specific condition is not met
                // if (!context.User.HasClaim(c => c.Type == "custom_claim" && c.Value == "required_value"))
                // {
                //     _logger.LogWarning($"User {context.User.Identity.Name} failed custom authorization.");
                //     context.Response.StatusCode = StatusCodes.Status403Forbidden;
                //     await context.Response.WriteAsync("Forbidden by custom authorization policy.");
                //     return; // Short-circuit the pipeline
                // }

                _logger.LogInformation($"User {context.User.Identity.Name} passed custom authorization.");
            }
            else
            {
                _logger.LogInformation("No authenticated user. Skipping custom authorization logic.");
            }

            await _next(context);
        }
    }
}
