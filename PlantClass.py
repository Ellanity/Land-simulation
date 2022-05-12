import random
from CreatureClass import Creature


class Plant(Creature):

    def __init__(self, coords, world):
        super().__init__(world)
        self.parameters = {
            "type_id": 1,
            # "symbol_on_map": "G",
            "symbol_on_map": "▒",
            "coords": coords,
            "viewing_radius": 0,
            "can_change_position": False,
            "distance_it_can_overcome": 0,
            "have_health_points": True,
            "health_points": 1000,
            "need_food": False,
            "type_of_food": "NO",
            "food_points": 0,
            "need_food_for_one_step": 0,
            "count_of_steps_without_food": 0,
            "count_of_steps_can_live_without_food": 0,
            "chance_to_survive_in_danger_situation": 0,
            "have_size": False,
            "size": 0,
            "age": 0,
            "max_age": 100,
            "can_reproduce_in_neighboring_cell": True,
            "need_a_breeding_partner": False,
            "have_gender": False,
            "count_of_child": 0,
            "gender": 0
        }

    def action(self):
        if self.possible_for_reproduction() is True:
            return "REPRODUCTION"
        else:
            self.parameters["health_points"] += (random.randint(-6, 1) * 20)
            if self.parameters["health_points"] > 100:
                self.parameters["health_points"] = 100
            if self.parameters["health_points"] <= 0:
                return "DIE"
            return "NO"

    def action_reproduction(self, creature=None):
        self.parameters["count_of_child"] += 1
        return Plant(self.parameters["coords"], self.world)

    def possible_for_reproduction(self):
        if self.parameters["health_points"] == 100:
            return True
        else:
            return False
