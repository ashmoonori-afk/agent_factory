# Skill: Text Summarizer

## When to Use
Use this skill when the user wants to condense a long piece of text — an article, a document, a conversation transcript, code comments, or a meeting log — into a shorter, accurate summary.

## Policy
Level: ALLOW
Summarization is a purely generative, non-destructive operation. No confirmation is required.

## Instructions
1. Receive the text to summarize. Accept it as a direct paste, a file path, or a URL.
2. Identify the summarization target:
   - **Brief** (1-3 sentences): key point only.
   - **Standard** (1 paragraph): main ideas and supporting points.
   - **Structured** (bullet list): one bullet per major topic.
   - **Executive** (title + bullets + action items): for business documents.
   Default to Standard if the user does not specify.
3. Preserve factual accuracy. Do not introduce information not present in the source.
4. Maintain the original language of the source text unless the user requests translation.
5. If the text exceeds 100,000 tokens, split into sections, summarize each, then produce a meta-summary.
6. Return the summary clearly labelled, followed by the word count reduction (e.g., "Reduced from 2,400 to 180 words").

## Constraints
- Never fabricate facts, statistics, names, or dates that are not in the source text.
- Never omit content that contradicts the user's assumed position — summarize neutrally.
- Do not reproduce more than 150 consecutive words verbatim from copyrighted material.
- Always indicate the summarization mode used (Brief/Standard/Structured/Executive).

## Examples
User: "Summarize this article in 3 bullet points: [article text]"
Agent: [returns 3 concise bullets capturing the main points, labels as Structured]

User: "Give me an executive summary of the Q3 report: [document]"
Agent: [returns title, 4-5 bullet points, and a list of recommended actions]
