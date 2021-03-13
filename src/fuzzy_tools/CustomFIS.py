import numpy as np
import random

def createUniformInput(numbInputs,numbMems,lbs,ubs,show):
        inputMatrix = np.array([[]]*numbInputs)
        inputMatrix = inputMatrix.tolist()
        for n in range(numbInputs):
            # translate lower bound to zero
            translb = lbs[n] - lbs[n]
            
            # translate upper bound respectively
            transup = ubs[n] - lbs[n]
            
            # divide up range evenly 
            div = transup/(numbMems-1)
                        
            # create membership functions
            for i,mem in enumerate(range(numbMems)):
                a = (div*i) - div + lbs[n] + random.uniform(-1,1)
                b = div*i + lbs[n] + random.uniform(-1,1)
                c = (div*i) + div + lbs[n] + random.uniform(-1,1)
                inputMatrix[n].append([a,b,c])  
        if show:
            plotMembershipFunctions(inputMatrix[0])
            plt.show()
            plotMembershipFunctions(inputMatrix[1])
            plt.show()
            plotMembershipFunctions(inputMatrix[2])
        return inputMatrix

def determineMembership(x, bounds):
    # define bounds
    le = bounds[0]
    ce = bounds[1]
    re = bounds[2]

    # determine intersection value
    if x >= le and x < ce:
        mu = (x - le)/(ce - le)
    elif x >= ce and x <= re:
        mu = (re - x)/(re - ce)
    else:
        mu = 0

    # return mu
    return mu

def findCentroid(p):
    x = round((p[0] + p[1] + p[2]) / 3, 2)
    return x

class antecedent():
    def __init__(self, name, in_range):
        self.name = name
        self.range = in_range
        self.mfs = {}
        self.memValues = {}

    def autoGenerate(self, numb):
        mems = createUniformInput(1, numb, [self.range[0]], [self.range[-1]], False)[0]
        if numb == 3:
            classifires = ['poor', 'average', 'good']
        
        for i,mf in enumerate(classifires):
            self.mfs[mf] = mems[i]

    def inputMembershipsFunctions(self, bounds, classifiers=None):
        '''
        Takes only triangler membership functions for now.
        '''
        lenBounds = len(bounds)
        if lenBounds == 3:
            classifiers = ['0','1','2']
        
        for i,mf in enumerate(classifiers):
            self.mfs[mf] = bounds[i]
    
    def calcMemValue(self, name, value):
        for x in self.mfs.items():
            name = x[0]
            bounds = x[1]
            memVal = determineMembership(value, bounds)
            self.memValues[name] = memVal
    
    def __str__(self):
        return str(self.mfs)

class Consequent():
    def __init__(self, name, in_range):
        self.name = name
        self.range = in_range
        self.mfs = {}

    def autoGenerate(self, numb):
        mems = createUniformInput(1, numb, [self.range[0]], [self.range[-1]], False)[0]
        if numb == 3:
            classifires = ['poor', 'average', 'good']
        
        for i,mf in enumerate(classifires):
            self.mfs[mf] = mems[i]

    def inputMembershipsFunctions(self, bounds, classifiers=None):
        '''
        Takes only triangler membership functions for now.
        '''
        lenBounds = len(bounds)
        if lenBounds == 3:
            classifiers = ['0','1','2']
        
        for i,mf in enumerate(classifiers):
            self.mfs[mf] = bounds[i]
    
    def __str__(self):
        return str(self.mfs)

class HeiTerry_FIS():
    def __init__(self):
        self.inputs = {}
        self.outputs = {}
        self.ruleBase = []

    def add_input(self, name, input_range, mems):
        if type(mems) == int:
            inputMem = antecedent(name, input_range)
            inputMem.autoGenerate(mems)
            self.inputs[name] = inputMem
        else:
            inputMem = antecedent(name, input_range)
            inputMem.inputMembershipsFunctions(mems)
            self.inputs[name] = inputMem

    def add_output(self, name, input_range, mems):
        if type(mems) == int:
            outputMem = antecedent(name, input_range)
            outputMem.autoGenerate(mems)
            self.outputs[name] = outputMem

        else:
            outputMem = antecedent(name, input_range)
            outputMem.inputMembershipsFunctions(mems)
            self.outputs[name] = outputMem

    def generate_mamdani_rule(self, ruleBase):
        self.ruleBase = ruleBase

    def compute(self, inputs, outputName):
        for i in inputs:
            self.inputs[i[0]].calcMemValue(i[0], i[1])
        
        finalMue = []
        for rule in self.ruleBase:
            if rule[1][0] == 'OR':
                ruleArr = []
                for r in rule[0]:
                    ruleArr.append(self.inputs[r[0]].memValues[r[1]])
                finalMue.append([rule[2][1], max(ruleArr)])
            elif rule[1][0] == 'AND':
                ruleArr = []
                for r in rule[0]:
                    ruleArr.append(self.inputs[r[0]].memValues[r[1]])
                finalMue.append([rule[2][1], min(ruleArr)])

        areaSum = 0
        areaMue = 0
        for Mue in finalMue:
            centroid = findCentroid(self.outputs[outputName].mfs[Mue[0]])
            """print(self.outputs[outputName].mfs[Mue[0]])
            print(self.outputs)
            print(Mue)"""
            left = self.outputs[outputName].mfs[Mue[0]][0]
            right = self.outputs[outputName].mfs[Mue[0]][2]
            areaSum += .5*Mue[1]*(right-left)
            areaMue += centroid * .5*Mue[1]*(right-left)

        try:
            output = areaMue / areaSum
        except:
            output = 0
        """print(output)
        print(areaMue)
        print(areaSum)
        print('next')"""
        return output
        
def main():
    FIS = HeiTerry_FIS()
    FIS.add_input('quality', np.arange(0,11,1), 3)
    FIS.add_input('service', np.arange(0,11,1), 3)
    FIS.add_output('tip', np.arange(0,28,1), [[0, 0, 13], [0, 13, 25], [13, 25, 25]])

    rules = [
        [[['quality','poor'],['service','poor']], ['OR'], ['tip', '0']],
        [[['service','average']], ['OR'], ['tip', '1']],
        [[['quality','good'], ['service','good']], ['OR'], ['tip', '2']]
    ]
    FIS.generate_mamdani_rule(rules)
    output = FIS.compute([['quality', 6.5],['service', 9.8]], 'tip')
    print(output)

if __name__ == '__main__':
    main()
