import pygame
import math
import sys

# 初期化
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Mini4WD:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.angle = 0
        self.prev_angle = 0
        self.speed = 0
        self.max_speed = 5
        self.accel = 0.1
        self.turn_speed = math.radians(4)
        self.size = 15

    def update(self, keys):
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_angle = self.angle

        # 操作
        if keys[pygame.K_UP]:
            self.speed = min(self.max_speed, self.speed + self.accel)
        elif keys[pygame.K_DOWN]:
            self.speed = max(-self.max_speed, self.speed - self.accel)
        else:
            self.speed *= 0.95

        if keys[pygame.K_LEFT]:
            self.angle -= self.turn_speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.turn_speed

        # 移動
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def get_acceleration(self):
        ax = (self.x - self.prev_x) - math.cos(self.prev_angle) * self.speed
        ay = (self.y - self.prev_y) - math.sin(self.prev_angle) * self.speed
        return ax, ay

    def get_gyro(self):
        # 角速度（rad/frame）
        return self.angle - self.prev_angle

    def get_ir_distance(self, walls, max_dist=100):
        # 赤外線センサの直線を壁まで伸ばす
        dx = math.cos(self.angle)
        dy = math.sin(self.angle)
        for d in range(1, max_dist):
            px = int(self.x + dx * d)
            py = int(self.y + dy * d)
            if not (0 <= px < WIDTH and 0 <= py < HEIGHT):
                return d
            if walls.get_at((px, py)) != WHITE:
                return d
        return max_dist

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.size)
        # 赤外線センサの線を表示
        dx = math.cos(self.angle)
        dy = math.sin(self.angle)
        pygame.draw.line(screen, GREEN, (self.x, self.y), (self.x + dx * 50, self.y + dy * 50), 2)

def check_wall_collision(car):
    if car.x < car.size:
        car.x = car.size
        car.speed = 0
    elif car.x > WIDTH - car.size:
        car.x = WIDTH - car.size
        car.speed = 0

    if car.y < car.size:
        car.y = car.size
        car.speed = 0
    elif car.y > HEIGHT - car.size:
        car.y = HEIGHT - car.size
        car.speed = 0
    
    if car.x < car.size or car.x > WIDTH - car.size:
        car.angle = math.pi - car.angle
        car.speed *= -0.5  # 少しエネルギー損失



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sensor Mini 4WD Simulator")
    clock = pygame.time.Clock()

    car = Mini4WD(150, 150)

    # 壁（サーフェスに描いておく）
    walls = pygame.Surface((WIDTH, HEIGHT))
    walls.fill(WHITE)
    pygame.draw.rect(walls, GRAY, (50, 50, WIDTH - 100, HEIGHT - 100), 10)  # 壁
    # 枠の壁を可視化（5pxの太さで描画）
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HEIGHT), 5)

    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        car.update(keys)
        check_wall_collision(car)

        # センサ読み取り
        acc_x, acc_y = car.get_acceleration()
        gyro = car.get_gyro()
        ir_dist = car.get_ir_distance(walls)

        # 表示
        screen.blit(walls, (0, 0))
        car.draw(screen)

        # デバッグ情報表示
        font = pygame.font.SysFont(None, 24)
        info = [
            f"Accel X: {acc_x:.2f}",
            f"Accel Y: {acc_y:.2f}",
            f"Gyro: {gyro:.2f} rad/frame",
            f"IR Dist: {ir_dist}px"
        ]
        for i, text in enumerate(info):
            img = font.render(text, True, (0, 0, 0))
            screen.blit(img, (10, 10 + i * 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
