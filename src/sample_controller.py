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
    def __init__(self):
        """
        Create your fuzzy logic controllers and other objects here
        """
        chromosome = [[1, 0, 2, 0, 2, 1, 1, 0, 1, 2, 1, 0, 0, 0, 1, 1, 2, 2, 1, 0, 1, 2, 0, 0, 1, 2, 0],
                      [1, 0, 2, 0, 2, 1, 1, 0, 1, 2, 1, 0, 0, 0, 1, 1, 2, 2, 1, 0, 1, 2, 0, 0, 1, 2, 0]]

        self.A1 = HeiTerry_FIS()
        rule_base = chromosome[0]

        self.A1.add_input('relative_heading', np.arange(-180.0, 180.0, 1.0), 3)
        self.A1.add_input('distance', np.arange(0.0, 1.0, 0.1), 3)
        self.A1.add_input('closure_rate', np.arange(-1.0, 1.0, 0.1), 3)
        turn_rate_mems = [[-180.0, -180.0, 0.0], [-180.0, 0.0, 180.0], [0.0, 180.0, 180.0]]
        self.A1.add_output('turn_rate', np.arange(-180.0, 180.0, 1.0), turn_rate_mems)

        v_str = ['relative_heading', 'distance', 'closure_rate', 'turn_rate']
        mfs3 = ['poor', 'average', 'good']
        # Find a way to automate finding num rules per input earlier and for num inputs
        rules_all = []
        for wow in range(3):
            for gee in range(3):
                for zoop in range(3):
                    rules_all.append([[[v_str[0], mfs3[wow]], [v_str[1], mfs3[gee]], [v_str[2], mfs3[zoop]]],
                                      ['AND'], [v_str[3], str(rule_base[(wow * 3 * 3) + (gee * 3) + (zoop + 1) - 1])]])
        self.A1.generate_mamdani_rule(rules_all)

        self.A2 = HeiTerry_FIS()
        rule_base = chromosome[1]

        self.A2.add_input('relative_heading', np.arange(-180, 180, 1), 3)
        self.A2.add_input('distance', np.arange(0, 1, 0.1), 3)
        self.A2.add_input('closure_rate', np.arange(-1, 1, 0.1), 3)
        thrust_mems = [[-1.0, -1.0, 0], [-0.5, 0, 0.5], [0.0, 1.0, 1.0]]
        self.A2.add_output('thrust', np.arange(-4.0, 4.0, 0.1), thrust_mems)

        v_str = ['relative_heading', 'distance', 'closure_rate', 'thrust']
        mfs3 = ['poor', 'average', 'good']
        # Find a way to automate finding num rules per input earlier and for num inputs
        rules_all = []
        for wow in range(3):
            for gee in range(3):
                for zoop in range(3):
                    rules_all.append([[[v_str[0], mfs3[wow]], [v_str[1], mfs3[gee]], [v_str[2], mfs3[zoop]]],
                                      ['AND'], [v_str[3], str(rule_base[(wow * 3 * 3) + (gee * 3) + (zoop + 1) - 1])]])
        self.A2.generate_mamdani_rule(rules_all)

        # CLUSTER AVOIDANCE
        self.C1 = HeiTerry_FIS()
        rule_base = chromosome[0]

        self.C1.add_input('relative_heading', np.arange(-180.0, 180.0, 1.0), 3)
        self.C1.add_input('distance', np.arange(0.0, 1.0, 0.1), 3)
        self.C1.add_input('closure_rate', np.arange(-1.0, 1.0, 0.1), 3)
        turn_rate_mems = [[-180.0, -180.0, 0.0], [-180.0, 0.0, 180.0], [0.0, 180.0, 180.0]]
        self.C1.add_output('turn_rate', np.arange(-180.0, 180.0, 1.0), turn_rate_mems)

        v_str = ['relative_heading', 'distance', 'closure_rate', 'turn_rate']
        mfs3 = ['poor', 'average', 'good']
        # Find a way to automate finding num rules per input earlier and for num inputs
        rules_all = []
        for wow in range(3):
            for gee in range(3):
                for zoop in range(3):
                    rules_all.append([[[v_str[0], mfs3[wow]], [v_str[1], mfs3[gee]], [v_str[2], mfs3[zoop]]],
                                      ['AND'], [v_str[3], str(rule_base[(wow * 3 * 3) + (gee * 3) + (zoop + 1) - 1])]])
        self.C1.generate_mamdani_rule(rules_all)

        self.C2 = HeiTerry_FIS()
        rule_base = chromosome[1]

        self.C2.add_input('relative_heading', np.arange(-180, 180, 1), 3)
        self.C2.add_input('distance', np.arange(0, 1, 0.1), 3)
        self.C2.add_input('closure_rate', np.arange(-1, 1, 0.1), 3)
        thrust_mems = [[-1.0, -1.0, 0], [-0.5, 0, 0.5], [0.0, 1.0, 1.0]]
        self.C2.add_output('thrust', np.arange(-4.0, 4.0, 0.1), thrust_mems)

        v_str = ['relative_heading', 'distance', 'closure_rate', 'thrust']
        mfs3 = ['poor', 'average', 'good']
        # Find a way to automate finding num rules per input earlier and for num inputs
        rules_all = []
        for wow in range(3):
            for gee in range(3):
                for zoop in range(3):
                    rules_all.append([[[v_str[0], mfs3[wow]], [v_str[1], mfs3[gee]], [v_str[2], mfs3[zoop]]],
                                      ['AND'], [v_str[3], str(rule_base[(wow * 3 * 3) + (gee * 3) + (zoop + 1) - 1])]])
        self.C2.generate_mamdani_rule(rules_all)



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
        # print(centers)


        # heading is -180 to 180, distance 0 to 1, closure rate -1 to 1
        ins = [['relative_heading', 80], ['distance', 0.2], ['closure_rate', 0.6]]
        ship.turn_rate = self.A1.compute(ins, 'turn_rate')
        thrust = self.A2.compute(ins, 'thrust')
        if thrust > 0.2: ship.thrust = ship.thrust_range[1]
        elif thrust < -0.2: ship.thrust = ship.thrust_range[0]
        else: ship.thrust = 0
        ship.thrust = 0

        # print(ship.angle % 360)
        xa = 400 # asteroid x
        ya = 200 # asteroid y
        xv = ship.position[0]
        yv = ship.position[1]
        ang = np.radians(ship.angle % 360)
        """print(np.arccos((-np.sin(ang)*(xa-xv) + np.cos(ang)*(ya-yv))/((((xa-xv)**2)+((ya-yv)**2))**0.5)))
        relative_heading = np.degrees(np.arccos((-np.sin(ang)*(xa-xv) + np.cos(ang)*(ya-yv))/((((xa-xv)**2)+((ya-yv)**2))**0.5)))
        """

        dot = -np.sin(ang) * (xa-xv) + (np.cos(ang)) * (ya-yv)  # dot product
        det = -np.sin(ang) * (ya-yv) - (np.cos(ang)) * (xa-xv)  # determinant
        angle = np.degrees(np.arctan2(det, dot)) # atan2(y, x) or atan2(sin, cos)
        if angle < 0:
            angle += 360
        relative_heading = -angle+360


        ship.turn_rate = 40.0
        ship.shoot()
