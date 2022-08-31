"""
Pong game with Python
"""

import pygame
pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 3

class Paddle:
    """
    Class for the left and right paddle
    """

    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        """
        Draw paddle
        """
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        """
        Move paddle up or down
        """
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        """
        Reset paddle to its original position
        """
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    """
    Class for the game's ball
    """

    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        """
        Draw ball
        """
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        """
        Move ball
        """
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        """
        Reset ball position to the middle of the board
        """
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel *= -1
        self.y_vel = 0

def draw(win, paddles, ball, left_score, right_score):
    """
    Function to draw game on a window
    """

    win.fill(BLACK)
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH*  (3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)

    pygame.display.update()

def calculate_y_vel(paddle, ball):
    """
    Function to calculate y_vel according to the position where the ball hit the paddle.
    The further the ball hits the middle of the paddle, the faster it bounces.
    """

    middle_y = paddle.y + paddle.height / 2
    difference_in_y = middle_y - ball. y
    reduction_factor = (paddle.height / 2) / ball.MAX_VEL

    return (difference_in_y / reduction_factor) * -1

def handle_collision(ball, left_paddle, right_paddle):
    """
    Function to handle ball's collisions with the paddles and the board's borders
    """

    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        # Collision with board's borders
        ball.y_vel *= -1

    if ball.x_vel < 0:
        # Collision with left paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                ball.y_vel = calculate_y_vel(left_paddle, ball)
    else:
        # Collision with right paddle
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                ball.y_vel = calculate_y_vel(right_paddle, ball)

def handle_paddle_movement(keys, left_paddle, right_paddle):
    """
    Function to handle the paddles movement
    """

    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

def reset_elements(ball, left_paddle, right_paddle):
    """
    Reset the ball, the left paddle and the right paddle to their original position
    """

    ball.reset()
    left_paddle.reset()
    right_paddle.reset()

def main():
    """
    Main function to run the game
    """

    run  =  True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2,
                          PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    left_score = 0
    right_score = 0

    while run:
        # Regulate the speed of the while loop so the game runs with at the maximum
        # speed of FPS on every computer
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            reset_elements(ball, left_paddle, right_paddle)
            pygame.time.delay(1000)
        elif ball.x > WIDTH:
            left_score += 1
            reset_elements(ball, left_paddle, right_paddle)
            pygame.time.delay(1000)

        won = False
        if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!" if left_score >= WINNING_SCORE else "Right Player Won!"

        if won:
            # Show winning player
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)

            # Reset the game
            reset_elements(ball, left_paddle, right_paddle)
            left_score = 0
            right_score = 0

    pygame.quit()


if __name__ == '__main__':
    main()
