import numpy as np
import random
import operator
import pandas as pd

class Fitness: 
  def __init__(self,route, dist_matrix):
    self.route = route 
    self.distance = 0
    self.fitness = 0.0
    self.dist_matrix = dist_matrix
    
  def route_distance(self):
    verbose = False
    if verbose: print(self.route)
    if self.distance ==0:
      path_length = 0
      for i in range(0, len(self.route)):
        from_city = self.route[i]
        to_city = None
        if i + 1 < len(self.route):
          to_city = self.route[i + 1]
        else:
          to_city = self.route[0]
        path_length += self.dist_matrix[from_city-1][to_city-1]
      self.distance = path_length
    if verbose: print(self.distance)
    return self.distance

  def route_fitness(self): 
    if self.fitness == 0:
      self.fitness = 1 / self.route_distance()
    return self.fitness

def generate_route(city_matrix):
  # create some random, but still valid, list of ciies to visit
  route = []
  for i in range(len(city_matrix)):
    route.append(i+1)
  random.shuffle(route)
  return route

def initial_pop(pop_size, city_list):
  pop = []
  for i in range(0, pop_size):
    pop.append(generate_route(city_list))
  return pop

def rankRoutes(population,dist_matrix):
  fitnessResults = {}
  for i in range(0,len(population)):
    fitnessResults[i] = (Fitness(population[i],dist_matrix).route_fitness())
  return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

def selection(popRanked, eliteSize):
  selectionResults = []
  df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
  df['cum_sum'] = df.Fitness.cumsum()
  df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
  for i in range(0, eliteSize):
    selectionResults.append(popRanked[i][0])
  for i in range(0, len(popRanked) - eliteSize):
    pick = 100*random.random()
    for i in range(0, len(popRanked)):
      if pick <= df.iat[i,3]:
        selectionResults.append(popRanked[i][0])
        break
  return selectionResults

def matingPool(population, selectionResults):
  matingpool = []
  for i in range(0, len(selectionResults)):
    index = selectionResults[i]
    matingpool.append(population[index])
  return matingpool

def breed(parent1, parent2):
  child = []
  childP1 = []
  childP2 = []
    
  geneA = int(random.random() * len(parent1))
  geneB = int(random.random() * len(parent1))
    
  startGene = min(geneA, geneB)
  endGene = max(geneA, geneB)

  for i in range(startGene, endGene):
    childP1.append(parent1[i])
        
  childP2 = [item for item in parent2 if item not in childP1]

  child = childP1 + childP2
  return child

def breedPopulation(matingpool, eliteSize):
  children = []
  length = len(matingpool) - eliteSize
  pool = random.sample(matingpool, len(matingpool))

  for i in range(0,eliteSize):
    children.append(matingpool[i])
    
  for i in range(0, length):
    child = breed(pool[i], pool[len(matingpool)-i-1])
    children.append(child)
  return children

def mutate(individual, mutationRate):
  for swapped in range(len(individual)):
    if(random.random() < mutationRate):
      swapWith = int(random.random() * len(individual))
            
      city1 = individual[swapped]
      city2 = individual[swapWith]
            
      individual[swapped] = city2
      individual[swapWith] = city1
  return individual

def mutatePopulation(population, mutationRate):
  mutatedPop = []
    
  for ind in range(0, len(population)):
    mutatedInd = mutate(population[ind], mutationRate)
    mutatedPop.append(mutatedInd)
  return mutatedPop

def nextGeneration(currentGen, eliteSize, mutationRate, dist_matrix):
  popRanked = rankRoutes(currentGen, dist_matrix)
  selectionResults = selection(popRanked, eliteSize)
  matingpool = matingPool(currentGen, selectionResults)
  children = breedPopulation(matingpool, eliteSize)
  nextGeneration = mutatePopulation(children, mutationRate)
  return nextGeneration

def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
  verbose = True

  # Generate the initial population 
  pop = initial_pop(popSize, population)
  if verbose: print(pop)
  print("Initial distance: " + str(1 / rankRoutes(pop,population)[0][1]))
    
  for i in range(0, generations):
    pop = nextGeneration(pop, eliteSize, mutationRate, population)
    
  print("Final distance: " + str(1 / rankRoutes(pop,population)[0][1]))
  bestRouteIndex = rankRoutes(pop, population)[0][0]
  bestRoute = pop[bestRouteIndex]
  return bestRoute

cityList = [
[0, 4272, 1205, 6363],
[4272, 0, 3588, 2012],
[1205, 3588, 0, 5163],
[6363, 2012, 5163, 0]
]

geneticAlgorithm(population=cityList, popSize=4, eliteSize=2, mutationRate=0.01, generations=500)
