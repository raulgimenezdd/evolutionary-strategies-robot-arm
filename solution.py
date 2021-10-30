import random
import requests
import numpy as np

class ES:
    n_genes = 4
    individual = []
    variance = []
    errors_generations = []
    success_vector = []
    success_vector_size = 10
    current_generation = 0
    n_generations = 100
    improvement_ratio = 0
    c = 0.82

    def initialize_individual(self):
        for i in range(self.n_genes):
            self.individual.append(random.uniform(0, 360))
            self.variance.append(random.uniform(0, 180))

        for i in range(self.success_vector_size):
            self.success_vector.append(-1)

        print(str(self.individual) + "\n" + str(self.variance))

    def evaluate_individual(self, individual=None):
        url = ""
        if individual is not None:
            url = "http://memento.evannai.inf.uc3m.es/age/robot4?c1=" + str(individual[0]) + \
                 "&c2=" + str(individual[1]) + \
                 "&c3=" + str(individual[2]) + \
                 "&c4=" + str(individual[3])
            r = requests.get(url)
            print("Evaluating **NEW** individual\nError: " + r.text)
        else:
            url = "http://memento.evannai.inf.uc3m.es/age/robot4?c1=" + str(self.individual[0]) + \
                  "&c2=" + str(self.individual[1]) +\
                  "&c3=" + str(self.individual[2]) +\
                  "&c4=" + str(self.individual[3])
            r = requests.get(url)
            print("Evaluating individual\nError: " + r.text)
        return r.text

    def evolution(self):
        # evaluation of the current individual
        error_individual = self.evaluate_individual()
        new_individual = []

        # creation & evaluation of the new individual
        for i in range(self.n_genes):
            new_individual.append(self.individual[i] + random.gauss(0, self.variance[i]))
        error_new_individual = self.evaluate_individual(new_individual)

        # comparison of the individuals
        success_vector_value = -1
        if error_new_individual < error_individual:
            self.individual = new_individual.copy()
            success_vector_value = 1
        else:
            success_vector_value = 0

        if self.current_generation < self.success_vector_size:
            iterate = True
            counter_while = 0
            while iterate:
                if self.success_vector[counter_while] == -1:
                    self.success_vector[counter_while] == success_vector_value
                    iterate = False
        else:
            self.success_vector.pop()
            self.success_vector.insert(0, success_vector_value)

if __name__ == '__main__':
    ind = ES()
    ind.initialize_individual()
    ind.evolution()