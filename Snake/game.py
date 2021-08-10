import os
import pygame
from myclasses import Snake, Fruit, Text, Score, Sprite

W_WIDTH = 600
W_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (225, 0, 50)
GRAY = (125, 125, 125)
BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
ORANGE = (255, 150, 100)

FPS = 60


# перехват нажатий клавиш во время игры
def keyboard():
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
            main_screen()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_LEFT or i.key == pygame.K_RIGHT or i.key == pygame.K_UP or i.key == pygame.K_DOWN:
                player.update(move=(i.type, i.key))
        elif i.type == pygame.KEYUP:
            if i.key == pygame.K_LEFT or i.key == pygame.K_RIGHT or i.key == pygame.K_UP or i.key == pygame.K_DOWN:
                player.update(move=(i.type, i.key))


# проверка нахождения головы и фрукта в одной клетке
def eat():
    if player.rect.x == fruit.rect.x and player.rect.y == fruit.rect.y:
        fruit.dead()
        player.update(grow=True)
        txt_score.update(10)


# основной игровой цикл
def game_loop(run):
    player.update()
    if player.dead:
        txt_score.score = 0

    while run:
        if player.dead:
            run = False

        else:
            keyboard()
            fruit.update()
            player.update()

            sc.fill(BLACK)
            pygame.draw.rect(sc, WHITE, ((40, 100), (W_WIDTH-80, W_HEIGHT-140)), 1)
            player.draw(sc)
            fruit.draw(sc)
            txt_score.draw(sc)

            x = W_WIDTH-180
            for live in range(0, player.lives):
                heart = Sprite(image_heart, x, 30)
                heart.draw(sc)
                x += 50

            eat()

            pygame.display.update()
            clock.tick(FPS)


# экран с меню
def main_screen():
    while True:
        x_pos, y_pos = 0, 0
        for i in pygame.event.get():
            if i.type == pygame.QUIT or i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                exit()
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    x_pos, y_pos = i.pos[0], i.pos[1]

        if txt_newgame.rect.x <= x_pos <= txt_newgame.rect.x + txt_newgame.rect.size[0] \
                and txt_newgame.rect.y <= y_pos <= txt_newgame.rect.y + txt_newgame.rect.size[1]:
            game_loop(True)

        elif txt_exit.rect.x <= x_pos <= txt_exit.rect.x + txt_exit.rect.size[0] \
                and txt_exit.rect.y <= y_pos <= txt_exit.rect.y + txt_exit.rect.size[1]:
            exit()
        
        if player.dead:
            txt_newgame.draw(sc)
        else:
            txt_continue.draw(sc)
        txt_exit.draw(sc)

        pygame.display.update()
        clock.tick(FPS)


# загрузка картинок из папки (fruits)
def load_sprites(suffix, path, size):
    images = []
    for file in os.listdir(path=f'./{path}'):
        if file.startswith(suffix):
            images.append(pygame.transform.scale(pygame.image.load(f'./{path}/{file}').convert_alpha(), size))
    return images


if __name__ == '__main__':
    pygame.init()

    sc = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
    pygame.display.set_caption("Snake")

    clock = pygame.time.Clock()

    image_heart = load_sprites('heart', 'images', (40, 40))
    images_fruits = load_sprites('fruit', 'images', (20, 20))
    # image_fruit = pygame.transform.scale(pygame.image.load('berry.png').convert_alpha(), (20, 20))

    player = Snake()

    txt_newgame = Text(None, 72, 'Новая игра', RED, W_WIDTH//2, W_HEIGHT//2)
    txt_continue = Text(None, 72, 'Продолжить', RED, W_WIDTH//2, W_HEIGHT//2)
    txt_exit = Text(None, 72, 'Выход', RED, W_WIDTH//2, W_HEIGHT//2 + 100)
    txt_score = Score(None, 72, '0', WHITE, 50, 50)

    fruit = Fruit(images_fruits)

    main_screen()
