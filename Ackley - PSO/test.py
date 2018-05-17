import random
import matplotlib.pyplot as plt, pylab
import numpy
import string


class Individ:
    # defined as a list of words, for every row in the puzzle
    def __init__(self, words):
        self.words = words

    def fitness(self, problem):
        # defined as the difference between the numbers of correct words and guessed words
        correct = {}
        guessed = {}

        sol = self.words + problem.get_column_words(self.words)

        for word in problem.words:
            if word not in correct.keys():
                correct[word] = 1
                guessed[word] = 0
            else:
                correct[word] += 1

        for word in sol:
            if word in guessed.keys():
                guessed[word] += 1
            else:
                guessed[word] = 1

        score = 0

        for word in sol:
            if word not in correct.keys():
                score += guessed[word]
            else:
                score += abs(correct[word] - guessed[word])

        return score

    def mutate(self, problem):
        # inject into the individ a random input word on a random position
        random_word = problem.words[random.randint(0, len(problem.words) - 1)]
        random_index = random.randint(0, len(self.words) - 1)

        return Individ(self.words[:random_index] + [random_word] + self.words[random_index + 1:])

    def crossover(self, other):
        # return an individ that has the first half words from this individ and second half from the other
        half = len(self.words) // 2
        return Individ(self.words[:half] + other.words[half:])

    def __str__(self):
        return str(self.words)


class Population:

    def __init__(self, individs, problem):
        self.individs = individs
        self.problem = problem

    def best_fitness(self):
        # calculate and return the best fitness from all population
        return min([individ.fitness(self.problem) for individ in self.individs])

    def avg_fitness(self):
        f = [i.fitness(self.problem) for i in self.individs]
        return numpy.mean(f)

    def selection(self):
        new_generation = []

        # sort the individs based on fitness
        self.individs = sorted(self.individs, key=lambda individ: individ.fitness(self.problem))
        # the top 10% remain
        last_top = int(0.1 * len(self.individs))
        if (last_top < 1):
            last_top = 1
        new_generation += [self.individs[i] for i in range(last_top)]
        #         #select randomly 20% from the bottom 60%
        #         to_select = int(0.2 * len(self.individs))
        #         lucky_few = set()
        #         while(len(lucky_few) != to_select):
        #             lucky_few.add(self.individs[random.randint(to_select, len(self.individs) - 1)])

        #         new_generation += lucky_few

        # mutate the bottom 20%
        to_select = int(0.2 * len(self.individs))
        mutants = set()
        while (len(mutants) != to_select):
            mutants.add(self.individs[random.randint(to_select, len(self.individs) - 1)].mutate(self.problem))

        new_generation += mutants

        # breed the new generation until population reaches previous generation
        while (len(new_generation) != len(self.individs)):
            individ1 = new_generation[random.randint(0, len(new_generation) - 1)]
            individ2 = new_generation[random.randint(0, len(new_generation) - 1)]
            new_generation.append(individ1.crossover(individ2))

        # move on to the next generation
        self.individs = new_generation

    def __str__(self):
        return "\n".join([
            str(index) + ". " + str(individ) + " -> " + str(individ.fitness(self.problem))
            for index, individ in enumerate(self.individs)
        ])


class Problem:
    def __init__(self, file_name):
        self.load_data(file_name)

    def load_data(self, file_name):
        with open(file_name, 'r') as f:
            self.words = [line.strip(" ").strip("\n") for line in f]
            self.n = len(self.words)
            self.words = self.words + self.get_column_words(self.words)

    def get_column_words(self, words):
        s = [
            "".join(
                [
                    words[row][col]

                    for row in range(len(words))
                ]
            )

            for col in range(len(words[0]))
        ]
        # s=[]
        # for row in range(len(words)):
        #    l=[]
        #    for col in range(len(words[row])):
        #        l.append(words[row][col])
        #    s.append("".join(l))

        return s


class Application:

    @staticmethod
    def main():
        population_size = 20
        iteration_nr = 1000

        problem = Problem("easy.txt")

        population = Population(
            [
                Individ(
                    [
                        problem.words[random.randint(0, len(problem.words) - 1)]
                        for _ in range(problem.n)
                    ]
                )
                for _ in range(population_size)
            ],
            problem
        )


        iteration_scores = []
        for iteration in range(iteration_nr):
            iteration_scores.append(population.avg_fitness())
            population.selection()
            #             plt.plot(iteration_scores)
            #             plt.show()


        plt.plot(iteration_scores)
        pylab.show()

        print(population)


Application.main()