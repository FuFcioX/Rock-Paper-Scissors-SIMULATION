#Importing necessary stuff
import pygame as pg
import random
import sys
import math



#Setting game window dimensions
pg.init()
pg.mixer.init()
WIDTH, HEIGHT = 800, 600
SIZE = (25, 25)
VAL = 10
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Rock, Paper, Scissors Simulation")
#Initializing music
pg.mixer.music.load("audio/Ambient Music - Chilled Sounds For Meditation, Sleep, Study and Deep Relaxation.wav")
pg.mixer.music.set_volume(1)
pg.mixer.music.play(-1)

rock_aud = pg.mixer.Sound("audio/Minecraft Stone Sound Effect (1).wav")
paper_aud = pg.mixer.Sound("audio/Paper Sound Effect.wav")
scissors_aud = pg.mixer.Sound("audio/Scissors - Sound Effect For Editing.wav")

rock_aud.set_volume(1)
paper_aud.set_volume(0.5)
scissors_aud.set_volume(0.7)

#Setting images and scaling
background_start = pg.transform.scale(pg.image.load('imgs/physicists.jpg'), (WIDTH, HEIGHT))
rock_img = pg.transform.scale(pg.image.load('imgs/stone.png'), SIZE)
scissors_img = pg.transform.scale(pg.image.load('imgs/scissor.png'), SIZE)
paper_img = pg.transform.scale(pg.image.load('imgs/paper.png'), SIZE)
background_img = pg.transform.scale(pg.image.load('imgs/background.jpg'), (WIDTH, HEIGHT))
icon_img = pg.image.load('imgs/icon.png')

#Font settings
font = pg.font.Font(None, 36)
font_2 = pg.font.Font("fonts/Minecrafter.Alt.ttf", 50)
font_3 = pg.font.Font("fonts/Minecrafter.Alt.ttf", 30)
#Creating window icon
pg.display.set_icon(icon_img)


#Creating object class

class Object:
    def __init__(self, count):
        self.count = count
        self.vel_x = 0.05
        self.vel_y = 0.05

        self.rock_positions = []
        self.paper_positions = []
        self.scissors_positions = []

        self.starting_positions()
    def starting_positions(self):
        for _ in range(self.count):
            self.rock_positions.append((random.randrange(50, WIDTH-50), random.randrange(50, HEIGHT-50)))
            self.paper_positions.append((random.randrange(50, WIDTH-50), random.randrange(50, HEIGHT-50)))
            self.scissors_positions.append((random.randrange(50, WIDTH-50), random.randrange(50, HEIGHT-50)))
    def collision(self):
        #Ruch dla rock, scissors
        for idx1, position_1 in enumerate(self.rock_positions):
            value = math.inf
            target_position = None
            target_idx = None
            for idx2, position_2 in enumerate(self.scissors_positions):
                d = math.sqrt((position_1[0] - position_2[0])**2 + (position_1[1] - position_2[1])**2)
                if d < value:
                    value = d
                    target_position = position_2
                    target_idx = idx2
            if target_position:
                position_1 = list(position_1)
                target_position = list(target_position)
                if value < VAL:
                    pg.mixer.Sound.play(rock_aud)
                    self.scissors_positions.pop(target_idx)
                    self.rock_positions.append(tuple(target_position))
                    continue

                dx = target_position[0] - position_1[0]
                dy = target_position[1] - position_1[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)

                if distance != 0:
                    position_1[0] += self.vel_x * (dx / distance)
                    position_1[1] += self.vel_x * (dy / distance)



                self.rock_positions[idx1] = tuple(position_1)


        #Ruch dla scissors, paper
        for idx1, position_1 in enumerate(self.scissors_positions):
            value = math.inf
            target_position = None
            target_idx = None
            for idx2, position_2 in enumerate(self.paper_positions):
                d = math.sqrt((position_1[0] - position_2[0])**2 + (position_1[1] - position_2[1])**2)
                if d < value:
                    value = d
                    target_position = position_2
                    target_idx = idx2
            if target_position:
                position_1 = list(position_1)
                target_position = list(target_position)
                if value < VAL:
                    pg.mixer.Sound.play(scissors_aud)
                    self.paper_positions.pop(target_idx)
                    self.scissors_positions.append(tuple(target_position))
                    continue
                dx = target_position[0] - position_1[0]
                dy = target_position[1] - position_1[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)

                if distance != 0:
                    position_1[0] += self.vel_x * (dx / distance)
                    position_1[1] += self.vel_x * (dy / distance)
                elif distance == 0:
                    pass

                self.scissors_positions[idx1] = tuple(position_1)


        #Ruch dla paper, rock
        for idx1, position_1 in enumerate(self.paper_positions):
            value = math.inf
            target_position = None
            target_idx = None
            for idx2, position_2 in enumerate(self.rock_positions):
                d = math.sqrt((position_1[0] - position_2[0])**2 + (position_1[1] - position_2[1])**2)
                if d < value:
                    value = d
                    target_position = position_2
                    target_idx = idx2
            if target_position:
                position_1 = list(position_1)
                target_position = list(target_position)
                if value < VAL:
                    pg.mixer.Sound.play(paper_aud)
                    self.rock_positions.pop(target_idx)
                    self.paper_positions.append(tuple(target_position))
                    continue
                dx = target_position[0] - position_1[0]
                dy = target_position[1] - position_1[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)

                if distance != 0:
                    position_1[0] += self.vel_x * (dx / distance)
                    position_1[1] += self.vel_x * (dy / distance)

                self.paper_positions[idx1] = tuple(position_1)

    def score(self):
        win.blit(rock_img, (40, 20))
        win.blit(paper_img, (120, 20))
        win.blit(scissors_img, (200, 20))

        rock_score_text = font.render(str(len(self.rock_positions)), True, (255,255,255))
        win.blit(rock_score_text, (75, 20))
        paper_score_text = font.render(str(len(self.paper_positions)), True, (255, 255, 255))
        win.blit(paper_score_text, (160, 20))
        scissors_score_text = font.render(str(len(self.scissors_positions)), True, (255, 255, 255))
        win.blit(scissors_score_text, (235, 20))

        if len(self.rock_positions) > len(self.paper_positions) and len(self.rock_positions) > len(self.scissors_positions):
            rock_score_text = font.render(str(len(self.rock_positions)), True, (255, 0, 0))
            win.blit(rock_score_text, (75, 20))
            paper_score_text = font.render(str(len(self.paper_positions)), True, (255, 255, 255))
            win.blit(paper_score_text, (160, 20))
            scissors_score_text = font.render(str(len(self.scissors_positions)), True, (255, 255, 255))
            win.blit(scissors_score_text, (235, 20))
        elif len(self.paper_positions) > len(self.rock_positions) and len(self.paper_positions) > len(self.scissors_positions):
            rock_score_text = font.render(str(len(self.rock_positions)), True, (255, 255, 255))
            win.blit(rock_score_text, (75, 20))
            paper_score_text = font.render(str(len(self.paper_positions)), True, (255, 0, 0))
            win.blit(paper_score_text, (160, 20))
            scissors_score_text = font.render(str(len(self.scissors_positions)), True, (255, 255, 255))
            win.blit(scissors_score_text, (235, 20))
        elif len(self.scissors_positions) > len(self.paper_positions) and len(self.scissors_positions) > len(self.rock_positions):
            rock_score_text = font.render(str(len(self.rock_positions)), True, (255, 255, 255))
            win.blit(rock_score_text, (75, 20))
            paper_score_text = font.render(str(len(self.paper_positions)), True, (255, 255, 255))
            win.blit(paper_score_text, (160, 20))
            scissors_score_text = font.render(str(len(self.scissors_positions)), True, (255, 0, 0))
            win.blit(scissors_score_text, (235, 20))

    def game_over(self):
        game_over = False
        rock_wins = font_2.render("ROCK WIN!", True, (255,255,255))
        paper_wins = font_2.render("PAPER WIN!", True, (255, 255, 255))
        scissors_wins = font_2.render("SCISSORS WIN!", True, (255, 255, 255))
        if len(self.rock_positions) == 0 and len(self.paper_positions) == 0:
            pg.time.delay(1000)
            win.blit(scissors_wins, (180, 280))
            game_over = True

        elif len(self.rock_positions) == 0 and len(self.scissors_positions) == 0:
            pg.time.delay(1000)
            win.blit(paper_wins, (180, 280))
            game_over = True

        elif len(self.scissors_positions) == 0 and len(self.paper_positions) == 0:
            pg.time.delay(1000)
            win.blit(rock_wins, (180, 280))
            game_over = True
        if game_over:
            restart_button, restart_rect = button("RESTART", 325, 350, 300, 200, (255,255,255))
            win.blit(restart_button, restart_rect.topleft)
            pg.display.update()

            waiting_for_input = True
            while waiting_for_input:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        if restart_rect.collidepoint(event.pos):
                            waiting_for_input = False
                            return 'restart'
        return 'continue'

    def draw(self):
        for _ in self.rock_positions:
            win.blit(rock_img, _)
        for _ in self.paper_positions:
            win.blit(paper_img, _)
        for _ in self.scissors_positions:
            win.blit(scissors_img, _)


def button(text, x, y, width, height, color):
    button_surface = font_3.render(text, True, color)
    button_rect = button_surface.get_rect(center=(x+width//2, y +height//2))
    return button_surface, button_rect
def draw_text_input_box(x, y, width, height, active, user_text):
    box_color = (0,0,0) if active else (255,255,255)
    pg.draw.rect(win,box_color, (x,y, width, height), 2)
    text_surface = font_3.render(user_text, True, (0,0,0))
    win.blit(text_surface, (x+5, y+5))
def handle_input(event, active, user_text):
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_RETURN:
            return False, user_text
        elif event.key == pg.K_BACKSPACE:
            user_text = user_text[:-1]
        else:
            user_text += event.unicode
    return active, user_text





def main_screen():
    screen_title = font_2.render("R,P,S SIMULATOR", True, (0, 0, 0))
    start_button, start_rect = button("START", 100, 150, 150, 50, (0,0,0))
    quit_button, quit_rect = button("QUIT", 230, 150, 150, 50, (0,0,0))
    count_button, count_rect = button("COUNT", 400, 150, 150, 50, (0,0,0))

    input_box = pg.Rect(550,150,140,40)
    active = False
    user_text = ''



    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return int(user_text) if user_text.isdigit() and int(user_text) > 0 else 0
                elif quit_rect.collidepoint(event.pos):
                    pg.quit()
                    sys.exit()
                elif input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
            elif active:
                active, user_text = handle_input(event, active, user_text)
        win.blit(background_start, (0,0))
        win.blit(screen_title, (180, 80))
        win.blit(start_button, start_rect.topleft)
        win.blit(quit_button, quit_rect.topleft)
        win.blit(count_button, count_rect.topleft)
        draw_text_input_box(input_box.x, input_box.y, input_box.width, input_box.height, active, user_text)


        pg.display.update()


    pg.quit()





#Main game loop
def main():
    running = True
    count = main_screen()
    game_result = Object(count)



    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        win.blit(background_img, (0,0))
        game_result.collision()
        game_result.draw()
        game_result.score()
        pg.display.update()

        game_state = game_result.game_over()
        if game_state == 'restart':
            main()


    pg.quit()







if __name__ == "__main__":
    main()

