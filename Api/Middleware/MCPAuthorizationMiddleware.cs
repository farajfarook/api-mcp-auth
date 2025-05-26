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
            var path = context.Request.Path;
            if (path == "/sse" && context.User.Identity?.IsAuthenticated != true && false)
            {
                _logger.LogWarning("Unauthorized access attempt to SSE endpoint without authentication.");
                context.Response.StatusCode = StatusCodes.Status401Unauthorized;
                context.Response.ContentType = "application/json";
                var errorResponse = new { error = "invalid_token", error_description = "Missing or invalid access token" };
                await context.Response.WriteAsync(System.Text.Json.JsonSerializer.Serialize(errorResponse));
                return; // Stop further processing in the pipeline
            }
            else if (path == "/message")
            {
                // get the json body and log it
                context.Request.EnableBuffering(); // Enable buffering to read the request body multiple times
                using (var reader = new System.IO.StreamReader(context.Request.Body, leaveOpen: true)) // Keep the stream open
                {
                    var body = await reader.ReadToEndAsync();
                    _logger.LogInformation("Message endpoint accessed with body: {Body}", body);
                    context.Request.Body.Position = 0; // Reset the stream position for further processing
                }
            }

            await _next(context); // Call the next middleware in the pipeline
        }
    }
}
