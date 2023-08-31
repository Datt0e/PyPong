import pygame
from sys import exit
from Entities import Player
from Entities import Ball
from random import randint


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640,360))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("font/Super Mario Bros.ttf", 40) 
        self.active = True
        #Score
        self.left_score = 0
        self.right_score = 0

        #Images
        self.bg_surf = pygame.image.load("Pictures/background.png").convert()

        #Player
        self.player_surf = pygame.image.load("Pictures/Player.png").convert_alpha()
        self.left_player_rect = self.player_surf.get_rect(center = (30,180))
        self.right_player_rect = self.player_surf.get_rect(center= (610,180))

        #Ball
        self.ball_surf = pygame.image.load("Pictures/Ball.png")
        self.ball_rect = self.ball_surf.get_rect(center=(320,randint(10,350)))

        #Player
        global player_left  #irwann global entfernen, is nicht gut
        global player_right
        player_left = Player(self.player_surf,self.left_player_rect)
        player_right = Player(self.player_surf,self.right_player_rect)
        
        #Ball class
        global ball
        ball = Ball(self.ball_surf,self.ball_rect)
        ball.set_angle()


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            print("pressed")
                            self.active = False

                if self.active == False:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.active = True
                                
            if self.active:
                keys = pygame.key.get_pressed()

                #Movement
                if keys[pygame.K_w]:
                    player_left.move_up()
                elif keys[pygame.K_s]:
                    player_left.move_down()

                if keys[pygame.K_UP]:
                    player_right.move_up()
                elif keys[pygame.K_DOWN]:
                    player_right.move_down()

                #Background
                self.screen.blit(self.bg_surf,(0,0))
                
                #Players
                self.screen.blit(self.player_surf,self.left_player_rect)
                self.screen.blit(self.player_surf,self.right_player_rect)

                #Score
                self.score_surf_left = self.font.render(str(self.left_score), False, "White")
                self.score_rect_left = self.score_surf_left.get_rect(midtop = (250,20))
                self.score_surf_right = self.font.render(str(self.right_score),False,"White")
                self.score_rect_right = self.score_surf_right.get_rect(midtop = (390,20))
                self.screen.blit(self.score_surf_left,self.score_rect_left)
                self.screen.blit(self.score_surf_right,self.score_rect_right)

                #Ball
                self.screen.blit(self.ball_surf,self.ball_rect)
                ball.start_mov()
                    
                #Ball collision with players
                if self.ball_rect.colliderect(self.right_player_rect):
                    ball.change_direc()

                if self.ball_rect.colliderect(self.left_player_rect):
                    ball.change_direc()
                
                #Ball collision with "Wall"
                if self.ball_rect.bottom >= 360:
                    ball.change_up_down()
                if self.ball_rect.top <= 0:
                    ball.change_up_down()

                #Ball out and someone scored
                if self.ball_rect.x > 660:
                    self.left_score += 1
                    self.ball_rect.center = (320,randint(10,350))
                    ball.change_direc()
                    ball.set_angle()
                if self.ball_rect.x < -20:
                    self.right_score +=1
                    self.ball_rect.center = (320,randint(10,350))
                    ball.change_direc()
                    ball.set_angle()

                #Rects in the middle
                pygame.draw.rect(self.screen, "grey", pygame.Rect(0,0,10,10))

            else:
                self.screen.fill("Black")


            pygame.display.update()
            self.clock.tick(60)




Game().run()