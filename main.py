import pygame
pygame.init()


WIDTH, HEIGHT = 700,500
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("pong")

FPS =60

WHITE = (255,255,255)
BLACK =(0,0,0)
BALL_RADIUS=7
WINNING_SCORE =10

paddleHeight, paddleWidth = 100, 20

SCORE_FONT= pygame.font.SysFont("comicsans",50)

class Paddle():
    COLOR = WHITE
    VELOCITY=   4
    def __init__(self,x,y,width,height):
        self.x =self.originalX =x
        self.y=self.originalY =y
        self.width =width
        self.height =height
    def draw(self, window):
        pygame.draw.rect(window,self.COLOR,(self.x,self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -=self.VELOCITY
        else:
            self.y += self.VELOCITY
    def reset(self):
        self.x = self.originalX
        self.y=self.originalY

class Ball:
    maxVel=5
    COLOR =WHITE
    def __init__(self,x,y,radius):
        self.x =self.originalX =x
        self.y =self.originalY = y
        self.radius =radius
        self.xVel= self.maxVel
        self.yVel = 0

    def draw(self,window):
        pygame.draw.circle(window,self.COLOR,(self.x,self.y),self.radius)

    def move(self):
        self.x += self.xVel
        self.y+=self.yVel

    def reset(self):
        self.x = self.originalX
        self.y= self.originalY
        self.yVel=0
        self.xVel*=-1


def draw(window, paddles,ball,leftScore,rightScore):
    window.fill(BLACK)

    leftScoreText=SCORE_FONT.render(f"{leftScore}",1,WHITE)
    rightScoreText=SCORE_FONT.render(f"{rightScore}",1,WHITE)
    window.blit(leftScoreText,(WIDTH//4-leftScoreText.get_width()//2,20))
    window.blit(rightScoreText,(WIDTH*(3/4)-rightScoreText.get_width()//2,20))



    for paddle in paddles:
        paddle.draw(window)

    for i in range(10, HEIGHT,HEIGHT//20):
        if i % 2 ==1:
            continue
        pygame.draw.rect(window,WHITE,(WIDTH//2-5, i, 10,HEIGHT//20))
    
    ball.draw(window)

    pygame.display.update()


def handleCollision(ball,leftPaddle,rightPaddle):
    if ball.y +ball.radius >=HEIGHT:
        ball.yVel*=-1
    elif ball.y-ball.radius <=0:
        ball.yVel*=-1

    if ball.xVel<0:
        if ball.y>=leftPaddle.y and ball.y<=leftPaddle.y+leftPaddle.height:
            if ball.x -ball.radius<=leftPaddle.x+leftPaddle.width:
                ball.xVel *= -1

                middleY=leftPaddle.y+leftPaddle.height/2
                diffInY = middleY-ball.y
                reductionFactor =(leftPaddle.height/2)/ball.maxVel
                yVel= diffInY/reductionFactor
                ball.yVel=-1 *yVel
    else:
        if ball.y>=rightPaddle.y and ball.y <= rightPaddle.y+rightPaddle.height:
            if ball.x + ball.radius>=rightPaddle.x:
                ball.xVel *=-1

                middleY=rightPaddle.y+rightPaddle.height/2
                diffInY = middleY-ball.y
                reductionFactor =(rightPaddle.height/2)/ball.maxVel
                yVel= diffInY/reductionFactor
                ball.yVel=-1 *yVel



def handlePaddleMovement(keys, leftPaddle,rightPaddle):
    if keys[pygame.K_w] and leftPaddle.y - leftPaddle.VELOCITY >=0:
        leftPaddle.move(up=True)
    if keys[pygame.K_s] and leftPaddle.y + leftPaddle.VELOCITY+leftPaddle.height <=HEIGHT:
        leftPaddle.move(up=False)


    if keys[pygame.K_UP] and rightPaddle.y - rightPaddle.VELOCITY >=0 :
        rightPaddle.move(up=True)
    if keys[pygame.K_DOWN] and rightPaddle.y +  rightPaddle.VELOCITY+   rightPaddle.height <=HEIGHT:
        rightPaddle.move(up=False)

    

    


def main():
    run =True
    clock = pygame.time.Clock()

    leftPaddle =Paddle(10, HEIGHT//2- paddleHeight//2, paddleWidth, paddleHeight)
    rightPaddle =Paddle(WIDTH -10 - paddleWidth, HEIGHT//2- paddleHeight//2, paddleWidth, paddleHeight)

    ball=  Ball(WIDTH//2,HEIGHT//2,BALL_RADIUS)

    leftScore = 0
    rightScore=0

    while run:
        clock.tick(FPS)
        draw(WINDOW,[leftPaddle,rightPaddle],ball,leftScore,rightScore)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run =False
                break
        
        keys = pygame.key.get_pressed()
        handlePaddleMovement(keys,leftPaddle,rightPaddle)

        ball.move()
        handleCollision(ball,leftPaddle, rightPaddle)

        if ball.x<0:
            rightScore +=1
            ball.reset()
            rightPaddle.reset()
            leftPaddle.reset()
        elif ball.x>WIDTH:
            leftScore+=1    
            ball.reset()
            leftPaddle.reset()
            rightPaddle.reset()

        won =False
        if leftScore >=WINNING_SCORE:
            won =True
            winText="Left player won!"
        elif rightScore >= WINNING_SCORE:
            won =True
            winText= "Right player won!"
        if won:
            text = SCORE_FONT.render(winText,1,WHITE)
            WINDOW.blit(text,(WIDTH//2-text.get_width()//2,HEIGHT//2-text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            leftPaddle.reset()
            rightPaddle.reset()
            leftScore=0
            rightScore=0


    pygame.quit()


if __name__ =="__main__":
    main()