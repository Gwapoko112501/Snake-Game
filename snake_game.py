import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 12

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
DARK_PURPLE = (64, 0, 64)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)

# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont('Arial', 28, bold=True)
large_font = pygame.font.SysFont('Arial', 48, bold=True)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.color = GREEN
        self.score = 0
        self.grow_steps = 0
    
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head = self.get_head_position()
        x, y = self.direction
        new_head = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)
        
        # Check for self collision
        if new_head in self.positions[2:]:
            return False
        
        # Add new head
        self.positions.insert(0, new_head)
        
        # Remove tail if not growing
        if len(self.positions) > self.length:
            self.positions.pop()
        
        return True
    
    def render(self, surface):
        # Render snake body with gradient effect
        for i, p in enumerate(self.positions):
            # Calculate color based on position in snake
            color_ratio = i / len(self.positions)
            segment_color = (
                int(GREEN[0] * (1 - color_ratio) + DARK_GREEN[0] * color_ratio),
                int(GREEN[1] * (1 - color_ratio) + DARK_GREEN[1] * color_ratio),
                int(GREEN[2] * (1 - color_ratio) + DARK_GREEN[2] * color_ratio)
            )
            
            # Draw snake segment
            rect = pygame.Rect(
                p[0] * GRID_SIZE, 
                p[1] * GRID_SIZE, 
                GRID_SIZE, 
                GRID_SIZE
            )
            pygame.draw.rect(surface, segment_color, rect)
            
            # Add glow effect to head
            if i == 0:
                glow_rect = pygame.Rect(
                    p[0] * GRID_SIZE - 2, 
                    p[1] * GRID_SIZE - 2, 
                    GRID_SIZE + 4, 
                    GRID_SIZE + 4
                )
                pygame.draw.rect(surface, (0, 200, 0, 128), glow_rect, border_radius=4)
        
        # Draw snake face on head
        head_pos = self.positions[0]
        head_rect = pygame.Rect(
            head_pos[0] * GRID_SIZE, 
            head_pos[1] * GRID_SIZE, 
            GRID_SIZE, 
            GRID_SIZE
        )
        
        # Draw eyes
        eye_size = GRID_SIZE // 5
        eye_offset = GRID_SIZE // 3
        
        # Determine eye positions based on direction
        if self.direction == UP:
            left_eye = (head_pos[0] * GRID_SIZE + eye_offset, head_pos[1] * GRID_SIZE + eye_offset)
            right_eye = (head_pos[0] * GRID_SIZE + GRID_SIZE - eye_offset - eye_size, head_pos[1] * GRID_SIZE + eye_offset)
        elif self.direction == DOWN:
            left_eye = (head_pos[0] * GRID_SIZE + eye_offset, head_pos[1] * GRID_SIZE + GRID_SIZE - eye_offset - eye_size)
            right_eye = (head_pos[0] * GRID_SIZE + GRID_SIZE - eye_offset - eye_size, head_pos[1] * GRID_SIZE + GRID_SIZE - eye_offset - eye_size)
        elif self.direction == LEFT:
            left_eye = (head_pos[0] * GRID_SIZE + eye_offset, head_pos[1] * GRID_SIZE + eye_offset)
            right_eye = (head_pos[0] * GRID_SIZE + eye_offset, head_pos[1] * GRID_SIZE + GRID_SIZE - eye_offset - eye_size)
        else:  # RIGHT
            left_eye = (head_pos[0] * GRID_SIZE + GRID_SIZE - eye_offset - eye_size, head_pos[1] * GRID_SIZE + eye_offset)
            right_eye = (head_pos[0] * GRID_SIZE + GRID_SIZE - eye_offset - eye_size, head_pos[1] * GRID_SIZE + GRID_SIZE - eye_offset - eye_size)
        
        # Draw white part of eyes
        pygame.draw.circle(surface, WHITE, left_eye, eye_size)
        pygame.draw.circle(surface, WHITE, right_eye, eye_size)
        
        # Draw pupils
        pupil_size = eye_size // 2
        pupil_offset = eye_size // 3
        
        # Adjust pupil position based on direction
        if self.direction == UP:
            left_pupil = (left_eye[0], left_eye[1] + pupil_offset)
            right_pupil = (right_eye[0], right_eye[1] + pupil_offset)
        elif self.direction == DOWN:
            left_pupil = (left_eye[0], left_eye[1] - pupil_offset)
            right_pupil = (right_eye[0], right_eye[1] - pupil_offset)
        elif self.direction == LEFT:
            left_pupil = (left_eye[0] + pupil_offset, left_eye[1])
            right_pupil = (right_eye[0] + pupil_offset, right_eye[1])
        else:  # RIGHT
            left_pupil = (left_eye[0] - pupil_offset, left_eye[1])
            right_pupil = (right_eye[0] - pupil_offset, right_eye[1])
        
        pygame.draw.circle(surface, BLACK, left_pupil, pupil_size)
        pygame.draw.circle(surface, BLACK, right_pupil, pupil_size)
        
        # Draw mouth
        mouth_width = GRID_SIZE // 2
        mouth_height = GRID_SIZE // 4
        
        if self.direction == UP:
            mouth_rect = pygame.Rect(
                head_pos[0] * GRID_SIZE + (GRID_SIZE - mouth_width) // 2,
                head_pos[1] * GRID_SIZE + GRID_SIZE - mouth_height,
                mouth_width,
                mouth_height
            )
        elif self.direction == DOWN:
            mouth_rect = pygame.Rect(
                head_pos[0] * GRID_SIZE + (GRID_SIZE - mouth_width) // 2,
                head_pos[1] * GRID_SIZE,
                mouth_width,
                mouth_height
            )
        elif self.direction == LEFT:
            mouth_rect = pygame.Rect(
                head_pos[0] * GRID_SIZE + GRID_SIZE - mouth_height,
                head_pos[1] * GRID_SIZE + (GRID_SIZE - mouth_width) // 2,
                mouth_height,
                mouth_width
            )
        else:  # RIGHT
            mouth_rect = pygame.Rect(
                head_pos[0] * GRID_SIZE,
                head_pos[1] * GRID_SIZE + (GRID_SIZE - mouth_width) // 2,
                mouth_height,
                mouth_width
            )
        
        pygame.draw.rect(surface, BLACK, mouth_rect)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.spawn()
        self.pulse_size = 0
        self.pulse_direction = 1
    
    def spawn(self, snake_positions=None):
        if snake_positions is None:
            snake_positions = []
        
        # Find a position not occupied by the snake
        while True:
            self.position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if self.position not in snake_positions:
                break
    
    def render(self, surface):
        # Draw pulsing effect
        self.pulse_size += self.pulse_direction
        if self.pulse_size >= 10 or self.pulse_size <= 0:
            self.pulse_direction *= -1
        
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE, 
            self.position[1] * GRID_SIZE, 
            GRID_SIZE, 
            GRID_SIZE
        )
        
        # Draw main food
        pygame.draw.rect(surface, self.color, rect, border_radius=GRID_SIZE // 2)
        
        # Draw pulsing glow
        glow_rect = pygame.Rect(
            self.position[0] * GRID_SIZE - self.pulse_size, 
            self.position[1] * GRID_SIZE - self.pulse_size, 
            GRID_SIZE + 2 * self.pulse_size, 
            GRID_SIZE + 2 * self.pulse_size
        )
        pygame.draw.rect(surface, (255, 100, 100, 128), glow_rect, border_radius=GRID_SIZE // 2)

class Particle:
    def __init__(self, position, color):
        self.position = list(position)
        self.color = color
        self.lifespan = 30
        self.age = 0
        self.velocity = [
            random.uniform(-1, 1) * GRID_SIZE / 10,
            random.uniform(-1, 1) * GRID_SIZE / 10
        ]
    
    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.age += 1
    
    def render(self, surface):
        alpha = max(0, 255 * (1 - self.age / self.lifespan))
        color = (self.color[0], self.color[1], self.color[2], alpha)
        rect = pygame.Rect(
            self.position[0] - GRID_SIZE // 4,
            self.position[1] - GRID_SIZE // 4,
            GRID_SIZE // 2,
            GRID_SIZE // 2
        )
        pygame.draw.rect(surface, color, rect, border_radius=GRID_SIZE // 4)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.particles = []
        self.game_over = False
        self.score = 0
        self.level = 1
        self.speed = FPS
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                else:
                    if event.key == pygame.K_UP and self.snake.direction != DOWN:
                        self.snake.next_direction = UP
                    elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                        self.snake.next_direction = DOWN
                    elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                        self.snake.next_direction = LEFT
                    elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                        self.snake.next_direction = RIGHT
    
    def update(self):
        if self.game_over:
            return
        
        # Update snake
        if not self.snake.update():
            self.game_over = True
            return
        
        # Check if snake ate food
        if self.snake.get_head_position() == self.food.position:
            self.snake.length += 1
            self.snake.score += 1
            self.score = self.snake.score
            self.food.spawn(self.snake.positions)
            
            # Create particles when eating food
            for _ in range(10):
                particle_color = (
                    random.randint(200, 255),
                    random.randint(0, 100),
                    random.randint(0, 100)
                )
                self.particles.append(
                    Particle(
                        (
                            self.food.position[0] * GRID_SIZE + GRID_SIZE // 2,
                            self.food.position[1] * GRID_SIZE + GRID_SIZE // 2
                        ),
                        particle_color
                    )
                )
            
            # Level up every 5 points
            if self.score % 5 == 0:
                self.level += 1
                self.speed = min(FPS + self.level, 25)
    
    def render(self, surface):
        # Draw background grid
        surface.fill(GRAY)
        for x in range(0, WIDTH, GRID_SIZE):
            for y in range(0, HEIGHT, GRID_SIZE):
                rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(surface, LIGHT_GRAY, rect, 1)
        
        # Draw snake
        self.snake.render(surface)
        
        # Draw food
        self.food.render(surface)
        
        # Draw particles
        for particle in self.particles[:]:
            particle.update()
            particle.render(surface)
            if particle.age >= particle.lifespan:
                self.particles.remove(particle)
        
        # Draw score and level
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        level_text = font.render(f'Level: {self.level}', True, WHITE)
        surface.blit(score_text, (10, 10))
        surface.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))
        
        # Draw game over screen
        if self.game_over:
            game_over_text = large_font.render('GAME OVER', True, RED)
            restart_text = font.render('Press SPACE to restart', True, WHITE)
            surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
    
    def reset(self):
        self.snake.reset()
        self.food.spawn()
        self.particles = []
        self.game_over = False
        self.score = 0
        self.level = 1
        self.speed = FPS

# Main game loop
def main():
    game = Game()
    
    while True:
        game.handle_events()
        game.update()
        
        screen.fill(BLACK)
        game.render(screen)
        
        pygame.display.flip()
        clock.tick(game.speed)

if __name__ == "__main__":
    main()
