from typing import Tuple, Dict, Any
import numpy as np
from fuzzy_asteroids.fuzzy_controller import ControllerBase, SpaceShip
from fuzzy_tools.fuzzy_c_means import c_means
from fuzzy_tools.CustomFIS import HeiTerry_FIS


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
    def __init__(self, chromosome):
        """
        Create your fuzzy logic controllers and other objects here
        """
        F1 = HeiTerry_FIS()
        rule_base = chromosome[0]

        F1.add_input('relative_heading', np.arange(-180, 180, 1), 3)
        F1.add_input('distance', np.arange(0, 1, 0.1), 3)
        F1.add_input('closure_rate', np.arange(-1, 1, 0.1), 3)
        F1.add_output('turn_rate', np.arange(-180, 180, 0.1), 3)

        v_str = ['relative_heading', 'distance', 'closure_rate', 'turn_rate']
        mfs3 = ['poor', 'average', 'good']
        # Find a way to automate finding num rules per input earlier and for num inputs
        rules_all = []
        for wow in range(3):
            for gee in range(3):
                for zoop in range(3):
                    rules_all.append([[[v_str[0], mfs3[wow]], [v_str[1], mfs3[gee]], [v_str[2], mfs3[zoop]]],
                                      ['AND'], [v_str[3], str(rule_base[(wow * 3 * 3) + (gee * 3) + (zoop + 1)])]])
        F1.generate_mamdani_rule(rules_all)
        self.F1 = F1

        F2 = HeiTerry_FIS()
        rule_base = chromosome[1]

        F2.add_input('relative_heading', np.arange(-180, 180, 1), 3)
        F2.add_input('distance', np.arange(0, 1, 0.1), 3)
        F2.add_input('closure_rate', np.arange(-1, 1, 0.1), 3)
        F2.add_output('velocity', np.arange(-1.0, 1.0, 0.1), 3)

        v_str = ['relative_heading', 'distance', 'closure_rate', 'velocity']
        mfs3 = ['poor', 'average', 'good']
        # Find a way to automate finding num rules per input earlier and for num inputs
        rules_all = []
        for wow in range(3):
            for gee in range(3):
                for zoop in range(3):
                    rules_all.append([[[v_str[0], mfs3[wow]], [v_str[1], mfs3[gee]], [v_str[2], mfs3[zoop]]],
                                      ['AND'], [v_str[3], str(rule_base[(wow * 3 * 3) + (gee * 3) + (zoop + 1)])]])
        F2.generate_mamdani_rule(rules_all)
        self.F2 = F2

        pass

    def actions(self, ship: SpaceShip, input_data: Dict[str, Tuple]) -> None:
        """
        Compute control actions of the ship. Perform all command actions via the ``ship``
        argument. This class acts as an intermediary between the controller and the environment.

        The environment looks for this function when calculating control actions for the Ship sprite.

        :param ship: Object to use when controlling the SpaceShip
        :param input_data: Input data which describes the current state of the environment
        """
        print(ship.velocity)
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
        # could probably delete line 69

        # heading is -180 to 180, distance 0 to 1, closure rate -1 to 1
        ins = [['relative_heading', 0], ['distance', 0], ['closure_rate', 0]]
        ship.turn_rate = self.F1.compute(ins, 'turn_rate')
        commanded_velocity = self.F2.compute(ins, 'velocity')


        # ship.turn_rate = 180.0
        ship.thrust = ship.thrust_range[1]
        ship.shoot()
