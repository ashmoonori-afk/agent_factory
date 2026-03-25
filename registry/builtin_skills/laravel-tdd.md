# Skill: Laravel TDD Workflow

## When to Use
- New features or endpoints in Laravel
- Bug fixes or refactors
- Testing Eloquent models, policies, jobs, and notifications
- Prefer Pest for new tests unless the project already standardizes on PHPUnit

## Policy
Level: ALLOW

## Instructions
## How It Works

### Red-Green-Refactor Cycle

1) Write a failing test
2) Implement the minimal change to pass
3) Refactor while keeping tests green

### Test Layers

- **Unit**: pure PHP classes, value objects, services
- **Feature**: HTTP endpoints, auth, validation, policies
- **Integration**: database + queue + external boundaries

Choose layers based on scope:

- Use **Unit** tests for pure business logic and services.
- Use **Feature** tests for HTTP, auth, validation, and response shape.
- Use **Integration** tests when validating DB/queues/external services together.

### Database Strategy

- `RefreshDatabase` for most feature/integration tests (runs migrations once per test run, then wraps each test in a transaction when supported; in-memory databases may re-migrate per test)
- `DatabaseTransactions` when the schema is already migrated and you only need per-test rollback
- `DatabaseMigrations` when you need a full migrate/fresh for every test and can afford the cost

Use `RefreshDatabase` as the default for tests that touch the database: for databases with transaction support, it runs migrations once per test run (via a static flag) and wraps each test in a transaction; for `:memory:` SQLite or connections without transactions, it migrates before each test. Use `DatabaseTransactions` when the schema is already migrated and you only need per-test rollbacks.

### Testing Framework Choice

- Default to **Pest** for new tests when available.
- Use **PHPUnit** only if the project already standardizes on it or requires PHPUnit-specific tooling.

## Examples

### PHPUnit Example

```php
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

final class ProjectControllerTest extends TestCase
{
    use RefreshDatabase;

    public function test_owner_can_create_project(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->postJson('/api/projects', [
            'name' => 'New Project',
        ]);

        $response->assertCreated();
        $this->assertDatabaseHas('projects', ['name' => 'New Project']);
    }
}
```

### Feature Test Example (HTTP Layer)

```php
use App\Models\Project;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

final class ProjectIndexTest extends TestCase
{
    use RefreshDatabase;

    public function test_projects_index_returns_paginated_results(): void
    {
        $user = User::factory()->create();
        Project::factory()->count(3)->for($user)->create();

        $response = $this->actingAs($user)->getJson('/api/projects');

        $response->assertOk();
        $response->assertJsonStructure(['success', 'data', 'error', 'meta']);
    }
}
```

### Pest Example

```php
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;

use function Pest\Laravel\actingAs;
use function Pest\Laravel\assertDatabaseHas;

uses(RefreshDatabase::class);

test('owner can create project', fu

(Content truncated for registry. See original skill for full details.)

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.
- Do not perform actions outside the scope of this skill.

## Examples
User: "Help me with laravel tdd workflow"
Agent: [follows the skill instructions to complete the task]
