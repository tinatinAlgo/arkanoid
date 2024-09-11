import pygame # type: ignore
import time
import random

pygame.init()

WIDTH = 800
HEIGHT = 450

back_color = (24, 42, 48)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(back_color)
paddle_img = pygame.image.load("paddle.png")
ball_img = pygame.image.load("paddle.png")
bar_images = ["brickBlue.png", "brickBrown.png", "brickGreen.png", "brickRed.png"]


menu_background = pygame.image.load("menu.jpg")
losing_background = pygame.image.load("loseBackground.jpg")
win_background = pygame.image.load("winBackground.jpg")


menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
losing_background = pygame.transform.scale(losing_background, (WIDTH, HEIGHT))
win_background = pygame.transform.scale(win_background, (WIDTH, HEIGHT))


MENU = "menu"
PLAYING = "playing"
WON = "won"
LOST = "lost"

game_state = MENU

class Paddle():
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = WIDTH//2
        self.y = HEIGHT - 30
        self.image = pygame.transform.scale(paddle_img, (self.width, self.height))
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Ball(): 
    def __init__(self):
        self.width = 20
        self.height = 20
        self.image = pygame.transform.scale(ball_img, (self.width, self.height))
        self.rect = self.image.get_rect(center = (WIDTH//2, HEIGHT - 50))
        self.x_speed = 3 * random.choice([-1, 1])
        self.y_speed = 3 * random.choice([-1, 1])

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.x_speed = -self.x_speed
        if self.rect.top <= 0:
            self.y_speed = -self.y_speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def bounce(self, hit_paddle=False):
        self.y_speed *= -1

        if hit_paddle:
            offset = (self.rect.centerx - paddle.rect.centerx) / (paddle.width / 2)
            self.x_speed += offset  
            if self.x_speed > 5:
                self.x_speed = 5  
            elif self.x_speed < -5:
                self.x_speed = -5

class Bar():
    def __init__(self, y, x, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(topleft = (x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def reset_game():
    global paddle, ball, bars, game_state
    paddle = Paddle()
    ball = Ball()
    bars = []

    x = 120
    y = 100
    for bar_image in bar_images:
        for i in range(8):
            bar = Bar(y, x + i * 70, bar_image)
            bars.append(bar)
        y += 50

    game_state = PLAYING


reset_game()

game_state = MENU

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == MENU and event.key == pygame.K_SPACE:
                reset_game()
            elif game_state in [WON, LOST] and event.key == pygame.K_SPACE:
                reset_game()
    if game_state == PLAYING:
        paddle.move()
        ball.update()

        if ball.rect.colliderect(paddle.rect):
            ball.bounce(hit_paddle=True)

        for bar in bars[:]:
            if ball.rect.colliderect(bar.rect):
                bars.remove(bar)
                ball.bounce()

        if ball.rect.bottom >= HEIGHT:
            game_state = LOST

        if not bars:
            game_state = WON


    if game_state == PLAYING:
        screen.fill(back_color)
        paddle.draw(screen)
        ball.draw(screen)
        for bar in bars:
            bar.draw(screen)    
    elif game_state == MENU:
        screen.blit(menu_background, (0,0))
    elif game_state == WON:
        screen.blit(win_background, (0,0))
    elif game_state == LOST:
        screen.blit(losing_background, (0,0))


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
