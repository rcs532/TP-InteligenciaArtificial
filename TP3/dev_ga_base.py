'''
Condiciones
~~~~~~~~~~~
1. Hay 5 casas.
2. El Matematico vive en la casa roja.
3. El hacker programa en Python.
4. El Brackets es utilizado en la casa verde.
5. El analista usa Atom.
6. La casa verde esta a la derecha de la casa blanca.
7. La persona que usa Redis programa en Java
8. Cassandra es utilizado en la casa amarilla
9. Notepad++ es usado en la casa del medio.
10. El Desarrollador vive en la primer casa.
11. La persona que usa HBase vive al lado de la que programa en JavaScript.
12. La persona que usa Cassandra es vecina de la que programa en C#.
13. La persona que usa Neo4J usa Sublime Text.
14. El Ingeniero usa MongoDB.
15. EL desarrollador vive en la casa azul.

Quien usa vim?


Resumen:
Colores = Rojo, Azul, Verde, Blanco, Amarillo
Profesiones = Matematico, Hacker, Ingeniero, Analista, Desarrollador
Lenguaje = Python, C#, JAVA, C++, JavaScript
BD = Cassandra, MongoDB, Neo4j, Redis, HBase
editor = Brackets, Sublime Text, Atom, Notepad++, Vim
'''

import random
import time

colors = {'001': 'red',          '010': 'blue',
          '011': 'green',    '100': 'white',    '101': 'yellow'}
prefession = {'001': 'Mathematician', '010': 'Hacker',
              '011': 'Engineer', '100': 'Analyst',  '101': 'Developer'}
languaje = {'001': 'Python',       '010': 'C#',
            '011': 'Java',     '100': 'C++',      '101': 'JavaScript'}
database = {'001': 'Cassandra',    '010': 'MongoDB',
            '011': 'HBase',    '100': 'Neo4j',    '101': 'Redis'}
editor = {'001': 'Brackets',     '010': 'Sublime Text',
          '011': 'Vim',      '100': 'Atom',     '101': 'Notepad++'}

possible_attributes = [colors, prefession, languaje, database, editor]


class Phenotype:

    def __init__(self):
        # crear un individuo
        blocks = [self.create_block() for _ in range(5)]
        self.chromosome = [
            block for block_sublist in blocks for block in block_sublist]
        self.score = 0

    def create_block(self):
        return [random.choice(list(attribute.keys())) for attribute in possible_attributes]

    def decode(self):
        ''' traduce 0's y 1's (conjunto de genes: 3) en valores segun un diccionario '''
        return [[colors[self.chromosome[i*5+0]],
                 prefession[self.chromosome[i*5+1]],
                 languaje[self.chromosome[i*5+2]],
                 database[self.chromosome[i*5+3]],
                 editor[self.chromosome[i*5+4]]] for i in range(5)]

    def encode(self, decode):
        array = []
        for block in decode:
            for index, attribute in enumerate(block):
                for key, value in possible_attributes[index].items():
                    if value == attribute:
                        array.append(key)
        return array

    def mutate(self):
        ''' muta un fenotipo, optimizado'''
        decoded = self.decode()
        block_to_mutate = random.randint(0, 4)
        attribute_to_mutate = random.randint(0, 4)
        decoded[block_to_mutate][attribute_to_mutate] = random.choice(
            list(possible_attributes[attribute_to_mutate].values()))
        self.chromosome = self.encode(decoded)

    def fitness_function(self):
        ''' calcula el valor de fitness del cromosoma segun el problema en particular '''

        self.score = 0

        ok_score = 1
        fail_score = -1
        punish_score = -1

        COLOR = 0
        PROFESSION = 1
        LANGUAGE = 2
        DATABASE = 3
        EDITOR = 4
        FIRST_INDEX = 0
        MIDDLE_INDEX = 2

        chromosome = self.decode()

        def get_block_index_that_matches_condition(first_attribute, first_objective_value):
            return next((block_index for (block_index, block) in enumerate(chromosome) if block[first_attribute] == first_objective_value), None)

        def check_condition(first_attribute, first_objective_value, second_attribute, second_objective_value):
            block_index = get_block_index_that_matches_condition(
                first_attribute, first_objective_value)
            if not block_index:
                self.score += punish_score
                return
            if chromosome[block_index][second_attribute] == second_objective_value:
                self.score += ok_score
            else:
                self.score += fail_score

        def check_condition_and_index(first_attribute, first_objective_value, index_value):
            block_index = get_block_index_that_matches_condition(
                first_attribute, first_objective_value)
            if not block_index:
                self.score += punish_score
                return
            if block_index == index_value:
                self.score += ok_score
            else:
                self.score += fail_score

        def check_condition_on_neighbour(first_attribute, first_objective_value, second_attribute, second_objective_value, direction="all"):
            block_index = get_block_index_that_matches_condition(
                first_attribute, first_objective_value)
            if not block_index:
                self.score += punish_score
                return
            predecessor = block_index - 1
            successor = block_index + 1
            length = len(chromosome) - 1
            if (direction == "right" and successor <= length and chromosome[successor][second_attribute] == second_objective_value) or (predecessor >= 0 and chromosome[predecessor][second_attribute] == second_objective_value) or (direction == "all" and successor <= length and chromosome[successor][second_attribute] == second_objective_value):
                self.score += ok_score
            else:
                self.score += fail_score

        def check_repeated_values(attribute, attributes_objective_length):
            values = [block[attribute] for block in chromosome]
            unique_values = set(values)
            if len(values) == len(unique_values) and len(unique_values) == attributes_objective_length:
                self.score += 2 * ok_score
            else:
                self.score += 2 * punish_score

        #1. Hay 5 casas.
        check_repeated_values(COLOR, 5)
        check_repeated_values(PROFESSION, 5)
        check_repeated_values(DATABASE, 5)
        check_repeated_values(LANGUAGE, 5)
        check_repeated_values(EDITOR, 5)
        #2. El Matematico vive en la casa roja.
        check_condition(COLOR, "red", PROFESSION, "Mathematician")
        #3. El hacker programa en Python.
        check_condition(PROFESSION, "Hacker", LANGUAGE, "Python")
        #4. El Brackets es utilizado en la casa verde.
        check_condition(COLOR, "green", EDITOR, "Brackets")
        #5. El analista usa Atom.
        check_condition(PROFESSION, "Analyst", EDITOR, "Atom")
        #6. La casa verde esta a la derecha de la casa blanca.
        check_condition_on_neighbour(COLOR, "white", COLOR, "green", "right")
        #7. La persona que usa Redis programa en Java
        check_condition(DATABASE, "Redis", LANGUAGE, "Java")
        #8. Cassandra es utilizado en la casa amarilla
        check_condition(DATABASE, "Cassandra", COLOR, "yellow")
        #9. Notepad++ es usado en la casa del medio.
        check_condition_and_index(EDITOR, "Notepad++", MIDDLE_INDEX)
        #10. El Desarrollador vive en la primer casa.
        check_condition_and_index(PROFESSION, "Developer", FIRST_INDEX)
        #11. La persona que usa HBase vive al lado de la que programa en JavaScript.
        check_condition_on_neighbour(DATABASE, "HBase", LANGUAGE, "JavaScript")
        #12. La persona que usa Cassandra es vecina de la que programa en C#.
        check_condition_on_neighbour(DATABASE, "Cassandra", LANGUAGE, "C#")
        #13. La persona que usa Neo4J usa Sublime Text.
        check_condition(DATABASE, "Neo4J", EDITOR, "Sublime Text")
        #14. El Ingeniero usa MongoDB.
        check_condition(PROFESSION, "Engineer", DATABASE, "MongoDB")
        #15. EL desarrollador vive en la casa azul.
        check_condition(PROFESSION, "Developer", COLOR, "blue")


class Riddle:

    def __init__(self):
        self.start_time = time.time()
        self.population = []

    '''
    proceso general
    '''

    def solve(self, n_population):

        self.generate(n_population)
        print(f"Población creada con {len(self.population)} individuos")

        print(self.population[0].chromosome)
        print(self.population[0].decode())

        print("Inicio del proceso iterativo")
        fit, indi = self.iterar()

        print(
            f"Fin del proceso, mejor resultado \n - Fitness: {fit} \n - Individuo {indi.chromosome} \n - Individuo {indi.decode()}")

    def iterar(self):

        counter = 0
        break_condition = False

        crossover_prop = 0.80

        N2 = 17  # 15 + 2 puntos de penalización por combinación correcta

        while not(break_condition):

            if counter % 100 == 0:
                print("--------------------------------")
                print(counter)
                print(self.population[0].decode())

            # seleccion
            for individual in self.population:
                # Calculo la aptitud
                individual.fitness_function()
            # Ordeno individuos segun aptitud
            self.population.sort(key=lambda x: x.score, reverse=True)
            # Selecciono aleatoriamente individuos más aptos que van a trascender proxima generacion
            most_suitable_individuals = []
            for individual_to_survive in range(len(self.population)):
                if random.randrange(0, 100) <= (crossover_prop * 100):
                    most_suitable_individuals.append(
                        self.population[individual_to_survive])
            # crossover
            next_gen = []
            most_suitable_population_length = len(most_suitable_individuals)
            N = int(len(self.population) / 2)
            for _ in range(0, N):
                parents = random.sample(
                    range(0, most_suitable_population_length - 1), 2)
                parent_1 = self.population[parents[0]]
                parent_2 = self.population[parents[1]]
                children = self.crossOver(parent_1, parent_2)
                next_gen = next_gen + children
            self.population = next_gen
            # mutate
            self.mutate(self.population)
            for individual in self.population:
                # Calculo la aptitud
                individual.fitness_function()
            # condicion de corte
            self.population.sort(key=lambda x: x.score, reverse=True)
            highest_score = self.population[0].score
            if highest_score >= N2 or counter > 500:
                break_condition = True
            counter += 1

        return self.population[0].score, self.population[0]

    '''
    operacion: generar individuos y agregarlos a la poblacion
    '''

    def generate(self, i):
        for _ in range(0, i):
            newbie = Phenotype()
            self.population.append(newbie)

    '''
    operacion: mutación. Cambiar la configuración fenotipica de un individuo
    '''

    def mutate(self, population, prob=0.5):
        for individual in population:
            if random.randint(0, 100) <= prob * 100:
                individual.mutate()

    '''
    operacion: cruazamiento. Intercambio de razos fenotipicos entre individuos
    '''

    def crossOver(self, progenitor_1, progenitor_2):
        child1 = Phenotype()
        child2 = Phenotype()
        child1.chromosome = progenitor_1.chromosome[:]
        child2.chromosome = progenitor_2.chromosome[:]
        #Cruzamiento simple
        block_point = random.randrange(1, 24)
        child1.chromosome[block_point:] = progenitor_2.chromosome[block_point:]
        child2.chromosome[:block_point] = progenitor_1.chromosome[:block_point]
        return [child1, child2]


start = time.time()

rid = Riddle()
rid.solve(n_population=2000)
end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("Tiempo transcurrido {:0>2}:{:0>2}:{:05.2f}".format(
    int(hours), int(minutes), seconds))
