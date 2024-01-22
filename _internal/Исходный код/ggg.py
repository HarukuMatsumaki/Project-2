import os
import random
import math
import pygame

pygame.init()

def load_image(name, color_key=None):
    """Функция загрузки
    изображения в качестве
    спрайта"""
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print("Cannot load image:", name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image

# Размер окна
size = width, height = 500, 500

# Размер шрифта
fsize = 42

# Инициализация шрифта
f1 = pygame.font.SysFont("arial", fsize)

# Инициализация окна
start = pygame.display.set_mode(size)
start.fill(pygame.Color("black"))

# Создание надписей уровней
levels = [
    [f1.render(str(i), True, (180, 0, 0)), (height // 6 * i, (height - fsize) // 2)]
    for i in range(1, 6)
]

# Флаги для запуска окон
st = True
run = True
bye = True

# Счёт, скорость, уровень
score = 0
speed = 1
level = 1

while st:
    # Стартовое окно с выбором уровня
    for i in levels:
        start.blit(*i)
    pygame.display.flip()
    for event in pygame.event.get():
        # Если закрыть стартовое окно,
        # то остальные окна не запустятся
        if event.type == pygame.QUIT:
            st = False
            run = False
            bye = False
        # Выбор уровня (немного кривой)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (height - 42) // 2 <= event.pos[1] <= (height + 42) // 2:
                for i in range(5):
                    if 500 // 6 * i <= event.pos[0] <= 500 // 6 * (i + 1):
                        level = i + 1
                        st = False

# Инициализация основного игрового окна
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Running Ball 5 Levels")
cc = pygame.time.Clock()

class Ball(pygame.sprite.Sprite):
    """Объект "Догонятель":
    на протяжении игры гонится
    за игроком"""

    # Закгрузка изображения
    image = load_image("ball.png", -1)

    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        super().__init__(danger)

        # Натягиваем спрайт и делаем маску
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Стартовое положение
        self.rect.x = x
        self.rect.y = y

        # Радиус
        self.radius = radius

        # Скорость
        # По умолчанию равна нулю
        self.vx = 0
        self.vy = 0

    def update(self, vx, vy, speed):
        """Движение за игроком
        с заданной скоростью"""
        
        dx, dy = (
            player.rect.x
            + 0.5 * player.rect.width
            - self.rect.x
            - 0.5 * self.rect.width
        ), (
            player.rect.y
            + 0.5 * player.rect.height
            - self.rect.y
            - 0.5 * self.rect.height
        )
        l = math.sqrt(dx ** 2 + dy ** 2)
        if l:
            self.rect.x += level * speed * dx / l
            self.rect.y += level * speed * dy / l

class Player(pygame.sprite.Sprite):
    """Объект "Убегатель":
    управляется игроком"""
    
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        super().__init__(players)

        # Это круг
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("blue"), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)

        # Скорость
        # По умолчанию равна нулю
        self.vx = 0
        self.vx = 0

    def update(self, vx, vy, speed):
        """Движение в точку с заданными
        координатами с постоянной
        скоростью"""
        
        dx, dy = (vx - self.rect.x - 0.5 * self.rect.width), (
            vy - self.rect.y - 0.5 * self.rect.height
        )
        l = math.sqrt(dx ** 2 + dy ** 2)
        if l:
            self.rect.x += 5 * speed * dx / l
            self.rect.y += 5 * speed * dy / l

all_sprites = pygame.sprite.Group()
danger = pygame.sprite.Group()
players = pygame.sprite.Group()

# Объявление "Игрока" и "Бота"
ball = Ball(5, *map(lambda n: n // 2, size))
player = Player(10, 15, 15)

# Начальные координаты указателя мышки
vx = vy = 0

# Засекаем счёт
ssccoorree = pygame.time.get_ticks()

while run:
    # Основное окно
    for event in pygame.event.get():
        # Если закрыть основное
        # окно, то финальное окно
        # не запустится
        if event.type == pygame.QUIT:
            run = False
            bye = False

    # координаты указателя мышки
    vx, vy = pygame.mouse.get_pos()
    
    screen.fill(pygame.Color("black"))
    all_sprites.update(vx, vy, speed)
    all_sprites.draw(screen)
    pygame.display.flip()
    cc.tick(60)

    # Проверка на столкновение
    if pygame.sprite.collide_mask(player, ball):
        
        # Вычисление счёта
        score = (pygame.time.get_ticks() - ssccoorree) * level

        # Сохранение счёта
        try:
            # Случай, когда файл уже был
            rec = open("rec.txt", "r")
            data = [
                int(i[i.find(" ") + 1 :]) for i in rec.read().rstrip("\n").split("\n")
            ]
            rec.close
            data.append(score)
            data = sorted(data, reverse=True)
            rec = open("rec.txt", "w")
            rec.writelines(
                [str(i + 1) + ") " + str(data[i]) + "\n" for i in range(len(data))]
            )
            rec.close()
            score = f"Top {data.index(score) + 1}" + ": " + str(score)
        except FileNotFoundError:
            # Случай, когда файла нет
            rec = open("rec.txt", "w")
            rec.write("1) " + str(score) + "\n")
            rec.close()
            score = "New record: " + str(score)
        del rec
        run = False

# Инициализация финального окна
end = pygame.display.set_mode(size)
end.fill(pygame.Color("black"))

# Инициализация финального текста
text = f1.render(str(score), True, "red")
text_rect = text.get_rect(center=(width / 2, height / 2))

while bye:
    # Финальное окно
    end.blit(text, text_rect)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bye = False

pygame.quit()
print(score)
