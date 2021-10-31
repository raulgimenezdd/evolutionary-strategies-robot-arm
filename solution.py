import random
import requests

class ES:
    n_genes = 10
    individual = []
    variance = []
    errors_generations = []
    success_vector_size = 10
    current_generation = 0
    n_generations = 2000
    c = 0.82

    def initialize_individual(self):
        for i in range(self.n_genes):
            self.individual.append(random.uniform(0, 360))
            self.variance.append(random.uniform(0, 360))

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
            for i in range(self.n_genes):
                self.variance[i] = self.c * self.variance[i]
        elif success_ratio > 0.2:
            for i in range(self.n_genes):
                self.variance[i] = self.variance[i]/self.c
        print("New variance: " + str(self.variance))

    def run(self):
        problem = ES()
        problem.initialize_individual()
        iterations = self.n_generations / self.success_vector_size

        for i in range(iterations):
            self.evolution()



if __name__ == '__main__':
    problem = ES()
    problem.initialize_individual()
    iterations = int(problem.n_generations / problem.success_vector_size)

    for i in range(iterations):
        problem.evolution()
    print(str(problem.errors_generations))