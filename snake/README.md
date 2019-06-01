# SNAKE Game

The game is rewrite based on https://gist.github.com/sanchitgangwar/2158089 . We split the 
drawing logic and game inner state, so that it can be easily migrated to any other UI system. 
What's more, it the first step to make a snake-ai -> in trainning, we just need the game state, and
the GUI became a burden.

## Game Screenshot

![screenshot](snake_running.png)

## Files

```bash
---
  | - snake_game_state.py 
  | - game.py : a runable game based on Curses
```