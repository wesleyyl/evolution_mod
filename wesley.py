import analyzeAntimony
import evolUtils as ev
import tellurium as te
import uModel
from uModel import TReaction
import modTeUtils as tu
import random
import numpy as np



#CLASS VARIABLES:
numFloats = 0

### TEST THAT IT DOESN'T GENERATE AUTOCATALYTIC REACTIONS TO BEGIN WITH
# evolver = ev.Evolver()



# evolver.makePopulation()

# makeModel()


# evolver.addReaction()
# print(evolver)




def TESTaddReaction():
        nSpecies = 3 #self.currentConfig['numSpecies']
        #self.tracker["nAddReaction"] += 1
        floats = range(0, numFloats) #model.numFloats)  # numFloats = number of floating species
        rt = 2 #random.randint(0, 3)  # Reaction type
        reaction = TReaction()
        # reaction.reactionType = 2 #THIS IS THE UNI BI REACTION TYPE
        reaction.reactionType = rt
        reaction.rateConstant = random.random() * 50 #self.currentConfig['rateConstantScale']

        if rt == tu.TReactionType.UniUni:
            # UniUni
            reactant = random.randint(0, nSpecies - 1)
            product = random.randint(0, nSpecies - 1)
            # Disallow S1 -> S1 type of reaction
            while product == reactant:
                product = random.randint(0, nSpecies - 1)
            reaction.reactant1 = reactant
            reaction.product1 = product
            model.reactions.append(reaction)

        elif rt == tu.TReactionType.BiUni:
            # BiUni
            # Pick two reactants
            reactant1 = random.randint(0, nSpecies - 1)
            reactant2 = random.randint(0, nSpecies - 1)
            if tu.Settings.allowMassViolatingReactions:
                product = random.randint(0, nSpecies - 1)
            else:
                # pick a product but only products that don't include the reactants
                species = range(nSpecies)
                # Remove reactant1 and 2 from the species list
                species = np.delete(species, [reactant1, reactant2], axis=0)
                if len(species) == 0:
                    raise Exception("Unable to pick a species why maintaining mass conservation")
                # Then pick a product from the reactants that are left
                product = species[random.randint(0, len(species) - 1)]
            reaction.reactant1 = reactant1
            reaction.reactant2 = reactant2
            reaction.product1 = product

        elif rt == tu.TReactionType.UniBi:
            # UniBi
            reactant1 = random.randint(0, nSpecies - 1)
            #if self.autocatalysis or tu.Settings.allowMassViolatingReactions:
            if 1 + 1 == 5:
                product1 = random.randint(0, nSpecies - 1)
                product2 = random.randint(0, nSpecies - 1)
            # If we don't want autocatalysis, then UniBi reactions must be mass conserved.
            else:
                # pick a product but only products that don't include the reactant
                species = range(nSpecies)
                # Remove reactant1 from the species list
                species = np.delete(species, [reactant1], axis=0)
                if len(species) == 0:
                    raise Exception("Unable to pick a species why maintaining mass conservation")

                # Then pick a product from the reactants that are left
                product1 = species[random.randint(0, len(species) - 1)]
                product2 = species[random.randint(0, len(species) - 1)]
            reaction.reactant1 = reactant1
            reaction.product1 = product1
            reaction.product2 = product2

        elif rt == tu.TReactionType.BiBi:
            # BiBi
            reactant1 = random.randint(0, nSpecies - 1)
            reactant2 = random.randint(0, nSpecies - 1)
            if True:#not self.autocatalysis:
                # If we don't want autocatalysis, then neither of the products can be the same as the reactant
                species = range(nSpecies)
                # Remove reactant1 and 2 from the species list
                species = np.delete(species, [reactant1, reactant2], axis=0)
                if len(species) == 0:
                    raise Exception("Unable to pick a species why mainting mass conservation")
                    # Then pick a product from the reactants that are left
                product1 = species[random.randint(0, len(species) - 1)]
                product2 = species[random.randint(0, len(species) - 1)]
            else:
                # if we allow autocatalyis, then we can pick any products, the only risk being that they are the same
                # as the reactants so the reaction is irrelevant
                product1 = random.randint(0, nSpecies - 1)
                product2 = random.randint(0, nSpecies - 1)
            reaction.reactant1 = reactant1
            reaction.reactant2 = reactant2
            reaction.product1 = product1
            reaction.product2 = product2
        return reaction
        #model.reactions.append(reaction)
        #return model

def printReaction(reaction):
	# reactions = model.reactions
    astr = ''
    # for index in range(numFloats):
    #     astr += 'var S' + str(index) + '\n'

    # for b in range(nBoundary):
    #     astr += 'ext S' + str(b + nFloats) + '\n'

    # for i in range(nReactions):
    #     reaction = reactions[i]
    if reaction.reactionType == tu.TReactionType.UniUni:
        S1 = 'S' + str(reaction.reactant1)
        S2 = 'S' + str(reaction.product1)
        astr += S1 + ' -> ' + S2
        astr += '; k' + str(i) + '*' + S1 + '\n'
    if reaction.reactionType == tu.TReactionType.BiUni:
        S1 = 'S' + str(reaction.reactant1)
        S2 = 'S' + str(reaction.reactant2)
        S3 = 'S' + str(reaction.product1)
        astr += S1 + ' + ' + S2 + ' -> ' + S3
        astr += '; k' + str(i) + '*' + S1 + '*' + S2 + '\n'
    if reaction.reactionType == tu.TReactionType.UniBi:
        S1 = 'S' + str(reaction.reactant1)
        S2 = 'S' + str(reaction.product1)
        S3 = 'S' + str(reaction.product2)
        astr += S1 + ' -> ' + S2 + '+' + S3
        astr += '; k' + str(i) + '*' + S1 + '\n'
    if reaction.reactionType == tu.TReactionType.BiBi:
        S1 = 'S' + str(reaction.reactant1)
        S2 = 'S' + str(reaction.reactant2)
        S3 = 'S' + str(reaction.product1)
        S4 = 'S' + str(reaction.product2)
        astr += S1 + ' + ' + S2 + ' -> ' + S3 + ' + ' + S4
        astr += '; k' + str(i) + '*' + S1 + '*' + S2 + '\n'

    # for i in range(nReactions):
    #     reaction = reactions[i]
    #     astr += 'k' + str(i) + ' = ' + str(reaction.rateConstant) + '\n'
    # for i in range(nFloats + nBoundary):
    #     astr += 'S' + str(i) + ' = ' + str(model.initialConditions[i]) + '\n'

    return astr



for i in range(50):
	# amodel = makeModel(self.currentConfig['numSpecies'], self.currentConfig['numReactions'])
	reaction = TESTaddReaction()
	print(printReaction(reaction))









### TEST THAT IT CORRECTLY IDS AUTOCATALYTIC REACTIONS

ant = """
var S0
var S1
var S2
S1 + S1 -> S0; k0*S1*S1
S1 -> S1+S2; k1*S1
S0 -> S2+S2; k2*S0
S0 + S1 -> S2; k3*S0*S1
S1 -> S0+S1; k4*S1
S1 -> S1+S0; k5*S1
S1 -> S0; k6*S1
S1 -> S0; k7*S1
S0 -> S2+S2; k8*S0
S0 -> S2+S2; k9*S0
k0 = 30.022977610965405
k1 = 48.619603191689066
k2 = 50.50446514800127
k3 = 10.059995788394488
k4 = 3.7224489389637365
k5 = 14.867981731619016
k6 = 59.045787935656065
k7 = 50.85365050743356
k8 = 59.232629680429305
k9 = 21.758349806472882
S0 = 1.0
S1 = 5.0
S2 = 9.0
"""


output = analyzeAntimony.countReactions(ant)

print(output)

#r = te.loada(ant)


