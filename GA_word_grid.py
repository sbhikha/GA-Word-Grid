# Genetic Algorithm for Word Grid 4x4
# #############################################################################
# Assignment parameters:
#    Given a sparsely populated grid of size 4x4, use a genetic algorithm to find a solution to the grid given the following constraints:
#     - The grid must not have any duplicate letters in a row, column, or 2x2 square.
#
# Approach:
#    1. Create a grid with a random initial population of 4 letters.
#    (for/while loop) Until parent population = population_size: (i.e 10 parent grids) 
#       2. Randomly populate the initialised grid
#       3. Calculate fitness of grid
#       4. Store the grid, fitness and index 
#       5. If fitness = 0, store grid as a solution
#    5. Select the fittest grids (Those with the lowest fitness)
#    6. Crossover the fittest grids to create new (child) grid ####(Should we impltement two children (i.e split the parents both horizointally and vertically)? At this point it only splits horizontally) 
#    7. Mutate the child grid (based on muatation probability)
#    8. If fitness = 0, then store the grid as a solution
#    9. Create new children until enough children are created to replace the parent population (population_size)
#    10. Repeat step 2 to 9 for as many interations as necessary
#    11. Print the number of solutions and the corresponding grids

from time import time
import numpy as np
import random

#Control parameters
letters = ['a','b','c','d']
grid_size = 4
population_size = 10000
selection_size = 20
mutation_val = 0.1
iterations = 1000
                
##Grid population
#Create a grid of random letters
def empty_grid(grid_size):
    grid = np.empty((grid_size, grid_size), dtype=str)
    return grid

#Set intial population (4 randomly placed letters on the grid)
def initial_population():
    placement = {}
    for i in range(5):
        i = random.randint(0, 3)
        j = random.randint(0, 3)
        placement[(i, j)] = random.choice(letters)
    return placement

#Randomly populate grid (entire grid)
def populate_grid(grid, placement):
    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) in placement.keys():
                grid[i][j] = placement[(i, j)]
            else:
                grid[i][j] = random.choice(letters)
    return grid
    
#Create new grid, wiping old initilialised grid
def initialised_grid(placement):
    grid = empty_grid(grid_size)
    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) in placement.keys():
                grid[i][j] = placement[(i, j)]
    return grid

##Fitness function (Goal is to have low fitness (i.e no duplicates in row, column, or 2x2 square)))
#Get columns of grid, store in numpy array
def get_columns(grid):
    columns = []
    for i in range(grid_size):
        column = []
        for j in range(grid_size):
            column.append(grid[j][i])
        columns.append(column)
    return columns

#Get 2x2 squares of grid
def get_squares(grid):
    squares = []
    squares.append(np.concatenate(grid[0:2, 0:2]))
    squares.append(np.concatenate(grid[0:2, 2:4]))
    squares.append(np.concatenate(grid[2:4, 0:2]))
    squares.append(np.concatenate(grid[2:4, 2:4]))
    return squares

#Calculate fitness of a grid (adds one to fitness if duplicates are found in row, column, or 2x2 square)
def fitness(grid):
    fitness = 0
    for row in grid:
        for letter in letters:
            if np.count_nonzero(row == letter) > 1:
                fitness += 1
    for column in get_columns(grid):
        for letter in letters:
            if column.count(letter) > 1:
                fitness += 1
    for square in get_squares(grid):
        for letter in letters:
            if np.count_nonzero(square == letter) > 1:
                fitness += 1
    return fitness

##Mutation function (randomly mutate a grid)
#Mutate a grid

def mutate(grid):
    if random.random() < mutation_val:
        i = random.randint(0, grid_size - 1)
        j = random.randint(0, grid_size - 1)
        grid[i][j] = random.choice(letters)
        #print("Mutation occured")
    return grid

##Crossover function (Crossover function for 2 parents --> child)
#Crossover two grids

def crossover(grid1, grid2):
    crossover_point_1 = random.randint(0, grid_size - 1)
    crossover_point_2 = random.randint(0, grid_size - 1)
    child_a = np.concatenate((grid1[:,0:crossover_point_1], grid2[:,crossover_point_1:4]),axis=1)
    child_b = np.concatenate((grid1[0:crossover_point_2,:], grid2[crossover_point_2:4,:]))
    return child_a, child_b

## Main function ##NOT COMPLETE///NOT WORKING
# Run GA

def unique(arrays):
    unique_list = []
    for array in arrays:
        if unique_list == []:
            unique_list.append(array)
        for solution in unique_list:
            if np.array_equal(array, solution):
                continue
            else:
                unique_list.append(array)
    return unique_list

def main():
    start = time()
    initial_vals = initial_population()
    while fitness(initialised_grid(initial_vals)) != 0:
        initial_vals = initial_population()
    initial_grid = initialised_grid(initial_vals)
    solutions = []
    parent_grid_history = []
    child_grid_history = []
    for i in range(population_size):
        grid = populate_grid(empty_grid(grid_size), initial_vals)
        parent_grid_history.append([fitness(grid), grid])
        if fitness(grid) == 0:
            solutions.append(grid)
    parent_grid_history.sort(key=lambda x: x[0])
    for i in range(iterations):
    # while len(solutions) == 0:
        while len(child_grid_history) < population_size:
            parent_grid_history = parent_grid_history[0:selection_size]
            first = parent_grid_history[random.randint(0, len(parent_grid_history) - 1)]
            second = parent_grid_history[random.randint(0, len(parent_grid_history) - 1)]
            child_a, child_b = crossover(first[1], second[1])
            child_a = mutate(child_a)
            child_b = mutate(child_b)
            child_grid_history.append([fitness(child_a), child_a])
            child_grid_history.append([fitness(child_b), child_b])
            if fitness(child_a) == 0:
                solutions.append(child_a)
            if fitness(child_b) == 0:
                solutions.append(child_b)
        parent_grid_history = child_grid_history
        parent_grid_history.sort(key=lambda x: x[0])
        solutions = unique(solutions)
    end = time()
    return initial_grid, solutions, child_grid_history, (end-start)


# Call main function
initial_grid, solutions, child_grid_history, time_taken = main()
print("Initial grid:")
print(initial_grid)
print("\n Solutions found:" )
print(solutions)
print("\n Top 10 children from the final iteration:")
print(child_grid_history[:10])
print("\n Time taken: " + str(time_taken))