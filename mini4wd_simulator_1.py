import pygame
import math
import sys

# 画面サイズ
WIDTH, HEIGHT = 800, 600

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (200, 200, 200)
RED   = (255, 0, 0)

# ミニ四駆クラス
class Mini4WD:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0  # 向き（ラジアン）
        self.speed = 0
        self.max_speed = 5
        self.accel = 0.1
        self.turn_speed = math.radians(4)
        self.size = 15  # 半径

    def update(self, keys):
        # 前進・後退
        if keys[pygame.K_UP]:
            self.speed = min(self.max_speed, self.speed + self.accel)
        elif keys[pygame.K_DOWN]:
            self.speed = max(-self.max_speed, self.speed - self.accel)
        else:
            # 減速（摩擦）
            self.speed *= 0.95

        # 左右旋回
        if keys[pygame.K_LEFT]:
            self.angle -= self.turn_speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.turn_speed

        # 座標更新
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.size)

# 壁との衝突判定
def check_collision(car):
    if car.x < car.size or car.x > WIDTH - car.size or car.y < car.size or car.y > HEIGHT - car.size:
        car.speed = 0  # 衝突時に停止

# メインループ
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini 4WD Simulator")
    clock = pygame.time.Clock()

    car = Mini4WD(100, 100)

    running = True
    while running:
        clock.tick(60)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        car.update(keys)
        check_collision(car)

        screen.fill(WHITE)
        pygame.draw.rect(screen, GRAY, (50, 50, WIDTH-100, HEIGHT-100), 5)  # コース枠
        car.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
