from fuzzy_asteroids.fuzzy_asteroids import TrainerEnvironment

from src.sample_controller import FuzzyController
from sample_score import SampleScore
from GA.continousGeneticAlgorithm import CGA
from GA.selectionFunctions import basicSelection
from GA.crossoverFunctions import basicCrossover
from GA.mutationFunctions import basicMutation
from GA.elitismFunctions import basicElitism


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

    asteroid_ga = CGA.__init__(3,3,100,0.6,0.4,0.5,69)


    def fitnessFunction(chromosome, bounds):
        FuzzyController = chromosome
        #bounds????
        score = game.run(controller=FuzzyController, score=SampleScore())
        return score

    asteroid_ga.run(basicSelection, basicCrossover, fitnessFunction, basicMutation, basicElitism)

