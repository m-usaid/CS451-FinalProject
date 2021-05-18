from evol_algo import EA_imp
from generate_graphs import *
import random
import copy

graphs = generate_graphs(files)
m_Graph = graphs[0]

class graphBandiwdth(EA_imp):
    def __init__(self, graph, population_size, offspring_size, generations, mutation_rate, iterations, parent_ss, survivor_ss):
        self.Graph = graph 
        EA_imp.__init__(self, population_size, offspring_size, generations, 
                        mutation_rate, iterations, parent_ss, survivor_ss)

    def generate_individual(self):
        vertices = list(self.Graph.nodes())
        v_dict = {i:0 for i in vertices}
        # e_dict = {i:0 for i in edges}
        shuff_vert = copy.deepcopy(vertices) 
        random.shuffle(shuff_vert)
        for key in v_dict.keys():
            v_dict[key] = shuff_vert[int(key)-1]
        return v_dict

    def fitness_function(self, chromosome: dict) -> int:
        edges = self.Graph.edges()
        e_dict = {i:0 for i in edges}
        for edge in e_dict:
            x = abs(int(chromosome[edge[0]]) - int(chromosome[edge[1]]))
            e_dict[edge] = x
        return max(e_dict.values())

    def init_population(self):
        self.population = []
        # genes = []
        for _ in range(self.population_size):
            chromosome = self.generate_individual()
            # genes.append()
            self.population.append((chromosome, self.fitness_function(chromosome)))
        # return population

# pop = init_population(m_Graph, 10)

bandy = graphBandiwdth(m_Graph, 10, 5, 100, 0.1, 10, 'Random', 'Truncation')
bandy.init_population()
print(bandy.population)
# print(pop)
