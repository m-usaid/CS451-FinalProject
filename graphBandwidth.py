from evol_algo import EA_imp
from generate_graphs import *
import random
import copy

# graphs = generate_graphs(files)
# m_Graph = graphs[0]

class graphBandwidth(EA_imp):
    def __init__(self, graph, population_size, offspring_size, generations, mutation_rate, iterations, parent_ss, survivor_ss):
        EA_imp.__init__(self, graph, population_size, offspring_size, generations, 
                        mutation_rate, iterations, parent_ss, survivor_ss)

    def generate_individual(self):
        """Create a single chromosome. 

        Returns:
            dict: A mapping of vertices to integers in the range {1,...,len(Graph)}
        """        
        vertices = list(self.Graph.nodes())
        v_dict = {i:0 for i in vertices}
        # randomize vertices to generate random numberings        
        shuff_vert = copy.deepcopy(vertices) 
        random.shuffle(shuff_vert)
        for key in v_dict.keys():
            v_dict[key] = shuff_vert[int(key)-1]
        return v_dict

    def fitness_function(self, chromosome: dict) -> int:
        """Evaluate fitness of a given chromosome.

        Args:
            chromosome (dict): The chromosome to be evaluated. 

        Returns:
            int: The fitness value of the chromosome. 
        """        
        edges = self.Graph.edges()
        e_dict = {i:0 for i in edges}
        for edge in e_dict:
            # fit_ij = |f(i) - f(j)| forall ij in E(G)
            x = abs(int(chromosome[edge[0]]) - int(chromosome[edge[1]]))
            e_dict[edge] = x
        # the longest mapped edge is fitness value 
        return max(e_dict.values())

    def init_population(self):
        """Create gene pool by generating individuals in a loop.
        """        
        self.population = []
        # genes = []
        for _ in range(self.population_size):
            chromosome = self.generate_individual()
            # append (chromosome, fitness) to genepool 
            self.population.append((chromosome, self.fitness_function(chromosome)))

    def createChildfromNum(self, numbering: list) -> dict:
        """Generate an individual chromosome from given numbering

        Args:
            numbering (list): the corresponding numbering to generate 
            offspring from. 

        Returns:
            dict: The child chromosome. 
        """        
        vertices = list(self.Graph.nodes())
        child = {i:0 for i in vertices}
        for key in child.keys():
            child[key] = numbering[int(key)-1]
        return child 

    def crossover(self, parent1: dict, parent2: dict):
        """Perform 2-point crossover on 2 parents and return 2 children

        Args:
            parent1 (dict): The first parent.
            parent2 (dict): The second parent. 
        """                       
        childAP1 = []
        childAP2 = []
        childBP1 = []
        childBP2 = []
        child1 = []
        child2 = []
        # the ordered numbering of the two parents 
        numberingA = list(parent1.values())
        numberingB = list(parent2.values())
        size = len(numberingA)
        geneA = random.randint(0, size-1)
        geneB = random.randint(0, size-1)
        # find randomized crossover points 
        startgene = min(geneA, geneB)
        endgene = max(geneA, geneB)
        # store parts of gene to create offspring 
        for i in range(startgene, endgene):
            childAP1.append(numberingA[i])
            childBP1.append(numberingB[i])
        childAP2 = [item for item in numberingA if item not in childAP1]
        childBP2 = [item for item in numberingB if item not in childBP1]
        child1 = childAP2[:startgene] + childAP1 + childAP2[startgene:]
        child2 = childBP2[:startgene] + childBP1 + childBP2[startgene:]
        # create offspring from given numberings 
        offspring1 = self.createChildfromNum(child1)
        offspring2 = self.createChildfromNum(child2)
        return offspring1, offspring2

    def mutation_operator(self, individual: dict) -> dict:
        """Perform mutation on a chromosome by swapping the numbering 
        of two vertices randomly based on mutation rate. 

        Args:
            individual (dict): the individual on whom mutation is being applied.

        Returns:
            dict: mutated individual. 
        """            
        random.seed()
        randNum = random.random()
        if randNum < self.mutation_rate:
            key1, key2 = random.sample(list(individual), 2)
            individual[key1], individual[key2] = individual[key2], individual[key1]
        return individual


