from core.player.PlayerSuper import Player
# class of Circlce, child of Player

class PlayerCircle(Player):
    """
    class atribute - don't care about things that can be passed into, but can be assigned.
    It's same for all instances, so exacly like game need... It's not care about
    it is Jessica, Hello or World, because they all are playing as Circle.

    Instance of this child class is done by parent class
    """
    char = 'O'
