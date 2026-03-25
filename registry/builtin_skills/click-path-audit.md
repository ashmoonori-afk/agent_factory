# Skill: /click-path-audit — Behavioural Flow Audit

## When to Use
- After systematic debugging finds "no bugs" but users report broken UI
- After modifying any Zustand store action (check all callers)
- After any refactor that touches shared state
- Before release, on critical user flows
- When a button "does nothing" — this is THE tool for that

## Policy
Level: ALLOW

## Instructions
## The Problem This Solves

Traditional debugging checks:
- Does the function exist? (missing wiring)
- Does it crash? (runtime errors)
- Does it return the right type? (data flow)

But it does NOT check:
- **Does the final UI state match what the button label promises?**
- **Does function B silently undo what function A just did?**
- **Does shared state (Zustand/Redux/context) have side effects that cancel the intended action?**

Real example: A "New Email" button called `setComposeMode(true)` then `selectThread(null)`. Both worked individually. But `selectThread` had a side effect resetting `composeMode: false`. The button did nothing. 54 bugs were found by systematic debugging — this one was missed.

---

## How It Works

For EVERY interactive touchpoint in the target area:

```
1. IDENTIFY the handler (onClick, onSubmit, onChange, etc.)
2. TRACE every function call in the handler, IN ORDER
3. For EACH function call:
   a. What state does it READ?
   b. What state does it WRITE?
   c. Does it have SIDE EFFECTS on shared state?
   d. Does it reset/clear any state as a side effect?
4. CHECK: Does any later call UNDO a state change from an earlier call?
5. CHECK: Is the FINAL state what the user expects from the button label?
6. CHECK: Are there race conditions (async calls that resolve in wrong order)?
```

---

## Execution Steps

### Step 1: Map State Stores

Before auditing any touchpoint, build a side-effect map of every state store action:

```
For each Zustand store / React context in scope:
  For each action/setter:
    - What fields does it set?
    - Does it RESET other fields as a side effect?
    - Document: actionName → {sets: [...], resets: [...]}
```

This is the critical reference. The "New Email" bug was invisible without knowing that `selectThread` resets `composeMode`.

**Output format:**
```
STORE: emailStore
  setComposeMode(bool) → sets: {composeMode}
  selectThread(thread|null) → sets: {selectedThread, selectedThreadId, messages, drafts, selectedDraft, summary} RESETS: {composeMode: false, composeData: null, redraftOpen: false}
  setDraftGenerating(bool) → sets: {draftGenerating}
  ...

DANGEROUS RESETS (actions that clear state they don't own):
  selectThread → resets composeMode (owned by setComposeMode)
  reset → resets everything
```

### Step 2: Audit Each Touchpoint

For each button/toggle/form submit in the target area:

```
TOUCHPOINT: [Button label] in [Component:line]
  HANDLER: onClick → {
    call 1: functionA() → sets {X: true}
    call 2: functionB() → sets {Y: null} RESETS {X: false}  ← CONFLICT
  }
  EXPECTED: User sees [description of what button label promises]
  ACTUAL: X is false because functionB reset it
  VERDICT: BUG — [description]
```

**Check each of these bug patterns:**

#### Pattern 1: Sequential Undo
```
handler() {
  setState_A(true)     // sets X = true
  setState_B(null)     // side effect: resets X = false
}
// Result: X is false. First call was pointless.
```

#### Pattern 2: Async Race
`

(Content truncated for registry. See original skill for full details.)

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.
- Do not perform actions outside the scope of this skill.

## Examples
User: "Help me with /click-path-audit — behavioural flow audit"
Agent: [follows the skill instructions to complete the task]
