import pygame
import math
import random
import CLASSES
#Initialization
pygame.init()
SCREEN = pygame.display.set_mode((CLASSES.WIDTH,CLASSES.HEIGHT))
pygame.display.set_caption("Mines and Memes")
logo = pygame.image.load("./Assets/MainThings/Logo.jpg")
helpscreen = pygame.image.load("./Assets/MainThings/HelpScreen.jpg")
pygame.display.set_icon(logo)
run = False
menu_screen = True
help_screen = False
#Image Loading
Background = pygame.image.load("./Assets/MainThings/Background.jpg")
pimage = pygame.image.load("./Assets/MainThings/Boat.png")
mimage = pygame.image.load("./Assets/MainThings/Mine.jpeg")
meme1 = pygame.image.load("./Assets/MEMES/meme1.jpg")
ameme1 = pygame.image.load("./Assets/MEMES/ameme1.jpg")
meme2 = pygame.image.load("./Assets/MEMES/meme2.png")
ameme2 = pygame.image.load("./Assets/MEMES/ameme2.png")
meme3 = pygame.image.load("./Assets/MEMES/meme3.jpg")
ameme3 = pygame.image.load("./Assets/MEMES/ameme3.jpg")
meme4 = pygame.image.load("./Assets/MEMES/meme4.jpg")
ameme4 = pygame.image.load("./Assets/MEMES/ameme4.jpg")
meme5 = pygame.image.load("./Assets/MEMES/meme5.jpeg")
ameme5 = pygame.image.load("./Assets/MEMES/ameme5.jpeg")
meme6 = pygame.image.load("./Assets/MEMES/meme6.jpg")
ameme6 = pygame.image.load("./Assets/MEMES/ameme6.jpg")
meme7 = pygame.image.load("./Assets/MEMES/meme7.jpeg")
ameme7 = pygame.image.load("./Assets/MEMES/ameme7.jpeg")
meme8 = pygame.image.load("./Assets/MEMES/meme8.jpeg")
ameme8 = pygame.image.load("./Assets/MEMES/ameme8.jpeg")
memes_list = [meme1,meme2,meme3,meme4,meme5,meme6,meme7,meme8] 
amemes_list = [ameme1,ameme2,ameme3,ameme4,ameme5,ameme6,ameme7,ameme8] 
meme_index = 0
ameme_index = 0
lis = CLASSES.List()
lis.player.append(CLASSES.Player(CLASSES.WIDTH/2,CLASSES.HEIGHT/2,pimage))
lis.memes.append(CLASSES.Meme(lis.player[0],memes_list[meme_index % 8]))
coll = CLASSES.CollideCheck(SCREEN)
count = 1
lis.specmemes.append(CLASSES.SpecMeme( lis.player[0],amemes_list[ameme_index % 8],lis))
#Game Loop
while menu_screen:
    SCREEN.blit(Background,(-50,0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                menu_screen = False
                run = True
            if event.key == pygame.K_b:
                menu_screen = False
                help_screen = True
            if event.key == pygame.K_ESCAPE:
                menu_screen = False
        if event.type == pygame.QUIT:
            menu_screen = False
while help_screen:
    SCREEN.blit(helpscreen,(-10,0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                help_screen = False
                run = True
            if event.key == pygame.K_ESCAPE:
                help_screen = False
        if event.type == pygame.QUIT:
            help_screen = False
while run:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    pygame.time.delay(20)
    if (lis.mines,lis.memes,lis.mines) != ([],[],[]):
        SCREEN.fill(CLASSES.COLOUR)
    if len(lis.player) != 0:
        lis.player[0].draw(SCREEN)
        lis.player[0].move()
    if len(lis.player) != 0:
        for obj in lis.player:
            for meme in lis.memes:
                if math.sqrt((meme.xpos-obj.xpos)**2 + (meme.ypos-obj.ypos)**2) < CLASSES.OBJ_WIDTH:
                    pygame.mixer.music.load("./Assets/Sounds/CoinCollect.mp3")
                    pygame.mixer.music.play(0)
                    lis.memes.pop()
                    meme_index += 1
                    obj.score += 10
                    count = count + 1
                    lis.mines.append(CLASSES.Mine(obj,mimage))
                    lis.memes.append(CLASSES.Meme(obj,memes_list[meme_index % 8]))
            if count%6==0:
                CLASSES.Mine.VEL *= 1.0005
                CLASSES.SpecMine.VEL *= 1.0005
            if count%11 ==0 :
                lis.specmemes[0].draw(SCREEN)
                if math.sqrt((lis.specmemes[0].xpos-obj.xpos)**2 + (lis.specmemes[0].ypos-obj.ypos)**2) < CLASSES.OBJ_WIDTH:
                    pygame.mixer.music.load("./Assets/Sounds/SpecCoinCollect.mp3")
                    pygame.mixer.music.play(0)
                    lis.memes.pop()
                    lis.specmemes.pop()
                    obj.score += 50
                    ameme_index += 1
                    count = count%10 + 1
                    lis.mines.append(CLASSES.SpecMine(obj,mimage))
                    lis.memes.append(CLASSES.Meme(obj,memes_list[meme_index % 8]))
                    lis.specmemes.append(CLASSES.SpecMeme(obj,amemes_list[ameme_index % 8],lis))
            for mine in lis.mines:
                 mine.follow(obj)
            for mine in lis.mines:
                if coll.IsColliding(mine,obj):
                    pygame.mixer.music.load("./Assets/Sounds/DeathSound.mp3")
                    pygame.mixer.music.play(0)
                coll. Collide(lis, mine, obj)
                for mine2 in lis.mines:
                    if mine2 != mine:
                        if coll.IsColliding(mine,mine2):
                            pygame.mixer.music.load("./Assets/Sounds/BombExplosionSoundEffect.mp3")
                            pygame.mixer.music.play(0)
                        coll.Collide(lis, mine,mine2)
    if len(lis.memes) != 0:
        for meme in lis.memes:
            meme.draw(SCREEN)
    if len(lis.mines) != 0:
        for mine in lis.mines:
            mine.draw(SCREEN)
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    if keys[pygame.K_ESCAPE]:
        run = False
    pygame.display.update()
