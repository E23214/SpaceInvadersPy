import pygame
import os
import random
import csv

width = 1200
height = 800
ship_y = 600
ship_x = width/2
ship_width = 80
ship_length = 80
astroid_width = 80
astroid_length = 80
alien_width = 60
alien_length = 60
UI_Scale_Lives = 40
Bullet_width = 20
Bullet_len = 30
UI_Scale_BulletLen = 20
UI_Scale_BulletWid = 10


bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space.png")),(width, height))
pygame.display.set_caption("Elliot Alien Invasion")
ShipLives = pygame.transform.scale(pygame.image.load(os.path.join("assets","spaceship.png")),(UI_Scale_Lives,UI_Scale_Lives))
AmmoPng = pygame.transform.scale(pygame.image.load(os.path.join("assets","Orange.png")),(UI_Scale_BulletWid,UI_Scale_BulletLen))
display = pygame.display.set_mode((1200,800))
class Bullet:
    speed = 5
    x = 0
    y = ship_y
    def __init__(self, shipX):
        if(shipX < 0):
            speed = 0
            x = -10
            y = -10
        self.x = shipX
    def updatePosition(self):
        self.y-=10
    def drawBullet(self):
        BulletPng = pygame.transform.scale(pygame.image.load(os.path.join("assets","Orange.png")),(Bullet_width,Bullet_len))
        display.blit(BulletPng,(self.x,self.y))

class Astroid:
    y = 0
    x = 0
    def __init__(self):
        self.x =  random.randint(astroid_width,(width-astroid_width))
    def updatePosition(self):
        self.y+= 3
        
    def drawAstroid(self):
        AstroidPng = pygame.transform.scale(pygame.image.load(os.path.join("assets","asteroid.png")),(astroid_width,astroid_length))
        display.blit(AstroidPng,(self.x,self.y))

class Alien:
    alive = True
    y = 20
    x = 10
    iteration = 0
    deltaX = 3
    deltaY = 0
    def updatePosition(self):
        if(0  >= self.x or self.x >= width-astroid_width):
            self.deltaX = 0
            self.deltaY = height/200
        if(self.deltaY != 0 and self.y >= (self.iteration)*height/5):
            self.deltaY = 0
            self.deltaX = -3*self.iteration*(self.iteration%2) + 3*self.iteration*((self.iteration+1)%2)
            self.iteration+=1
        self.x+=self.deltaX
        self.y+=self.deltaY

    def drawAlien(self):
        AlienPng = pygame.transform.scale(pygame.image.load(os.path.join("assets","aliens.png")),(alien_width,alien_length))
        display.blit(AlienPng,(self.x,self.y))

class Player:
    PClock =  pygame.time.Clock()
    x = ship_x
    y = ship_y
    vel = 0
    accel = 0
    bulletsLive = []
    bulletsAmmo = 5
    bullets_cooldown = 400
    cooldown_tracker = 0
    last_shot = 0
    
    def draw(self):
        PlayerPng = pygame.transform.scale(pygame.image.load(os.path.join("assets","spaceship.png")),(ship_width,ship_length))
        display.blit(PlayerPng,(self.x, self.y))
        for i in self.bulletsLive:
            i.drawBullet()

    def calc_accel(self):
        self.vel = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
 
            self.vel = -10
        if keys[pygame.K_RIGHT]:

            self.vel = 10
        if(keys[pygame.K_SPACE]):
            self.shoot()
        if((self.x < 1 and keys[pygame.K_LEFT] )  or (self.x >= (width-ship_length) and keys[pygame.K_RIGHT])):
            self.vel = 0
        self.x +=self.vel

    def updatePosition(self):
        self.PClock.tick()
        self.calc_accel()
        self.bulletManager()
        self.x +=self.accel

    def bulletManager(self):
        self.cooldown_tracker += self.PClock.get_time()

        for i in self.bulletsLive:
            i.updatePosition()
            if(i.y < 0):
                self.bulletsLive.remove(i)
        if(self.cooldown_tracker >= 1300 and self.bulletsAmmo < 6):
            self.cooldown_tracker  = 0
            self.bulletsAmmo +=1
    def shoot(self):
        self.last_shot += self.PClock.get_time()
        if (self.bulletsAmmo > 0 and self.last_shot > self.bullets_cooldown):
            newBullet =  Bullet(self.x)
            self.bulletsLive.append(newBullet)
            self.bulletsAmmo-=1 
            self.last_shot = 0
class ScoreBoard:
    score = 0
    scores_list = {}
    scoreClock = pygame.time.Clock()
    def updateScore(self,int):
        self.score += int
    def printScore(self):
        text = pygame.font.SysFont('Corbel',35).render(f"Score: {self.score}", True,(150,150,150))
        display.blit(text , (width - 200 , 150))
    def ReadScore(self):
        with open(os.path.join("assets","Book1.csv"), mode='r', encoding='utf-8-sig')as scores_file:
            scores_dict = csv.reader(scores_file)
            self.scores_list = list(scores_dict)
            self.scores_list.remove(["Name","Score"])
            self.scores_list.sort(key=lambda x:int(x[1]))
            self.scores_list.insert(0,["Name","Score"])
                
    def WriteScore(self,Name):
        with open(os.path.join('assets','Book1.csv'), mode='a') as scores_file:
            score_writer = csv.writer(scores_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            score_writer.writerow([Name,self.score])
    def UserName(self):
        run = True
        user_text = ''
        display.blit(bg,(0,0))
        text = pygame.font.SysFont('Corbel',70).render("Enter your name:", True,(200,200,200))
        display.blit(text,((width/2 - 200),200))
        while(run):
            for event in pygame.event.get():
                # display.blit(text,((width/2 - 200),200))
                pygame.display.flip()
                user_name = pygame.font.SysFont('Corbel',50).render(user_text, True,(230,230,230))
                if(len(user_text)<6):
                    user_name = pygame.font.SysFont('Corbel',50).render(user_text+'_', True,(230,230,230))
                if event.type == pygame.QUIT:
                        return False
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:
                        run = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                        display.blit(bg,(0,0))
                        display.blit(text,((width/2 - 200),200))
                        display.blit(user_name,(width/2-50, height/3))
                    else:
                        if(len(user_text) <5 and event.key != pygame.K_SPACE):
                            user_text += event.unicode
                display.blit(user_name,(width/2-50, height/3))
            pygame.display.flip()
        if(len(user_text) != 0):
            self.WriteScore(user_text)
        self.ReadScore()
        display.blit(bg,(0,0))
        return True
    def PrintScoreBoard(self):
        open = self.UserName()
        Title = pygame.font.SysFont('Corbel',100).render("Highscores", True,(240,240,240))
        text = pygame.font.SysFont('Corbel',40).render("Press Space to Continue", True,(150,150,150))
        display.blit(Title, (width/2 -235, height/5))
        display.blit(text , (width/2 -175, height-50))
        i = 1
        Formatted_score = f"{'Name':<10} {'Score'}"
        Scores = pygame.font.SysFont('Corbel',50).render(Formatted_score, True,(230,230,230))
        for scores in reversed(self.scores_list):
            if(height/3+50*i < height):
                Formatted_score = f"{i}: {scores[0][0:6]:<10} {scores[1]}"
                Scores = pygame.font.SysFont('Courier',40).render(Formatted_score, True,(230,230,230))
                display.blit(Scores,(width/2 -235, height/3+40*i+10))
                i+=1
        while(open):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
        
            keys =pygame.key.get_pressed()
            
            if(keys[pygame.K_SPACE]):
                return True
            pygame.display.flip()        
        
class AlienInvaion:
    FPS = 60
    Astroids = []
    cooldown_tracker = 0
    lives = 3
    Aliens = []
    GameClock = pygame.time.Clock()
    MonsterList = [Astroids, Aliens]
    alien_timer = 0
    swarm_timer = 0
    swarm_size = 5
    score = 0
    swarm_tracker = 0
    ScoreBoard = ScoreBoard()
    def __init__(self):
        pygame.init()
        
        self.player_hit = pygame.mixer.Sound(os.path.join("assets","BeepBox-Song (1).wav"))
        
    def astroidManager(self):
        if(len(self.Astroids) < 5+int(self.ScoreBoard.score/7500) and self.cooldown_tracker == 0):
            x = Astroid()
            self.Astroids.append(x)
        self.cooldown_tracker += self.GameClock.get_time() +.01*self.ScoreBoard.score
        for i in self.Astroids:
            i.updatePosition()
            if(i.y > height):
                self.ScoreBoard.updateScore(10)
                self.Astroids.remove(i)

        if(self.cooldown_tracker >= 2000):
            self.cooldown_tracker  = 0

    def AlienManager(self):
        for i in self.Aliens:
            i.updatePosition()
            if(i.y > height):
                self.Aliens.remove(i)
        self.alien_timer+=self.GameClock.get_time()
        self.swarm_timer+=self.GameClock.get_time()
        if(self.swarm_timer > 10000-self.ScoreBoard.score):
            if(len(self.Aliens) < 20 +int(self.ScoreBoard.score/10000) and self.alien_timer > 500):
                    self.swarm_tracker+=1
                    self.Aliens.append(Alien())
                    self.alien_timer = 0
                    if(self.swarm_tracker == 5):
                        self.swarm_timer = 0
                        self.swarm_tracker = 0
    def main_menu(self):
        mainMenu = True
        pygame.mixer.music.load(os.path.join("assets","SimpleMainLoop.wav"))
        pygame.mixer.music.play(-1)
        while(mainMenu):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            keys =pygame.key.get_pressed()
            self.redraw()
            Title = pygame.font.SysFont('Corbel',100).render("Alien Invasion", True,(230,230,230))
            Assignment = pygame.font.SysFont('Corbel',40).render("Elliot Hagyard, SFWE 101", True,(200,200,200))
            text = pygame.font.SysFont('Corbel',50).render("Press Space to Continue", True,(150,150,150))
            display.blit(Title, (width/2 -235, height/2-50))
            display.blit(Assignment, (width/2-160, (height/20)))
            display.blit(text , (width/2 -185, height/2+55))
            if(keys[pygame.K_SPACE]):
                return True
            pygame.display.flip()
        pygame.mixer.music.unload()
        
    def run_game(self):
        open = True
        while open:
            self.player = Player()
            self.Aliens.clear()
            self.Astroids.clear()

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        open = False
            self.lives = 3
            open = self.main_menu()
            pygame.mixer.music.load(os.path.join("assets","MAinLoop1.wav"))
            pygame.mixer.music.play(-1)
            while(self.lives >0):
                self.GameClock.tick(self.FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        open = False
                        break   
                self.player.updatePosition()
                self.redraw()
                self.astroidManager()
                self.AlienManager()
                self.collisionDetection()
                self.bulletCollision()
                pygame.display.flip()
                if(open == False):
                    break
            if(open):
                open = self.ScoreBoard.PrintScoreBoard()
                self.ScoreBoard.score = 0 
        
    def redraw(self):
        display.blit(bg, (0,0))
        self.player.draw()
        for i in range(self.lives):
            display.blit(ShipLives,(width-UI_Scale_Lives*(self.lives-i) - UI_Scale_Lives, 50))
        for i in range(self.player.bulletsAmmo):
            display.blit(AmmoPng,(width-3*UI_Scale_BulletWid*(self.player.bulletsAmmo-i) - UI_Scale_BulletWid, 100))
        for i in self.Astroids:
            i.drawAstroid()
        for i in self.Aliens:
            i.drawAlien()
        self.ScoreBoard.printScore()

    def collisionDetection(self):
        for k in self.MonsterList:
            for i in k:
                if ((self.player.x > i.x
            and self.player.x < (i.x + 50))
            or ((self.player.x + 50) > i.x
            and (self.player.x + 50) < (i.x + 50))):
                    if ((self.player.y > i.y
                    and self.player.y < (i.y + 50))
                    or ((self.player.y + 50) > i.y
                    and (self.player.y + 50) < (i.y + 50))):
                        k.remove(i)
                        self.lives-=1
                        self.player_hit.play()


    
    def bulletCollision(self):
        for k in self.MonsterList:
            for i in k:
                for  j in self.player.bulletsLive:
                    if ((j.x > i.x
                    and j.x < (i.x + 60))
                    or ((j.x+ 60) > i.x
                    and (j.x + 60) < (i.x + 60))):
                        if ((j.y > i.y
                        and j.y < (i.y + 60))
                        or ((j.y + 60) > i.y
                        and (j.y + 60) < (i.y + 60))):
                        
                            self.ScoreBoard.updateScore(100)
                            k.remove(i)
                            self.player.bulletsLive.remove(j)
if __name__ == '__main__':
    ai = AlienInvaion()
    ai.run_game()
    pygame.quit()