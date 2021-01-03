import numpy as np
import random
import operator
import pandas as pd


###################### Fitness Class ########################
class Fitness: 
  def __init__(self,route, dist_matrix):
    self.route = route 
    self.distance = 0
    self.fitness = 0.0
    self.dist_matrix = dist_matrix
    
  def route_distance(self):
  # route_distance function determines the distance of the route

    # Make verbose true to see print statements
    verbose = False
    if verbose: print("route: ", self.route)
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
    if verbose: print("route dist: ",self.distance)
    return self.distance

  def route_fitness(self):
  # route_fitness function determines the fitness of the route
    if self.fitness == 0:
      self.fitness = 1 / self.route_distance()
    return self.fitness

def generate_route(city_matrix):
# create some random, but still valid, list of cities to visit
  route = []
  for i in range(len(city_matrix)):
    route.append(i+1)
  random.shuffle(route)
  return route

def initial_pop(pop_size, city_list):
# generate the initial population by making a list of several routes
  pop = []
  for i in range(0, pop_size):
    while True:
      temp_route = generate_route(city_list)
      if (pop.count(temp_route)==0):
       pop.append(temp_route)
      else:
        break
  return pop

def rank_routes(population,dist_matrix,fitness_count):
  fitnessResults = {}
  fit_count = fitness_count
  for i in range(0,len(population)):
    fitnessResults[i] = (Fitness(population[i],dist_matrix).route_fitness())
    fit_count += 1
  return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True),fit_count

def selection(popRanked, eliteSize):
  selection_results = []
  df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
  df['cum_sum'] = df.Fitness.cumsum()
  df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
  for i in range(0, eliteSize):
    selection_results.append(popRanked[i][0])
  for i in range(0, len(popRanked) - eliteSize):
    pick = 100*random.random()
    for i in range(0, len(popRanked)):
      if pick <= df.iat[i,3]:
        selection_results.append(popRanked[i][0])
        break
  return selection_results

def mating_pool(population, selection_results):
  matingpool = []
  for i in range(0, len(selection_results)):
    index = selection_results[i]
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

def breed_population(matingpool, eliteSize):
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

def mutate_population(population, mutationRate):
  mutated_pop = []
    
  for ind in range(0, len(population)):
    mutatedInd = mutate(population[ind], mutationRate)
    mutated_pop.append(mutatedInd)
  return mutated_pop

def nextGeneration(currentGen, eliteSize, mutationRate, dist_matrix, fitness_count):
  popRanked,fit_count = rank_routes(currentGen, dist_matrix, fitness_count)
  selectionResults = selection(popRanked, eliteSize)
  matingpool = mating_pool(currentGen, selectionResults)
  children = breed_population(matingpool, eliteSize)
  nextGeneration = mutate_population(children, mutationRate)
  return nextGeneration,fit_count

def geneticAlgorithm(population, popSize, eliteSize, mutationRate, max_fitness):
  verbose = False
  fitness_count = 0
  # Generate the initial population 
  pop = initial_pop(popSize, population)
  if verbose: print(pop)
  #print("Initial distance: " + str(1 / rank_routes(pop,population)[0][1]))
    
  while fitness_count < max_fitness:
    pop,fitness_count = nextGeneration(pop, eliteSize, mutationRate, population, fitness_count)
    
  best, fitness_count = rank_routes(pop, population,fitness_count)
  bestRouteIndex = best[0][0]
  bestRoute = pop[bestRouteIndex]
  print("best route: ", bestRoute)
  print("Final distance: " + str(1 / best[0][1]))
  return bestRoute

cost_matrix=[]
cost_file_name = input("Intercity costs file name: ")

try:
# open cost file
  cost_file = open(cost_file_name)

# write values into cost_matrix
  lines = cost_file.read().splitlines()
  for x in range(0, len(lines)):
    line = lines[x].split(' ')
    line = list(map(int, line)) #convert str to int
    cost_matrix += [line]

# print cost_matrix
  print("COST MATRIX: " + str(cost_matrix))

except (IOError, ValueError, EOFError) as e:
# catch if cannot open file, invalid value, or end of file before expect
    cost_file.close()

#if no crossover, eliteSize = popSize
geneticAlgorithm(population=cost_matrix, popSize=4, eliteSize=4, mutationRate=0.01, max_fitness=500)
