import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800,500))

# images
ball_image = pygame.transform.scale(pygame.image.load("ping pong game/ball.png"),(50,50))
paddle_image = pygame.transform.scale(pygame.image.load("ping pong game/paddle1.png"),(20,100))
dotted_line = pygame.transform.scale(pygame.image.load("ping pong game/dotted_line.png"),(20,500))
dotted_line_rect = dotted_line.get_rect(center = (400,250))

# fonts
font_sm = pygame.font.Font(None,30)
font_md = pygame.font.Font(None,40)
font_lg = pygame.font.Font(None,50)

score_font = pygame.font.Font(None,60)
space_font = pygame.font.Font(None, 70)

# rendering fonts
win = font_md.render("You win",False,"Black")
win_rect = win.get_rect(center = (400,250))
lose = font_md.render("You lose",False,"Black")
lose_rect = lose.get_rect(center = (400,250))
p1score = score_font.render(f"0",False,"white")
p2score = score_font.render(f"0",False,"white")
space = space_font.render("Click SPACE to start",False,"white")
manual_mode = font_sm.render("manual mode...",False,"yellow")
ai_mode = font_sm.render(f"AI Mode",False,"green")


class Ball():
    def __init__(self,ball_image , dx,dy):
        self.ball = ball_image
        self.ball_rect = self.ball.get_rect(center = (400,250))
        self.dx = dx
        self.dy = dy
        self.condition = "centre"
 
    def move(self):
        self.ball_rect.left += self.dx
        self.ball_rect.top += self.dy

    def checkWL(self):
        if self.ball_rect.left > 800:
            self.condition = "lose"

        if self.ball_rect.right < 0:
            self.condition = "win"


    
    def reset(self):
        self.ball_rect = self.ball.get_rect(center = (400,250))
        self.condition = "centre"

 
class Paddle:
    def __init__ (self,paddle,x,y):
        self.paddle = paddle
        self.paddle_rect = self.paddle.get_rect(center = (10,50))
        self.paddle_rect.left = x 
        self.paddle_rect.top = y
        self.score = 0
        self.speed = 1

    def up(self):
        self.paddle_rect.top -= self.speed
        if self.paddle_rect.top <= 0:
            self.paddle_rect.top += self.speed
       
    def down(self):
        self.paddle_rect.top += self.speed
        if self.paddle_rect.bottom >= 500:
            self.paddle_rect.top -= self.speed


class UserPaddle(Paddle):
    def __init__(self , paddle , x , y):
        # hey I am child and super() is my parent
        # why don't I pass all my value to my parent
        super().__init__(paddle , x , y)


class ComputerPaddle(Paddle):
    def __init__(self , paddle , x , y , mode):
        super().__init__(paddle , x , y)
        self.mode = mode

    def autoControl(self,ball):
        if self.mode == "manual" : 
            return 
        
        if ball.ball_rect.center[1] < self.paddle_rect.center[1]:
            self.up()
        elif ball.ball_rect.center[1] > self.paddle_rect.center[1]:
            self.down()
        else:
            pass


ball = Ball(ball_image, 3,0)

paddle1 = ComputerPaddle(paddle_image,0,0 , "automated")
paddle2 = UserPaddle(paddle_image,775,100)

print("1 - automated ( default ) - 2 - manual ")

def controlPaddles():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        paddle2.up()

    if keys[pygame.K_DOWN]:
        paddle2.down()

    if paddle1.mode == "manual":
        screen.blit(manual_mode,(30,20))
        if keys[pygame.K_w]:
            paddle1.up()
        if keys[pygame.K_s]:
            paddle1.down()
    
    else:
        screen.blit(ai_mode,(30,20))
        paddle1.autoControl(ball)

    if keys[pygame.K_a]:
        paddle1.mode = "automated"
        print("Switched to AI mode")
        
    if keys[pygame.K_m]:
        paddle1.mode = "manual"
        print("Switched to manual mode")
  
def ballMotion():
    keys = pygame.key.get_pressed()

    ball.checkWL()

    if ball.ball_rect.bottom > 500:
        ball.dy *= -1
    if ball.ball_rect.top< 0:
        ball.dy *= -1

    if pygame.Rect.colliderect(ball.ball_rect,paddle2.paddle_rect):
        ball.dx = -abs(ball.dx)
        ball.dy = random.randint(-abs(int(ball.dx)),abs(int(ball.dx)))
    if pygame.Rect.colliderect(ball.ball_rect,paddle1.paddle_rect):
        ball.dx = abs(ball.dx)
        ball.dy = random.randint(-abs(int(ball.dx)),abs(int(ball.dx)))

        
    if ball.condition == "lose":
        paddle1.score += 1
        ball.dx *= 1.2
        paddle1.speed *= 1.3
        paddle2.speed *= 1.3

        p1score = score_font.render(f"{paddle1.score}",False,"white")
        ball.reset()
        ball.condition = "centre"
   
    if ball.condition == "win":
        paddle2.score += 1
        ball.dx *= 1.2
        paddle1.speed *= 1.3
        paddle2.speed *= 1.3
        p2score = score_font.render(f"{paddle2.score}",False,"white")
        ball.reset()
        ball.condition = "centre"
    
    if ball.condition == "centre":
        #print("ball at centre")
        ball_rect = ball.center = (400,250)
        screen.blit(space,(200,150))
        if keys[pygame.K_SPACE]:
            ball.dy = 0 
            ball.condition = "moving"
            print("input detected")

    if ball.condition == "moving":
        ball.move() 

def draw():
    keys = pygame.key.get_pressed()

    screen.blit(dotted_line,dotted_line_rect)
    screen.blit(ball.ball,ball.ball_rect)
    screen.blit(paddle1.paddle,(paddle1.paddle_rect))
    screen.blit(paddle2.paddle,(paddle2.paddle_rect))

    # updateing score before blitting it
    p1score = score_font.render(f"{paddle1.score}",False,"white")
    p2score = score_font.render(f"{paddle2.score}",False,"white")
    win = font_md.render("Player 1(left) wins",False,"white")
    lose = font_md.render("player 2(right) wins ",False,"white")
    restart = font_lg.render("Click spacebar to restart",False,"white")
    screen.blit(font_md.render("P1",False,"white"),(10,470))
    screen.blit(font_md.render("P2",False,"white"),(760,470))
    
    screen.blit(p1score,(350,25))
    screen.blit(p2score,(425,25))

    if paddle1.score >= 7:
        screen.fill("red")
        
        screen.blit(win,(270,220))
        screen.blit(restart,(200,280))

        if keys[pygame.K_SPACE]:
            paddle1.score = 0
            paddle2.score = 0 
            ball.dx = 3
            paddle1.speed = 1
            paddle2.speed = 1

    if paddle2.score >= 7:
        screen.fill("green")
        
        screen.blit(lose,(270,220))
        screen.blit(restart,(200,280))

        if keys[pygame.K_SPACE]:
            paddle1.score = 0
            paddle2.score = 0
            ball.dx = 3
            paddle1.speed = 1
            paddle2.speed = 1

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.fill("black")

    ballMotion()
    controlPaddles()
    draw()
    
    pygame.display.flip()

    clock.tick(60)


