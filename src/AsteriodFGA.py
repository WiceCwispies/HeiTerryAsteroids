import numpy as np
import matplotlib.pyplot as plt
import random
from fuzzy_asteroids.fuzzy_asteroids import TrainerEnvironment
# from GA.fitnessFunction2 import *
from GA.chromosome import *
from GA.initializationFunctions import *
from GA.selectionFunctions import *
from GA.crossoverFunctions import *
from GA.mutationFunctions import *
from GA.elitismFunctions import *
from GA.continousGeneticAlgorithm import CGA
from HeiTerryController import FuzzyController
from sample_score import SampleScore
from shapely import speedups
from GA.chromosome import *
speedups.disable()

settings = {
    "real_time_multiplier": 2,
}
chrom = [[1, 0, 2, 0, 2, 1, 1, 0, 1, 2, 1, 0, 0, 0, 1, 1, 2, 2, 1, 0, 1, 2, 0, 0, 1, 2, 0,
            1, 0, 2, 0, 2, 1, 1, 0, 1, 2, 1, 0, 0, 0, 1, 1, 2, 2, 1, 0, 1, 2, 0, 0, 1, 2, 0],
          [1, 0, 2, 0, 2, 1, 1, 0, 1, 2, 1, 0, 0, 0, 1, 1, 2, 2, 1, 0, 1, 2, 0, 0, 1, 2, 0,
           1, 0, 2, 0, 2, 1, 1, 0, 1, 2, 1, 0, 0, 0, 1, 1, 2, 2, 1, 0, 1, 2, 0, 0, 1, 2, 0]]
chrom = Chromosome(chrom)
game = TrainerEnvironment(settings=settings)
score = game.run(controller=FuzzyController(chrom), score=SampleScore())

"""
myCGA = CGA(NumberOfChrom = 1,
          NumbofGenes = 1,
          maxGen = 1,
          PC = 0.75,
          PM = 0.20,
          Er = 0.15,
          bounds = game)

myCGA.initialization(asteriodInitialize)

def AsteriodFitness(chrom, bounds):
    # settings = {
    #     # "graphics_on": True,
    #     # "sound_on": False,
    #     # "frequency": 60,
    #     "real_time_multiplier": 2,
    #     # "lives": 3,
    #     # "prints": True,
    #     # "allow_key_presses": False
    # }
    #
    # #game = TrainerEnvironment(settings=settings)
    score = game.run(controller=FuzzyController(chrom), score=SampleScore())
    return score.fitness

myCGA.run(selectionFunction = basicSelection,
        crossoverFunction = AsteriodsCrossoverRand1Point,
        mutationFunction = asteriodMutation,
        fitnessFunction = AsteriodFitness,
        elitismFunction = basicElitism)

best = myCGA.getBestChromosome()

print("\n\n",best)"""