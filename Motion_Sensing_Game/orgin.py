import pygame
from random import *
import math
import time

def game(result):
    # 初始化Pygame
    pygame.init()

    # 创建游戏窗口
    screen_width = 720
    screen_height = 960
    screen = pygame.display.set_mode((screen_width, screen_height))

    # 设置游戏标题
    pygame.display.set_caption('弹幕游戏')
    Gicon = pygame.image.load("Motion_Sensing_Game/image/Gicon.png")
    pygame.display.set_icon(Gicon)
    # 定义颜色
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    
    # 定义角色类
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface([20, 20])
#             self.image.fill((70, 130, 253))
            self.image.fill((4, 62, 103))
            self.rect = self.image.get_rect()
            self.rect.centerx = screen_width // 2
            self.rect.centery = screen_height // 2
            self.speed = 5

        def update(self, direction):
            # 根据移动方向更新位置
            self.rect.x += direction[0] * self.speed
            self.rect.y += direction[1] * self.speed
            # 确保角色不会移出屏幕边界
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > screen_width:
                self.rect.right = screen_width
            if self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
        def move_To(self, move_xy):
            self.rect.x = move_xy[0]
            self.rect.y = move_xy[1]
            # 确保角色不会移出屏幕边界
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > screen_width:
                self.rect.right = screen_width
            if self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.bottom > screen_height:
                self.rect.bottom = screen_height

    # 定义弹幕类
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, speed, angle=None):
            super().__init__()
            self.image = pygame.Surface([10, 10])
            self.image.fill((211, 53, 78))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.angle = angle
            self.speed = speed if (speed > 4) else 4

        def update(self):
            if self.angle is None:
                self.angle = uniform(-math.pi/2, math.pi/2)
            dx = self.speed * math.cos(self.angle)
            dy = self.speed * math.sin(self.angle)
            self.rect.x += dx
            self.rect.y += dy
            if self.rect.left > screen_width or self.rect.right < 0 or self.rect.top > screen_height or self.rect.bottom < 0:
                self.kill()

    # 创建精灵组
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # 创建角色
    player = Player()
    all_sprites.add(player)

    # 设置计分器
    score = 0
    font = pygame.font.Font(None, 36)

    # 游戏循环
    
    gameDisplay = pygame.display.set_mode((screen_width,screen_height))
    background = pygame.image.load('./Motion_Sensing_Game/image/1.png').convert()
    background = pygame.transform.smoothscale(background, gameDisplay.get_size())
    gameDisplay.blit(background, (0, 0))
    
    running = False
    begin_time = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    bullet_delay = 0  # 计数器，用于控制弹幕的生成
    bullet_count = 0  # 弹幕计数器，用于控制弹幕数量
    bullet_speed = 4  # 弹幕速度，用于控制弹幕生成速度
    direction = [0, 0]
#     move_xy = [player.rect.centerx, player.rect.centery]
    move_xy = [player.rect.centerx, player.rect.centery]
    while True:
        if(running==True):
            # 设置游戏帧率
            clock.tick(60)

            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            #
            try:   
                move_xy = [result[0][0] // 2, int(result[0][1] * 1.4)]
            except: pass
#             direction = [keys[pygame.K_RIGHT]-keys[pygame.K_LEFT], keys[pygame.K_DOWN]-keys[pygame.K_UP]]
            # 更新角色状态
            #player.update(direction)
            player.move_To(move_xy)
            bullet_delay += 1
            # 生成弹幕
            if randint(0, 96 + bullet_delay // 30) > 95:
                #screen_width = 720
                #screen_height = 960
            
                if bullet_speed < 8:
                    bullet_speed += 0.4
                if (randint(0, 10) % 2 == 1):
                    x = randint(screen_width - 30, screen_width) if (randint(0, 10) % 2 == 1) else randint(0, 30)
                    y = randint(0, screen_height)
                else:
                    x = randint(0, screen_width)
                    y = randint(screen_height - 20, screen_height) if (randint(0, 10) % 2 == 1) else randint(0, 20)
                #x = randint(600, screen_width) if (randint(0, 10) % 2 == 1) else random.randint(0, 50)
                #y = randint(440, screen_height) if (randint(0, 10) % 2 == 0) else random.randint(0, 50)
                angle = None
                if randint(1, 4) < 4: #自瞄准(3/4的概率)
                    dx = player.rect.centerx - x
                    dy = player.rect.centery - y
                    angle = math.atan2(dy, dx)
                bullet = Bullet(x, y, bullet_speed, angle)
                all_sprites.add(bullet)
                bullets.add(bullet)
            

            # 更新弹幕状态并进行碰撞检测
            hits = pygame.sprite.spritecollide(player, bullets, False)
            if hits:
                running = False
            for bullet in bullets:
                bullet.update()

            # 绘制游戏画面
            score = (pygame.time.get_ticks()-begin_time) // 1000
#             screen.fill(BLACK)
            background = pygame.image.load(f'./Motion_Sensing_Game/image/{score+1}.png').convert()
            background = pygame.transform.smoothscale(background, gameDisplay.get_size())
            gameDisplay.blit(background, (0, 0))
            all_sprites.draw(screen)
#             score_text = font.render(f"Score: {score}", True, WHITE)
#             screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))
            pygame.display.flip()
        if(running==False):
            # 游戏结束后显示分数并等待退出
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                bullet_delay = 0  # 计数器，用于控制弹幕的生成
                bullet_count = 0  # 弹幕计数器，用于控制弹幕数量
                bullet_speed = 0  # 弹幕速度，用于控制弹幕生成速度
                score = 0
                direction = [0, 0]
                running=True
                begin_time = pygame.time.get_ticks()
                # 创建精灵组
                all_sprites = pygame.sprite.Group()
                bullets = pygame.sprite.Group()
                # 创建角色
                player = Player()
                all_sprites.add(player)

            pygame.display.flip()

if (__name__ == "__main__"):
    game([0])