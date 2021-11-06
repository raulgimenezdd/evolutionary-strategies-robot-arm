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
    success_vector_size = 10
    current_generation = 0
    n_generations = 100
    c = 0.82


    def initialize_individual(self):
        for i in range(self.n_genes):
            self.individual.append(random.uniform(0, 10))
            self.variance.append(random.uniform(10, 15))

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

            # evaluation of the current individual
            if self.n_genes == 4:
                error_individual = self.evaluate_individual()
            else:
                error_individual = self.final_evaluate_individual()

            new_individual = []

            # creation & evaluation of the new individual
            for i in range(self.n_genes):
                new_individual.append((self.individual[i] + random.gauss(0, self.variance[i])) % 360)
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
    n_genes = 10
    poblation_size = 10
    lambd = 5
    population = []
    population_variaces = []
    best_fitness_generations = []
    n_generations = 100
    errors_generation = []
    best_individual_generations = []
    tasa_aprendizaje0 = 1 / math.sqrt(2 * lambd)
    tasa_aprendizaje = 1 / math.sqrt(2 * math.sqrt(lambd))

    def initialize_individual(self):
        individual = []
        variance = []
        for i in range(self.n_genes):
            individual.append(random.uniform(0, 10))
            variance.append(random.uniform(10, 15))
        return individual, variance

    def initialize_poblation(self):
        for j in range(self.poblation_size):
            individual, variance = self.initialize_individual()
            self.population.append(individual)
            self.population_variaces.append(variance)

    def evaluate_individual(self, individual=None):
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
        self.print_population()

        # storing the best values
        self.best_individual_generations.append(self.population[0])
        self.best_fitness_generations.append(min(current_fitness))

    def sort_population(self):
        self.population.sort(key=lambda x: x[-1])

    def generate_new_individuals(self):

        for i in range(self.lambd):
            new_individual = []
            new_individual_variances = []
            for j in range(self.n_genes):
                new_gen = (self.population[i][j] + self.population[i + 1][j]) / 2
                new_gen_variance = (self.population_variaces[i][j] + self.population_variaces[i + 1][j]) / 2
                new_gen = (new_gen + random.gauss(0, new_gen_variance)) % 360
                new_individual.append(new_gen)
                new_individual_variances.append(new_gen_variance)


            fitness_new = self.evaluate_individual(new_individual)
            new_individual.append(fitness_new)
            self.population.append(new_individual)
            self.population_variaces.append(new_individual_variances)
        self.sort_population()
        self.print_population()
        for i in range(self.lambd):
            self.population.pop()
        self.print_population()

    def mutate_variance(self):
        for i in range(len(self.population_variaces)):
            for j in range(self.n_genes):
                self.population_variaces[i][j] = ((math.e ** random.gauss(0, self.tasa_aprendizaje0))
                                                  * self.population_variaces[i][j]
                                                  * (math.e ** random.gauss(0, self.tasa_aprendizaje))) % 360

    def print_population(self):
        for i in range(len(self.population)):
            print(str(self.population[i]))
        print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")

if __name__ == '__main__':

    problem = MuPlusLambda()
    problem.initialize_poblation()

    for i in range(problem.n_generations):
        problem.evaluate_population()
        problem.generate_new_individuals()
        problem.mutate_variance()

    '''
    problem.print_population()
    print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
    problem.generate_new_individuals()
    problem.print_population()
    '''



    '''
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
    '''
