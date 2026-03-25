# Skill: FoundationModels: On-Device LLM (iOS 26)

## When to Use
- Building AI-powered features using Apple Intelligence on-device
- Generating or summarizing text without cloud dependency
- Extracting structured data from natural language input
- Implementing custom tool calling for domain-specific AI actions
- Streaming structured responses for real-time UI updates
- Need privacy-preserving AI (no data leaves the device)

## Policy
Level: ALLOW

## Instructions
## Core Pattern — Availability Check

Always check model availability before creating a session:

```swift
struct GenerativeView: View {
    private var model = SystemLanguageModel.default

    var body: some View {
        switch model.availability {
        case .available:
            ContentView()
        case .unavailable(.deviceNotEligible):
            Text("Device not eligible for Apple Intelligence")
        case .unavailable(.appleIntelligenceNotEnabled):
            Text("Please enable Apple Intelligence in Settings")
        case .unavailable(.modelNotReady):
            Text("Model is downloading or not ready")
        case .unavailable(let other):
            Text("Model unavailable: \(other)")
        }
    }
}
```

## Core Pattern — Basic Session

```swift
// Single-turn: create a new session each time
let session = LanguageModelSession()
let response = try await session.respond(to: "What's a good month to visit Paris?")
print(response.content)

// Multi-turn: reuse session for conversation context
let session = LanguageModelSession(instructions: """
    You are a cooking assistant.
    Provide recipe suggestions based on ingredients.
    Keep suggestions brief and practical.
    """)

let first = try await session.respond(to: "I have chicken and rice")
let followUp = try await session.respond(to: "What about a vegetarian option?")
```

Key points for instructions:
- Define the model's role ("You are a mentor")
- Specify what to do ("Help extract calendar events")
- Set style preferences ("Respond as briefly as possible")
- Add safety measures ("Respond with 'I can't help with that' for dangerous requests")

## Core Pattern — Guided Generation with @Generable

Generate structured Swift types instead of raw strings:

### 1. Define a Generable Type

```swift
@Generable(description: "Basic profile information about a cat")
struct CatProfile {
    var name: String

    @Guide(description: "The age of the cat", .range(0...20))
    var age: Int

    @Guide(description: "A one sentence profile about the cat's personality")
    var profile: String
}
```

### 2. Request Structured Output

```swift
let response = try await session.respond(
    to: "Generate a cute rescue cat",
    generating: CatProfile.self
)

// Access structured fields directly
print("Name: \(response.content.name)")
print("Age: \(response.content.age)")
print("Profile: \(response.content.profile)")
```

### Supported @Guide Constraints

- `.range(0...20)` — numeric range
- `.count(3)` — array element count
- `description:` — semantic guidance for generation

## Core Pattern — Tool Calling

Let the model invoke custom code for domain-specific tasks:

### 1. Define a Tool

```swift
struct RecipeSearchTool: Tool {
    let name = "recipe_search"
    let description = "Search for recipes matching a given term and return a list of results."

    @Generable
    struct Arguments {
        var searchTerm: String
        var numberOfResults: Int
    }

    func call(arguments: Ar

(Content truncated for registry. See original skill for full details.)

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.
- Do not perform actions outside the scope of this skill.

## Examples
User: "Help me with foundationmodels: on-device llm (ios 26)"
Agent: [follows the skill instructions to complete the task]
