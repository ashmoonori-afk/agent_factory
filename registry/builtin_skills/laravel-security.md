# Skill: Laravel Security Best Practices

## When to Use
- Adding authentication or authorization
- Handling user input and file uploads
- Building new API endpoints
- Managing secrets and environment settings
- Hardening production deployments

## Policy
Level: DENY

## Instructions
## How It Works

- Middleware provides baseline protections (CSRF via `VerifyCsrfToken`, security headers via `SecurityHeaders`).
- Guards and policies enforce access control (`auth:sanctum`, `$this->authorize`, policy middleware).
- Form Requests validate and shape input (`UploadInvoiceRequest`) before it reaches services.
- Rate limiting adds abuse protection (`RateLimiter::for('login')`) alongside auth controls.
- Data safety comes from encrypted casts, mass-assignment guards, and signed routes (`URL::temporarySignedRoute` + `signed` middleware).

## Core Security Settings

- `APP_DEBUG=false` in production
- `APP_KEY` must be set and rotated on compromise
- Set `SESSION_SECURE_COOKIE=true` and `SESSION_SAME_SITE=lax` (or `strict` for sensitive apps)
- Configure trusted proxies for correct HTTPS detection

## Session and Cookie Hardening

- Set `SESSION_HTTP_ONLY=true` to prevent JavaScript access
- Use `SESSION_SAME_SITE=strict` for high-risk flows
- Regenerate sessions on login and privilege changes

## Authentication and Tokens

- Use Laravel Sanctum or Passport for API auth
- Prefer short-lived tokens with refresh flows for sensitive data
- Revoke tokens on logout and compromised accounts

Example route protection:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::middleware('auth:sanctum')->get('/me', function (Request $request) {
    return $request->user();
});
```

## Password Security

- Hash passwords with `Hash::make()` and never store plaintext
- Use Laravel's password broker for reset flows

```php
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\Rules\Password;

$validated = $request->validate([
    'password' => ['required', 'string', Password::min(12)->letters()->mixedCase()->numbers()->symbols()],
]);

$user->update(['password' => Hash::make($validated['password'])]);
```

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.
- Do not perform actions outside the scope of this skill.

## Examples
User: "Help me with laravel security best practices"
Agent: [follows the skill instructions to complete the task]
