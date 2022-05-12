import random
import datetime
from PlantClass import Plant
from HerbivoreClass import Herbivore
from PredatorClass import Predator


class World:
    class Cell:
        coords = tuple()
        creatures_in_cell = list()

        def __init__(self, coords):
            self.creatures_in_cell = list()
            self._coords = coords

        def creature_add(self, creature):
            if len(self.creatures_in_cell) - self.creatures_count_with_type("NO") < 4:
                self.creatures_in_cell.append(creature)
            elif creature.parameters["type_of_food"] == "NO" and self.creatures_count_with_type("NO") == 0:
                self.creatures_in_cell.append(creature)
            return

        def creature_remove(self, creature):
            if creature in self.creatures_in_cell:
                self.creatures_in_cell.remove(creature)
            return

        def creatures_count(self):
            return len(self.creatures_in_cell)

        def creatures_count_with_type(self, type_of_food):
            count = 0
            for creature in self.creatures_in_cell:
                if creature.parameters["type_of_food"] == type_of_food:
                    count += 1
            return count

        def presentation(self):
            if len(self.creatures_in_cell) != 0:
                plant = [False, chr(0)]
                herbivore = [False, chr(0)]
                predator = [False, chr(0)]
                for creature in self.creatures_in_cell:
                    if creature.parameters["type_of_food"] == "NO":
                        plant[0] = True
                        plant[1] = creature.parameters["symbol_on_map"]
                    if creature.parameters["type_of_food"] == "PLANT":
                        herbivore[0] = True
                        herbivore[1] = creature.parameters["symbol_on_map"]
                    if creature.parameters["type_of_food"] == "MEAT":
                        predator[0] = True
                        predator[1] = creature.parameters["symbol_on_map"]

                if plant[0] is True and herbivore[0] is True and predator[0] is True:
                    return predator[1]
                elif plant[0] is True and herbivore[0] is True:
                    return herbivore[1]
                elif plant[0] is True and predator[0] is True:
                    return predator[1]
                elif herbivore[0] is True and predator[0] is True:
                    return predator[1]
                elif predator[0] is True:
                    return predator[1]
                elif herbivore[0] is True:
                    return herbivore[1]
                elif plant[0] is True:
                    return plant[1]
            else:
                return "░"

    creatures = list()
    world_sizes = tuple()
    map = list()

    count_of_plants = 0
    count_of_herbivores = 0
    count_of_predators = 0
    count_of_steps = 0

    def __init__(self, world_sizes):
        self.world_sizes = world_sizes
        for i in range(world_sizes[0]):
            row = list()
            for j in range(world_sizes[1]):
                row.append(World.Cell((i, j)))
            self.map.append(row)

    def creature_add_in_arrays(self, creature):
        if creature is not None:
            self.creatures.append(creature)
            x = int(creature.parameters["coords"][0])
            y = int(creature.parameters["coords"][1])
            self.map[x][y].creature_add(creature)
            if creature.parameters["type_of_food"] == "NO":
                self.count_of_plants += 1
            if creature.parameters["type_of_food"] == "PLANT":
                self.count_of_herbivores += 1
            if creature.parameters["type_of_food"] == "MEAT":
                self.count_of_predators += 1

    def creature_generate(self):
        # Generate plants
        if self.world_sizes[0] > 3 and self.world_sizes[1] > 3:
            plants_count = int((self.world_sizes[0] * self.world_sizes[1]) / ((self.world_sizes[0] +
                                                                               self.world_sizes[1])) * 2)
        else:
            plants_count = 2
        for i in range(plants_count):
            pos = self.creature_find_position("NO")
            if pos != (-1, -1):
                new_plant = Plant(pos, self)
                self.creature_add_in_arrays(new_plant)

        # Generate herbivores
        if self.world_sizes[0] > 3 and self.world_sizes[1] > 3:
            herbivores_count = int((self.world_sizes[0] * self.world_sizes[1]) / ((self.world_sizes[0] +
                                                                                   self.world_sizes[1])) * 2)
        else:
            herbivores_count = 2
        for i in range(herbivores_count):
            pos = self.creature_find_position("PLANT")
            if pos != (-1, -1):
                new_herbivore = Herbivore(pos, self)
                self.creature_add_in_arrays(new_herbivore)

        # Generate predators
        if self.world_sizes[0] > 3 and self.world_sizes[1] > 3:
            predators_count = int((self.world_sizes[0] * self.world_sizes[1]) / ((self.world_sizes[0] +
                                                                                  self.world_sizes[1])) * 2)
        else:
            predators_count = 0
        for i in range(predators_count):
            pos = self.creature_find_position("MEAT")
            if pos != (-1, -1):
                new_predator = Predator(pos, self)
                self.creature_add_in_arrays(new_predator)

    def creature_find_position(self, food_type=None, check_place=False):

        if check_place:
            exist_place = False
            for i in range(0, self.world_sizes[0]):
                if exist_place:
                    break
                for j in range(0, self.world_sizes[1]):
                    if food_type == "NO":
                        if self.map[i][j].creatures_count_with_type(food_type) == 0:
                            exist_place = True
                    if food_type == "PLANT" or food_type == "MEAT":
                        if self.map[i][j].creatures_count() - self.map[i][j].creatures_count_with_type("NO") < 4:
                            exist_place = True
                    if exist_place:
                        break
            if not exist_place:
                pos = (-1, -1)
                return pos

        random.seed(datetime.datetime.now())
        while True:
            x = random.randint(0, self.world_sizes[0] - 1)
            y = random.randint(0, self.world_sizes[1] - 1)
            random_position = (x, y)

            if food_type == "NO":
                if self.map[x][y].creatures_count_with_type(food_type) == 0:
                    return random_position
            elif food_type == "PLANT" or food_type == "MEAT":
                if self.map[x][y].creatures_count() - self.map[x][y].creatures_count_with_type("NO") < 4:
                    return random_position

    def creature_locate(self, creature):
        if creature.parameters["type_of_food"] == "NO":
            empty_cells_near = {
                (creature.parameters["coords"][0] - 1, creature.parameters["coords"][1] - 1): False,
                (creature.parameters["coords"][0] - 1, creature.parameters["coords"][1] + 0): False,
                (creature.parameters["coords"][0] - 1, creature.parameters["coords"][1] + 1): False,
                (creature.parameters["coords"][0] + 0, creature.parameters["coords"][1] - 1): False,
                (creature.parameters["coords"][0] + 0, creature.parameters["coords"][1] + 1): False,
                (creature.parameters["coords"][0] + 1, creature.parameters["coords"][1] - 1): False,
                (creature.parameters["coords"][0] + 1, creature.parameters["coords"][1] + 0): False,
                (creature.parameters["coords"][0] + 1, creature.parameters["coords"][1] + 1): False
            }
            have_empty_cells_near = False
            for coords in empty_cells_near:
                if (0 <= coords[0] < self.world_sizes[0]) and (0 <= coords[1] < self.world_sizes[1]) and \
                        self.map[coords[0]][coords[1]].creatures_count_with_type("NO") == 0:
                    empty_cells_near[coords] = True
                    have_empty_cells_near = True

            if have_empty_cells_near is True:
                empty_cells_near_list = list(empty_cells_near)
                while True:
                    way = random.choice(empty_cells_near_list)
                    if empty_cells_near[way] is True:
                        creature.parameters["coords"] = way
                        # print("new plant:", creature.parameters["coords"],
                        # f"in cell {way} with {self._map[way[0]][way[1]].creatures_count_with_type('NO')} plants")
                        self.count_of_plants += 1
                        self.creatures.append(creature)
                        self.map[way[0]][way[1]].creature_add(creature)
                        break
            else:
                self.creature_remove(creature)
        else:
            if self.map[creature.parameters["coords"][0]][creature.parameters["coords"][1]].creatures_count() - \
                    self.map[creature.parameters["coords"][0]][creature.parameters["coords"][1]].\
                    creatures_count_with_type("NO") < 4:
                if creature.parameters["type_of_food"] == "PLANT":
                    self.count_of_herbivores += 1
                if creature.parameters["type_of_food"] == "MEAT":
                    self.count_of_predators += 1
                self.creatures.append(creature)
                self.map[creature.parameters["coords"][0]][creature.parameters["coords"][1]].creature_add(creature)

    def creature_add(self, creature, coords):
        if 0 <= int(coords[0]) < self.world_sizes[0] and 0 <= int(coords[1]) < self.world_sizes[1]:

            if creature.parameters["type_of_food"] == "PLANT" or creature.parameters["type_of_food"] == "MEAT":
                if self.map[int(coords[0])][int(coords[1])].creatures_count() < 4:
                    self.map[int(coords[0])][int(coords[1])].creature_add(creature)
                    self.creatures.append(creature)

                    if creature.parameters["type_of_food"] == "PLANT":
                        self.count_of_herbivores += 1
                    if creature.parameters["type_of_food"] == "MEAT":
                        self.count_of_predators += 1
                    return True
                elif self.map[int(coords[0])][int(coords[1])].creatures_count() >= 4 and \
                        (creature.parameters["type_of_food"] == "PLANT" or
                         creature.parameters["type_of_food"] == "MEAT"):
                    print("In cell already are 4 creatures")
                    return False

            # PLANTS
            if creature.parameters["type_of_food"] == "NO":
                # if self.map[int(coords[0])][int(coords[1])].creatures_count() < 1 and \
                if self.map[int(coords[0])][int(coords[1])].creatures_count_with_type("NO") < 1:

                    self.map[int(coords[0])][int(coords[1])].creature_add(creature)
                    self.creatures.append(creature)
                    self.count_of_plants += 1
                    return True
                # elif self.map[int(coords[0])][int(coords[1])].creatures_count() >= 1 and \
                elif self.map[int(coords[0])][int(coords[1])].creatures_count_with_type("NO") >= 1:
                    print("In cell already is 1 grass")
                    return False

        else:
            print("No such coords on map")
            return False

    def creature_remove(self, creature):
        try:
            self.creatures.remove(creature)
            self.map[creature.parameters["coords"][0]][creature.parameters["coords"][1]].creature_remove(creature)
            if creature.parameters["type_of_food"] == "NO":
                self.count_of_plants -= 1
            if creature.parameters["type_of_food"] == "PLANT":
                self.count_of_herbivores -= 1
            if creature.parameters["type_of_food"] == "MEAT":
                self.count_of_predators -= 1
        except Exception:
            pass

    def step_generate(self):
        creatures_to_locate = []
        # creatures_to_remove = []

        creatures_previous_step = self.creatures.copy()
        for creature in creatures_previous_step:
            # print (creature in creatures_previous_step, creature)
            result = creature.action()
            # if creature.parameters["type_of_food"] == "PLANT":
            #   print(f"{creature.parameters.get('type_id')})", creature.parameters["coords"], result)

            if result == "REPRODUCTION":
                new_creature = creature.action_reproduction()
                creatures_to_locate.append(new_creature)

            if result == "EATING":
                eaten_creature = creature.action_eating()
                if eaten_creature is not None and eaten_creature.parameters["health_points"] <= 0:
                    self.creature_remove(eaten_creature)
                    if eaten_creature in creatures_previous_step:
                        creatures_previous_step.remove(eaten_creature)

            if result == "MOVEMENT":
                creature.action_movement()

            if result == "DIE":
                self.creature_remove(creature)
                if creature in creatures_previous_step:
                    creatures_previous_step.remove(creature)

        for creature in creatures_to_locate:
            self.creature_locate(creature)

        self.count_of_steps += 1

    def step_print(self):
        for row in self.map:
            row_str = ""
            for cell in row:
                row_str += cell.presentation()
            print(row_str)

    def command(self, command):
        com = command.split(" ")
        # commands for debug
        if command == "help":
            print("ig  - info grass\nigm - info grass map\nih  - info herbivore\nihm - info herbivore map\n"
                  "ip  - info predators\nipm - info predators map\nia  - info all\n"
                  "cgc x y - count of grass in coords\n"
                  "chc x y - count of herbivores in coords\n"
                  "cpc x y - count of predators in coords\n"
                  "ag x y  - add grass\n"
                  "ah x y  - add herbivore\n"
                  "ap x y  - add predator")
            return True
        if com[0] == "ig" or command == "info grass":
            for creature in self.creatures:
                if creature.parameters["type_of_food"] == "NO":
                    print(creature.parameters)
            return True
        if com[0] == "igm" or command == "info grass map":
            for row in self.map:
                for cell in row:
                    for creature in cell.creatures_in_cell:
                        if creature.parameters["type_of_food"] == "NO":
                            print(creature.parameters)
            return True
        if com[0] == "ih" or command == "info herbivore":
            for creature in self.creatures:
                if creature.parameters["type_of_food"] == "PLANT":
                    print(creature.parameters)
            return True
        if com[0] == "ihm" or command == "info herbivore map":
            for row in self.map:
                for cell in row:
                    for creature in cell.creatures_in_cell:
                        if creature.parameters["type_of_food"] == "PLANT":
                            print(creature.parameters)
            return True
        if com[0] == "ip" or command == "info predators":
            for creature in self.creatures:
                if creature.parameters["type_of_food"] == "MEAT":
                    # print(creature)
                    print(creature.parameters)
            return True
        if com[0] == "ipm" or command == "info predators map":
            for row in self.map:
                for cell in row:
                    for creature in cell.creatures_in_cell:
                        if creature.parameters["type_of_food"] == "MEAT":
                            print(creature.parameters)
                            # print(creature)
            return True
        if com[0] == "ia" or command == "info all":
            for creature in self.creatures:
                print(creature.parameters)
                # print(creature)
            return True

        # count of grass in coords
        if com[0] == "cgc" and len(com) == 3:
            x = int(com[1])
            y = int(com[2])
            print(self.map[x][y].creatures_count_with_type('NO'))
            return True
        elif com[0] == "cgc":
            for i in range(0, self.world_sizes[0]):
                for j in range(0, self.world_sizes[1]):
                    print(f"{i} {j})", self.map[i][j].creatures_count_with_type('NO'))
            return True
        if com[0] == "chc" and len(com) == 3:
            x = int(com[1])
            y = int(com[2])
            print(self.map[x][y].creatures_count_with_type('PLANT'))
            return True
        elif com[0] == "chc":
            for i in range(0, self.world_sizes[0]):
                for j in range(0, self.world_sizes[1]):
                    print(f"{i} {j})", self.map[i][j].creatures_count_with_type('PLANT'))
            return True
        if com[0] == "cpc" and len(com) == 3:
            x = int(com[1])
            y = int(com[2])
            print(self.map[x][y].creatures_count_with_type('MEAT'))
            return True
        elif com[0] == "cpc":
            for i in range(0, self.world_sizes[0]):
                for j in range(0, self.world_sizes[1]):
                    print(f"{i} {j})", self.map[i][j].creatures_count_with_type('MEAT'))
            return True

        if com[0] == "ag" and len(com) == 3:
            coords = (int(com[1]), int(com[2]))
            self.creature_add(Plant(coords, self), coords)
            return True
        if com[0] == "ah" and len(com) == 3:
            coords = (int(com[1]), int(com[2]))
            self.creature_add(Herbivore(coords, self), coords)
            return True
        if com[0] == "ap" and len(com) == 3:
            coords = (int(com[1]), int(com[2]))
            self.creature_add(Predator(coords, self), coords)
            return True

        return False
