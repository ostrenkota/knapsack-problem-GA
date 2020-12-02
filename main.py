from pyeasyga import pyeasyga
import csv


dataVariant21 = []
maxWeight = 0
maxVolume = 0
with open('21.txt', 'r') as fd:
    reader = csv.reader(fd, delimiter=' ')
    index = 0
    for row in reader:
        index += 1
        if index == 1:
            maxWeight = int(row[0])
            maxVolume = int(row[1])
            continue
        dataVariant21.append(tuple(map(lambda x: float(x), row)))


ga = pyeasyga.GeneticAlgorithm(dataVariant21)
ga.population_size = 100


def fitness(individual, data):
    weight, volume, price = 0, 0, 0
    for (selected, item) in zip(individual, data):
        if selected:
            weight += item[0]
            volume += item[1]
            price += item[2]
    if weight > maxWeight or volume > maxVolume:
        price = 0
    return price


ga.fitness_function = fitness
ga.run()
print(ga.best_individual())