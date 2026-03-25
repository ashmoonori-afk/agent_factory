# Skill: Ktor Server Patterns

## When to Use
- Building Ktor HTTP servers
- Configuring Ktor plugins (Auth, CORS, ContentNegotiation, StatusPages)
- Implementing REST APIs with Ktor
- Setting up dependency injection with Koin
- Writing Ktor integration tests with testApplication
- Working with WebSockets in Ktor

## Policy
Level: ALLOW

## Instructions
## Application Structure

### Standard Ktor Project Layout

```text
src/main/kotlin/
├── com/example/
│   ├── Application.kt           # Entry point, module configuration
│   ├── plugins/
│   │   ├── Routing.kt           # Route definitions
│   │   ├── Serialization.kt     # Content negotiation setup
│   │   ├── Authentication.kt    # Auth configuration
│   │   ├── StatusPages.kt       # Error handling
│   │   └── CORS.kt              # CORS configuration
│   ├── routes/
│   │   ├── UserRoutes.kt        # /users endpoints
│   │   ├── AuthRoutes.kt        # /auth endpoints
│   │   └── HealthRoutes.kt      # /health endpoints
│   ├── models/
│   │   ├── User.kt              # Domain models
│   │   └── ApiResponse.kt       # Response envelopes
│   ├── services/
│   │   ├── UserService.kt       # Business logic
│   │   └── AuthService.kt       # Auth logic
│   ├── repositories/
│   │   ├── UserRepository.kt    # Data access interface
│   │   └── ExposedUserRepository.kt
│   └── di/
│       └── AppModule.kt         # Koin modules
src/test/kotlin/
├── com/example/
│   ├── routes/
│   │   └── UserRoutesTest.kt
│   └── services/
│       └── UserServiceTest.kt
```

### Application Entry Point

```kotlin
// Application.kt
fun main() {
    embeddedServer(Netty, port = 8080, module = Application::module).start(wait = true)
}

fun Application.module() {
    configureSerialization()
    configureAuthentication()
    configureStatusPages()
    configureCORS()
    configureDI()
    configureRouting()
}
```

## Routing DSL

### Basic Routes

```kotlin
// plugins/Routing.kt
fun Application.configureRouting() {
    routing {
        userRoutes()
        authRoutes()
        healthRoutes()
    }
}

// routes/UserRoutes.kt
fun Route.userRoutes() {
    val userService by inject<UserService>()

    route("/users") {
        get {
            val users = userService.getAll()
            call.respond(users)
        }

        get("/{id}") {
            val id = call.parameters["id"]
                ?: return@get call.respond(HttpStatusCode.BadRequest, "Missing id")
            val user = userService.getById(id)
                ?: return@get call.respond(HttpStatusCode.NotFound)
            call.respond(user)
        }

        post {
            val request = call.receive<CreateUserRequest>()
            val user = userService.create(request)
            call.respond(HttpStatusCode.Created, user)
        }

        put("/{id}") {
            val id = call.parameters["id"]
                ?: return@put call.respond(HttpStatusCode.BadRequest, "Missing id")
            val request = call.receive<UpdateUserRequest>()
            val user = userService.update(id, request)
                ?: return@put call.respond(HttpStatusCode.NotFound)
            call.respond(user)
        }

        delete("/{id}") {
            val id = call.parameters["id"]
                ?: return@delete call.respond(HttpStatusCode.BadRequest, "Missing id")
            val deleted = userService.delet

(Content truncated for registry. See original skill for full details.)

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.
- Do not perform actions outside the scope of this skill.

## Examples
User: "Help me with ktor server patterns"
Agent: [follows the skill instructions to complete the task]
