from core.player.PlayerSuper import Player
# class of Cross, child of Player
class PlayerCross(Player):
    # char that have PlayerCross
    char = 'X'

    def __init__(self, name):
        """
        way of instancioning child of parent class, when there are some same fields
        :param name: name of the PlayerCross
        """
        super().__init__(name)
