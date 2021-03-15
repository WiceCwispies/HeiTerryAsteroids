import numpy as np
import matplotlib.pyplot as plt
import random
from fuzzy_asteroids.fuzzy_asteroids import TrainerEnvironment
import sys
sys.path.append("./GA")
from fitnessFunction2 import *
from chromosome import *
from initializationFunctions import *
from selectionFunctions import *
from crossoverFunctions import *
from mutationFunctions import *
from elitismFunctions import *
from continousGeneticAlgorithm import CGA

settings = {
    "real_time_multiplier": 2,
}

game = TrainerEnvironment(settings=settings)

myCGA = CGA(NumberOfChrom = 30,
          NumbofGenes = 7,
          maxGen = 500,
          PC = 0.75,
          PM = 0.20,
          Er = 0.15,
          bounds = game)

myCGA.initialization(asteriodInitialize)

myCGA.run(selectionFunction = basicSelection,
        crossoverFunction = asteriodCrossoverRand1Point,
        mutationFunction = asteriodMutation,
        fitnessFunction = AsteriodFitness,
        elitismFunction = basicElitism)

best = myCGA.getBestChromosome()

print("\n\n",best)