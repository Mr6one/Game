from command import Command


# пользователь отпускает клавишу клавиатуры
class KeyUpCommand(Command):
    def event(self, button_key):
        self.world.change_player_directory(button_key, False)
