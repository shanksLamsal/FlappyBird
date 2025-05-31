import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
PIPE_WIDTH = 70
PIPE_GAP = 150
BIRD_RADIUS = 20
GRAVITY = 0.5
JUMP_STRENGTH = -10
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
BROWN = (222, 184, 135)

# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird")

# Load bird image
bird_img = pygame.transform.scale(pygame.image.load("bird.png"), (40, 40))


class Bird:
    def __init__(self):
        self.x = 80
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = JUMP_STRENGTH

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        screen.blit(bird_img, (self.x - BIRD_RADIUS, self.y - BIRD_RADIUS))

    def get_rect(self):
        return pygame.Rect(self.x - BIRD_RADIUS, self.y - BIRD_RADIUS, 2 * BIRD_RADIUS, 2 * BIRD_RADIUS)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - GROUND_HEIGHT - 50)

    def move(self):
        self.x -= 4

    def draw(self):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        # Bottom pipe
        bottom_pipe_y = self.height + PIPE_GAP
        pygame.draw.rect(screen, GREEN, (self.x, bottom_pipe_y, PIPE_WIDTH, SCREEN_HEIGHT - bottom_pipe_y - GROUND_HEIGHT))

    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP - GROUND_HEIGHT)
        return top_rect, bottom_rect


def check_collision(bird, pipes):
    bird_rect = bird.get_rect()
    for pipe in pipes:
        if bird_rect.colliderect(pipe.get_rects()[0]) or bird_rect.colliderect(pipe.get_rects()[1]):
            return True
    if bird.y - BIRD_RADIUS < 0 or bird.y + BIRD_RADIUS > SCREEN_HEIGHT - GROUND_HEIGHT:
        return True
    return False


def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * 200) for i in range(3)]
    score = 0
    running = True
    font = pygame.font.SysFont("Arial", 32)

    while running:
        screen.fill(BLUE)
        pygame.draw.rect(screen, BROWN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.move()
        bird.draw()

        for pipe in pipes:
            pipe.move()
            pipe.draw()
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                pipes.append(Pipe(SCREEN_WIDTH + 200))
                score += 1

        if check_collision(bird, pipes):
            print(f"Game Over! Final Score: {score}")
            pygame.quit()
            sys.exit()

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
create an bird.png image for this code

