---
name: my-version-script
description: Turn a broken-down reel into the user's own version - same format, same beats, same pace, all new words in their voice - with three hooks (outcome, niche, broad claim). Use after reel-breakdown, or when the user says "write my version of this reel", "recreate this for me", "script this in my voice".
---

# My version of the reel

Read `CONTEXT.md` (run context-profile first if it does not exist) and the reel's `BREAKDOWN.md`, sheets and stills.

## The rule: keep the format, change the content

- **Keep:** the kind of hook, the order of beats, the pace, the length (within a few seconds), and every edit move at the same point.
- **Change:** every sentence. Never reuse the original's sentences or its claims. The user's version is about the same idea from where they stand, for their viewer.
- **Only true things.** Facts about the user come only from "True things I can say" in CONTEXT.md. Anything else becomes a plain placeholder like `[how many hours it saved]` for them to fill in before filming. Never invent a number, a client, a result, a price or a quote.

## How it has to read (they will say it out loud)

- Full conversational sentences, first person, contractions, run on with "and", "so", "but", "now".
- No chopped two- and three-word fragments. No slogans.
- Match the user's own phrases from CONTEXT.md.

## Write `reels/<short-name>/script.md`

```markdown
# <working title>
Modeled on: <reel link or file> (format only)

## Hooks
1. Outcome: <one natural sentence about the result>
2. Niche: <one sentence aimed at the exact viewer in CONTEXT.md>
3. Broad claim: <one sentence anyone would stop for>

## Spoken script
(0 to 3 s) <hook 1, or say which hook>
(3 to 7 s) <beat 2>
...
(last beat) <the call to action from CONTEXT.md>
```

One beat per paragraph, each starting with its time range. Then hand over to shot-plan-from-my-footage.
