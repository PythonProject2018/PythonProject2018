import math
import random
import pygame
WIDTH = 700
HEIGHT = 700
COLOUR = (255,255,255)
OBJ_WIDTH = 30
OBJ_HEIGHT = 30
class Player:
    def __init__(self,xpos,ypos,image):
        self.VEL = 10
        self.xpos = xpos
        self.ypos = ypos
        self.score = 0
        self.image = image
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.xpos>0:
                self.xpos -= self.VEL
        if keys[pygame.K_RIGHT] and self.xpos<(WIDTH-OBJ_WIDTH):
                self.xpos += self.VEL
        if keys[pygame.K_UP] and self.ypos>0:
                self.ypos -= self.VEL
        if keys[pygame.K_DOWN] and self.ypos<(HEIGHT-OBJ_HEIGHT):
                self.ypos += self.VEL
    def draw(self,screen):
        screen.blit(self.image,(self.xpos,self.ypos))
class Meme:
    def __init__(self,player,image):
        self.xpos = random.randint(0,WIDTH-OBJ_WIDTH)
        self.ypos = random.randint(0,HEIGHT-OBJ_HEIGHT)
        self.image = image
        while True:
            if math.sqrt((player.xpos - self.xpos)**2 + (player.ypos - self.ypos) ** 2) < 5 * OBJ_WIDTH:
                self.xpos = random.randint(0,WIDTH-OBJ_WIDTH)
                self.ypos = random.randint(0,HEIGHT-OBJ_HEIGHT)
                continue
            else:
                break
    def draw(self,screen):
        screen.blit(self.image,(self.xpos,self.ypos))
class Mine:
    VEL = 0.5
    def __init__(self,player,image):
        self.xpos = random.randint(0,WIDTH-OBJ_WIDTH) 
        self.ypos = random.randint(0,HEIGHT-OBJ_HEIGHT)
        self.image = image
        self.d = math.sqrt((self.xpos - player.xpos)**2 + (self.ypos - player.ypos)**2)
    def follow(self,player):
        if self.xpos != player.xpos:
            theta = math.atan(abs(float(self.ypos-player.ypos)/float(self.xpos-player.xpos)))
        else:
            theta = math.pi/2
        speed_factor = (1 + self.d/100)
        if self.xpos > player.xpos:
            if self.ypos > player.ypos:
                self.ypos -= Mine.VEL * math.sin(theta) * speed_factor
            if self.ypos < player.ypos:
                self.ypos += Mine.VEL * math.sin(theta) * speed_factor
            self.xpos -= Mine.VEL * math.cos(theta) * speed_factor
        if self.xpos < player.xpos:
            if self.ypos > player.ypos:
                self.ypos -= Mine.VEL * math.sin(theta) * speed_factor
            if self.ypos < player.ypos:
                self.ypos += Mine.VEL * math.sin(theta) * speed_factor
            self.xpos += Mine.VEL * math.cos(theta) * speed_factor
    def draw(self,screen):
        screen.blit(self.image,(self.xpos,self.ypos))
class List:
    def __init__(self):
        self.memes = []
        self.mines = []
        self.player = []
        self.specmemes = []
    def draw(self,screen):
        for x in self.mines:
            x.draw(screen)
        for x in self.memes:
            x.draw(screen)
class SpecMeme(Meme):
    def __init__(self,player,image,lists):
        Meme.__init__(self,player,image)
        self.xpos = random.randint(0, WIDTH - OBJ_WIDTH)
        self.ypos = random.randint( 0, HEIGHT - OBJ_HEIGHT)
        if (self.xpos == player.xpos and self.ypos == player.pos)or (self.xpos == lists.memes[0].xpos and self.ypos == lists.memes[0].ypos):
            self.xpos = random.randint(0, WIDTH - OBJ_WIDTH)
            self.ypos = random.randint( 0, HEIGHT - OBJ_HEIGHT)
class SpecMine(Mine):
    VEL = 2 
    def __init__(self,player,image):
        Mine.__init__(self,player,image)
        self.VEL = 2
        self.xpos = random.randint(0, WIDTH - OBJ_WIDTH)
        self.ypos = random.randint( 0, HEIGHT - OBJ_HEIGHT)
        if (self.xpos == player.xpos and self.ypos == player.pos):
            self.xpos = random.randint(0, WIDTH - OBJ_WIDTH)
            self.ypos = random.randint( 0, HEIGHT - OBJ_HEIGHT)
    def follow(self,player):
        if self.xpos != player.xpos:
            theta = math.atan(abs(float(self.ypos-player.ypos)/float(self.xpos-player.xpos)))
        else:
            theta = math.pi/2
        speed_factor = (1 + self.d/100)
        if self.xpos > player.xpos:
            if self.ypos > player.ypos:
                self.ypos -= SpecMine.VEL * math.sin(theta) * speed_factor
            if self.ypos < player.ypos:
                self.ypos += SpecMine.VEL * math.sin(theta) * speed_factor
            self.xpos -= SpecMine.VEL * math.cos(theta) * speed_factor
        if self.xpos < player.xpos:
            if self.ypos > player.ypos:
                self.ypos -= SpecMine.VEL * math.sin(theta) * speed_factor
            if self.ypos < player.ypos:
                self.ypos += SpecMine.VEL * math.sin(theta) * speed_factor
            self.xpos += SpecMine.VEL * math.cos(theta) * speed_factor
class CollideCheck:
    def __init__(self,screen):
        self.screen = screen
    def IsColliding(self,a,b):
        return math.sqrt((a.xpos-b.xpos)**2 + (a.ypos-b.ypos)**2) < OBJ_WIDTH         #Checking if there is a collision between two objects.
    def Collide(self,lists,a,b):
        self.l = [a.__class__.__name__,b.__class__.__name__]
        if self.IsColliding(a,b):
            if self.l == [ "Player", "Mine"]:
                self.screen.fill( (0,0,0) )
                lists.player = []
                lists.memes = []
                lists.mines = []
                pygame.font.init()
                font= pygame.font.SysFont ('Comic Sans MS', 30)
                textSurf=  font.render( 'Your score is'+ str(a.score)+'Click on X in top right corner to exit.' ,False, (255,255,255) )
                self.screen.blit( textSurf, (0, HEIGHT/2))
            if self.l == ["Mine", "Player"]:
                self.screen.fill( (0,0,0) )
                lists.player = []
                lists.memes = []
                lists.mines = []
                pygame.font.init()
                font= pygame.font.SysFont ('Comic Sans MS', 30)
                textSurf1=  font.render( 'Your score is '+ str(b.score),False, (255,255,255) )
                textSurf2=  font.render( 'Press ESCAPE or click X in the top-right of the window to quit',False, (255,255,255) )
                self.screen.blit( textSurf1, (0,0))
                self.screen.blit( textSurf2, (0,60))
            if self.l == [ "Player", "SpecMine"]:
                self.screen.fill( (0,0,0) )
                lists.player = []
                lists.memes = []
                lists.mines = []
                pygame.font.init()
                font= pygame.font.SysFont ('Comic Sans MS', 30)
                textSurf1=  font.render( 'Your score is '+ str(b.score),False, (255,255,255) )
                textSurf2=  font.render( 'Press ESCAPE or click X in the top-right of the window to quit',False, (255,255,255) )
                self.screen.blit( textSurf1, (0,0))
                self.screen.blit( textSurf2, (0,60))
            if self.l == ["SpecMine", "Player"]:
                self.screen.fill( (0,0,0) )
                lists.player = []
                lists.memes = []
                lists.mines = []
                pygame.font.init()
                font= pygame.font.SysFont ('Comic Sans MS', 30)
                textSurf1=  font.render( 'Your score is '+ str(b.score),False, (255,255,255) )
                textSurf2=  font.render( 'Press ESCAPE or click X in the top-right of the window to quit',False, (255,255,255) )
                self.screen.blit( textSurf1, (0,0))
                self.screen.blit( textSurf2, (0,60))
            if self.l == [ "Mine", "Mine"]:
                lists.mines.pop(lists.mines.index(a))
                lists.mines.pop(lists.mines.index(b))
            if self.l == [ "SpecMine","Mine"]:
                lists.mines.pop(lists.mines.index(a))
                lists.mines.pop(lists.mines.index(b))

