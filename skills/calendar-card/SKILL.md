---
name: calendar-card
description: Put a finished "my version" (script, hooks, shot plan) on the user's content calendar - a Notion database if the Notion connector is on, otherwise a dated Markdown card in calendar/. Use at the end of save-to-my-version, or when the user says "put it on my calendar", "add this to my content calendar".
---

# Calendar card

A script nobody can find never gets filmed. Put it where the user plans their week.

## Where it goes

1. **Notion connector available** (tools named `notion` in this session): ask once which database is their content calendar, then create a page there with: title, status "Scripted", the date they want to film or post, the reel it is modeled on, and the full `script.md` and `shot-plan.md` as the page body. Remember the database for next time in CONTEXT.md under "Calendar".
2. **Otherwise:** write `calendar/<YYYY-MM-DD>-<short-name>.md` with the same fields at the top (title, status, date, modeled on), then the script, then the shot plan. If they did not give a date, use the next free day in `calendar/`.

## The card

```markdown
# <working title>
Status: Scripted
Date: <YYYY-MM-DD>
Modeled on: <reel link> (format only)

<script.md, from "## Hooks" down>

<shot-plan.md>
```

Tell the user where the card is in one line, by its title.
