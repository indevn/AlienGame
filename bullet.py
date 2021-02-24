import pygame
from pygame.sprite import Sprite
"""关于精灵类：
   可将游戏中相关元素编组，进而同时操作编组中的所有元素"""
class Bullet(Sprite):
    # 一个对子弹进行管理的类

    def __init__(self, ai_settings, screen, ship):
        # 在飞船所处位置创建子弹对象
        super().__init__()# 调用super继承精灵类 #？？？？？？？？？？？？？？？？？？？？？？？？？
        self.screen = screen

        # 在(0,0)创建子弹对应矩形，设置正确位置
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        # 参数：左上角x、y坐标，矩形宽、高
        self.rect.centerx = ship.rect.centerx# 子弹初始位置取决于飞船当前位置
        self.rect.top = ship.rect.top# 从飞船顶部射出 piu~

        # 存储用小数表示的子弹位置，便于调整子弹速度
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        # 更新子弹位置对应小数值
        self.y -= self.speed_factor
        # 更新子弹rect位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen,self.color,self.rect)
