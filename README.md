# Drone Playground

A drone swarm simulator built with [pygame-ce](https://pyga.me/). Drones fly through a 3D world (x, y, z), drawn on screen with perspective projection: drones farther away (higher z) look smaller and drift toward the center of the view, the way they would through a real camera.

Swarm choreography is loaded from JSON "composition" files, where each drone follows a scripted route of timed keyframes.

## Getting started

Requires Python 3.

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## How it works

**World space.** Every axis runs from 0 to 1000. World `y = 1000` is the top of the screen, and `z` is distance from the viewer.

**Perspective.** The camera sits a fixed distance (`CAM_DIST`) behind the `z = 0` plane. Positions and sizes are scaled by `f / (z + CAM_DIST)` (the pinhole camera model), so apparent size falls off with the inverse of distance. The offset keeps drones from growing without bound as they get close.

**Motion.** Each drone moves along its keyframes with linear interpolation. After its last keyframe, a drone holds its final position.

## Composition files

Compositions live in `compositions/`. Each file lists drones, each with an `id` and a list of keyframes:

```json
{
  "drones": [
    {
      "id": "alpha",
      "keyframes": [
        {"t": 0.0, "x": 100, "y": 500, "z": 200},
        {"t": 4.0, "x": 478, "y": 456, "z": 200}
      ]
    }
  ]
}
```

- `t`: absolute time in seconds; times must increase within a drone's keyframes
- `x`, `y`, `z`: world coordinates, 0 to 1000

To play a different composition, change `COMPOSITION_FILE` in `main.py`.

## Settings

These constants are at the top of `main.py`:

| Constant | What it controls |
| --- | --- |
| `WORLD_SIZE` | Size of each world axis |
| `DRONE_RADIUS` | Drone size, in world units |
| `CAM_DIST` | Camera distance behind `z = 0`. Higher values give flatter perspective. |
| `SCREEN_WIDTH`, `SCREEN_HEIGHT` | Window size, in pixels |
| `TIME_SCALE` | Playback speed (`2.0` is double speed) |
| `FPS` | Frame rate |

## Roadmap

- Draw drone shapes (body, arms, rotors) in place of circles
- Draw farther drones first, so nearer drones overlap them correctly
- Looping and ping-pong playback modes for routes
- Validate composition files on load
- Behavioral "follower" drones that flock around the scripted leaders for more fluid motion
