import os
import random
from abc import ABC, abstractmethod
import pygame
import squad
import constants
import costs
from help_structures import Direction, ObjectCollision


class Unit(pygame.sprite.Sprite, squad.Squad):  # класс юнита
    def __init__(self, pos, image_files, group):
        pygame.sprite.Sprite.__init__(self)
        squad.Squad.__init__(self)
        image_names = []
        for i in range(len(image_files)):
            image_names.append(os.path.join(os.getcwd(), 'unit_images',
                                            image_files[i]))

        # картинки юнитов
        self.left_images = [pygame.image.load(image_names[0]),
                            pygame.image.load(image_names[4])]
        self.right_images = [pygame.image.load(image_names[1]),
                             pygame.image.load(image_names[5])]
        self.front_images = [pygame.image.load(image_names[2]),
                             pygame.image.load(image_names[6])]
        self.back_images = [pygame.image.load(image_names[3]),
                            pygame.image.load(image_names[7])]

        self.current_state = 0
        self.namespace = 5.0
        self.set_image(self.front_images[0])
        self.rect = self.image.get_rect(center=pos)

        if pygame.sprite.spritecollideany(self, group) is not None:
            raise ObjectCollision

        self.add(group)
        self.speed = 3
        self.power = 4.0
        self.attack_distance = 1.2
        self.health = 100.0
        self.max_health = 100.0
        self.goal = (self.rect.center[0], self.rect.center[1])
        self.direction = Direction.NONE

    def set_image(self, image):  # изменение картинки юнита
        self.image = image
        self.image.set_colorkey(constants.TRANSPARENT)
        self.image = pygame.transform.scale(self.image, (constants.UNIT_SIZE,
                                                         constants.UNIT_SIZE))

    def action(self, enemy_player):
        if self.attack(enemy_player):
            return

        nearby_enemies = self.get_nearby_enemies(enemy_player)
        if nearby_enemies is not None:
            for enemy in nearby_enemies:
                self.set_goal(enemy.rect.center)
                break

        self.increase_health(0.01)
        self.move()

    # восстановление здоровья юнита
    def increase_health(self, additional_health):
        self.health += additional_health
        self.health = min(self.health, self.max_health)

    def decrease_health(self, damage):  # нанесение урона юниту
        self.health -= damage
        if self.health <= 0.0:
            self.die()

    def get_image(self):  # текущая картинка юнита
        if self.direction == Direction.LEFT:
            return self.left_image
        if self.direction == Direction.RIGHT:
            return self.right_image
        # если юнит повёрнут вперёд, то возвращаем картинку спины
        if self.direction == Direction.FRONT:
            return self.back_image
        return self.front_image

    def move(self):  # передвижение юнита
        if (self.rect.x + self.rect.y) % (self.speed * 8) < self.speed * 4:
            self.current_state = 0
        else:
            self.current_state = 1

        # проверка на достижение цели
        if self.rect.center[0] < self.goal[0] - 2:
            self.direction = Direction.RIGHT
        elif self.rect.center[0] > self.goal[0] + 2:
            self.direction = Direction.LEFT
        elif self.rect.center[1] < self.goal[1] - 2:
            self.direction = Direction.BACK
        elif self.rect.center[1] > self.goal[1] + 2:
            self.direction = Direction.FRONT
        else:
            self.direction = Direction.NONE

        if random.randint(0, 1) == 0:
            if self.rect.center[1] < self.goal[1] - 2:
                self.direction = Direction.BACK
            elif self.rect.center[1] > self.goal[1] + 2:
                self.direction = Direction.FRONT

        # перемещение юнита
        if self.direction == Direction.LEFT:
            self.rect.x -= self.speed
            self.set_image(self.left_images[self.current_state])
        elif self.direction == Direction.RIGHT:
            self.rect.x += self.speed
            self.set_image(self.right_images[self.current_state])
        elif self.direction == Direction.FRONT:
            self.rect.y -= self.speed
            self.set_image(self.back_images[self.current_state])
        elif self.direction == Direction.BACK:
            self.rect.y += self.speed
            self.set_image(self.front_images[self.current_state])

    # получение вражеских юнитов и зданий поблизости
    def get_nearby_enemies(self, enemy_player):
        collided = pygame.sprite.collide_circle_ratio(self.namespace)
        enemy_units = pygame.sprite.spritecollide(self,
                                                  enemy_player.unit_group,
                                                  False,
                                                  collided=collided)
        collided = pygame.sprite.collide_circle_ratio(self.namespace / 3)
        new_enemy = pygame.sprite.spritecollide(self,
                                                enemy_player.building_group,
                                                False,
                                                collided=collided)
        enemy_units.extend(new_enemy)
        return enemy_units

    def attack(self, enemy_player):  # атака юнитов и зданий врага
        collided = pygame.sprite.collide_circle_ratio(self.attack_distance)
        enemy_units = pygame.sprite.spritecollide(self,
                                                  enemy_player.building_group,
                                                  False)
        enemy_units.extend(pygame.sprite.spritecollide(self,
                                                       enemy_player.unit_group,
                                                       False,
                                                       collided=collided))
        if len(enemy_units) == 0:
            return False
        damage = self.power / len(enemy_units)
        for enemy in enemy_units:
            enemy.decrease_health(damage)
        return True

    def set_goal(self, goal):  # установка цели
        self.goal = goal

    def die(self):  # уничтожение юнита
        self.kill()


class Archer(Unit):  # класс лучника
    def __init__(self, pos, group):
        images = ['knt1_lf1.gif', 'knt1_rt1.gif', 'knt1_fr1.gif',
                  'knt1_bk1.gif',
                  'knt1_lf2.gif', 'knt1_rt2.gif', 'knt1_fr2.gif',
                  'knt1_bk2.gif']
        super().__init__(pos, images, group)
        self.attack_distance = 2.5
        self.power = 0.7


class Swordsman(Unit):  # класс мечника
    def __init__(self, pos, group):
        images = ['avt2_lf1.gif', 'avt2_rt1.gif', 'avt2_fr1.gif',
                  'avt2_bk1.gif',
                  'avt2_lf2.gif', 'avt2_rt2.gif', 'avt2_fr2.gif',
                  'avt2_bk2.gif']
        super().__init__(pos, images, group)


class Spear(Unit):  # класс копейщика
    def __init__(self, pos, group):
        images = ['ftr3_lf1.gif', 'ftr3_rt1.gif', 'ftr3_fr1.gif',
                  'ftr3_bk1.gif',
                  'ftr3_lf2.gif', 'ftr3_rt2.gif', 'ftr3_fr2.gif',
                  'ftr3_bk2.gif']
        super().__init__(pos, images, group)
        self.power = 5.0


class Arbalester(Unit):  # класс арбалетчика
    def __init__(self, pos, group):
        images = ['pdn1_lf1.gif', 'pdn1_rt1.gif', 'pdn1_fr1.gif',
                  'pdn1_bk1.gif',
                  'pdn1_lf2.gif', 'pdn1_rt2.gif', 'pdn1_fr2.gif',
                  'pdn1_bk2.gif']
        super().__init__(pos, images, group)
        self.attack_distance = 3.0
        self.power = 1.0


class Settler(Unit):  # класс поселенца
    def __init__(self, pos, group):
        images = ['man1_lf1.gif', 'man1_rt1.gif', 'man1_fr1.gif',
                  'man1_bk1.gif',
                  'man1_lf2.gif', 'man1_rt2.gif', 'man1_fr2.gif',
                  'man1_bk2.gif']
        super().__init__(pos, images, group)
        self.health = 50.0
        self.power = 1.0


class UnitCreator(ABC):  # фабричный метод
    def __init__(self):
        self.speed = 1

    @abstractmethod
    def create_unit(self, pos, player) -> Unit:
        pass

    def increase_creation_speed(self):
        self.speed += 1

    def decrease_creation_speed(self):
        self.speed -= 1


class ArcherCreator(UnitCreator):
    def create_unit(self, pos, player) -> Archer:
        try:
            if player.resources.check_values(*costs.ARCHER_COST):
                unit = Archer(pos, player.unit_group)
                player.resources.change_values(*costs.ARCHER_COST)
                return unit
        except ObjectCollision:
            raise ObjectCollision
        return None


class SwordsmanCreator(UnitCreator):
    def create_unit(self, pos, player) -> Swordsman:
        try:
            if player.resources.check_values(*costs.SWORDSMAN_COST):
                unit = Swordsman(pos, player.unit_group)
                player.resources.change_values(*costs.SWORDSMAN_COST)
                return unit
        except ObjectCollision:
            raise ObjectCollision
        return None


class SpearCreator(UnitCreator):
    def create_unit(self, pos, player) -> Spear:
        try:
            if player.resources.check_values(*costs.SPEAR_COST):
                unit = Spear(pos, player.unit_group)
                player.resources.change_values(*costs.SPEAR_COST)
                return unit
        except ObjectCollision:
            raise ObjectCollision
        return None


class ArbalesterCreator(UnitCreator):
    def create_unit(self, pos, player) -> Arbalester:
        try:
            if player.resources.check_values(*costs.ARBALESTER_COST):
                unit = Arbalester(pos, player.unit_group)
                player.resources.change_values(*costs.ARBALESTER_COST)
                return unit
        except ObjectCollision:
            raise ObjectCollision
        return None


class SettlerCreator(UnitCreator):
    def create_unit(self, pos, player) -> Settler:
        try:
            if player.resources.check_values(*costs.SETTLER_COST):
                unit = Settler(pos, player.unit_group)
                player.resources.change_values(*costs.SETTLER_COST)
                return unit
        except ObjectCollision:
            raise ObjectCollision
        return None
