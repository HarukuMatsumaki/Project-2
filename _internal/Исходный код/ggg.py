import os
import random
import math
import pygame

pygame.init()

def load_image(name, color_key=None):
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

size = width, height = 500, 500
fsize = 42

f1 = pygame.font.SysFont("arial", fsize)

start = pygame.display.set_mode(size)
start.fill(pygame.Color("black"))

levels = [
    [f1.render(str(i), True, (180, 0, 0)), (height // 6 * i, (height - fsize) // 2)]
    for i in range(1, 6)
]

st = True
run = True
bye = True

score = 0
speed = 1
level = 1

while st:
    for i in levels:
        start.blit(*i)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            st = False
            run = False
            bye = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (height - 42) // 2 <= event.pos[1] <= (height + 42) // 2:
                for i in range(5):
                    if 500 // 6 * i <= event.pos[0] <= 500 // 6 * (i + 1):
                        level = i + 1
                        st = False

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Running Ball 5 Levels")
cc = pygame.time.Clock()

class Ball(pygame.sprite.Sprite):
    image = load_image("ball.png", -1)

    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        super().__init__(danger)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

        self.radius = radius
        self.vx = 0
        self.vy = 0

    def update(self, vx, vy, speed):
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
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        super().__init__(players)
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("blue"), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = 0
        self.vx = 0

    def update(self, vx, vy, speed):
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
ball = Ball(5, *map(lambda n: n // 2, size))
player = Player(10, 15, 15)
vx = vy = 0
ssccoorree = pygame.time.get_ticks()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            bye = False
    vx, vy = pygame.mouse.get_pos()
    screen.fill(pygame.Color("black"))
    all_sprites.update(vx, vy, speed)
    all_sprites.draw(screen)
    pygame.display.flip()
    cc.tick(60)
    if pygame.sprite.collide_mask(player, ball):
        score = (pygame.time.get_ticks() - ssccoorree) * level
        try:
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
            rec = open("rec.txt", "w")
            rec.write("1) " + str(score) + "\n")
            rec.close()
            score = "New record: " + str(score)
        del rec
        run = False

end = pygame.display.set_mode(size)
end.fill(pygame.Color("black"))
text = f1.render(str(score), True, "red")
text_rect = text.get_rect(center=(width / 2, height / 2))

while bye:
    end.blit(text, text_rect)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bye = False

pygame.quit()
print(score)
