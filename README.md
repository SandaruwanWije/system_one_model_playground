# System One Model Playground

This repository is a place to try small projects that use System One models from TypeSafe, especially Jev.

Each project lives in its own folder. Start with the one you care about, read its own README, then run it from that folder.

## Projects

### snake_game_jev

A Snake game where Jev chooses each move, and you can also play by hand and compare scores.

Open [snake_game_jev/README.md](snake_game_jev/README.md) for setup, controls, and how the code is arranged.

## What you need

1. Python 3.13 or newer
2. [uv](https://docs.astral.sh/uv/) to install packages and run the apps
3. A TypeSafe API key for any project that calls Jev

## Quick start

```bash
cd snake_game_jev
uv sync
uv run python main.py
```

If the API key is missing, the game shows a small dialog. Paste your key, save it, and the app writes it into a local `.env` file and starts.

## Repository layout

```text
system_one_model_playground/
  README.md
  snake_game_jev/
    README.md
    main.py
    game/
    sounds/
```

## Notes

Keep API keys in `.env`. Do not commit that file.

New playground ideas can be added as new folders next to `snake_game_jev`.
