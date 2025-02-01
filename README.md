# GA-Word-Grid
This repository details a Genetic Algorithm (GA) designed to solve a designed to solve a 4x4 word puzzle, similar to Sudoku but using letters instead of numbers. The goal is to create a grid where no duplicate letters appear in any row, column, or 2x2 sub-grid.


## Pseudocode

The GA will use genetic operators to lower the fitness of the parent population, converg-ing to find a solution to the word grid problem.

The GA is initialised with the following variables, which will be further elaborated in sec-tion 2.4.4:
- Letters - A list of the 4 letters in the grid
- Population_size – Size of the parent/child populations
- Selection_size – Size of the subset of fittest parents
- Mutation_value – Probability of mutation
- Iterations – Number of iterations for the genetic operations


![image](https://github.com/user-attachments/assets/bb987c2e-6954-492c-8e4b-0bcf3644303b)

