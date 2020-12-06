""" 1.1 - случайная генерация
    2.2 - выбрать только 20% самых приспособленных особей
    3.2 - однородный (каждый бит от случайно выбранного родителя)
    4.3 - добавление 1 случайной вещи 5% особей
    5.2 - «штраф» за «старость» -10% функции приспособленности, выбор лучших
"""
import random
import csv
import numpy as np

individuals_number = 200
cargo_number = 30
max_weight = 0
max_volume = 0
weight_arr = []
volume_arr = []
price_arr = []


def generate_random_sequence():
    sequence = [random.randint(0, 1) for x in range(0, 30)]
    while not (check_volume(sequence) and check_weight(sequence)):
        sequence = [random.randint(0, 1) for x in range(0, 30)]
    return sequence


def check_weight(individual):
    tmp = individual[0:30]
    return sum(tmp * np.array(weight_arr)) if \
        sum(tmp * np.array(weight_arr)) <= max_weight else 0


def check_volume(individual):
    tmp = individual[0:30]
    return sum(tmp * np.array(volume_arr)) if \
        sum(tmp * np.array(volume_arr)) <= max_volume else 0


def total_price_count(individual):
    return sum(individual * np.array(price_arr))


def create_children(first_parent, second_parent):
    mask = generate_random_sequence()
    child = []
    for ind, item in enumerate(mask):
        if item == 0:
            child.append(first_parent[ind])
        elif item == 1:
            child.append(second_parent[ind])
    return child


def initial_population_creation():
    initial_population = [generate_random_sequence() for x in range(0, 200)]
    return initial_population


def filter_population(population):
    filtered_population = list(filter(lambda x: check_weight(x) and check_volume(x), population))
    return filtered_population


def sort_population(population):
    population.sort(key=lambda x: total_price_count(x), reverse=True)


def sort_marked_population(marked_population):
    marked_population.sort(key=lambda x: x[len(x) - 1], reverse=True)


def homogeneous_crossing(individuals_for_crossing):
    population_of_children = []
    length = len(individuals_for_crossing) - 1
    while length > 0:
        first_parent_index = random.randint(0, length)
        first_parent = individuals_for_crossing[first_parent_index]
        individuals_for_crossing.pop(first_parent_index)
        length -= 1
        second_parent_index = random.randint(0, length)
        second_parent = individuals_for_crossing[second_parent_index]
        individuals_for_crossing.pop(second_parent_index)
        first_child = create_children(first_parent, second_parent)
        second_child = create_children(first_parent, second_parent)
        population_of_children.append(first_child)
        population_of_children.append(second_child)
        length -= 1
    return population_of_children


def mutation(individual):
    item_number = random.randint(0, len(individual) - 1)
    while individual[item_number] != 0:
        item_number = random.randint(0, len(individual) - 1)
    individual[item_number] = 1
    return individual


def life_algorithm(init_population, min_cost):
    n = 10  #count of values in best_values
    population = []
    best_values = [0] * n
    population.extend(init_population)
    sort_population(population)

    for index in range(0, 500):
        population_of_children = homogeneous_crossing(population[0:40])

        for i in range(0, round(len(population) / 100 * 5)):
            individual_for_mutation_number = random.randint(0, len(population) - 1)
            population[individual_for_mutation_number] = \
                mutation(population[individual_for_mutation_number])

        for i in range(0, round(len(population_of_children) / 100 * 5)):
            individual_for_mutation_number = random.randint(0, len(population_of_children) - 1)
            population_of_children[individual_for_mutation_number] = \
                mutation(population_of_children[individual_for_mutation_number])

        for item in population:
            item.append(total_price_count(item) / 100 * 90)

        for item in population_of_children:
            item.append(total_price_count(item))

        population.extend(population_of_children)
        population = filter_population(population)
        sort_marked_population(population)
        population = population[0:200]

        for item in population:
            item.pop()

        best_value = total_price_count(population[0])
        best_values[index % n] = best_value

        if index < n - 1:
            continue

        if abs(min(best_values) - max(best_values)) <= min_cost:
            break

    return population[0]


if __name__ == '__main__':
    with open('21.txt', 'r') as fd:
        reader = csv.reader(fd, delimiter=' ')
        index = 0
        for row in reader:
            index += 1
            if index == 1:
                max_weight = int(row[0])
                max_volume = int(row[1])
                continue
            weight_arr.append(float(row[0]))
            volume_arr.append(float(row[1]))
            price_arr.append(float(row[2]))

    init_population = initial_population_creation()
    result = life_algorithm(init_population, min(price_arr))

    print(result)
    print(total_price_count(result))
