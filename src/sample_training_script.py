from fuzzy_asteroids.fuzzy_asteroids import TrainerEnvironment
import numpy as np
from sample_score import SampleScore
from GA.chromosome import Chromosome
from HeiTerryController import FuzzyController
from fuzzy_asteroids.fuzzy_asteroids import AsteroidGame, FuzzyAsteroidGame
from fuzzy_asteroids.util import Scenario


if __name__ == "__main__":
    # Available settings
    settings = {
        # "frequency": 60,
        # "lives": 3,
        # "prints": False,
    }
    """chromosome = [[0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 2, 2, 1, 2, 1, 0, 0, 1, 2, 1, 0, 2, 1, 2, 1, 2, 2, 1, 0, 2, 2, 0, 0, 1, 0,
      0, 2, 1, 2, 0, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 2],
     [2, 0, 2, 0, 2, 1, 0, 2, 1, 2, 2, 0, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2, 2, 2, 0, 2, 0, 0, 1, 2, 0, 0, 1, 1, 0, 2, 0,
      1, 2, 2, 0, 2, 0, 0, 0, 2, 0, 1, 0, 2, 2, 2, 0]]"""
    chromosome = [
        [1, 0, 2, 2, 1, 0, 0, 2, 2, 0, 0, 1, 1, 1, 0, 1, 2, 2, 2, 2, 2, 2, 2, 0, 1, 1, 2, 2, 0, 0, 2, 2, 0, 1, 1, 1, 1,
         1, 1, 0, 2, 0, 2, 2, 1, 2, 0, 1, 0, 2, 0, 0, 0, 2],
        [0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 1, 1, 2, 2, 1, 0, 0, 0, 2, 2, 1, 0, 1, 1, 2, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 2, 2,
         0, 0, 2, 2, 2, 1, 1, 0, 0, 0, 2, 1, 2, 1, 2, 2, 0]]
    """chromosome = [
        [1, 0, 2, 2, 1, 0, 0, 2, 2, 0, 0, 1, 1, 1, 0, 1, 2, 2, 2, 2, 2, 2, 2, 0, 1, 1, 2, 2, 0, 0, 0, 1, 1, 1, 2, 1, 0,
         1, 1, 0, 2, 0, 2, 2, 1, 2, 0, 1, 0, 2, 0, 0, 0, 2],
        [0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 1, 1, 2, 2, 1, 0, 0, 0, 2, 2, 1, 0, 1, 0, 1, 2, 2, 1, 1, 0, 1, 1, 0, 0, 1, 2, 2,
         0, 0, 2, 2, 2, 1, 1, 0, 0, 0, 2, 1, 2, 1, 2, 2, 0]]"""
    chrom = Chromosome(chromosome)
    scenario_ast = Scenario(
        asteroid_states=[{"position": (200, 550), "angle": 84.6, "speed": 25},
                         {"position": (600, 500), "angle": 169.0, "speed": 40},
                         {"position": (700, 200), "angle": 46.8, "speed": 30},
                         {"position": (300, 100), "angle": 135.0, "speed": 50},
                         {"position": (100, 400), "angle": -26.0, "speed": 42},
                         {"position": (500, 200), "angle": -96.0, "speed": 25},
                         ]
    )
    # To use the controller within the context of a training solution
    # It is important to not create a new instance of the environment everytime
    game = FuzzyAsteroidGame(settings=settings)
    score = game.run(controller=FuzzyController(chrom), score=SampleScore(), scenario=scenario_ast)
    print(score.time)

