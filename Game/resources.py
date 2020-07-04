from resources_event_manager import ResourcesEventManager
from resources_events import ResourceEvent


class Resources:
    def __init__(self, gold=1200, wood=1000, food=1400):
        self.manager = ResourcesEventManager()
        self.wood = wood
        self.food = food
        self.gold = gold

    # проверка достаточности кол-ва ресурсов
    def check_values(self, gold_value=0, wood_value=0, food_value=0):
        if self.gold < -gold_value or self.wood < -wood_value or \
                self.food < -food_value:
            return False
        return True

    # изменение кол-ва ресурсов
    def change_values(self, gold_value=0, wood_value=0, food_value=0):
        self.gold += gold_value
        self.manager.notify(ResourceEvent.NEW_GOLD_VALUE, self.gold)
        self.wood += wood_value
        self.manager.notify(ResourceEvent.NEW_WOOD_VALUE, self.wood)
        self.food += food_value
        self.manager.notify(ResourceEvent.NEW_FOOD_VALUE, self.food)

    def get_values(self):
        self.manager.notify(ResourceEvent.NEW_GOLD_VALUE, self.gold)
        self.manager.notify(ResourceEvent.NEW_WOOD_VALUE, self.wood)
        self.manager.notify(ResourceEvent.NEW_FOOD_VALUE, self.food)
        return tuple((self.gold, self.wood, self.food))

    @staticmethod
    def get_resources_names():
        return tuple(("Gold", "Wood", "Food"))
