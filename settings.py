class Settings():
    def __init__(self):
        """静态设置"""
        # basic settings
        self.screen_width = 1024
        self.screen_height = 768
        self.bg_color = (250,250,250)

        # bullet settings
        self.bullet_width = 1
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 100  # 最大子弹数

        # alien settings
        self.fleet_drop_speed = 10

        # ship settings
        self.ship_limit = 3

        self.speedup_scale = 1 # 难度系数
        self.score_scale = 2# 奖励系数

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 0.75
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        self.fleet_direction = 1 # 1表示向右移动，-1表示向左移动

        self.enemy_points = 50

    def update_level(self, stats, sb):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.enemy_points = int(self.enemy_points * self.score_scale)

        stats.level += 1
        sb.prep_level()

