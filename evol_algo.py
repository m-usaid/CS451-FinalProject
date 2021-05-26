from random import seed
from random import randint
from random import random
import matplotlib.pyplot as plt
import numpy as np
import math
import copy

class EA_imp():  
  def __init__(self, graph, population_size, offspring_size, generations, mutation_rate, iterations, parent_ss, survivor_ss, max_min='min'):
    self.Graph = graph 
    self.population_size = population_size
    self.offspring_size = offspring_size
    self.generations = generations
    self.mutation_rate = mutation_rate
    self.iterations = iterations
    self.BSF_table = [[0 for i in range(iterations + 1)] for i in range(generations)]
    self.ASF_table = [[0 for i in range(iterations + 1)] for i in range(generations)]
    self.population = []
    self.parent_ss = parent_ss
    self.survivor_ss = survivor_ss
    self.gen_num = 0
    self.iter_num = 0
    self.max_min = max_min
    self.best_fitness = 0
    self.avg_fitness = 0

  def init_population(self):
    # is different for all 
    pass 
  
  def check_repetition(self, chromosome, gene):
    #is different for all
    pass

  def generate_individual(self):
    #is different for all
    pass

  def fitness_function(self, chromosome):
    #is different for all
    pass

  def parent_selection(self):
    #sort the population from highest fitness to lowest fitness
    ranked_arrangement, total_rank = self.insertionSort(self.population)
    #select two parents according to chosen selection scheme
    for i in range(int(self.offspring_size/2)):
      if self.parent_ss == "FPS":
        parent_1 = self.FPS(ranked_arrangement)
        parent_2 = self.FPS(ranked_arrangement)
      elif self.parent_ss == "RBS":
        parent_1 = self.RBS(ranked_arrangement, total_rank)
        parent_2 = self.RBS(ranked_arrangement, total_rank)
      elif self.parent_ss == "BT":
        parent_1 = self.BT()
        parent_2 = self.BT()
      elif self.parent_ss == "Truncation":
        parent_1 = self.Truncation(self.offspring_size/2, ranked_arrangement)
        parent_2 = self.Truncation(self.offspring_size/2, ranked_arrangement)
      else:
        parent_1 = self.Random()
        parent_2 = self.Random()
      #perform cross-over operation on chosen parents to produce offspring
      offspring1, offspring2 = self.crossover(parent_1[0], parent_2[0])
      #perform mutation operation on the offspring
      offspring1 = self.mutation_operator(offspring1)
      offspring2 = self.mutation_operator(offspring2)
      # print(offspring1)
      # print(offspring2)
      #calculate fitness of the offspring
      fitness1 = self.fitness_function(offspring1)
      fitness2 = self.fitness_function(offspring2)
      #add offspring to the population
      self.population.append((offspring1, fitness1))
      self.population.append((offspring2, fitness2))
  
  def survivor_selection(self):
    new_population = []
    #sort the population from highest fitness to lowest fitness
    ranked_arrangement, total_rank = self.insertionSort(self.population)
    #select survivors according to chosen selection scheme and add them to the new population
    for i in range(self.population_size):
      if self.survivor_ss == "FPS":
        survivor = self.FPS(ranked_arrangement)
      elif self.survivor_ss == "RBS":
        survivor = self.RBS(ranked_arrangement, total_rank)
      elif self.survivor_ss == "BT":
        survivor = self.BT()
      elif self.survivor_ss == "Truncation":
        survivor = self.Truncation(self.population_size, ranked_arrangement)
      else:
        survivor = self.Random()
      new_population.append(survivor)
    return new_population

  def crossover(self, parent1, parent2):
    # different for all
    pass

  def mutation_operator(self, individual):
    # different for all
    pass

  def end_of_gen(self):
    #find the best fitness value in the generation
    # if we need to find local minima then best fitness value is the minimum fitness in the population
    # if we need to find local maxima then best fitness value is the maximum fitness in the population
    avg = 0
    if self.max_min == 'max':
      BSF = -math.inf
      for individual, fitness in self.population:
        if fitness > BSF:
          BSF = fitness
        avg += fitness
    else:
      BSF = math.inf
      for individual, fitness in self.population:
        if fitness < BSF:
          BSF = fitness
        avg += fitness
    ASF = avg/len(self.population)
    #update the BSF and ASF tables with the BSF and ASF value in the current generation
    self.BSF_table[self.gen_num][self.iter_num] = BSF
    self.ASF_table[self.gen_num][self.iter_num] = ASF
    self.gen_num += 1

  def end_of_iter(self):
    #calculate the average BSF value and ASF value for all generations
    #update the average value column in the table with the above value
    for gen in range(self.generations):
      sum_BSF = sum(self.BSF_table[gen])- self.BSF_table[gen][-1]
      sum_ASF = sum(self.ASF_table[gen])- self.ASF_table[gen][-1]
      self.BSF_table[gen][-1] = sum_BSF/(self.iter_num + 1)
      self.ASF_table[gen][-1] = sum_ASF/(self.iter_num + 1)
    self.iter_num += 1
    # print(self.iter_num)

  def insertionSort(self, population):
    lst = []
    total_rank = 0
    cur = 0
    for i in population:
      _, rank = i
      j = 0
      inserted = False
      while j < len(lst):
        if rank < lst[j][1]:
          lst.insert(j, i)
          inserted = True
          break
        else:
          j += 1
      if inserted == False:
        lst.append(i)
      cur += 1
      total_rank += cur
    return lst, total_rank

  def FPS(self, ranked_arrangement):
    #generate random number
    seed()
    rand_num = random()
    total_fitness = 0
    if self.max_min == 'max':
      ranked_arrangement = ranked_arrangement[::-1]
    #calculate the total fitness of all chromosomes (individuals) in the population
    for individual, fitness in ranked_arrangement:
      total_fitness += fitness 
    current_cumulation = 0
    for chromosome in ranked_arrangement:
      individual, fitness = chromosome
      #calculate current cumulative fitness
      if self.max_min == 'max':
        current_cumulation += fitness/total_fitness
      else:
        current_cumulation += (1- fitness/total_fitness)/(len(ranked_arrangement) -1)
      #return chromosome if the random number generated is within the current cumulative value
      if rand_num <= current_cumulation:
        return chromosome

  def RBS(self, ranked_arrangement, total_rank):
    seed()
    rand_num = random()
    if self.max_min == 'min':
      ranked_arrangement = ranked_arrangement[::-1]
    current_cumulation = 0
    #calculate current cumulative fitness
    for i in range(len(ranked_arrangement)):
      chromosome = ranked_arrangement[i]
      current_cumulation += (i+1)/total_rank
      #return chromosome if the random number generated is within the current cumulative value
      if rand_num <= current_cumulation:
        return chromosome

  def BT(self):
    #select two random chromosomes from the population
    seed()
    player1 = self.population[randint(0, (self.population_size-1))]
    player2 = self.population[randint(0, (self.population_size-1))]
    #select chromosome with larger fitness value if we need to find local maxima
    #otherwise select chromosome with smaller fitness value
    if self.max_min == 'max':
      if player1[1] > player2[1]:
        return player1
      else:
        return player2
    else:
      if player1[1] > player2[1]:
        return player2
      else:
        return player1

  def Truncation(self, N, ranked_arrangement):
    #choose the top N individuals with best fitness values
    if self.max_min == "min":
      ranked_arrangement = ranked_arrangement[:int(N)]
    else:
      ranked_arrangement = ranked_arrangement[::-1]
      ranked_arrangement = ranked_arrangement[:int(N)]
    #choose random individual from top N individuals
    seed()
    size = len(ranked_arrangement)
    rand_num = randint(0, size-1)
    return ranked_arrangement[rand_num]
        
  def Random(self):
    #select a random individual from the population
    seed()
    size = self.population_size
    rand_num = randint(0, size-1)
    return self.population[rand_num]

  def run_algo(self):
    self.iter_num = 0
    # print(self.population)
    while self.iter_num < self.iterations:
      self.init_population()
      self.gen_num = 0
      while self.gen_num < self.generations:
        self.parent_selection()
        self.population = self.survivor_selection()
        self.end_of_gen()
      self.end_of_iter()
      best = min(self.population, key=lambda x: x[1])
      print("Iteration " + str(self.iter_num) + ' : ' + str(best[1]))
    # self.show_result()
    arr_x, arr_y_BSF, arr_y_ASF = self.collect_info()
    # self.plot_graph(arr_x, arr_y_BSF, arr_y_ASF)
    return arr_x, arr_y_BSF, arr_y_ASF

  def show_result(self):
    print("BSF TABLE")
    for gen_num in range(len(self.BSF_table)):
      print(gen_num+1, ": ", self.BSF_table[gen_num])
    print("\n\n")
    print("*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *")
    print("\n\n")
    print("ASF TABLE")
    for gen_num in range(len(self.ASF_table)):
      print(gen_num+1, ": ", self.ASF_table[gen_num])

  def collect_info(self):
    arr_x = []
    arr_y_BSF = []
    arr_y_ASF = []
    for gen_num in range(len(self.BSF_table)):
      arr_x.append(gen_num+1)
      arr_y_BSF.append(self.BSF_table[gen_num][-1])
      arr_y_ASF.append(self.ASF_table[gen_num][-1])
    if self.max_min == 'min':
      self.avg_fitness = min(arr_y_ASF)
      self.best_fitness = min(arr_y_BSF)
      print("Best fitness so far =", min(arr_y_BSF))
      print("Best Average fitness so far =", min(arr_y_ASF))
    else:
      self.avg_fitness = max(arr_y_ASF)
      self.best_fitness = max(arr_y_BSF)
      print("Best fitness so far =", max(arr_y_BSF))
      print("Best Average fitness so far =", max(arr_y_ASF))
    return arr_x, arr_y_BSF, arr_y_ASF

  def plot_graph(self, arr_x, arr_y_BSF, arr_y_ASF):
    x = np.array(arr_x)
    y_BSF = np.array(arr_y_BSF)
    y_ASF = np.array(arr_y_ASF)
    y_bla = np.array([0 for i in range(len(arr_x))])
    plt.plot(x, y_BSF, label = 'Best Fitness so far')
    plt.plot(x, y_ASF, label = 'Average Fitness so far')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('EA graph analysis')
    plt.legend()
    # plt.show()
    text = str(self.parent_ss) + '_' + str(self.survivor_ss) + '_' + str(
            self.population_size) + '_' + str(self.offspring_size) + '_' + str(self.generations)
    plt.savefig('Results\_' + text + '.png',
                    facecolor='white', transparent=False)
    plt.clf()
