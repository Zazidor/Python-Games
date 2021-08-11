#!/usr/bin/python3
import time, random
import pygame


class Figure():
    # список из фигур и их расположение в пространстве
    FIGURES = [
        [ [ [1,1,1,1] ], [ [1],[1],[1],[1] ] ],                                                                 # I 0
        [ [ [0,1,0], [1,1,1] ], [ [1,0], [1,1], [1,0] ], [ [1,1,1], [0,1,0] ], [ [0,1], [1,1], [0,1] ] ],       # T 1
        [ [ [1,1], [1,1] ] ],                                                                                   # square 2
        [ [ [1,0], [1,0], [1,1] ], [ [0,0,1], [1,1,1] ], [ [1,1], [0,1], [0,1] ], [ [1,1,1], [1,0,0] ] ],       # L 3
        [ [ [0,1], [0,1], [1,1] ], [ [ 1,1,1], [0,0,1] ], [ [1,1], [1,0], [1,0] ], [ [1,0,0], [1,1,1] ] ],      # L - reverse 4
        [ [ [1,1,0],[0,1,1] ], [ [0,1],[1,1],[1,0] ] ],                                                         # Z 5
        [ [ [0,1,1], [1,1,0] ], [ [1,0], [1,1], [0,1] ] ],                                                      # Z - reverse 6
    ]

    def __init__(self):
        self.type = self.FIGURES[random.randint(0, len(self.FIGURES)-1)]    # выбор типа фигуры
        self.direction = random.randint(0,len(self.type)-1)                 # выбор расположение фигуры
        self.figure = self.type[self.direction]                             # фигура с учетом типа и расположением
        self.x = 3                                                          # координата по Х (column - в массиве)
        self.y = 0                                                          # координата по У (row - в массиве)
        self.time_f = time.time()                                           # последнее время когда фигура передвигалась вниз
        self.key_down = False


    def rotate(self):
        if self.x < 10 - len(self.figure[0]):
            self.direction = (self.direction + 1) % len(self.type)
            self.figure = self.type[self.direction]
        else:
            self.direction = (self.direction + 1) % len(self.type)
            self.figure = self.type[self.direction]
            self.x = 10 - len(self.figure[0])

    def falling(self, lvl):
        # падение фигура, сравнивается время когда фигуру последний раз двигали вниз
        if self.key_down:
            d_spd = 5
        else:
            d_spd = 1
        
        if lvl > 0:
            l_spd = 0.5 * (0.9 ** (lvl))
        else:
            l_spd = 0.5
        
        if time.time() - self.time_f  >= l_spd/d_spd:
            self.y += 1
            self.time_f = time.time()
    
    def moving(self, key):
        # движение фигуры в зависимости от ввода игрока

        if key == 'right':
            if self.x < 10 - len(self.figure[0]): self.x += 1
            
        elif key == 'left':
            if self.x > 0: self.x -= 1


class Draw():
    # отрисовка одного "пикселя"
    @staticmethod
    def draw(surf, x, y):
        # метод принимает в качестве переменных поверхноить и кооодинаты Х и У
        image = pygame.Surface((20, 20))                    # содзаем "пиксель" 20 на 20 
        image.fill((0, 200, 64))                            # закрашиваем его зеленым
        pygame.draw.rect(image, (0,0,0), (1, 1, 18, 18), 1) #поверхность, цвет (x, y, ширина, высота), толщина
        rect = image.get_rect(topleft=(x * 20, y * 20))     # прямоугольная область
        surf.blit(image, rect)                              # отрисовываем


class Grid():
    # игровое поле в котором хранится информация с "упавшими" фигурами
    def __init__(self):
        # генерация поля размерами 10 на 20 
        self.grid = [[0 for col in range(10)] for row in range(20)]
        

    def add_to_grid(self, arr, x, y):
        # добавляет "упавшую" фигуру на поле
        for i_row in range(len(arr)):
            for j_col in range(len(arr[i_row])):
                el = arr[i_row][j_col]
                if el == 1:
                    self.grid[y+i_row][x+j_col] = el

    def remove_full_rows(self):
        # удаляем строки полные
        # подсчитываем полные строки
        cnt = 0
        for row in self.grid:
            if not 0 in row:
                cnt += 1
        # убираем полные строки
        self.grid = [row for row in self.grid if 0 in row]
        # добавляем новые стройки
        new_rows = [[0 for col in range(10)] for row in range(cnt)]
        self.grid = new_rows + self.grid

        return cnt
                    

class Text(pygame.sprite.Sprite):
    def __init__(self, font, size, text, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(font, size)
        self.surf = self.font.render(self.text, 1, self.color)
        self.rect = self.surf.get_rect(center=(x, y))

    def draw(self, surf):
        surf.blit(self.surf, self.rect)

# -------------------------------------------------------- #

def check_collision_bottom(GRID, FIGURE):
    # проверяем находится ли фигура на дне
    if FIGURE.y == 20 - len(FIGURE.figure):
        return True
    # проверяем столкновение с "упавшими фигурами"
    for row in range(len(FIGURE.figure)):               # Y это
        for col in range(len(FIGURE.figure[row])):      # Х это
            # проверяем только "существующие" "пиксели"
            if FIGURE.figure[row][col] == 1:
                # проверяем "пиксель" в поле
                if GRID.grid[FIGURE.y+row+1][FIGURE.x+col] == 1:
                    return True


def check_collision_side(GRID, FIGURE, side):
    # СДЕЛАТЬ ПРОВЕРКУ СЛЕВА И СПРАВА
    for row in range(len(FIGURE.figure)):               # Y это
        for col in range(len(FIGURE.figure[row])):      # Х это
            # проверяем только "существующие" "пиксели"
            if FIGURE.figure[row][col] == 1:
                # убеждаемся что фигура не на краю поля
                if FIGURE.x < 10 - len(FIGURE.figure[0]):
                    # проверяем "пиксель" в поле
                    if side == 'right' and GRID.grid[FIGURE.y+row][FIGURE.x+col+1] == 1:
                        return False
                if FIGURE.x > 0: 
                    if side == 'left' and GRID.grid[FIGURE.y+row][FIGURE.x+col-1] == 1:
                        return False
    return True

# главный цикл
def game():
    score = 0
    lines = 0
    level = 0
    
    GRID = Grid()                   # создаем поле
    FIGURE = Figure()               # создаем первую фигуру
    FIGURE_NEXT = Figure()          # следующая фигура 

    while True:
        # обработка нажатий
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE: main_menu(con=True)
                elif i.key == pygame.K_RIGHT:
                    if check_collision_side(GRID, FIGURE, 'right'):
                        FIGURE.moving('right')
                elif i.key == pygame.K_LEFT:
                    if check_collision_side(GRID, FIGURE, 'left'):
                        FIGURE.moving('left')
                elif i.key == pygame.K_DOWN: 
                    FIGURE.key_down = True
                elif i.key == pygame.K_UP: FIGURE.rotate()
            
            elif i.type == pygame.KEYUP:
                if i.key == pygame.K_DOWN: 
                    FIGURE.key_down = False     

        sc.fill(BLACK)
        # --------
        # изменение объектов и многое др.
        # --------
        field = pygame.Surface((200, 400))
        field.fill(BLACK)  # белая     
        pygame.draw.rect(field, WHITE, (0, 0, 200, 400), 1)
        field_rect = pygame.Rect((20, 20, 0, 0))



        # отрисовываем фигуру
        for row in range(len(FIGURE.figure)):               # Y это
            for col in range(len(FIGURE.figure[row])):      # Х это
                if FIGURE.figure[row][col] == 1:
                    Draw.draw(field, col+FIGURE.x, row+FIGURE.y)    

        # отрисовываем поле с "упавшими" фигурами
        for row in range(len(GRID.grid)):                   # Y это
            for col in range(len(GRID.grid[row])):          # Х это
                if GRID.grid[row][col] == 1:
                    Draw.draw(field, col, row)
        
        # отрисовываем следующую фигуру
        for row in range(len(FIGURE_NEXT.figure)):               # Y это
            for col in range(len(FIGURE_NEXT.figure[row])):      # Х это
                if FIGURE_NEXT.figure[row][col] == 1:
                    Draw.draw(sc, 14+col, 3+row)    

        txt_next.draw(sc)
        txt_score.draw(sc)
        txt_lines.draw(sc)
        txt_level.draw(sc)

        color = WHITE
        text = pygame.font.Font(None, 36).render(str(score), True, color)
        sc.blit(text, (270, 190))
        text = pygame.font.Font(None, 36).render(str(lines), True, color)
        sc.blit(text, (270, 270))
        text = pygame.font.Font(None, 36).render(str(level), True, color)
        sc.blit(text, (270, 350))
        # отрисовываем всё на основном слое
        sc.blit(field, field_rect)

        # фигура падает
        FIGURE.falling(lvl=level)

        # проверка на столкновение      
        if check_collision_bottom(GRID, FIGURE):
            GRID.add_to_grid(FIGURE.figure, FIGURE.x, FIGURE.y)
            FIGURE = FIGURE_NEXT
            FIGURE_NEXT = Figure()
            # удаляем заполненые строки
            rows_deleted = GRID.remove_full_rows()
            lines += rows_deleted
            level = lines//10 
            if rows_deleted > 0:
                if rows_deleted == 1: score += 100
                elif rows_deleted == 2: score += 300
                elif rows_deleted == 3: score += 700
                elif rows_deleted == 4: score += 1500
            
        if FIGURE.y == 0 and check_collision_bottom(GRID, FIGURE):
            pygame.display.update()
            main_menu()

        pygame.display.update()
        clock.tick(FPS)


def main_menu(con=False):
    while True:
        x_pos, y_pos = 0, 0
        for i in pygame.event.get():
            if i.type == pygame.QUIT or i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                exit()
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    x_pos, y_pos = i.pos[0], i.pos[1]

        txt_newgame.draw(sc)
        if con:
            txt_continue.draw(sc)
        txt_exit.draw(sc)

        if txt_newgame.rect.x <= x_pos <= txt_newgame.rect.x + txt_newgame.rect.size[0] \
                and txt_newgame.rect.y <= y_pos <= txt_newgame.rect.y + txt_newgame.rect.size[1]:
            game()

        elif txt_exit.rect.x <= x_pos <= txt_exit.rect.x + txt_exit.rect.size[0] \
                and txt_exit.rect.y <= y_pos <= txt_exit.rect.y + txt_exit.rect.size[1]:
            exit()

        elif txt_continue.rect.x <= x_pos <= txt_continue.rect.x + txt_continue.rect.size[0] \
                and txt_continue.rect.y <= y_pos <= txt_continue.rect.y + txt_continue.rect.size[1]:
            return

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    # здесь определяются константы, классы и функции
    W_HEIGHT = 440
    W_WIDTH = 400


    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (225, 0, 50)
    GRAY = (125, 125, 125)
    BLUE = (64, 128, 255)
    GREEN = (0, 200, 64)
    YELLOW = (225, 225, 0)
    PINK = (230, 50, 230)
    ORANGE = (255, 150, 100)
    MOCCASIN = (255, 228, 181)

    FPS = 60

    # здесь происходит инициация, создание объектов и др.
    pygame.init()

    sc = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
    sc.fill(BLACK)
    pygame.display.set_caption("Tetris")
    

    txt_newgame = Text(None, 72, 'New game', RED, W_WIDTH//2, W_HEIGHT//2 - 50)
    txt_continue = Text(None, 72, 'Continue', RED, W_WIDTH//2, W_HEIGHT//2 - 150)
    txt_exit = Text(None, 72, 'Exit', RED, W_WIDTH//2, W_HEIGHT//2 + 50)
    
    color = WHITE
    txt_next = Text(None, 36, 'Next', color, 300, 30)
    txt_score = Text(None, 36, 'Score', color, 300, 170)
    txt_lines = Text(None, 36, 'Lines', color, 300, 250)
    txt_level = Text(None, 36, 'Level', color, 300, 330)
    
    # если надо до цикла отобразить объекты на экране
    pygame.display.update()

    clock = pygame.time.Clock()

    main_menu()
