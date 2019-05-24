from PyGameFuncs import Button as BT, Screen_Display as SD
import time, random, sys, pygame, os
from pathlib import Path

#Config
width = 800
height = 800
fps = 100

players = input('How many people are playing? ')

#Initiation
pygame.init()
Screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
clock = pygame.time.Clock()

deadImage = pygame.image.load(os.path.join(Path(__file__).parent, 'Deadline Pics', 'Dead.png'))

LineList = []

class Player():
    def __init__(self, num):
        self.dead = False
        self.num = num
        if num == 1:
            self.images = (pygame.image.load(os.path.join(Path(__file__).parent, 'Deadline Pics', 'BlueArrowRight.png')).convert(),
                           pygame.image.load(os.path.join(Path(__file__).parent, 'Deadline Pics', 'BlueArrowUp.png')).convert(),
                           pygame.image.load(os.path.join(Path(__file__).parent, 'Deadline Pics', 'BlueArrowLeft.png')).convert(),
                           pygame.image.load(os.path.join(Path(__file__).parent, 'Deadline Pics', 'BlueArrowDown.png')).convert()
                           )
            self.direction = 'Right'
            self.rect = pygame.Rect(100, 400, 50, 40)
            self.keys = (pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_s)
        if num == 2:
            self.images = (pygame.image.load(os.path.join(Path(__file__).parent, 'Deadline Pics', 'PurpleArrowRight.png')).convert(),
                           pygame.image.load(os.path.join(Path(__file__).parent, 'Deadline Pics', 'PurpleArrowUp.png')).convert(),
                           pygame.image.load(os.path.join(Path(__file__).parent, 'Deadline Pics', 'PurpleArrowLeft.png')).convert(),
                           pygame.image.load(os.path.join(Path(__file__).parent, 'Deadline Pics', 'PurpleArrowDown.png')).convert()
                           )
            self.direction = 'Left'
            self.rect = pygame.Rect(700, 400, 50, 40)
            self.keys = (pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN)
        LineList.append(Line(num, self))

    def draw(self, death=None):
        if not self.dead:
            if self.direction == 'Right':
                self.rect[3] = 35
                self.rect[2] = 45
                Screen.blit(self.images[0], (self.rect[0] - self.rect[2], self.rect[1] - self.rect[3]))
            elif self.direction == 'Up':
                self.rect[3] = 45
                self.rect[2] = 35
                Screen.blit(self.images[1], (self.rect[0] - self.rect[2], self.rect[1] - self.rect[3]))
            elif self.direction == 'Left':
                self.rect[3] = 35
                self.rect[2] = 45
                Screen.blit(self.images[2], (self.rect[0] - self.rect[2], self.rect[1] - self.rect[3]))
            elif self.direction == 'Down':
                self.rect[3] = 45
                self.rect[2] = 35
                Screen.blit(self.images[3], (self.rect[0] - self.rect[2], self.rect[1] - self.rect[3]))
        elif death != None:
            Screen.blit(deadImage, (self.rect[0] - self.rect[2], self.rect[1] - self.rect[3]))

    def move(self):
        if not self.dead:
            keyed = pygame.key.get_pressed()
            directList = ('Right', 'Up', 'Left', 'Down')
            count = 0
            for key in self.keys:
                if keyed[key]:
                    try:
                        if self.direction != directList[count + 2] and self.direction != directList[count]:
                            self.direction = directList[count]
                            LineList.append(Line(self.num, self))
                    except:
                        if self.direction != directList[count - 2] and self.direction != directList[count]:
                            self.direction = directList[count]
                            LineList.append(Line(self.num, self))
                count = count + 1
            if self.direction == 'Right':
                self.rect[0] += 2
            elif self.direction == 'Up':
                self.rect[1] -= 2
            elif self.direction == 'Left':
                self.rect[0] -= 2
            elif self.direction == 'Down':
                self.rect[1] += 2
            if self.rect[0] - self.rect[2] <= 0 or self.rect[0] >= width or self.rect[1] - self.rect[3] <= 0 or self.rect[1] >= height:
                self.dead = True

    def main(self):
        self.draw()
        self.move()

class Line():
    def __init__(self, num, p):
        self.num = num
        self.parent = p
        self.direction = self.parent.direction
        self.XY = pygame.Rect(self.parent.rect[0], self.parent.rect[1], 0, 0)
        self.rect = pygame.Rect(self.XY[0], self.XY[1], 0, 0)
        self.cut = False
        if num == 1:
            self.color = (24, 38, 207)
        elif num == 2:
            self.color = (173, 40, 220)

    def draw(self):
        if self.direction == self.parent.direction and self.cut == False:
            self.update()
        else:
            self.cut = True
        if self.direction == 'Right' or self.direction == 'Left':
            pygame.draw.rect(Screen, self.color, (self.rect[0], self.rect[1], self.rect[2], 2))
        if self.direction == 'Up' or self.direction == 'Down':
            pygame.draw.rect(Screen, self.color, (self.rect[0], self.rect[1], 2, self.rect[3]))

    def update(self):
        plrPosX = self.parent.rect[0]
        plrPosY = self.parent.rect[1]
        linePosX = self.XY[0]
        linePosY = self.XY[1]
        self.rect[2] = plrPosX - linePosX
        self.rect[3] = plrPosY - linePosY

def StartMenu():
    starting = True
    while starting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                starting = False
        Screen.fill((255, 0, 0))
        SD.message_display(Screen, 'Deadline', 100, (0, 0, 255), width/2, height/2)
        SD.message_display(Screen, 'Press any button to start', 60, (0, 0, 255), width/2, round(height*0.75))
        pygame.display.update()
        clock.tick(round(fps/5))

def Main():
    PlayerList = []
    StartMenu()
    PlayerNum = int(players)
    for x in range(1, PlayerNum + 1):
        PlayerList.append(Player(x))
    playing = True
    while playing:
        Screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                
        for plr in PlayerList:
            if plr.dead:
                plr.draw(True)
                
        for line in LineList:
            line.draw()
            for plr in PlayerList:
                if line.rect.colliderect(plr.rect):
                    plr.dead = True
                    
        for plr in PlayerList:
            plr.main()

        ExitBtn = BT((750, 0, 50, 50), 'X', 40, (0, 0, 255))
        ExitBtn.draw(Screen, (255, 0, 0))
        ExitBtn.optClick(Screen, (200, 0, 0), (255, 0, 0), pygame.quit)
        pygame.display.update()
        clock.tick(fps)

    
Main()
sys.exit()
