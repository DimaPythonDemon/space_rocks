import pygame
from PIL import Image
from utils import load_sprite, load_sound, check_zone, print_text, draw_rectangle
from models import Button, Spaceship, Harvester
from game import SpaceRocks

class Menu:

    def __init__(self):

        self._init_pygame()
        self.mouse = pygame.mouse
        bg_name = 'bg'
        self.fps = 30
        self.start = False
        im = Image.open("assets/sprites/" + bg_name + ".png")
        self.width, self.height = im.size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = load_sprite(bg_name, False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 50)
        self.buttons = []
        self.buttons.append(Button(button_name="Выживание",
                                   position=[200, 300],
                                   sizes=[240, 90],
                                   onclick="onclicks",
                                   surface=self.screen))
        self.buttons.append(Button(button_name="newbutt",
                                   position=[400, 300],
                                   sizes=[100, 50],
                                   onclick="off",
                                   surface=self.screen))

        self.main_loop()

    def main_loop(self):
        while not self.start:
            self._handle_input()
            self._process_game_logic()
            self._draw()


    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Меню :)")

    def _handle_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        for button in self.buttons:
            button.OnClick(self.mouse)

    def _draw(self):

        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(self.fps)

    def _get_game_objects(self):

        game_objects = [*self.buttons]
        return game_objects

