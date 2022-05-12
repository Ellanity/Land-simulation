import pygame.sprite


class Creature(pygame.sprite.Sprite):

    parameters = {
        "type_id": 0,
        "symbol_on_map": "",
        "coords": tuple(),
        "viewing_radius": 0,
        "can_change_position": False,
        "distance_it_can_overcome": 0,
        "have_health_points": False,
        "health_points": 0,
        "need_food": False,
        "type_of_food": "",
        "food_points": 0,
        "need_food_for_one_step": 0,
        "count_of_steps_without_food": 0,
        "count_of_steps_can_live_without_food": 0,
        "chance_to_survive_in_danger_situation": 0,
        "have_size": False,
        "size": 0,
        "age":  0,
        "max_age": 0,
        "can_reproduce_in_neighboring_cell": False,
        "need_a_breeding_partner": False,
        "have_gender": False,
        "gender": 0
    }

    def __init__(self, world=None):
        super().__init__()
        if world is not None:
            self.world = world
        self.image = None
        self.rect = None
        self.position_x = 0
        self.position_y = 0

    def recalculate_the_rect(self):
        self.rect = pygame.Rect(self.position_x, self.position_y, self.image.get_width(), self.image.get_height())

    def update_sprite(self):
        self.recalculate_the_rect()

    def action(self):
        pass

    def action_eating(self, creature_food=None):
        pass

    def action_movement(self):
        pass

    def action_reproduction(self, creature=None):
        pass

    def possible_for_reproduction(self):
        pass
