from evol_algo import EA_imp
from generate_graphs import *
import random
import copy

graphs = generate_graphs(files)
m_Graph = graphs[0]

class graphBandiwdth(EA_imp):
    def __init__(self, graph, population_size, offspring_size, generations, mutation_rate, iterations, parent_ss, survivor_ss):
        EA_imp.__init__(self, graph, population_size, offspring_size, generations, 
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


    def crossover(self, parent: list):
        ### GENERAL METHOD 
        """Crossover method to create child chromosome.

        Args:
            parent (list): A list of size 2 containing the parent chromosomes.

        Returns:
            [list]: 2 offspring chromosome.
        """
        
        childAP1 = []
        childAP2 = []
        childBP1 = []
        childBP2 = []
        child1 = []
        child2 = []
        numberingA = list(parent[0].values())
        numberingB = list(parent[1].values())
        size = len(numberingA)
        geneA = random.randint(0, size-1)
        geneB = random.randint(0, size-1)
        startgene = min(geneA, geneB)
        endgene = max(geneA, geneB)
        print(startgene, endgene)
        for i in range(startgene, endgene):
            childAP1.append(numberingA[i])
            childBP1.append(numberingB[i])
        childAP2 = [item for item in numberingA if item not in childAP1]
        childBP2 = [item for item in numberingB if item not in childBP1]
        child1 = childAP2[:startgene] + childAP1 + childAP2[startgene:]
        child2 = childBP2[:startgene] + childBP1 + childBP2[startgene:]
        return child1, child2

# lst = [['1','3', '2', '6', '7', '5'], ['5', '4', '7', '6', '1', '3', '2']]
bandy = graphBandiwdth(m_Graph, 10, 5, 100, 0.1, 10, 'Random', 'Truncation')
bandy.init_population()
print(bandy.crossover([bandy.population[1][0], bandy.population[2][0]]))