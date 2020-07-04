import pytest
from units import *
from player import Player
from help_structures import ObjectCollision


def test_unit_load():
    player = Player()
    archer_creator: UnitCreator = ArcherCreator()
    swordsman_creator: UnitCreator = SwordsmanCreator()
    spear_creator: UnitCreator = SpearCreator()
    arbalester_creator: UnitCreator = ArbalesterCreator()

    for i in range(1000):
        archer_creator.create_unit((0, i * 60), player)
        swordsman_creator.create_unit((60, i * 60), player)
        spear_creator.create_unit((120, i * 60), player)
        arbalester_creator.create_unit((180, i * 60), player)


def test_unit_collision():
    with pytest.raises(ObjectCollision):
        player = Player()
        archer_creator: UnitCreator = ArcherCreator()

        archer_creator.create_unit((0, 0), player)
        archer_creator.create_unit((0, 0), player)
