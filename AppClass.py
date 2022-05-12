# standard
import os
import sys
import pickle
import pygame
from pygame.locals import *
#
import variables
import WorldClass


class App:

    def __init__(self, **kwargs):
        self.args = kwargs["args"]
        self.world = None
        if self.args.console:
            self.console = Console(self)
        if self.args.window:
            self.pygame_window = PyGameWindow(self)

    def GUI(self):
        if self.args.window:
            self.pygame_window.run()
            return 1
        elif self.args.console:
            return self.console.run()

    def run(self):
        while True:
            try:
                result = self.GUI()
                if result == 0:
                    break
            except Exception as ex:
                print(ex)

    def world_create(self):
        self.world = WorldClass.World((variables.WORLD_WIDTH, variables.WORLD_HEIGHT))
        self.world.creature_generate()
        # self.GUI()

    def world_load(self, filename="saved_game"):
        try:
            file = open(f'{filename}.txt', 'rb')
            self.world = pickle.load(file)
            self.world.map.clear()
            self.world.creatures.clear()

            for i in range(0, self.world.world_sizes[0]):
                row = list()
                for j in range(0, self.world.world_sizes[1]):
                    cell = pickle.load(file)
                    for creature in cell.creatures_in_cell:
                        self.world.creatures.append(creature)
                    row.append(cell)
                self.world.map.append(row)
            file.close()
        except Exception as ex:
            print(ex)

    def world_save(self, filename="saved_game"):
        try:
            for creature in self.world.creatures:
                creature.image = None
            file = open(f'{filename}.txt', 'wb')

            pickle.dump(self.world, file)
            for row_i in range(self.world.world_sizes[0]):
                for cell_j in range(self.world.world_sizes[1]):
                    pickle.dump(self.world.map[row_i][cell_j], file)
            for creature in self.world.creatures:
                pickle.dump(creature, file)

            file.close()
        except Exception as ex:
            print(ex)


class PyGameWindow:

    def __init__(self, app):
        self.buttons = []
        self.app = app
        # pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Land simulation")
        self.clock = pygame.time.Clock()
        # variables
        self.sprites = {}
        self.load_sprites()
        self.start_sound()
        self.buttons_init()

    def run(self):
        if self.app.world is None:
            self.app.world_create()

        self.update_sprites()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.buttons_action(event.pos)

            # low
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.app.world.step_generate()
        # fast
        if pygame.key.get_pressed()[K_SPACE]:
            self.app.world.step_generate()

        self.print_world_map()
        self.world_stats()
        self.buttons_print()
        if pygame.mouse.get_pressed()[2]:
            self.creature_stats(self.define_creature_by_pos_on_screen(pygame.mouse.get_pos()))

        pygame.display.flip()
        self.clock.tick(40)

    def print_world_map(self):
        # background
        ground = pygame.transform.scale(self.sprites["Ground"], (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(ground, (0, 0))

        # creatures
        for i in range(0, self.app.world.world_sizes[0]):
            for j in range(0, self.app.world.world_sizes[1]):
                for creature in self.app.world.map[i][j].creatures_in_cell:
                    if creature.parameters["type_of_food"] == "NO" and creature.image is not None:
                        self.screen.blit(creature.image, (creature.position_x, creature.position_y))

        for i in range(0, self.app.world.world_sizes[0]):
            for j in range(0, self.app.world.world_sizes[1]):
                for creature in self.app.world.map[i][j].creatures_in_cell:
                    if creature.parameters["type_of_food"] == "PLANT" and creature.image is not None:
                        self.screen.blit(creature.image, (creature.position_x, creature.position_y))

        for i in range(0, self.app.world.world_sizes[0]):
            for j in range(0, self.app.world.world_sizes[1]):
                for creature in self.app.world.map[i][j].creatures_in_cell:
                    if creature.parameters["type_of_food"] == "MEAT" and creature.image is not None:
                        self.screen.blit(creature.image, (creature.position_x, creature.position_y))

    def update_sprites(self):
        block_width = self.screen.get_width() / self.app.world.world_sizes[0]
        block_height = self.screen.get_height() / self.app.world.world_sizes[1]
        # images
        herbivore_large_1 = self.sprites["Herbivore1"]
        herbivore_small_1 = pygame.transform.scale(herbivore_large_1, (herbivore_large_1.get_width() // 2,
                                                                       herbivore_large_1.get_height() // 2))
        herbivore_large_0 = self.sprites["Herbivore0"]
        herbivore_small_0 = pygame.transform.scale(herbivore_large_0, (herbivore_large_0.get_width() // 2,
                                                                       herbivore_large_0.get_height() // 2))

        predator_large_1 = self.sprites["Predator1"]
        predator_small_1 = pygame.transform.scale(predator_large_1, (predator_large_1.get_width() // 2,
                                                                     predator_large_1.get_height() // 2))
        predator_large_0 = self.sprites["Predator0"]
        predator_small_0 = pygame.transform.scale(predator_large_0, (predator_large_0.get_width() // 2,
                                                                     predator_large_0.get_height() // 2))

        # set images
        for i in range(0, self.app.world.world_sizes[0]):
            for j in range(0, self.app.world.world_sizes[1]):
                herbivores = []
                predators = []
                for creature in self.app.world.map[i][j].creatures_in_cell:

                    if creature.parameters["type_of_food"] == "NO":
                        creature.image = pygame.transform.scale(self.sprites["Grass"], (block_width, block_height))
                        creature.position_x = i * block_width
                        creature.position_y = j * block_height

                    if creature.parameters["type_of_food"] == "PLANT":
                        if creature.parameters["gender"] == 1:
                            creature.image = herbivore_large_0
                            if creature.parameters["age"] < 10:
                                creature.image = herbivore_small_0
                        else:
                            creature.image = herbivore_large_1
                            if creature.parameters["age"] < 10:
                                creature.image = herbivore_small_1
                        herbivores.append(creature)

                    if creature.parameters["type_of_food"] == "MEAT":
                        if creature.parameters["gender"] == 1:
                            creature.image = predator_large_0
                            if creature.parameters["age"] < 10:
                                creature.image = predator_small_0
                        else:
                            creature.image = predator_large_1
                            if creature.parameters["age"] < 10:
                                creature.image = predator_small_1
                        predators.append(creature)

                    creature.update_sprite()

                for herbivore in herbivores:
                    herbivore.position_x = (i * block_width) + (block_width / 5 * (herbivores.index(herbivore) % 4))
                    herbivore.position_y = (j * block_height)

                for predator in predators:
                    predator.position_x = (i * block_width) + (block_width / 5 * (predators.index(predator) % 4))
                    predator.position_y = (j * block_height)

    def start_sound(self):
        pygame.mixer.music.load("sounds/ambient-piano-amp-strings.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def load_sprites(self):
        path_to_sprite = "img"
        self.sprites["Ground"] = pygame.image.load(f"{path_to_sprite}/ground.png")

        self.sprites["Grass"] = pygame.image.load(f"{path_to_sprite}/grass.png")

        self.sprites["Herbivore1"] = pygame.image.load(f"{path_to_sprite}/herbivore1.png")
        self.sprites["Herbivore0"] = pygame.image.load(f"{path_to_sprite}/herbivore0.png")
        self.sprites["Predator0"] = pygame.image.load(f"{path_to_sprite}/predator0.png")
        self.sprites["Predator1"] = pygame.image.load(f"{path_to_sprite}/predator1.png")

        self.sprites["GrassAdd"] = pygame.image.load(f"{path_to_sprite}/grass_add.png")
        self.sprites["HerbivoreAdd"] = pygame.image.load(f"{path_to_sprite}/herbivore_add.png")
        self.sprites["PredatorAdd"] = pygame.image.load(f"{path_to_sprite}/predator_add.png")

    def world_stats(self):
        self.world_stat("Step", str(self.app.world.count_of_steps), 1, 5)
        self.world_stat("All", str(len(self.app.world.creatures)), 2, 5)
        self.world_stat("Plants", str(self.app.world.count_of_plants), 3, 5)
        self.world_stat("Herbivores", str(self.app.world.count_of_herbivores), 4, 5)
        self.world_stat("Predators", str(self.app.world.count_of_predators), 5, 5)

    def world_stat(self, stat_name, stat, serial_number, quantity_stats):
        font = pygame.font.Font("font/AllTheWayToTheSun-o2O0.TTF", 36)
        white = (255, 255, 255)
        block_width = self.screen.get_width() / quantity_stats
        text_stat_name = font.render(stat_name, True, white)
        text_stat_count = font.render(stat, True, white)
        text_space = font.render(" ", True, white)

        stat_text_width = text_stat_name.get_width() + text_space.get_width() + text_stat_count.get_width()

        pos_x_for_stat_name = block_width * (serial_number - 1) + ((block_width - stat_text_width) / 2)
        pos_x_for_stat_count = pos_x_for_stat_name + text_stat_name.get_width() + text_space.get_width()

        # self.screen.blit(text_stat_name, (pos_x_for_stat_name, self.screen.get_height() - 46))
        # self.screen.blit(text_stat_count, (pos_x_for_stat_count, self.screen.get_height() - 46))
        self.screen.blit(text_stat_name, (pos_x_for_stat_name, 10))
        self.screen.blit(text_stat_count, (pos_x_for_stat_count, 10))

    def define_creature_by_pos_on_screen(self, pos):
        for creature in self.app.world.creatures:
            if creature.rect.collidepoint(pos):
                return creature
        return None

    def creature_stats(self, creature):
        if creature is not None:
            font = pygame.font.Font("font/CONSOLA.TTF", 11)

            params = str(creature.parameters).replace(", \'", "\n\'").replace("{", ""). \
                replace("}", "").replace("\'", "")
            full_text = params.split("\n")

            full_text = [font.render(text, True, (255, 255, 255)) for text in full_text]

            # background
            max_width = 0
            for text in full_text:
                max_width = max(max_width, text.get_width())
            background_color = (67, 42, 24)
            background_width = max_width + 10
            background_height = (len(full_text) * (11 + 2)) + 10  # 11 - font size, 2 - indent
            background_x = creature.position_x + creature.image.get_width() / 2
            background_y = creature.position_y + creature.image.get_height() / 2
            if creature.position_x + creature.image.get_width() / 2 + background_width > self.screen.get_width():
                background_x -= background_width
            if creature.position_y + creature.image.get_height() / 2 + background_height > self.screen.get_height():
                background_y -= background_height
            background = pygame.Surface((background_width, background_height))
            background.fill(background_color)
            background.set_alpha(192)
            self.screen.blit(background, (background_x, background_y))

            # draw
            for text in full_text:
                self.screen.blit(text, (background_x + 5, (background_y + 5) + full_text.index(text) * (11 + 2)))

    class Button(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = None
            self.rect = None
            self.position_x = 0
            self.position_y = 0
            self.type_ = str()

        def recalculate_the_rect(self):
            self.rect = pygame.Rect(self.position_x, self.position_y, self.image.get_width(), self.image.get_height())

    def buttons_init(self):
        # ADD CREATURES BUTTONS
        count = self.screen.get_width() / self.sprites["GrassAdd"].get_width()
        self.button_create(self.sprites["GrassAdd"], "add_plant", (count / 2) - 2, count)
        self.button_create(self.sprites["HerbivoreAdd"], "add_herbivore", (count / 2), count)
        self.button_create(self.sprites["PredatorAdd"], "add_predator", (count / 2) + 2, count)
        # SAVE/LOAD
        font = pygame.font.Font("font/AllTheWayToTheSun-o2O0.TTF", 36)
        self.button_create(font.render("Save", True, (255, 255, 255)), "save")
        self.button_create(font.render("Load", True, (255, 255, 255)), "load")

    def buttons_print(self):
        for button in self.buttons:
            self.screen.blit(button.image, (button.position_x, button.position_y))

    def button_create(self, image, type_, button_number=None, quantity_buttons=None):
        button = self.Button()
        button.image = image
        button.type_ = type_
        if button_number is not None and quantity_buttons is not None:
            block_width = self.screen.get_width() / quantity_buttons
            button.position_x = block_width * (button_number - 1) + ((block_width - image.get_width()) / 2)
            # button.position_y = 10
        else:
            if type_ == "save":
                button.position_x = 10
            elif type_ == "load":
                button.position_x = self.screen.get_width() - button.image.get_width() - 10
            else:
                button.position_x = self.screen.get_width() / 2

        button.position_y = self.screen.get_height() - button.image.get_height() - 10
        self.screen.blit(image, (button.position_x, button.position_y))
        button.recalculate_the_rect()
        self.buttons.append(button)

    def buttons_action(self, event_pos):
        for button in self.buttons:
            if button.rect.collidepoint(event_pos):
                # add creature
                pos = tuple()
                creature = None
                if button.type_ == "add_plant":
                    pos = self.app.world.creature_find_position("NO", True)
                    creature = WorldClass.Plant(pos, self.app.world)
                elif button.type_ == "add_herbivore":
                    pos = self.app.world.creature_find_position("PLANT", True)
                    creature = WorldClass.Herbivore(pos, self.app.world)
                elif button.type_ == "add_predator":
                    pos = self.app.world.creature_find_position("MEAT", True)
                    creature = WorldClass.Predator(pos, self.app.world)

                if pos != (-1, -1):
                    self.app.world.creature_add_in_arrays(creature)

                # save / load world
                if button.type_ == "save":
                    self.app.world_save(filename="saved_game")
                if button.type_ == "load":
                    self.app.world_load(filename="saved_game")

        self.update_sprites()


class Console:

    def __init__(self, app):
        self.app = app

    def print_world_map(self):
        os.system("cls")
        self.app.world.step_print()
        self.world_stats()

    def run(self):
        if self.app.world is None:
            self.start_menu()
            self.print_world_map()
        self.print_world_map()
        result = self.execute_commands()
        return result

    def start_menu(self):
        os.system("cls")

        print("start - new game\n"
              "load  - load game from file")
        first_command = input()
        if first_command == "start" or first_command == "":
            self.app.world_create()
        elif first_command == "load":
            self.app.world_load(filename="saved_game")
        else:
            print("error")
            exit()

    def execute_commands(self):
        user_command = input()
        correct_command = False
        # GLOBAL COMMANDS
        if user_command == "save":
            self.app.world_save(filename="saved_game")
            correct_command = True

        if user_command == "exit":
            return 0

        # LOCAL COMMANDS FOR WORD
        if correct_command is False:
            correct_command = self.app.world.command(user_command)
            os.system("pause")

        if user_command is not None and correct_command is False:
            os.system("cls")
            self.app.world.step_generate()
            # time.sleep(0.01)

        return 1

    def world_stats(self):
        print("step:", self.app.world.count_of_steps,
              "\nall:", len(self.app.world.creatures),
              "plants:", self.app.world.count_of_plants,
              "herbivores:", self.app.world.count_of_herbivores,
              "predators:", self.app.world.count_of_predators)
