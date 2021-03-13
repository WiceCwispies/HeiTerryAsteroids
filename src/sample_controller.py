from typing import Tuple, Dict, Any
import numpy as np
from fuzzy_asteroids.fuzzy_controller import ControllerBase, SpaceShip
from fuzzy_c_means import c_means


class FuzzyController(ControllerBase):
    """
    Class to be used by UC Fuzzy Challenge competitors to create a fuzzy logic controller
    for the Asteroid Smasher game.

    Note: Your fuzzy controller class can be called anything, but must inherit from the
    the ``ControllerBase`` class (imported above)

    Users must define the following:
    1. __init__()
    2. actions(self, ship: SpaceShip, input_data: Dict[str, Tuple])

    By defining these interfaces, this class will work correctly
    """
    def __init__(self):
        """
        Create your fuzzy logic controllers and other objects here
        """
        pass

    def actions(self, ship: SpaceShip, input_data: Dict[str, Tuple]) -> None:
        """
        Compute control actions of the ship. Perform all command actions via the ``ship``
        argument. This class acts as an intermediary between the controller and the environment.

        The environment looks for this function when calculating control actions for the Ship sprite.

        :param ship: Object to use when controlling the SpaceShip
        :param input_data: Input data which describes the current state of the environment
        """

        ## Calculate center of 3 clusters
        num_asteroids = len(input_data['asteroids'])
        X = np.ndarray((num_asteroids,2))
        for e in range(num_asteroids):
            X[e] = [input_data['asteroids'][e]['position'][0], input_data['asteroids'][e]['position'][1]]
        try:
            centers = c_means(X, nodes=3)
        except:
            centers = None
        print(centers)
        del X



        # ship.turn_rate = 180.0
        ship.thrust = ship.thrust_range[1]
        ship.shoot()
