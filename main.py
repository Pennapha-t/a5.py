import random
import pygame
from pygame.math import Vector2

class Food():
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.r = 10

    def draw(self, screen):
        pygame.draw.circle(screen, (250,100,155), (self.position.x, self.position.y), self.r )    

    def recreate(self):
        self.position.x = random.randrange(100, 1180)
        self.position.y = random.randrange(100, 620)

class Agent():

    def __init__(self, x, y) -> None:
        self.r = 10
        self.mass = 1
        self.force = Vector2(1, 0)

        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acc = Vector2(1,0)

    def update(self):
        self.velocity = self.velocity + self.acc
        if self.velocity.magnitude() > 0 :
            self.velocity = self.velocity.clamp_magnitude(40)
        self.velocity = self.velocity * 0.9  
        self.position = self.position + self.velocity
        self.acc = Vector2(0,0)

    def draw(self, screen):
        pygame.draw.circle(screen, (100,100,255), (self.position.x, self.position.y), self.r )

    def applyForce(self, force):
        self.acc += force/self.mass

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    foods = []
    food_num = 10
    for i in range(food_num):
        x = random.randrange(20, 1260)
        y = random.randrange(20, 700)
        food = Food(x, y)
        foods.append(food)

    agents = []
    agent_num = 5
    for i in range(agent_num):
        x = random.randrange(20, 1000)
        y = random.randrange(20, 1000)
        agent = Agent(x, y)
        agents.append(agent)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("gray")

        for agent in agents:
            closest_food = min(foods, key=lambda f:(f.position - agent.position).magnitude())
            d = closest_food.position - agent.position
            distance = d.magnitude()

            if distance <= 300:
                if distance <= 100:
                    agent.applyForce(d.normalize())
                else:
                    agent.applyForce(d.normalize() * (distance / 100))
                if distance <= 2:
                    closest_food.recreate()

            agent.update()
            agent.draw(screen)

        for food in foods:
            food.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()