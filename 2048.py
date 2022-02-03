import pygame as pg
import numpy as np

pg.init()
COTE = 100 # largeur du rectangle en pixels
NB_CASES = 4
screen = pg.display.set_mode((COTE*NB_CASES, COTE*NB_CASES))
clock = pg.time.Clock()
pace = 10

class Game:
    def __init__(self, nb_cases, cote):
        self.grid = np.zeros((NB_CASES, NB_CASES), dtype=int)
        self.score = 0
        self.cote = cote 
        self.nb_cases = nb_cases
        self.colors = ((77,63,49), (57,42,26), (71,55,23), (127,65,12),
            (142,54,9), (144,34,8), (166,37,8), (129,102,17), (141,111,16), 
            (151,119,16), (162,128,15), (172,137,15), (49,43,36), (60,50,40))
        self.background = (87,74,62)

    def move_possible(self):
        if (self.grid == 0).any():
            return True
        mvt_vert = np.invert(np.diff(self.grid, axis=0).astype(bool)).any()
        mvt_hori = np.invert(np.diff(self.grid, axis=1).astype(bool)).any()
        return mvt_vert or mvt_hori
    
    def game_over(self):
        center = self.cote*self.nb_cases // 2
        font_obj = pg.font.SysFont("Helvetica Neue", 65)
        score = font_obj.render(f'Score: {self.score}', True, (255, 255, 255))
        text_rect = score.get_rect(center=(center, center))
        screen.blit(score, text_rect)

    def new_case(self):
        if np.random.rand() < 0.9:
            value = 1
        else:
            value = 2
        cases = self.available_cases()
        if cases:
            np.random.shuffle(cases)
            x, y = cases[0]
            self.grid[x, y] = value
        if not self.move_possible():
            self.draw_grid()
            self.game_over()
            return False
        return True
    
    def available_cases(self):
        coor = np.where(self.grid == 0)
        return [(x, y) for x, y in zip(coor[0], coor[1])]
    
    def draw_case(self, x, y, val):
        size = self.cote
        rect = pg.Rect(x*size+5, y*size+5, size-10, size-10)
        pg.draw.rect(screen, self.colors[val], rect)

        if val:
            if val < 10:
                font_size = 65
            else:
                font_size = 50
            font_obj = pg.font.SysFont("Helvetica Neue", font_size)
            digit = font_obj.render(str(2**val), True, (255, 255, 255))
            text_rect = digit.get_rect(center=((x+.5)*size, (y+.5)*size))
            screen.blit(digit, text_rect)

    def draw_grid(self):
        screen.fill(self.background)
        for value in np.unique(self.grid):
            coor = np.where(self.grid == value)
            for x, y in zip(coor[0], coor[1]):
                self.draw_case(x, y, value)
    
    def arrange(self, line):
        i = 0
        prev = -1
        new_line = np.zeros(len(line), dtype=int)
        for num in line:
            if num == 0:
                continue
            if prev == num:
                i -= 1
                new_line[i] = num + 1
                self.score += 2**(num+1)
            else:
                new_line[i] = num
            i += 1
            prev = new_line[i-1]
        return new_line

    def move(self, dir):
        if dir in ['LEFT', 'RIGHT']:
            self.grid = self.grid.T
        for i, row in enumerate(self.grid):
            if dir in ['DOWN', 'RIGHT'] :
                new_line = np.flip(self.arrange(np.flip(row)))
            else:
                new_line = self.arrange(row)
            self.grid[i] = new_line
        if dir in ['LEFT', 'RIGHT']:
            self.grid = self.grid.T


game = Game(NB_CASES, COTE)
game.new_case()
game.new_case()
game.draw_grid()

running = True

while running:
    clock.tick(pace)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                running = False
                continue
            elif event.key == pg.K_UP:
                game.move('UP')
            elif event.key == pg.K_DOWN:
                game.move('DOWN')
            elif event.key == pg.K_LEFT:
                game.move('LEFT')
            elif event.key == pg.K_RIGHT:
                game.move('RIGHT')

            if game.new_case():
                game.draw_grid() 

    pg.display.set_caption(f"Score: {game.score}")
    pg.display.update()

pg.quit()