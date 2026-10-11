# Jev Snake

A Snake game powered by Jev from TypeSafe.

Jev picks the next safe move from facts the game computes. You can also take the controls yourself and race for a better score.

## What you get

1. Jev mode: the model plays and you see live move probabilities
2. You mode: play with arrow keys or WASD
3. Separate current score and best score for You and for Jev
4. Pause and resume
5. Soft snake body, glowing apple, and an eat sound
6. If the API key is missing, a dialog asks for it and saves it to `.env`

## Requirements

1. Python 3.13 or newer
2. [uv](https://docs.astral.sh/uv/)
3. A TypeSafe API key

## Run

From this folder:

```bash
uv sync
uv run python main.py
```

On first run without a key, enter your `TYPESAFE_API_KEY` in the dialog. The app stores it in `.env` and starts.

You can also create `.env` yourself:

```text
TYPESAFE_API_KEY=your_key_here
```

## Controls

Switch to You or Jev with the top left buttons.

Pause or resume with the pause icon, Space, or P.

In You mode, move with arrow keys, WASD, or the direction pads.

Quit by closing the window.

## How a turn works

1. The board lists only legal moves.
2. For each legal move, the game builds short facts such as distance to food and reachable space.
3. In Jev mode those facts go to TypeSafe as one choice question. Jev answers with probabilities.
4. The snake takes the chosen direction. Eating food plays a sound and raises the score.
5. Hitting a wall or the body ends the run and updates best score for the active player.

## Folder map

```text
snake_game_jev/
  main.py                 starts the app and checks the API key
  pyproject.toml          project and dependencies
  sounds/                 eat sound
  game/
    app.py                main loop
    core/                 config, env, directions, API key dialog
    domain/               board rules and scores
    ai/                   Jev client
    audio/                sound playback
    engine/               session, clock, input
    view/                 drawing
      widgets/            top bar, pads, disc, grid, pause overlay
      sprites/            snake, apple, dotted routes
```

## Code roles in plain words

`Board` knows the grid, snake, food, and what happens after a move.

`Jev` asks TypeSafe which way to go.

`Session` ties board, Jev, scores, pause, and mode together.

`InputHandler` reads keyboard and mouse.

`Renderer` paints the screen using small view pieces.

## Tips

Keep `.env` private. It is listed in `.gitignore`.

Jev needs a network call each turn, so moves wait on the API.

Use Pause if you want to stop and look at the board.

## Credit

This project is part of the System One Model Playground. Jev and the TypeSafe API belong to TypeSafe AI.

The eat sound comes from Pixabay:
https://pixabay.com/sound-effects/people-eating-sound-effect-36186/
