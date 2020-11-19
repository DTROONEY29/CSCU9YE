#!/usr/bin/env python
# coding: utf-8

# University of Stirling<br>
# Computing Science and Mathematics<br>
# #### CSCU9YE - Artificial Intelligence<p>   
# ## Assignment: Organising a Colour Palette 
# This notetbook offers some auxiliary code to support your programming assignment.    

# ### Reading the data file 

# In[1]:


import numpy as np      # Numerical library, used keeing the list of colours and computing the Euclidean distance
import pandas as pd

# Read in the color data file 
# Input: string with file name
# Oputput: the number of colours (integer), and a list numpy arrays with all the colours
def read_data(fname):
    cols = np.loadtxt(fname, skiprows = 4) # The first 4 lines have text information, and are ignored     
    ncols = len(cols)     # Total number of colours and list of colours
    return ncols,cols


# #### Read and explore the data file: either the 10, 100, or 500 colours dataset
# 
# The colorus are stored in a list, where each element of the list is a numpy array of dimension 3. That is arrays of 3 real numbers where the real numbers indicate the R,G, and B values of the colour (RGB colour model). 

# In[2]:


ncolors, colors = read_data("col100.txt")

print(f'Number of colours: {ncolors}')
print("First 5 colours:")
print(colors[0:5,  :])


# ### Plotting a sequence of colours
# 
# The function <b>plot_colors()</b> displaysthe colours from the color list *col_list* the order given by the *col_order* list. 
# 
# *col_list* and *col_order* need to be of the same length. The *ratio* parameter indicates height/width proportion of each bar of colour in the plot.

# In[3]:


import matplotlib.pyplot as plt

# Dsiplay the colors as a strip of color bars
# Input: list of colors, order of colors, and height/ratio

def plot_colors(col_list, col_order, ratio = 10): 
    assert len(col_list) == len(col_order)
    img = np.zeros((ratio, len(col_list), 3))
    for i in range(0, len(col_list)):
        img[:, i, :] = col_list[col_order[i]]
    fig, axes = plt.subplots(1, figsize=(10,6)) # figsize=(width,height) handles window dimensions
    axes.imshow(img, interpolation='nearest')
    axes.axis('off')
    plt.show()


# ### Examples of ploting a colour ordering
# 
# Let us see how to call the plot function, using the original order in which the colours appear in the data file, and another randomised order.

# In[4]:


import random as rnd

# Plot all the colors in the order they are listd in the file
order1 = list(range(ncolors))   # list of consequtive numbers from 0 to ncolors
plot_colors(colors, order1)    #  You will notice that colors are not ordered in the file

# Function to generate a random solution (random ordering)  - we can generate a random ordering of the list by using
# the shuffle function from the random library
def random_sol():
    sol = list(range(ncolors))   # list of consequtive numbers from 0 to ncolors
    # Shuffle the elements in the list randomly. Shuffles in place and doesn’t retunr a value
    rnd.shuffle(sol)   
    return sol

order2 = random_sol()
print("Another random solution: ", order2)
plot_colors(colors, order2)  # the colors are not ordered, but this is a different order

# You can test different ratios of the hight/width of the lines in the plot
print("Same ordering of colurs with a larger ratio")
plot_colors(colors, order2, 20)


# ### Evaluation function to determine the quality of a given ordering of colours
# 
# When solving the problem using optimisation heuristics, we need an evaluation function to measure the quality of a sulution. The problem is formulated as a minimisation  problem. We want to minimise the pair-wise distance between consequtive colours in the ordering. 
# 
# This function computes the quality of given ordering of colours. The smaller the evaluation function the better, as this is is formulated as a minimisation problem

# In[5]:


# This is an auxiliary function. It calculate the Euclidean distance between two individual colours
# Input: v and u as to be numpy arrays, vectors of real numbers with the RGB coordinates.

def euclid(v, u):
    return np.linalg.norm(v - u)

# Evaluation function.  Measures the quality of a given solution (ordering of colours) 
# The function computes the sum of the distances between all consecutive colours in the ordering
# Input: cols: list of colours 
#        ordc: ordering of colours
# Output: real number with the sumf of pair-wise differences in the colour ordering

def evaluate(cols, ordc):     
    adjacentColPairs = [[cols[ordc[i]],cols[ordc[i-1]]] for i in range(1,len(ordc))]
    return sum([euclid(i[1], i[0]) for i in adjacentColPairs])


# #### Evaluating the quality of given solutions
# 
# Let us use the evaluation function to calculate the quality of the arbitrary orderings of colours *order1* and *order2*

# In[6]:


e1 = evaluate(colors, order1)
print(f'Evaluation of order1: {e1}') # Displaying all decimals
print(f'Evaluation of order1: {np.round(e1,4)}') # rounding to display only 4 decimals. This is better for display

e2 = evaluate(colors, order2)
print(f'Evaluation of order1: {e2}') # Displaying all decimals
print(f'Evaluation of order1: {np.round(e2,4)}') # rounding to display only 4 decimals. This is better for display


# # Random Neighbour
The random neighbour function uses a 2-bit flip mutation on the solution it receives by swapping two randomly generated index values. The resulting solution (known as the random neighbour) is then returned for evaluation. The function also keeps track of all visited solutions so that it only returns solutions which haven't been explored. The 2 bit flip was chosen because its a simple but effective algorithm which can help the multi hill reach the local maximum faster. 
# In[7]:


def random_neighbour(solution):
    rand_index = rnd.randint(0, len(solution) - 1)
    rand_index_2 = rnd.randint(0, len(solution) - 1)

    while rand_index == rand_index_2: # Ensures that the two random indexes are not the same
        rand_index_2 = rnd.randint(0, len(solution) - 1)

    solution[rand_index], solution[rand_index_2] = solution[rand_index_2], solution[rand_index] # Swaps the two index values

    return solution


# # Visualizing Performance 
This function plots the line diagram for the initial run of the multi hill and the hill climbing diagram to illustrate their performance. 
# In[8]:


# A plot function to visualise the performance of the multihill algorithm
def plot_trace(algorithm, trace):
    
    plt.figure()
    plt.plot(trace, linewidth=2, color="blue")
    plt.title(algorithm)
    plt.ylabel('Value')
    plt.show()


# # Hill Climbing

# The hill climbing generates a random solution and iteratively calls the random neighbour function a specified amount of times. With each run it keeps track of the best solution found and returns this best solution where ever its called from. 

# In[9]:


def hill_climbing(iterations):
    solution_trace = [] # Keeps a track of all improving solution values
    rand_solution = random_sol()
    best_solution = rand_solution.copy()
    lowest_sum = evaluate(colors, rand_solution)
    solution_trace.append(lowest_sum)
    solution_visited = []
    

    for x in range(iterations):
            rand_neighbour = random_neighbour(rand_solution) # Random neighbour
            
            if rand_neighbour not in solution_visited: # Does not evaluate a solution which has already occured before
                rand_sum = evaluate(colors, rand_neighbour)

                if rand_sum < lowest_sum: # If the random neighbour is less than the current smallest evaluation value, it becomes the best solution
                    lowest_sum = rand_sum
                    best_solution = rand_neighbour.copy()
                    solution_trace.append(lowest_sum)

    return best_solution, solution_trace


# In[10]:


hill_solution, hill_trace = hill_climbing(10)
print("Evaluation Values: ", evaluate(colors, hill_solution))
plot_trace("Hill Climbing", hill_trace)


# # Multi Hill Climbing

# Multi hill climbing calls the hill climbing function a specified number of times. The algorithm improves by iteratively comparing its best solution against the best solution found by the hill climbing. 

# In[11]:


def multi_hill_climbing(multi_tries, hill_iterations):
    solution_trace = [] # Keeps a track of all improving solution values
    best_solution = random_sol()
    lowest_sum = evaluate(colors, best_solution)
    solution_trace.append(lowest_sum)
    solution_visited = []

    for x in range(multi_tries):
        hill_sol, trace = hill_climbing(hill_iterations)
        
        if hill_sol not in solution_visited: # Does not evaluate a solution which has already occured before
            rand_sum = evaluate(colors, hill_sol) # Random neighbour
            solution_visited.append(hill_solution)

            if rand_sum < lowest_sum:  # If the random neighbour is less than the current smallest evaluation value, it becomes the best solution
                lowest_sum = rand_sum
                best_solution = hill_sol.copy()
                solution_trace.append(lowest_sum)

    return best_solution, solution_trace


# In[12]:


multi_solution, multi_hill_trace = multi_hill_climbing(10, 10)
print("Evaluation Value: ", evaluate(colors, multi_solution))
plot_trace("Multi Hill Climbing", multi_hill_trace)


# # Analysis

# In[13]:


## The function runs the multi hill algorithm a specified number of times and keeps track of the best results found in each run
def multi_hill_best(multi_tries, hill_iterations, cols):
    global colors
    global ncolors
    ncolors, colors = read_data(cols) # Updating the colors to the appropriate method call
    solution_list = []
    values_list = []

    hill_sol, trace = multi_hill_climbing(multi_tries, hill_iterations)
    sol_value = evaluate(colors, hill_sol)

    return hill_sol, sol_value


# In[14]:


## Function for printing the best solution and its evaluation
def print_best(solutions, values, size):
    index = list(range(len(solution_list)))
    solution_collection = list(zip(index, solutions, values)) # Creating a value-solution dictionary
    solution_collection = sorted(solution_collection, key=lambda item: item[2], reverse=False) # Sorting it with value ascending order
    
    print(f'Best Solution: {solution_collection[0][1]}\n')
    print(f'Evaluation Value: {solution_collection[0][2]}\n\n')
    plot_colors(colors, solution_collection[0][1], size)


# In[15]:


## Function to generate a dataframe report of the results
def generate_report(multi_iter, hill_iter, value_list):
    
    index = list(range(len(solution_list)))
    solution_collection = list(zip(index, multi_iter, hill_iter, value_list)) # Creating a iterations-value dictionary
    solution_collection = sorted(solution_collection, key=lambda item: item[1], reverse=False) # Sorting with value ascending order
    
    frame_data = {'Multi hill iterations': multi_iter, 'Hill iterations': hill_iter, 'Evaluation': value_list}
    algorithm_report = pd.DataFrame(data = frame_data)

    return algorithm_report


# ### Multi-Hill Best 100
The main experimentation was done on this section by running the multi hill algorithm numberous times and monitoring the values found in each run. Instead of randomly guessing which iterations to use, a "for loop" was used to run the multi hill algorithm numbers times, manipulating he iterations with each run. The idea was to see which number of iterations produced the best results. 

In the particular run below for example the algorithm runs 10 times. In each run the multi hill tries are incremented by 50 and the hill tries are incremented by 100. The results are then displayed in table form for evaluation. Other tests conducted included only incrementing the hill climbing iterations, only incrementing multi hill tries, using the same amount of iterations with each run etc. The best solution found was:

 - Multi_Hill_Climbing_Best_100_Solution = [77, 61, 4, 56, 46, 48, 19, 15, 2, 51, 63, 41, 1, 33, 0, 75, 18, 25, 90, 32, 28, 89, 6, 57, 94, 74, 16, 38, 14, 5, 10, 64, 85, 65,    49, 86, 27, 88, 67, 76, 83, 59, 78, 69, 54, 95, 35, 44, 24, 66, 81, 11, 20, 36, 70, 53, 47, 23, 50, 52, 91, 43, 37, 31, 34, 9, 80, 45, 13, 73, 7, 12, 84, 26, 79, 42, 17,      21, 68, 29, 39, 62, 93, 82, 60, 30, 3, 55, 87, 8, 71, 58, 92, 72, 22, 40]

- Multi_Hill_Climbing_Best_100_Value = 50.766315

- Multi Hill Iterations = 500

- Hill Climbing Iterations = 50000


# In[16]:


runs = 10

multi_tries, hill_iterations = 0, 0
multi_tries_list, hill_tries_list, values_list, solution_list = [], [], [], []

# The loop runs n times and the best solution found is recorded to compare results
for run in range(runs):
    multi_tries += 50
    hill_iterations += 100
    mhc_best_100, mhc_100_value  = multi_hill_best(multi_tries, hill_iterations, "col100.txt")

    multi_tries_list.append(multi_tries)
    hill_tries_list.append(hill_iterations)
    solution_list.append(mhc_best_100)
    values_list.append(mhc_100_value)

print_best(solution_list, values_list, 50)
run_results = generate_report(multi_tries_list, hill_tries_list, values_list)
run_results


# In[ ]:





# ### Multi-Hill Best 500

# In[18]:


runs = 5
multi_tries, hill_iterations = 0, 0
multi_tries_list, hill_tries_list, values_list, solution_list = [], [], [], []

for run in range(runs):
    multi_tries = 10
    hill_iterations = 100
    mhc_best_500, mhc_500_value = multi_hill_best(multi_tries, hill_iterations, "col500.txt")

    multi_tries_list.append(multi_tries)
    hill_tries_list.append(hill_iterations)
    values_list.append(mhc_500_value)
    solution_list.append(mhc_best_500)

print_best(solution_list, values_list, 150)
run_results = generate_report(multi_tries_list, hill_tries_list, values_list)
run_results

Best Solution: [436, 390, 40, 147, 224, 261, 284, 164, 402, 240, 69, 117, 410, 181, 439, 419, 485, 288, 57, 180, 286, 395, 458, 316, 31, 0, 238, 358, 76, 360, 194, 326, 367, 229, 208, 144, 166, 1, 235, 253, 297, 46, 178, 493, 351, 103, 61, 88, 415, 198, 387, 366, 495, 123, 454, 324, 138, 298, 446, 257, 50, 305, 373, 483, 269, 145, 304, 312, 250, 106, 277, 183, 308, 243, 274, 174, 348, 287, 83, 217, 295, 440, 380, 259, 4, 93, 254, 438, 323, 34, 464, 302, 120, 124, 378, 201, 141, 291, 71, 341, 460, 114, 386, 67, 492, 281, 398, 130, 469, 105, 168, 47, 268, 121, 264, 207, 392, 58, 473, 80, 36, 11, 158, 280, 479, 127, 3, 342, 139, 152, 470, 148, 149, 192, 119, 195, 482, 230, 362, 52, 350, 299, 212, 184, 220, 370, 252, 84, 48, 9, 13, 347, 401, 49, 411, 494, 242, 193, 417, 185, 53, 455, 51, 344, 112, 21, 248, 346, 135, 443, 317, 222, 159, 394, 156, 459, 142, 310, 172, 434, 359, 260, 330, 371, 475, 356, 189, 352, 383, 487, 354, 315, 197, 321, 125, 337, 35, 445, 99, 480, 89, 472, 111, 8, 109, 375, 202, 389, 231, 41, 416, 476, 205, 101, 236, 432, 272, 86, 28, 173, 276, 361, 491, 334, 449, 245, 368, 328, 340, 25, 218, 163, 196, 79, 488, 169, 175, 115, 309, 467, 70, 313, 484, 59, 399, 16, 223, 95, 391, 37, 307, 428, 382, 209, 457, 322, 162, 72, 176, 412, 188, 22, 20, 104, 213, 6, 18, 452, 405, 478, 461, 404, 262, 379, 349, 33, 413, 134, 329, 331, 279, 237, 318, 239, 377, 87, 113, 294, 429, 256, 90, 407, 64, 153, 285, 388, 466, 182, 335, 481, 132, 421, 300, 118, 27, 396, 333, 327, 376, 433, 441, 128, 108, 19, 283, 265, 161, 369, 448, 73, 44, 206, 204, 336, 60, 32, 247, 301, 465, 275, 303, 365, 170, 422, 468, 338, 177, 155, 56, 293, 425, 273, 26, 186, 486, 38, 116, 91, 431, 133, 444, 471, 385, 244, 311, 211, 357, 447, 426, 267, 151, 462, 179, 24, 363, 199, 353, 10, 102, 314, 219, 39, 226, 2, 14, 81, 292, 453, 29, 233, 381, 85, 456, 489, 339, 107, 214, 122, 463, 7, 30, 296, 437, 450, 42, 92, 343, 320, 255, 221, 75, 474, 332, 306, 55, 129, 154, 131, 400, 418, 17, 66, 423, 325, 200, 137, 187, 23, 290, 203, 271, 241, 451, 234, 263, 427, 442, 364, 289, 77, 397, 435, 319, 63, 100, 15, 126, 490, 167, 393, 374, 345, 190, 82, 54, 78, 94, 62, 68, 136, 232, 157, 372, 215, 420, 216, 5, 384, 171, 165, 74, 210, 409, 258, 278, 249, 403, 143, 246, 228, 477, 43, 227, 65, 140, 266, 110, 430, 45, 146, 191, 97, 408, 150, 282, 355, 98, 414, 225, 424, 251, 270, 12, 406, 160, 96]

- Multi_Hill_Climbing_Best_500_Value = 301.981013

- Multi Hill Iterations = 50

- Hill Climbing Iterations = 1000
# In[ ]:




