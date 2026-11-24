# IG Reels Saved Content Workflow

Save a reel on Instagram. Get your own version back: the reel watched frame by frame, a script in your voice with three hooks, a shot plan from your own camera roll, and a card on your content calendar.

Six free Claude Code skills. This is the workflow from my reel, so you can run it yourself.

## What it does

| Step | Skill | You get |
|---|---|---|
| 0 | `context-profile` | `CONTEXT.md`: how you talk, who you talk to, what's true about you, where your footage lives |
| 1 | `reel-breakdown` | Contact sheets of the whole reel at 4 frames a second, a still after every cut, the transcript, and `BREAKDOWN.md` (every beat: what's said, what's on screen, the edit move) |
| 2 | `my-version-script` | `script.md`: same format, same pace, all new words in your voice, three hooks (outcome, niche, broad claim) |
| 3 | `shot-plan-from-my-footage` | `shot-plan.md`: every beat from your own talking head, your own clips by file name and real screenshots, plus what you still need to film |
| 4 | `calendar-card` | A card on your calendar (Notion if it's connected, otherwise a Markdown file in `calendar/`) |
| all | `save-to-my-version` | All of the above from one reel link |

The rule it follows: **copy the format, never the video.** The structure is what made the reel work. The story has to be yours, and it only uses facts you gave it.

## Setup (5 minutes)

1. Install [Claude Code](https://claude.com/claude-code), plus `ffmpeg` and `yt-dlp`:
   ```bash
   brew install ffmpeg yt-dlp
   ```
   For transcripts, also install whisper: `brew install whisper-cpp` and download a model to `~/.whisper-models/ggml-small.en.bin` (or `pip install openai-whisper`). Without it, the breakdown works from the frames alone.
2. Clone this repo and open it in Claude Code:
   ```bash
   git clone https://github.com/Bennettxai/ig-reels-saved-content-workflow.git
   cd ig-reels-saved-content-workflow
   claude
   ```
   The skills in `skills/` work from here. To use them in every project, copy the folders into `~/.claude/skills/`.
3. Build your context once: tell Claude **"set up my context profile"**.

## Use it

Paste a reel link you saved:

```
make my version of https://www.instagram.com/reel/XXXXXXXXXXX/
```

Claude downloads the public reel, reads every frame, writes your version, plans the shots from your footage and puts it on your calendar. Everything stays in `reels/<name>/` on your machine.

## Notes

- Public reels only. It never logs in to Instagram or touches your account.
- Reference reels are for study. Don't repost someone else's footage.
- No stock or AI footage in the shot plans, on purpose: people follow people.

Made by [@bennett.spooner](https://www.instagram.com/bennett.spooner/). If it helps, tag me in your version.

MIT licence.
