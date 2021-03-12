import numpy as np

class Chromosome:
    def __init__(self, string):
        self.string = string
        self.fitness = 0
        self.normFitness = 0
        
    def updateString(self,string):
        self.string = string
    
    def updateFitness(self,fitness):
        self.fitness = fitness

    def updateNormFitness(self,normFitness):
        self.normFitness = normFitness

    def __str__(self):
        rstr = "string: " + str(self.string) + "\n" + "fitness: " + str(self.fitness)
        return rstr
        
    def getString(self):
        return self.string

    def getFitness(self):
        return self.fitness
    
    def getNormFitness(self):
        return self.normFitness

class Population:
    def __init__(self):
        self.population = []

    def addChromosome(self,chrom):
        self.population.append(chrom)
    
    def __str__(self):
        for chrom in self.population:
            print(chrom,"\n")
        return "total number of Chromosomes: " + str(len(self.population))
    
    def chromosome(self,number):
        return self.population[number]
    


# Test
if __name__ == "__main__":
    chrom = Chromosome(np.array([1,2,3,4,5,6]))
    chrom2 = Chromosome(np.array([1,2,3,4,5,6]))
    chrom.updateFitness(8)
    chrom2.updateFitness(4)
    population = [chrom,chrom2]
    print(list(map(lambda a: a.getFitness(),population)))

    