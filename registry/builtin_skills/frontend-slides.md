# Skill: Frontend Slides

## When to Use
- Creating a talk deck, pitch deck, workshop deck, or internal presentation
- Converting `.ppt` or `.pptx` slides into an HTML presentation
- Improving an existing HTML presentation's layout, motion, or typography
- Exploring presentation styles with a user who does not know their design preference yet

## Policy
Level: ALLOW

## Instructions
## Non-Negotiables

1. **Zero dependencies**: default to one self-contained HTML file with inline CSS and JS.
2. **Viewport fit is mandatory**: every slide must fit inside one viewport with no internal scrolling.
3. **Show, don't tell**: use visual previews instead of abstract style questionnaires.
4. **Distinctive design**: avoid generic purple-gradient, Inter-on-white, template-looking decks.
5. **Production quality**: keep code commented, accessible, responsive, and performant.

Before generating, read `STYLE_PRESETS.md` for the viewport-safe CSS base, density limits, preset catalog, and CSS gotchas.

## Workflow

### 1. Detect Mode

Choose one path:
- **New presentation**: user has a topic, notes, or full draft
- **PPT conversion**: user has `.ppt` or `.pptx`
- **Enhancement**: user already has HTML slides and wants improvements

### 2. Discover Content

Ask only the minimum needed:
- purpose: pitch, teaching, conference talk, internal update
- length: short (5-10), medium (10-20), long (20+)
- content state: finished copy, rough notes, topic only

If the user has content, ask them to paste it before styling.

### 3. Discover Style

Default to visual exploration.

If the user already knows the desired preset, skip previews and use it directly.

Otherwise:
1. Ask what feeling the deck should create: impressed, energized, focused, inspired.
2. Generate **3 single-slide preview files** in `.ecc-design/slide-previews/`.
3. Each preview must be self-contained, show typography/color/motion clearly, and stay under roughly 100 lines of slide content.
4. Ask the user which preview to keep or what elements to mix.

Use the preset guide in `STYLE_PRESETS.md` when mapping mood to style.

### 4. Build the Presentation

Output either:
- `presentation.html`
- `[presentation-name].html`

Use an `assets/` folder only when the deck contains extracted or user-supplied images.

Required structure:
- semantic slide sections
- a viewport-safe CSS base from `STYLE_PRESETS.md`
- CSS custom properties for theme values
- a presentation controller class for keyboard, wheel, and touch navigation
- Intersection Observer for reveal animations
- reduced-motion support

### 5. Enforce Viewport Fit

Treat this as a hard gate.

Rules:
- every `.slide` must use `height: 100vh; height: 100dvh; overflow: hidden;`
- all type and spacing must scale with `clamp()`
- when content does not fit, split into multiple slides
- never solve overflow by shrinking text below readable sizes
- never allow scrollbars inside a slide

Use the density limits and mandatory CSS block in `STYLE_PRESETS.md`.

### 6. Validate

Check the finished deck at these sizes:
- 1920x1080
- 1280x720
- 768x1024
- 375x667
- 667x375

If browser automation is available, use it to verify no slide overflows and that keyboard navigation works.

### 7. Deliver

At handoff:
- delete temporary preview files unless the user wants to keep them
- open the deck with the platform-appropriate opener when useful
- summarize file 

(Content truncated for registry. See original skill for full details.)

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.
- Do not perform actions outside the scope of this skill.

## Examples
User: "Help me with frontend slides"
Agent: [follows the skill instructions to complete the task]
