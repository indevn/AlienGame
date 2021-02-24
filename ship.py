import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()

        self.screen = screen # the position of the ship
        self.ai_settings = ai_settings
        # 获取外接矩形
        self.image = pygame.image.load('images/ship.bmp') # 加载图像，返回surface
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # self.rect.centerx为整数，但就整体而言，反馈的是多次移动累计像素点的结果，问题不大
        self.rect.centerx = self.center


    def blitme(self): # 在指定位置绘制飞船
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        """飞船居中"""
        self.center = self.screen_rect.centerx