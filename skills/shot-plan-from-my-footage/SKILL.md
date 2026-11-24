---
name: shot-plan-from-my-footage
description: Write the shot plan for the user's version of a reel from their own material - talking head, their own camera-roll clips by file name, real screenshots - never stock or AI footage. Indexes their footage folders first. Use after my-version-script, or when the user says "what should I film", "find B-roll in my camera roll", "make the shot list".
---

# Shot plan from my own footage

## 1. Index the footage (once, and again when folders change)

```bash
python3 <this skill's folder>/scripts/footage_index.py <folder> [<folder> ...] --out footage.json
```

It lists every video with its length, size, orientation and date, and makes a thumbnail strip for each one in `footage-thumbs/` so you can see what is in it. Folders come from "Where my footage lives" in CONTEXT.md.

## 2. Plan every beat

For each beat of `script.md` give the time range, the line, and what is on screen. What is on screen comes only from these, in this order:

1. The user talking to camera (copy the original's framing: how big the face is, where the camera sits).
2. Their own clip, by file name from `footage.json` (look at its thumbnails before you pick it), with the in and out point.
3. A real screen or screenshot that proves the point (say exactly what it shows and where to capture it).
4. Something they have to film (one line: what, where, how long).

Never stock footage, never AI-generated footage, never the original reel's footage.

## 3. Write `reels/<short-name>/shot-plan.md`

The beat table, then three lists:

- **Film:** every shot they still have to record.
- **Screens and screenshots to capture:**
- **Edit moves to copy:** the cuts, captions, zooms and sounds from BREAKDOWN.md worth matching, with their times.
