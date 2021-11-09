import math
import random
import requests
import time
import matplotlib.pyplot as plt
import numpy as np

class OnePlusOneE:
    n_genes = 10
    individual = []
    variance = []
    errors_generations = []
    success_vector_size = 250
    current_generation = 0
    n_generations = 10000
    c = 0.82
    module_ind = 5
    module_variance = 7


    def initialize_individual(self):
        for i in range(self.n_genes):
            self.individual.append(random.uniform(0, self.module_ind))
            self.variance.append(random.uniform(0, self.module_variance))

        print(str(self.individual) + "\n" + str(self.variance))

    def final_evaluate_individual(self, individual=None):
        url = ""
        if individual is not None:
            url = "http://memento.evannai.inf.uc3m.es/age/robot10?c1=" + str(individual[0]) + \
                 "&c2=" + str(individual[1]) + \
                 "&c3=" + str(individual[2]) + \
                 "&c4=" + str(individual[3]) + \
                 "&c5=" + str(individual[4]) + \
                 "&c6=" + str(individual[5]) + \
                 "&c7=" + str(individual[6]) + \
                 "&c8=" + str(individual[7]) + \
                 "&c9=" + str(individual[8]) + \
                 "&c10=" + str(individual[9])
            r = requests.get(url)
            print("Evaluating **NEW** individual: " + str(individual) + "\nError: " + r.text)
        else:
            url = "http://memento.evannai.inf.uc3m.es/age/robot10?c1=" + str(self.individual[0]) + \
                  "&c2=" + str(self.individual[1]) + \
                  "&c3=" + str(self.individual[2]) + \
                  "&c4=" + str(self.individual[3]) + \
                  "&c5=" + str(self.individual[4]) + \
                  "&c6=" + str(self.individual[5]) + \
                  "&c7=" + str(self.individual[6]) + \
                  "&c8=" + str(self.individual[7]) + \
                  "&c9=" + str(self.individual[8]) + \
                  "&c10=" + str(self.individual[9])
            r = requests.get(url)
            print("Evaluating individual: " + str(self.individual) + "\nError: " + r.text)
        return float(r.text)

    def evaluate_individual(self, individual=None):
        url = ""
        if individual is not None:
            url = "http://memento.evannai.inf.uc3m.es/age/robot4?c1=" + str(individual[0]) + \
                 "&c2=" + str(individual[1]) + \
                 "&c3=" + str(individual[2]) + \
                 "&c4=" + str(individual[3])
            r = requests.get(url)
            print("Evaluating **NEW** individual: " + str(individual) + "\nError: " + r.text)
        else:
            url = "http://memento.evannai.inf.uc3m.es/age/robot4?c1=" + str(self.individual[0]) + \
                  "&c2=" + str(self.individual[1]) +\
                  "&c3=" + str(self.individual[2]) +\
                  "&c4=" + str(self.individual[3])
            r = requests.get(url)
            print("Evaluating individual: " + str(self.individual) + "\nError: " + r.text)
        return float(r.text)

    def evolution(self):

        n_success = 0
        for i in range(self.success_vector_size):
            print("------------------------------------\nGENERATION " + str(self.current_generation))

            if self.current_generation == 0:
                # evaluation of the current individual
                if self.n_genes == 4:
                    error_individual = self.evaluate_individual()
                else:
                    error_individual = self.final_evaluate_individual()
                self.errors_generations.append(error_individual)
            else:
                error_individual = self.errors_generations[-1]
            print("Current individual: " + str(self.individual))
            print("Current Error: " + str(error_individual))
            new_individual = []

            # creation & evaluation of the new individual
            for i in range(self.n_genes):
                new_individual.append((self.individual[i] + random.gauss(0, self.variance[i])) % self.module_ind)
            if self.n_genes == 4:
                error_new_individual = self.evaluate_individual(new_individual)
            else:
                error_new_individual = self.final_evaluate_individual(new_individual)

            # comparison of the individuals
            if error_new_individual < error_individual:
                self.individual = new_individual.copy()
                n_success = n_success + 1
                print("***NEW INDIVIDUAL WINS***  " + str(n_success) + "\nCurrent individual: " + str(self.individual))
                self.errors_generations.append(error_new_individual)
            else:
                self.errors_generations.append(error_individual)

            self.current_generation = self.current_generation + 1
        success_ratio = n_success / self.success_vector_size
        self.mutate_variance(success_ratio)

    def mutate_variance(self, success_ratio):
        print("------------------------------------\nMUTATING VARIANCE " + str(success_ratio))
        if success_ratio < 0.2:
            for j in range(self.n_genes):
                self.variance[j] = self.c * self.variance[j]
        elif success_ratio > 0.2:
            for x in range(self.n_genes):
                self.variance[x] = self.variance[x]/self.c
        print("New variance: " + str(self.variance))

class MuPlusLambda():
    n_genes = 4
    poblation_size = 50
    lambd = 30
    population = []
    population_variances = []
    best_fitness_generations = []
    n_generations = 500
    module_ind = 10
    module_variance = 15
    n_participants = 10
    best_individual_generations = []
    tasa_aprendizaje0 = 1 / math.sqrt(2 * lambd)
    tasa_aprendizaje = 1 / math.sqrt(2 * math.sqrt(lambd))

    def initialize_individual(self):
        individual = []
        variance = []
        for i in range(self.n_genes):
            individual.append(random.uniform(0, self.module_ind))
            variance.append(random.uniform(0, self.module_variance))
        return individual, variance

    def initialize_poblation(self):
        for j in range(self.poblation_size):
            individual, variance = self.initialize_individual()
            self.population.append(individual)
            self.population_variances.append(variance)

    def evaluate_individual(self, individual=None):
        url = ""
        if self.n_genes == 10:
            url = "http://memento.evannai.inf.uc3m.es/age/robot10?c1=" \
                  + str(individual[0]) + \
                  "&c2=" + str(individual[1]) + \
                  "&c3=" + str(individual[2]) + \
                  "&c4=" + str(individual[3]) + \
                  "&c5=" + str(individual[4]) + \
                  "&c6=" + str(individual[5]) + \
                  "&c7=" + str(individual[6]) + \
                  "&c8=" + str(individual[7]) + \
                  "&c9=" + str(individual[8]) + \
                  "&c10=" + str(individual[9])
            r = requests.get(url)
        else:
            url = "http://memento.evannai.inf.uc3m.es/age/robot4?c1=" \
                  + str(individual[0]) + \
                  "&c2=" + str(individual[1]) + \
                  "&c3=" + str(individual[2]) + \
                  "&c4=" + str(individual[3])
            r = requests.get(url)
        return float(r.text)

    def evaluate_population(self, population=None):

        #buffer for fitness values of the generation
        current_fitness = []

        # iterative evaluation of the individuals
        for i in range(self.poblation_size):
            fitness_value = self.evaluate_individual(self.population[i])
            current_fitness.append(fitness_value)

            self.population[i].append(fitness_value)
        self.sort_population()
        # print("EVALUATED POPULATION")
        # self.print_population()

        # storing the best values
        print("BEST FITNESS GENERATION: " + str(min(current_fitness)))
        print("BEST INDIVIDUAL GENERATION: " + str(self.population[0]) + "\n")
        self.best_individual_generations.append(self.population[0])
        self.best_fitness_generations.append(min(current_fitness))

    def sort_population(self):

        # adding index to sort variance list at the same time
        for i in range(len(self.population)):
            self.population[i].insert(0, i)

        # sorting population
        self.population.sort(key=lambda x: x[-1])

        #extracting order
        index_list = [x[0] for x in self.population]

        #removing index
        for i in range(len(self.population)):
            self.population[i].pop(0)

        #sorting variances
        sorted_variances = []
        for i in index_list:
            sorted_variances.append(self.population_variances[i])

        self.population_variances = sorted_variances.copy()

    def generate_new_individuals(self, generation):

        # generate as much indivduals as lambda value
        for i in range(self.lambd):
            new_individual = []
            new_individual_variances = []
            # if i == 0:
            #     print(str("parent 1: " + str(self.population[i])))
            #     print(str("parent 2: " + str(self.population[i + 1])))
            for j in range(self.n_genes):

                # each gen is the mean
                new_gen = (self.population[i][j] + self.population[i + 1][j]) / 2
                # print(str(j) + ": " + str(new_gen))
                gen_variance_posibilities = [self.population_variances[i][j], self.population_variances[i + 1][j]]
                new_gen_variance = random.choice(gen_variance_posibilities)

                # mutate the gen
                new_gen = (new_gen + random.gauss(0, new_gen_variance)) % self.module_ind
                # print(str(j) + "mut: " + str(new_gen))
                new_individual.append(new_gen)
                new_individual_variances.append(new_gen_variance)

            # evaluate new individual
            fitness_new = self.evaluate_individual(new_individual)
            new_individual.append(fitness_new)
            # if i == 0:
            #     print("NEW: " + str(new_individual))
            self.population.append(new_individual)
            self.population_variances.append(new_individual_variances)

        # sort the population again
        self.sort_population()
        #print("CANDIDATES")
        #self.print_population()

        # selection of the best individuals
        for i in range(self.lambd):
            self.population.pop()
            self.population_variances.pop()
        #print("SELECTED POPULATION")
        #self.print_population()

        self.tournaments()
        # popping the fitness values of each individual
        self.fitness_cleaning()

    def tournaments(self):
        selected_population = []
        selected_variances = []
        for i in range(len(self.population)):
            selected_individual = -1
            fitness_selected = 1000000
            for j in range(self.n_participants):
                participant = np.random.randint(0, len(self.population))
                fitness_participant = self.population[participant][-1]
                if (fitness_participant < fitness_selected):
                    selected_individual = participant
                    fitness_selected = fitness_participant
            ind_to_append = self.population[selected_individual].copy()
            var_to_append = self.population_variances[selected_individual].copy()
            selected_population.append(ind_to_append)
            selected_variances.append(var_to_append)
        self.population = selected_population.copy()
        self.population_variances = selected_variances.copy()

    def fitness_cleaning(self):
         for y in range(len(self.population)):
             tmp = self.population[y].copy()
             self.population[y].pop()

        #print("CLEANED POPULATION")
        #self.print_population()

    def mutate_variance(self):
        for i in range(len(self.population_variances)):
            #print("old variance: " + str(self.population_variaces[i]))
            for j in range(self.n_genes):
                self.population_variances[i][j] = ((math.e ** random.gauss(0, self.tasa_aprendizaje0))
                                                   * self.population_variances[i][j]
                                                   * (math.e ** random.gauss(0, self.tasa_aprendizaje))) % self.module_variance
            #print("new variance: " + str(self.population_variaces[i]) + "\n")

    def print_population(self):
        for i in range(len(self.population)):
            print("i(" + str(i) + "): " + str(self.population[i]))
            print("v(" + str(i) + "): " + str(self.population_variances[i]))
        print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")

if __name__ == '__main__':

    start = 0
    end = 0
    execution_time = 0
    strategy = 1

    if strategy == 0:
        start = time.time()
        problem = MuPlusLambda()
        problem.initialize_poblation()

        for i in range(problem.n_generations):

            print("-----------------------------------------------------------\nGENERATION "
                  + str(i) + "\n-----------------------------------------------------------")
            problem.evaluate_population()
            problem.generate_new_individuals(i)
            problem.mutate_variance()

        end = time.time()
        execution_time = str(end - start)
        print("------------------------------------\nALGORITHM FINISHED\n - "
              "Tiempo de ejecución: " + execution_time +
              "\n - Error minimo: " + str(min(problem.best_fitness_generations)) +
              "\n - Mejor individuo: " + str(problem.best_individual_generations[-1]))
        plt.plot(problem.best_fitness_generations)
        plt.title("Evolución Error")
        plt.xlabel("Generacion")
        plt.ylabel("Error")
        plt.show()
    else:
        start = time.time()
        problem = OnePlusOneE()
        problem.initialize_individual()
        iterations = int(problem.n_generations / problem.success_vector_size)

        for i in range(iterations):
            problem.evolution()
        end = time.time()
        execution_time = str(end - start)
        print("------------------------------------\nALGORITHM FINISHED\n - "
              "Tiempo de ejecución: " + execution_time +
              "\n - Error minimo: " + str(min(problem.errors_generations)) +
              "\n - Mejor individuo: " + str(problem.individual))

        plt.plot(problem.errors_generations)
        plt.title("Evolución Error")
        plt.xlabel("Generacion")
        plt.ylabel("Error")
        plt.show()

