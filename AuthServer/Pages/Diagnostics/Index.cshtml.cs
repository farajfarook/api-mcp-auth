// Copyright (c) Duende Software. All rights reserved.
// See LICENSE in the project root for license information.

using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Authorization;

namespace AuthServer.Pages.Diagnostics;

[SecurityHeaders]
[Authorize]
public class Index : PageModel
{
    public ViewModel View { get; set; } = default!;
    public async Task<IActionResult> OnGet()
    {
        View = new ViewModel(await HttpContext.AuthenticateAsync());

        return Page();
    }
}
