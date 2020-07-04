from command import Command


# пользователь нажимает на клавишу клавиатуры
class KeyDownCommand(Command):
    def event(self, button_key):
        self.world.change_player_directory(button_key, True)
