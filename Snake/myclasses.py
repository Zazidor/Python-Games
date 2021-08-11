import pygame
import random


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((34, 139, 34))
        self.rect = self.surf.get_rect(topleft=(pygame.display.get_surface().get_width() // 2,
                                                pygame.display.get_surface().get_height() // 2))
        pygame.draw.rect(self.surf, (255, 255, 255), (1, 1, 18, 18), 1)
        self.direction = None
        self.tail = []
        self.length = 1
        self.dead = True
        self.lives = 3

        self.timer_update_moving = pygame.time.get_ticks()

    def update(self, grow=None, move=()):
        if not self.dead:
            self.__dead_or_alive()
            if grow:
                self.__grow_a_tail()
            elif move:
                self.__move_state(move)
            elif pygame.time.get_ticks() > self.timer_update_moving:
                self.__moving()
                self.__tail_func()
                self.timer_update_moving = pygame.time.get_ticks() + (200 * (1.02 - self.length / 50))
        else:
            self.__reset()

    def draw(self, surf):
        for i in self.tail:
            surf.blit(self.surf, i)

    def __moving(self):
        if self.direction == 'right':
            self.rect.x += 20
        elif self.direction == 'left':
            self.rect.x -= 20
        elif self.direction == 'up':
            self.rect.y -= 20
        elif self.direction == 'down':
            self.rect.y += 20
        self.__check_borders()

    def __move_state(self, move):
        type, key = move[0], move[1]
        if type == pygame.KEYDOWN:
            if key == pygame.K_RIGHT and self.direction != 'left':
                self.direction = 'right'
            elif key == pygame.K_LEFT and self.direction != 'right':
                self.direction = 'left'
            elif key == pygame.K_UP and self.direction != 'down':
                self.direction = 'up'
            elif key == pygame.K_DOWN and self.direction != 'up':
                self.direction = 'down'

    def __check_borders(self):
        if self.rect.x >= pygame.display.get_surface().get_width() - 40 and self.direction == 'right':
            self.rect.x = 40
        elif self.rect.x < 40 and self.direction == 'left':
            self.rect.x = pygame.display.get_surface().get_width() - 60

        if self.rect.y >= pygame.display.get_surface().get_height() - 40 and self.direction == 'down':
            self.rect.y = 100
        elif self.rect.y < 100 and self.direction == 'up':
            self.rect.y = pygame.display.get_surface().get_height() - 60

    def __tail_func(self):
        self.tail.append((self.rect.x, self.rect.y))
        if len(self.tail) > self.length:
            self.tail.pop(0)

    def __grow_a_tail(self):
        self.length += 1

    def __dead_or_alive(self):
        if self.length > 3:
            index, needtocut = 0, False
            for i in self.tail[:-1]:
                index += 1
                if i == (self.rect.x, self.rect.y):
                    if self.lives > 1:
                        self.lives -= 1
                        needtocut = True
                        break
                    else:
                        self.lives -= 1
                        self.dead = True
            if needtocut:
                self.__need_to_cut(index)

    def __need_to_cut(self, index):
        self.tail = self.tail[index:]
        self.length = self.length - index

    def __reset(self):
        self.dead = False
        self.length = 1
        self.tail = []
        self.rect = self.surf.get_rect(topleft=(pygame.display.get_surface().get_width() // 2,
                                                pygame.display.get_surface().get_height() // 2))
        self.lives = 3


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


class Score(Text):
    def __init__(self, font, size, text, color, x, y):
        super().__init__(font, size, text, color, x, y)
        self.score = 0

    def update(self, score=0):
        self.__score_update(score)

    def __score_update(self, score):
        if score:
            self.text = str(int(self.text) + score)
            self.surf = self.font.render(self.text, 1, self.color)
        else:
            self.text = str(0)
            self.surf = self.font.render(self.text, 1, self.color)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, lst, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = lst
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surf):
        surf.blit(self.image, self.rect)


class Fruit(pygame.sprite.Sprite):
    def __init__(self, lst):
        pygame.sprite.Sprite.__init__(self)
        self.images = lst
        self.index = random.randint(0, len(self.images)-1)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(
                                            random.randint(4, pygame.display.get_surface().get_width()//20 - 5) * 20,
                                            random.randint(5, pygame.display.get_surface().get_height()//20 - 5) * 20)
                                        )
        self.dead_state = True

    def update(self):
        self.__new_fruit()

    def dead(self):
        self.dead_state = True

    def __new_fruit(self):
        if self.dead_state:
            self.rect.x = random.randint(4, pygame.display.get_surface().get_width()//20 - 5) * 20
            self.rect.y = random.randint(5, pygame.display.get_surface().get_height()//20 - 5) * 20
            self.index = random.randint(0, len(self.images)-1)
            self.image = self.images[self.index]
            self.dead_state = False

    def draw(self, surf):
        surf.blit(self.image, self.rect)
