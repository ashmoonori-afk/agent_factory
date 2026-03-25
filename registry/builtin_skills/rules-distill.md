# Skill: Rules Distill

## When to Use
- Periodic rules maintenance (monthly or after installing new skills)
- After a skill-stocktake reveals patterns that should be rules
- When rules feel incomplete relative to the skills being used

## Policy
Level: ASK

## Instructions
## How It Works

The rules distillation process follows three phases:

### Phase 1: Inventory (Deterministic Collection)

#### 1a. Collect skill inventory

```bash
bash ~/.claude/skills/rules-distill/scripts/scan-skills.sh
```

#### 1b. Collect rules index

```bash
bash ~/.claude/skills/rules-distill/scripts/scan-rules.sh
```

#### 1c. Present to user

```
Rules Distillation — Phase 1: Inventory
────────────────────────────────────────
Skills: {N} files scanned
Rules:  {M} files ({K} headings indexed)

Proceeding to cross-read analysis...
```

### Phase 2: Cross-read, Match & Verdict (LLM Judgment)

Extraction and matching are unified in a single pass. Rules files are small enough (~800 lines total) that the full text can be provided to the LLM — no grep pre-filtering needed.

#### Batching

Group skills into **thematic clusters** based on their descriptions. Analyze each cluster in a subagent with the full rules text.

#### Cross-batch Merge

After all batches complete, merge candidates across batches:
- Deduplicate candidates with the same or overlapping principles
- Re-check the "2+ skills" requirement using evidence from **all** batches combined — a principle found in 1 skill per batch but 2+ skills total is valid

#### Subagent Prompt

Launch a general-purpose Agent with the following prompt:

````
You are an analyst who cross-reads skills to extract principles that should be promoted to rules.

## Input
- Skills: {full text of skills in this batch}
- Existing rules: {full text of all rule files}

## Extraction Criteria

Include a candidate ONLY if ALL of these are true:

1. **Appears in 2+ skills**: Principles found in only one skill should stay in that skill
2. **Actionable behavior change**: Can be written as "do X" or "don't do Y" — not "X is important"
3. **Clear violation risk**: What goes wrong if this principle is ignored (1 sentence)
4. **Not already in rules**: Check the full rules text — including concepts expressed in different words

## Matching & Verdict

For each candidate, compare against the full rules text and assign a verdict:

- **Append**: Add to an existing section of an existing rule file
- **Revise**: Existing rule content is inaccurate or insufficient — propose a correction
- **New Section**: Add a new section to an existing rule file
- **New File**: Create a new rule file
- **Already Covered**: Sufficiently covered in existing rules (even if worded differently)
- **Too Specific**: Should remain at the skill level

## Output Format (per candidate)

```json
{
  "principle": "1-2 sentences in 'do X' / 'don't do Y' form",
  "evidence": ["skill-name: §Section", "skill-name: §Section"],
  "violation_risk": "1 sentence",
  "verdict": "Append / Revise / New Section / New File / Already Covered / Too Specific",
  "target_rule": "filename §Section, or 'new'",
  "confidence": "high / medium / low",
  "draft": "Draft text for Append/New Section/New File verdicts",
  "revision": {
    "reason": "Why the existing content is inacc

(Content truncated for registry. See original skill for full details.)

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.
- Do not perform actions outside the scope of this skill.

## Examples
User: "Help me with rules distill"
Agent: [follows the skill instructions to complete the task]
