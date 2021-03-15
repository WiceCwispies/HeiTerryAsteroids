from typing import Tuple, Dict, Any
import numpy as np
from fuzzy_asteroids.fuzzy_controller import ControllerBase, SpaceShip
from fuzzy_tools.fuzzy_c_means import c_means
from fuzzy_tools.CustomFIS import HeiTerry_FIS
from fuzzy_tools.circle_functions import findFISInputs, distanceFormula, inRectangle, findClusterInputs


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
        """chromosome = [[1, 0, 2, 0, 2, 1, 1, 0, 1, 2, 1, 0, 0, 0, 1, 1, 2, 2, 1, 0, 1, 2, 0, 0, 1, 2, 0,
                       1, 0, 2, 0, 2, 1, 1, 0, 1, 2, 1, 0, 0, 0, 1, 1, 2, 2, 1, 0, 1, 2, 0, 0, 1, 2, 0],
                      [1, 0, 2, 0, 2, 1, 1, 0, 1, 2, 1, 0, 0, 0, 1, 1, 2, 2, 1, 0, 1, 2, 0, 0, 1, 2, 0,
                       1, 0, 2, 0, 2, 1, 1, 0, 1, 2, 1, 0, 0, 0, 1, 1, 2, 2, 1, 0, 1, 2, 0, 0, 1, 2, 0]]"""

        self.A1 = HeiTerry_FIS()
        rule_base = chromosome[0]

        self.A1.add_input('relative_heading', np.arange(-180.0, 180.0, 1.0), 3)
        self.A1.add_input('distance', np.arange(0.0, 1.0, 0.1), 3)
        self.A1.add_input('closure_rate', np.arange(-1.0, 1.0, 0.1), 3)
        turn_rate_mems = [[-180.0, -180.0, 0.0], [-180.0, 0.0, 180.0], [0.0, 180.0, 180.0]]
        thrust_mems = [[-1.0, -1.0, 0], [-0.5, 0, 0.5], [0.0, 1.0, 1.0]]
        self.A1.add_output('turn_rate', np.arange(-180.0, 180.0, 1.0), turn_rate_mems)
        self.A1.add_output('thrust', np.arange(-4.0, 4.0, 0.1), thrust_mems)

        v_str = ['relative_heading', 'distance', 'closure_rate', 'turn_rate', 'thrust']
        mfs3 = ['0', '1', '2']
        # Find a way to automate finding num rules per input earlier and for num inputs
        rules_all = []
        for wow in range(3):
            for gee in range(3):
                for zoop in range(3):
                    rules_all.append([[[v_str[0], mfs3[wow]], [v_str[1], mfs3[gee]], [v_str[2], mfs3[zoop]]],
                                      ['AND'], [[v_str[3], str(rule_base[(wow * 3 * 3) + (gee * 3) + zoop])],
                                                [v_str[4], str(rule_base[27 + (wow * 3 * 3) + (gee * 3) + zoop])]]])

        self.A1.generate_mamdani_rule(rules_all)

        # CLUSTER AVOIDANCE
        self.C1 = HeiTerry_FIS()
        rule_base = chromosome[1]

        self.C1.add_input('relative_heading', np.arange(-180.0, 180.0, 1.0), 3)
        self.C1.add_input('distance', np.arange(0.0, 1.0, 0.1), 3)
        self.C1.add_input('closure_rate', np.arange(-1.0, 1.0, 0.1), 3)
        turn_rate_mems = [[-180.0, -180.0, 0.0], [-180.0, 0.0, 180.0], [0.0, 180.0, 180.0]]
        thrust_mems = [[-1.0, -1.0, 0], [-0.5, 0, 0.5], [0.0, 1.0, 1.0]]
        self.C1.add_output('turn_rate', np.arange(-180.0, 180.0, 1.0), turn_rate_mems)
        self.C1.add_output('thrust', np.arange(-4.0, 4.0, 0.1), thrust_mems)

        v_str = ['relative_heading', 'distance', 'closure_rate', 'turn_rate', 'thrust']
        mfs3 = ['0', '1', '2']
        # Find a way to automate finding num rules per input earlier and for num inputs
        rules_all = []
        for wow in range(3):
            for gee in range(3):
                for zoop in range(3):
                    rules_all.append([[[v_str[0], mfs3[wow]], [v_str[1], mfs3[gee]], [v_str[2], mfs3[zoop]]],
                                      ['AND'], [[v_str[3], str(rule_base[(wow * 3 * 3) + (gee * 3) + zoop])],
                                                [v_str[4], str(rule_base[27 + (wow * 3 * 3) + (gee * 3) + zoop])]]])

        self.C1.generate_mamdani_rule(rules_all)

    def actions(self, ship: SpaceShip, input_data: Dict[str, Tuple]) -> None:
        """
        Compute control actions of the ship. Perform all command actions via the ``ship``
        argument. This class acts as an intermediary between the controller and the environment.

        The environment looks for this function when calculating control actions for the Ship sprite.

        :param ship: Object to use when controlling the SpaceShip
        :param input_data: Input data which describes the current state of the environment
        """

        #### MAIN ####
        # ship positions
        x, y = ship.position
        sx = x  # [m]
        sy = y  # [m]

        # asteriod positions
        asteriods = []
        for x in input_data['asteroids']:
            asteriods.append([x['position'], x['velocity']])

        circles = []
        ychange = 600
        xchange = 800
        radius = 150
        circles.append([(sx, sy), radius, 1])
        circles.append([(sx + xchange, sy), radius, 0])
        circles.append([(sx, sy + ychange), radius, 0])
        circles.append([(sx + xchange, sy + ychange), radius, 0])
        circles.append([(sx - xchange, sy + ychange), radius, 0])
        circles.append([(sx - xchange, sy), radius, 0])
        circles.append([(sx - xchange, sy - ychange), radius, 0])
        circles.append([(sx, sy - ychange), radius, 0])
        circles.append([(sx + xchange, sy - ychange), radius, 0])

        circles = list(map(lambda a: inRectangle(a), circles))

        avoidanceFisInputs = []
        for c in circles:
            if c[2] == 1:
                for asteriod in asteriods:
                    if distanceFormula(asteriod[0], c[0]) < c[1]:
                        avoidanceFisInputs.append(findFISInputs(c, ship, asteriod))
        #distance, relative heading, closure rate

        num_asteroids = len(input_data['asteroids'])
        X = np.ndarray((num_asteroids, 2))
        for e in range(num_asteroids):
            X[e] = [input_data['asteroids'][e]['position'][0], input_data['asteroids'][e]['position'][1]]
        try:
            centers = c_means(X, nodes=3)
        except:
            centers = None

        clusterFisInputs = []
        for each_center in centers:
            clusterFisInputs.append(findClusterInputs(ship, each_center))
        # distance, relative heading, closure rate

        turn_each = []
        thrust_each = []
        for each_asteroid in avoidanceFisInputs:
            ins = [['relative_heading', each_asteroid[1]], ['distance', each_asteroid[0]], ['closure_rate', each_asteroid[2]]]
            [turn1, thrust1] = self.A1.compute2Plus(ins, ['turn_rate', 'thrust'])
            turn_each.append(turn1)
            thrust_each.append(thrust1)

        for each_cluster in clusterFisInputs:
            ins = [['relative_heading', each_cluster[1]], ['distance', each_cluster[0]], ['closure_rate', each_cluster[2]]]
            [turn2, thrust2] = self.C1.compute2Plus(ins, ['turn_rate', 'thrust'])
            turn_each.append(turn2)
            thrust_each.append(thrust2)

        ship.turn_rate = np.average(turn_each)

        thrust = np.average(thrust_each)
        if thrust > 0.2: ship.thrust = ship.thrust_range[1]
        elif thrust < -0.2: ship.thrust = ship.thrust_range[0]
        else: ship.thrust = 0

        ship.shoot()
