from typing import Tuple, Dict, Any

from fuzzy_asteroids.fuzzy_controller import ControllerBase, SpaceShip

import matplotlib.pyplot as plt
import numpy as np

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
        #### FUNCTIONS ####
        def inbetween(circle, radius, bound):
            if bound == 'xaxis':
                if 0 < circle[0] < 800:
                    return True
                elif 0 < circle[0] + radius < 800:
                    return True
                elif 0 < circle[0] - radius < 800:
                    return True
                else:
                    return False
            else:
                if 0 < circle[1] < 600:
                    return True
                elif 0 < circle[1] + radius < 600:
                    return True
                elif 0 < circle[1] - radius < 600:
                    return True
                else:
                    return False

        def pointLineDistance(L1, L2, c):
            return abs((L2[0] - L1[0])*(L1[1]-c[1]) - (L1[0] - c[0])*(L2[1]-L1[1])) / np.sqrt((L2[0]-L1[0])**2 + (L2[1]-L1[1])**2)

        def distanceFormula(p1, p2):
            return np.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))

        def inRectangle(circle):
            if circle[2] == 1:
                return circle

            c = circle[0]
            r = circle[1]
            TL = (0, 600)
            TR = (800, 600)
            BL = (0, 0)
            BR = (800, 0)

            # check top
            L1 = TL
            L2 = TR
            distance = pointLineDistance(L1, L2, c)
            if distance < r and inbetween(c, r, 'xaxis'):
                return [c, r, 1]
            # check right
            L1 = TR
            L2 = BR
            distance = pointLineDistance(L1, L2, c)
            if distance < r and inbetween(c, r, 'yaxis'):
                return [c, r, 1]
            # check bottom
            L1 = BL
            L2 = BR
            distance = pointLineDistance(L1, L2, c)
            if distance < r and inbetween(c, r,'xaxis'):
                return [c, r, 1]
            # check left
            L1 = TL
            L2 = BL
            distance = pointLineDistance(L1, L2, c)
            if distance < r and inbetween(c, r,'yaxis'):
                return [c, r, 1]

            return [c, r, 0]

        def findFISInputs(circle, ship, asteriod):
            ship_pos = circle[0]
            r = circle[1]
            ship_vel = ship.velocity
            ship_angle = ship.angle
            a = asteriod[0]
            a_vel = asteriod[1]

            distance = distanceFormula(ship_pos, a)
            m = np.degrees(np.tan(ship_angle))
            b = m * ship_pos[0] - ship_pos[1]
            L1 = ship_pos
            L2 = [ship_pos[0] + 1, m*(ship_pos[0] + 1) + b]
            plDistance = pointLineDistance(L1, L2, a)
            theta = np.degrees(np.arcsin(plDistance/distance))

            future_ship_pos = [ship_pos[0] + ship_vel[0], ship_pos[1] + ship_vel[1]]
            future_asteriod_pos = [a[0] + a_vel[0], a[1] + a_vel[1]]
            futureDistance = distanceFormula(future_ship_pos, future_asteriod_pos)
            closureRate = distance - futureDistance

            xa = a[0]  # asteroid x
            ya = a[1]  # asteroid y
            xv = ship.position[0]
            yv = ship.position[1]
            ang = np.radians(ship.angle % 360)
            """print(np.arccos((-np.sin(ang)(xa-xv) + np.cos(ang)(ya-yv))/((((xa-xv)2)+((ya-yv)2))0.5)))
            relative_heading = np.degrees(np.arccos((-np.sin(ang)(xa-xv) + np.cos(ang)(ya-yv))/((((xa-xv)2)+((ya-yv)2))0.5)))
            """

            dot = -np.sin(ang) * (xa - xv) + (np.cos(ang)) * (ya - yv)  # dot product
            det = -np.sin(ang) * (ya - yv) - (np.cos(ang)) * (xa - xv)  # determinant
            angle = np.degrees(np.arctan2(det, dot))  # atan2(y, x) or atan2(sin, cos)
            if angle < 0:
                angle += 360
            relative_heading = -angle + 360

            return [distance, relative_heading, closureRate]


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
        print(avoidanceFisInputs)

        show = True
        if show:
            # set grid positions
            ox, oy = [], []
            for i in range(0, 800):
                ox.append(i)
                oy.append(0.0)
            for i in range(0, 600):
                ox.append(0.0)
                oy.append(i)
            for i in range(0, 801):
                ox.append(i)
                oy.append(600.0)
            for i in range(0, 600):
                ox.append(800.0)
                oy.append(i)
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.plot(sx, sy, "ok")
            ychange = 600
            xchange = 800
            for c in circles:
                if c[2] == 1:
                    ax.add_patch(plt.Circle(c[0], c[1], color = 'g'))
                else:
                    ax.add_patch(plt.Circle(c[0], c[1], color='b'))

            ax.plot(ox, oy, "ok")
            for x in input_data['asteroids']:
                bx, by = x['position']
                ax.plot(bx, by, "xk")
            ax.grid(True)
            ax.axis("equal")
            plt.pause(0.03)
            fig.show()
            plt.close()
        ship.turn_rate = 180
        ship.thrust = ship.thrust_range[1]
        ship.shoot()
