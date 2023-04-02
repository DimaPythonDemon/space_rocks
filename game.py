import random
import time

import pygame

from models import Asteroid, Spaceship, Star, Harvester, ElectroStation, Talants, TalantsMenu, TalantsIcon, Preview, EnergyShield, NeuroNet
from utils import get_random_position, load_sprite, print_text, draw_rectangle, load_sound, check_zone

class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):

        self.was_preview_shown = False
        self.nickname = "Player 1"
        # print("Чтобы начать игру, выполните настройку (нажмите Enter) или напишите 'авто' ")
        # if input().strip().lower() == 'авто':
        self.height, self.width = 600, 800
        self.fps = 30
        # else:
        #     self.height, self.width = map(int, input("Введите разрешение (высота и ширина через пробел): ").split())
        #     self.fps = int(input('Кол-во FPS: '))
        #     self.nickname = input("Ник в игре: ")

        self._init_pygame()
        self.asteroid_broken = 0
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = load_sprite("bg", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 50)
        try:
            self.SOUND = load_sound('music')
            self.SOUND.play()
        except: print("Music not installed.")
        self.message = ""
        self.star_timer = 9
        self.aster_timer = 6
        self.electro_cd_timer = 0
        self.regen_cd = 0
        self.asteroids = []
        self.bullets = []
        self.starrings = []
        self.harvesters = []
        self.electrostations = []
        self.spaceship = Spaceship((self.width//2, self.height//2), self.bullets.append)
        self.tick_num = 0
        self.energy = 100
        self.enough_energy = True
        self.stardust = 0
        self.red_untill = 0
        self.health = 100
        self.exp = 0
        self.level = 1
        self.level_to_aseroid = {1: [2, 40], 2: [3, 50], 3: [3, 45], 4: [4, 70], 5: [4, 65], 6: [4, 60], 7: [5, 65],
                                 8: [5, 60], 9: [6, 80], 10: [7, 65], 11: [7, 60], 12: [7, 60], 13: [8, 70],
                                 14: [9, 70], 15: [10, 85], 16: [10, 90], 17: [11, 90], 18: [12, 90], 19: [11, 100],
                                 20: [12, 110], 21: [5, 37], 22: [13, 120], 23: [13, 115], 24: [13, 110],
                                 25: [13, 105], 26: [14, 140], 27: [14, 130], 28: [14, 125], 29: [15, 140],
                                 30: [1, 3], 31: [1, 0.5], 32: [1, 0.3]}
        self.pause = False
        self.pause_cd = 0
        self.talants_tree = None
        self.talant = Talants(position=(770, 200))
        self. talants_list = {"regen_icon": [(100, 150), 1, "+10 хп\nCD - 10 сек\n(Клавиша R)", True], "harvester": [(300, 200), 2, 'Притягивает звёзды\nСтоит 65 звёзд\n(Клавиша H)', False], "electrostation_icon": [(300, 100), 2, "Генерирует энергию\nСтоит 80 звёзд\n(Клавиша E)", False], "energy_save_icon": [(600, 100), 5, "Ускорение не тратит энергию\n+1 к её регенерации", False], "random_star_talant": [(450, 220), 6, 'Создаёт звездy\nКаждые 20 сек', False], "ultra_shot_icon": [(650, 220), 9, "Стреляешь 8 пулями\nCD - 15 сек\n(Клавиша F)", False], "shield_talant": [(650, 450), 12, "Щит снижает урон на 50%\nCD - 30 сек\nДлительность \nдействия - 7 сек\n(Клавиша Q)", False], "shield2": [(475, 450), 14, "Защита +2", False], "asteroid_dropstar": [(325, 400), 15, "Астероид дропает звезду\nШанс - 10%", False], "harvester_double": [(325, 500), 15, "Харвестеры дают +2\nзвезды", False], "spaceship_small_asteroid50": [(200, 400), 17, "Урон от маленьких\nастероидов снижен на 50%", False], "electrostation_double": [(200, 500), 17, "Макс. энергия +100\n+1 макс. электростанция", False], "uncharted_portal": [(85, 450), 25, "Позволяет\nставить портал,\nведущий в иные\nизмерения...\n(Клавиша O)", False]}
        self.upgrades = [TalantsIcon(position=self.talants_list[name][0], name=name) for name in self.talants_list]
        self.upgrade_info = []
        self.multi_shot_cd = 0
        self.shield_cd = 0
        self.free_upgrades = 0
        self.preview_list = [Preview(name="Кадры/Кадр" + str(i), position=(400, 400)) for i in range(1, 25)]
        self.rand_star_cd = 0
        self.defense = 0
        self.log_list = []
        #self.neuro_net = NeuroNet(parameters={"Delta": 'D', "Ultra": 'U', "Recombinator": 'R', "Linker": "L"}[input()], Spaceship=self.spaceship)

    def preview(self):
        for flip in self.preview_list:
            flip.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(round(self.fps / 3.5))

    def main_loop(self):
        while True:
            if not self.pause:
                self._handle_input()
                self._process_game_logic()
                self._draw(PAUSE=False)
            else:
                self.pause_logic()
                self._draw(PAUSE=True)

    def pause_logic(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p or event.type == pygame.MOUSEBUTTONDOWN and self.talants_tree and check_zone(
                    [770, 200], event.pos, 55):
                self.pause_cd = 0.1
                self.pause = False
                self.clock.tick(self.fps)
                if self.talants_tree: self.open_talants()
                self.upgrade_info = []
            elif event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and check_zone([770, 200], event.pos, 55):
                self.pause = False
                self.open_talants()
            elif event.type == pygame.MOUSEMOTION and self.talants_tree:
                for icon in self.upgrades:
                    if check_zone(icon.position, event.pos, 37):
                        if self.level >= self.talants_list[icon.name][1]:
                            self.upgrade_info = [self.talants_list[icon.name][2], self.talants_list[icon.name][0]]
                        else:
                            self.upgrade_info = ["Неизвестная\nтехнология", self.talants_list[icon.name][0]]
        self.pause_cd -= 1 / self.fps

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("SpaceRocks")

    def TICK(self):
        if self.energy < 100:
            regEn = (6+len(self.electrostations)+int(self.level>=5))/self.fps
            if self.energy + regEn < 100:
                self.energy += regEn
            else: self.energy = 100
        ticker = 1 / self.fps
        self.star_timer -= ticker
        self.aster_timer -= ticker
        self.electro_cd_timer -= ticker
        self.regen_cd -= ticker
        if self.electrostations and self.electro_cd_timer <= 0:
            self.electro_cd_timer = 5
            self.energy += 20
        if self.energy > 100:
            self.energy = 100
        if self.tick_num == self.red_untill:
            self.enough_energy = True
        self.pause_cd -= ticker
        self.multi_shot_cd -= ticker
        self.shield_cd -= ticker
        self.rand_star_cd -= ticker

    def open_talants(self):
        if self.talants_tree:
            self.talants_tree = None
            return None
        self.talants_tree = TalantsMenu()
        if self.talants_tree: self.pause = True
        else: self.pause = False

    def _handle_input(self):

        neuro_net_choose = []
        #neuro_net_choose = self.neuro_net.predict(data='None')

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                if self.energy >= 5:
                    self.spaceship.shoot(self.level > 7)
                    self.energy -= 5
                else:
                    self.enough_energy = False
                    self.red_untill = self.fps + self.tick_num
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if check_zone([770, 200], event.pos, 55):
                    self.open_talants()

        if "shoot" in neuro_net_choose:
            if self.energy >= 3:
                self.spaceship.shoot(self.level > 7)
                self.energy -= 3
            else:
                self.enough_energy = False
                self.red_untill = self.fps + self.tick_num


        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT] or is_key_pressed[pygame.K_d] or "R" in neuro_net_choose:
                self.spaceship.rotate(clockwise=True)
                self.log_list.append([" ".join(map(str, map(int, self.spaceship.position))), "R"])
            elif is_key_pressed[pygame.K_LEFT] or is_key_pressed[pygame.K_a] or "L" in neuro_net_choose:
                self.spaceship.rotate(clockwise=False)
                self.log_list.append([" ".join(map(str, map(int, self.spaceship.position))), "L"])
            if is_key_pressed[pygame.K_UP] or is_key_pressed[pygame.K_w] or "U" in neuro_net_choose:
                if self.energy >= 0.3:
                    self.spaceship.accelerate()
                    if self.level < 5 and neuro_net_choose == []: self.energy -= 0.3
                else:
                    self.enough_energy = False
                    self.red_untill = self.fps + self.tick_num
                self.log_list.append([" ".join(map(str, map(int, self.spaceship.position))), "U"])
            if is_key_pressed[pygame.K_DOWN] or is_key_pressed[pygame.K_s] or "D" in neuro_net_choose:
                self.spaceship.stop_acceleration()
                self.log_list.append([" ".join(map(str, map(int, self.spaceship.position))), "D"])
            if is_key_pressed[pygame.K_h] and self.level > 1:
                if self.stardust >= 65 and len(self.harvesters) < 2:
                    self.stardust -= 65
                    self.harvesters.append(Harvester(surface=self.screen, position=self.spaceship.position))
            if is_key_pressed[pygame.K_e]:
                if self.stardust >= 80 and len(self.electrostations) == 0 and self.level > 1:
                    self.stardust -= 80
                    self.electrostations.append(ElectroStation(surface=self.screen, position=self.spaceship.position))
            if is_key_pressed[pygame.K_d] and is_key_pressed[pygame.K_i] and is_key_pressed[pygame.K_m] and is_key_pressed[pygame.K_a]: self.spaceship.CHEATS_ON()
            if is_key_pressed[pygame.K_l]:
                self.spaceship.level_up(level=self.level+1)
                self.level += 1
            if is_key_pressed[pygame.K_f] and self.multi_shot_cd <= 0 and self.level >= 9:
                self.spaceship.octople_shot()
                self.spaceship.octople_shot()
                self.multi_shot_cd = 15
            if is_key_pressed[pygame.K_q] and self.level >= 12 and self.shield_cd <= 0:
                self.defense += 4
                self.shield_cd = 37
            if self.shield_cd <= 30 and self.defense >= 4:
                self.defense -= 4
            if is_key_pressed[pygame.K_p] and self.pause_cd < 0:
                self.pause = True
                self.pause_cd = 0.03
            #else:
             #   print("PauseCD = ", self.pause_cd)
            if self.level >= 15:
                if self.rand_star_cd <= 0:
                    self.starrings.append(Star(surface=self.screen))
                    self.rand_star_cd += 20
            if (is_key_pressed[pygame.K_r] or "Heal" in neuro_net_choose) and self.regen_cd <= 0:
                self.health += 10
                self.regen_cd = 10 - int(neuro_net_choose != []) * 2
            if is_key_pressed[pygame.K_x]:
                self.aster_timer -= 0.3
            # if is_key_pressed and not self.was_preview_shown:
            #     self.preview()
            #     self.was_preview_shown = True

    def _process_game_logic(self):

        for game_object in self._get_game_objects():
            game_object.move(self.screen, self.fps)

        if self.aster_timer <= 0:
            for _ in range(self.level_to_aseroid[self.level][0] if self.level < 33 else 1):
                while True:
                    position = get_random_position(self.screen)
                    if (
                        position.distance_to(self.spaceship.position)
                        > self.MIN_ASTEROID_DISTANCE
                    ):
                        break

                self.asteroids.append(Asteroid(position, self.asteroids.append))

            if self.level < 33: self.aster_timer += self.level_to_aseroid[self.level][1]

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    if self.health - asteroid.size * (10 - self.defense - (self.level >= 14) * 2) >= 0:
                        self.health -= asteroid.size * (10 - self.defense - (self.level >= 14) * 2)
                    else: self.health = 0
                    for i in range(asteroid.size):
                        self.spaceship.stop_acceleration()
                    self.asteroids.remove(asteroid)
                    asteroid.split()
                    self.asteroid_broken += 1

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    if self.level >= 15:
                        if random.randint(1, 30 // asteroid.size) == 5:
                            self.starrings.append(Star(surface=self.screen, position=asteroid.position))
                    self.exp += asteroid.size ** 2 * 5
                    self.asteroid_broken += 1
                    break

        if self.exp >= (100 * self.level):
            self.spaceship.level_up(level=self.level+1)
            self.exp -= 100 * self.level
            self.level += 1

        if self.star_timer <= 0:
            for _ in range(3):
                self.starrings.append(Star(surface=self.screen))
                self.star_timer += random.randint(7, 10)

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)
        for star in self.starrings[:]:
            if not self.screen.get_rect().collidepoint(star.position):
                self.starrings.remove(star)
            if self.spaceship:
                if star.collides_with(self.spaceship):
                    self.stardust += random.randint(5, 10)
                    self.starrings.remove(star)
                for harv in self.harvesters:
                    if star.collides_with(harv) and star in self.starrings:
                        self.stardust += 5 + (self.level >= 14) * 2
                        self.starrings.remove(star)
                        break

        if self.health <= 0:
            self.spaceship = None

        #if not self.asteroids and self.spaceship:
         #   self.message = "Вот ты молодец! Уничтожил " + str(self.asteroid_num) + ' aстероидa(ов)!'

    def _draw(self, PAUSE=False):

        if not self.spaceship:
            self.screen.fill(color=(0, 0, 0))
            print_text(surface=self.screen, text="Миссия провалена...", font=self.font)
            pygame.display.flip()
            time.sleep(3)

            with open("log.txt", "w") as log: [log.write(" ".join(string) + '\n') for string in self.log_list] # лог для нейросети

            while True:
                [quit() for event in pygame.event.get() if event.type == pygame.QUIT]
                self.screen.fill(color=(0,0,0))
                self.clock.tick(self.fps)
                print_text(surface=self.screen, text="Результаты",
                           font=pygame.font.Font(None, 80), color=(255, 0, 0), coords=(400, 150))
                print_text(surface=self.screen, text=self.nickname,
                           font=pygame.font.Font(None, 60), color=(255, 0, 0), coords=(400, 200))
                print_text(surface=self.screen, text="Уровень: " + str(self.level),
                           font=pygame.font.Font(None, 60), color=(255, 0, 0), coords=(400, 240))
                print_text(surface=self.screen, text="Уничтожено астероидов: " + str(self.asteroid_broken),
                           font=pygame.font.Font(None, 60), color=(255, 0, 0), coords=(400, 280))
                pygame.display.flip()

        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.shield_cd > 30:
            EnergyShield(position=(random.randint(round(self.spaceship.position[0]-7), round(self.spaceship.position[0]+7)), random.randint(round(self.spaceship.position[1]-7), round(self.spaceship.position[1]+7)))).draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        if self.health < 0: self.health = 0
        if self.health > 100: self.health = 100

        # Creating UI enviroment
        print_text(surface=self.screen, text=' '.join(["Energy:", str(round(self.energy))]), font=self.font, color=(255, 255*int(self.enough_energy), ([round(255*(self.electro_cd_timer-4)), 0][int(self.electro_cd_timer < 4.1)])*int(self.enough_energy)), coords=(110, 25))
        draw_rectangle(surface=self.screen, color=(255, 255*int(self.enough_energy), ([round(255*(self.electro_cd_timer-4)  ), 0][int(self.electro_cd_timer < 4.1)])*int(self.enough_energy)), params=(10, 45, round(self.energy)*2, 20), param2=8)

        print_text(surface=self.screen, text=' '.join(["StarDust:", str(self.stardust)]), font=self.font, color=(200, 200, 0), coords=(100, 570))

        print_text(surface=self.screen, text=' '.join(["Health:", str(round(self.health))]), font=self.font, color=(255, 255 if self.regen_cd > 0 else 0, 255 if self.regen_cd > 0 else 0), coords=(350, 25))
        draw_rectangle(surface=self.screen, color=(200 - self.health*2, self.health*2, 0), params=(250, 45, round(self.health)*2, 20), param2=10)

        level_color = round(self.level*25.5) if self.level < 10 else 255
        print_text(surface=self.screen, text=' '.join(["Level:", str(self.level)]), font=self.font, color=(255, 255, 100), coords=(600, 25))
        draw_rectangle(surface=self.screen, color=(level_color, level_color, level_color), params=(500, 45, round(self.exp / self.level) * 2, 20), param2=10)

        print_text(surface=self.screen, text=' '.join(["Next asteroid spawn in: ", str(round(self.aster_timer)), "sec"]), font=self.font, color=(255, 255, 100), coords=(500, 570))

        if PAUSE: print_text(surface=self.screen, text="Игра приостановлена", font=self.font, color=(255, 20, 0), coords=(400, 300))

        print_text(surface=self.screen, text=self.nickname + " [" + str(self.level) + "]", font=pygame.font.Font(None, 30), color=(255, 0, 0), coords=(self.spaceship.position[0], self.spaceship.position[1]-20))
        x, y = self.spaceship.position
        if self.shield_cd >= 0:
            draw_rectangle(surface=self.screen, color=(0, 255, 255), params=(x-50, y-33, round(self.shield_cd * 2.7), 4))
        if self.multi_shot_cd >= 0:
            draw_rectangle(surface=self.screen, color=(0, 255, 0), params=(x - 50, y - 38, round(self.multi_shot_cd * 6.66), 4))

        if self.talants_tree:
            self.talants_tree.draw(self.screen)
            for icon in self.upgrades:
                if self.talants_list[icon.name][1] <= self.level:
                    if self.talants_list[icon.name][3]:
                        x, y = self.talants_list[icon.name][0]
                        draw_rectangle(self.screen, (0, 255, 255), (x - 40, y - 40, x - 20, y - 70))
                    icon.draw(self.screen)
                else:
                    TalantsIcon(position=self.talants_list[icon.name][0]).draw(self.screen)
            print_text(surface=self.screen, text="Древо технологий (страница 1 / 18)  ",
                       font=pygame.font.Font(None, 60), color=(0, 255, 255),
                       coords=(400, 40))
        self.talant.draw(self.screen)
        if self.upgrade_info:
            for i in range(len(self.upgrade_info[0].split('\n'))):
                print_text(surface=self.screen, text=self.upgrade_info[0].split('\n')[i],
                       font=pygame.font.Font(None, 32), color=(255, 0, 0),
                       coords=(self.upgrade_info[1][0], self.upgrade_info[1][1]+(i-len(self.upgrade_info[0].split('\n'))/2)*25))

        pygame.display.flip()

        if not PAUSE:
            self.TICK() # <---- вся арифметика ПоТиково исполняется тут
            self.clock.tick(self.fps)
        self.tick_num += 1

    def _get_game_objects(self):
        game_objects = [*self.harvesters, *self.electrostations, *self.asteroids, *self.bullets, *self.starrings]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects