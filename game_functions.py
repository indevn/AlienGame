import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

#########################################################################
# 响应交互相关
#########################################################################

def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sb, aliens):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            fire_bullet(ai_settings, screen, ship, bullets)
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            game_start(ai_settings, screen, stats, sb, ship, aliens, bullets)



def check_keyup_events(event, ship):
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """相应按键和鼠标事件的主程序"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sb, aliens)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        game_start(ai_settings, screen, stats, sb, ship, aliens, bullets)


def game_start(ai_settings, screen, stats, sb, ship, aliens, bullets):
    pygame.mouse.set_visible(False)

    stats.reset_stats()
    stats.game_active = True

    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()

    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def game_over(stats, ai_settings):
    stats.game_active = False
    pygame.mouse.set_visible(True)
    ai_settings.initialize_dynamic_settings()

#########################################################################
# 外星人群相关
#########################################################################

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_alien_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_alien_y = get_number_aliens_y(ai_settings, ship.rect.height, alien.rect.height)
    # int()丢弃了小数部分==向下圆整，确保有足够空间

    # 创建第一行外星人
    for row_number in range(number_alien_y):
        for alien_number in range(number_alien_x):
            # 创建一个外星人并将其加入前行
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width  # 外星人间距为外星人宽度
    alien.x = alien_width + 2 * alien_width * alien_number  # 外星人右边也要留出一定空白空间，所以需要乘以2
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_aliens_x(ai_settings, alien_width):
    available_sapce_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_sapce_x / (2 * alien_width))
    return number_aliens_x


def get_number_aliens_y(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


#########################################################################
# 射击相关
#########################################################################

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        # 创建一个子弹，并将其编入bullets编组
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


#########################################################################
# update相关
#########################################################################

def update_screen(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button):
    screen.fill(ai_settings.bg_color)

    sb.show_score()

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹位置，并删除已消失的子弹"""
    bullets.update()

    # 删除已消失子弹
    for bullet in bullets.copy():  # 遍历副本
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    print(len(bullets))

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """相应子弹和外星人的碰撞"""

    # 碰撞检测&删除碰撞对象
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # groupcollide将两个rect进行比较，返回一个字典。key是子弹，对应的值是被击中的外星人

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        stats.check_high_score(sb)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.update_level(stats, sb)

        create_fleet(ai_settings, screen, ship, aliens)


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """响应飞船撞击"""
    if stats.ships_left > 0:
        stats.ships_left -= 1

        sb.prep_ships()

        # is mid turn:
        ai_settings.update_level(stats, sb)

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # pause
        sleep(0.5)
    else:
        game_over(stats, ai_settings)

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 撞到飞船or触底
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        print("Ship hit!!!")
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取的相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """下移外星人，并改变其方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
