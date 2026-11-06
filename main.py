import pygame
import json

WORLD_SIZE = 1000
DRONE_RADIUS = 5
CAM_DIST = 500
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
TIME_SCALE = 1.0
FPS = 60
COMPOSITION_FILE = "compositions/ilovealexa.json"

class Drone():
    def __init__(self, id, keyframes):
        self.id = id
        self.keyframes = keyframes
        self.x = keyframes[0]["x"]
        self.y = keyframes[0]["y"]
        self.z = keyframes[0]["z"]
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.v = 0

    def update(self, t):
        for a, b in zip(self.keyframes, self.keyframes[1:]):
            if t <= b["t"]:
                progress = (t - a["t"]) / (b["t"] - a["t"])
                self.x = a["x"] + (b["x"] - a["x"]) * progress
                self.y = a["y"] + (b["y"] - a["y"]) * progress
                self.z = a["z"] + (b["z"] - a["z"]) * progress
                return

        # Past the last keyframe, so stay there
        last = self.keyframes[-1]
        self.x, self.y, self.z = last["x"], last["y"], last["z"]


    def draw(self, screen):
        f = CAM_DIST * min(SCREEN_WIDTH, SCREEN_HEIGHT) / WORLD_SIZE
        d = self.z + CAM_DIST
        scale = f / d
        screen_x = SCREEN_WIDTH / 2 + (self.x - WORLD_SIZE / 2) * scale
        screen_y = SCREEN_HEIGHT / 2 - (self.y - WORLD_SIZE / 2) * scale
        radius = DRONE_RADIUS * scale
        pygame.draw.circle(screen, "white", pygame.Vector2(screen_x, screen_y), radius)

class Swarm():
    def __init__(self, filepath):
        self.drones = []
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for drone in data["drones"]:
                self.drones.append(Drone(
                    drone["id"],
                    drone["keyframes"]
                ))

    def update(self, t):
        for drone in self.drones:
            drone.update(t)

    def draw(self, screen):
        for drone in self.drones:
            drone.draw(screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    swarm = Swarm(COMPOSITION_FILE)
    t = 0

    while running:

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # NEXT STATE
        swarm.update(t)
        t += TIME_SCALE / FPS

        # WIPE SCREEN
        screen.fill("black")

        # RENDER STATE
        swarm.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()