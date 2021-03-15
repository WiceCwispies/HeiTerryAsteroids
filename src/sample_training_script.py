from fuzzy_asteroids.fuzzy_asteroids import TrainerEnvironment
import numpy as np
from src.sample_controller import FuzzyController
from sample_score import SampleScore
from GA.continousGeneticAlgorithm import CGA
from GA.selectionFunctions import basicSelection
from GA.crossoverFunctions import basicCrossover
from GA.mutationFunctions import basicMutation
from GA.elitismFunctions import basicElitism
from fuzzy_tools.CustomFIS import HeiTerry_FIS

if __name__ == "__main__":
    # Available settings
    settings = {
        # "frequency": 60,
        # "lives": 3,
        # "prints": False,
    }

    # To use the controller within the context of a training solution
    # It is important to not create a new instance of the environment everytime
    game = TrainerEnvironment(settings=settings)

    """for i in range(1000):
        # Call run() on an instance of the TrainerEnvironment
        # This function automatically manages cleanup"""
    for i in range(100):
        score = game.run(controller=FuzzyController(), score=SampleScore())
        print(score)

