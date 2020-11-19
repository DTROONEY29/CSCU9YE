#!/usr/bin/env python
# coding: utf-8

# # Internal Cluster Iterative Local Search  

# ### Reading the data file 

# In[1]:


import numpy as np      # Numerical library, used keeing the list of colours and computing the Euclidean distance

# Read in the color data file 
# Input: string with file name
# Oputput: the number of colours (integer), and a list numpy arrays with all the colours
def read_data(fname):
    cols = np.loadtxt(fname, skiprows = 4) # The first 4 lines have text information, and are ignored     
    ncols = len(cols)     # Total number of colours and list of colours
    return ncols,cols


# Use this function to specify which file to run:

# In[2]:


def specify_file(file):
    spec_file = file
    return spec_file


# In[3]:


# This is where you specify which file to use

s_file = specify_file('col100.txt')


# #### Read and explore the data file: either the 10, 100, or 500 colours dataset
# 
# The colorus are stored in a list, where each element of the list is a numpy array of dimension 3. That is arrays of 3 real numbers where the real numbers indicate the R,G, and B values of the colour (RGB colour model). 

# In[4]:


ncolors, colors = read_data(s_file)
restricted_ncolors, restricted_colors = read_data(s_file)


# ### Plotting a sequence of colours
# 
# The function <b>plot_colors()</b> displaysthe colours from the color list *col_list* the order given by the *col_order* list. 
# 
# *col_list* and *col_order* need to be of the same length. The *ratio* parameter indicates height/width proportion of each bar of colour in the plot.

# In[5]:


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


# ### Evaluation function to determine the quality of a given ordering of colours
# 
# When solving the problem using optimisation heuristics, we need an evaluation function to measure the quality of a sulution. The problem is formulated as a minimisation  problem. We want to minimise the pair-wise distance between consequtive colours in the ordering. 
# 
# This function computes the quality of given ordering of colours. The smaller the evaluation function the better, as this is is formulated as a minimisation problem

# In[6]:


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


# In[7]:


import random as rnd

def random_sol():
    sol = list(range(ncolors))   # list of consequtive numbers from 0 to ncolors
    # Shuffle the elements in the list randomly. Shuffles in place and doesn’t retunr a value
    rnd.shuffle(sol)   
    return sol


# ## Random Neighbour Function

# In[8]:


def random_neighbour(solution):
    rand_index = rnd.randint(0, len(solution) - 1)
    rand_index_2 = rnd.randint(0, len(solution) - 1)

    while rand_index == rand_index_2: # Ensures that the two random indexes are not the same
        rand_index_2 = rnd.randint(0, len(solution) - 1)

    solution[rand_index], solution[rand_index_2] = solution[rand_index_2], solution[rand_index]

    return solution


# ## Visualizing Performance 

# In[9]:


def plot_trace(algorithm, trace):
    plt.figure()
    plt.plot(trace, linewidth=2, color="blue")
    plt.title(algorithm)
    plt.ylabel('Value')
    plt.show()


# ## Clustering

# This function is explained in the accompanying clustering notebook.

# In[10]:


import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering
import pandas as pd

def load_dataframe(cols):
    color_data = pd.DataFrame(np.array(cols), columns=['Red', 'Green', 'Blue'])
    return color_data

data = load_dataframe(colors)

def agglomerative(number_of_clusters, linkage, data):
    acluster = AgglomerativeClustering(n_clusters = number_of_clusters, linkage=linkage)
    agg_clusters = acluster.fit_predict(data)
    return agg_clusters, number_of_clusters

def organise_by_cluster(data, ncolors, agg_clusters):

    data['Cluster'] = agg_clusters
    data.groupby('Cluster').size()
    agg_data_ordered = data.sort_values('Cluster')
    agg_data_top = agg_data_ordered.head(ncolors)
    agg_solution = list(agg_data_top.index.values)
    return agg_solution, agg_data_ordered


# ## Clustering Local Search

# The Clustering Local Algorithm aims to cluster the colors and then perform the local search algorithm within each cluster. Local search was chosen over multi hill because it reaches the local maximum faster than the former.

# In[11]:


def hill_climbing(sol, iterations):
    best_solution = sol.copy()
    lowest_sum = evaluate(colors, best_solution)

    for x in range(iterations):
        rand_neighbour = random_neighbour(best_solution)  #
        neighbour_sum = evaluate(colors, rand_neighbour)

        if neighbour_sum < lowest_sum:  # Loop is only entered when the swapped sum is smaller than current lowest sum
            lowest_sum = neighbour_sum
            best_solution = rand_neighbour.copy()

    return best_solution


def iterated_local_search(tries, hill_tries):
    initial_solution = random_sol()
    best_value = evaluate(colors, initial_solution)
    best_solution = hill_climbing(initial_solution, hill_tries)
    trace = []

    for x in range(tries):
        hill_solution = hill_climbing(random_neighbour(best_solution), hill_tries)
        hill_solution_value = evaluate(colors, hill_solution)
        trace.append(hill_solution_value)

        if hill_solution_value < best_value:
            best_solution = hill_solution.copy()
            best_value = hill_solution_value

    return best_solution


def internal_cluster_iterative_local_search(agg_data_ordered, nclusters):
    global colors;
    global ncolors;

    # Create list to hold final solution
    
    internal_cluster_iterative_local_search_solution = []
    
    # Loop iterates through specified number of clusters so it can access the color values and associated indexes 
    # of each cluster
    for x in range(n_clusters):
        
        # takes list of all colours and their associated indexes within specified cluster
        indexes = data.loc[data['Cluster'] == x].index.values.tolist()
        # creates new color dataframe from original to be used in iterative local search algorithm
        colors_data = data.loc[data['Cluster'] == x]
        
        # converts new dataframe into a numpy array and assigns it to the global colors variable - so as the 
        # algorithm iterates the iterative local search uses the correct data each time and not the original color file
        # - Therefore the original colors variable is updated in each iteration (different clusters will have a different
        # amount of colors).
        colors = colors_data[["Red", "Green", "Blue"]].to_numpy()
        # Takes length of new data 'colors' and assigns it to global ncolors variable so it iterative local 
        # search uses correct value in each iteration.
        ncolors = len(colors)
        
        # After passing through algorithm the newly ordered colors are assigned to solution variable
        solution = iterated_local_search(150, 2000)
        # the order of the new solution is stored in variable order
        order = solution 
        # A new list is created to store the indexes of the index list
        indexes_index_list = list(range(ncolors))
        # The new ordering in order is applied to the index of 'indexes' from the original color file, 
        #t herefore rearranging them:
        indexes_solution = [indexes[i] for i in order]
        # Newly ordered group of indexes(these are the roriginal indexes from the color file after undergoing
        # clustering) are appended cluster by cluster in original order into a new solution list
        internal_cluster_iterative_local_search_solution.extend(indexes_solution)
       # returns new solution
    return internal_cluster_iterative_local_search_solution


# In[12]:


print(ncolors)


# Our algorithm uses an initial solution from the agglomerative clustering algorithm. Each cluster is then extracted from the solution using the corresponding dataframe. The colors within each cluster are then ran through iterated local search and returned with their new ordering to a new solution list. This works on a cluster-by-cluster level aiming to improve upon the clustering algorithm within a small margin. Local search was chosen over multi hill because it reaches the local maximum faster than the former. 
# 
# As can be seen below - ran on the same parameters the new algorithm improves on the intial solution.
# 

# In[13]:


agg_clusters, n_clusters = agglomerative(22, 'ward', data)
agg_solution, agg_data_ordered = organise_by_cluster(data, ncolors, agg_clusters)
solution = internal_cluster_iterative_local_search(agg_data_ordered, n_clusters)
print(solution)
plot_colors(restricted_colors, solution, 40)
evalinit = evaluate(restricted_colors, agg_solution)
evalmet = evaluate(restricted_colors, solution)
print('Initial Metric:' + str(evalinit))
print('New Evaluation metric: ' + str(evalmet))


# ## 100 Colors
22 Clusters were used for the clustering portion of the algorithm because the clustering done in our clustering notebook had already revealed that this was the best option. Since local search uses random solution trial and error was used to experiment with the iterations, however the results found in the multi hill climbing algorithm were used as a guide. In every run the algorithm always managed to improve the value of the original clustering solution. 

Initial Value: 28.602593421472132

After Local Search: 28.02620212594869

Local Search Tries:150
    
Multi-Hill Tries: 2000

Local Search Solution: [90, 30, 87, 45, 39, 23, 49, 74, 48, 55, 22, 44, 72, 51, 24, 35, 18, 46, 79, 86, 75, 69, 58, 25, 5, 14, 12, 53, 33, 36, 56, 3, 73, 64, 89, 63, 47, 38, 21, 26, 52, 67, 1, 88, 65, 42, 34, 11, 95, 70, 10, 91, 2, 8, 82, 15, 43, 80, 60, 6, 54, 31, 0, 81, 93, 19, 66, 77, 16, 50, 84, 78, 94, 37, 28, 7, 40, 20, 13, 57, 59, 83, 17, 92, 32, 68, 29, 76, 61, 9, 85, 4, 27, 71, 62, 41]
# ## 500 Colors
53 Clusters were used for the clustering portion for the same reasons discussed in the 100 colors section.

Initial Metric: 108.26328981052588

After Local Search: 104.39939912561579
    
Local Search Tries: 200
    
Multi-Hill Tries: 1000

Local Search Solution: [28, 150, 227, 422, 146, 37, 451, 459, 50, 280, 408, 184, 492, 198, 475, 225, 196, 333, 320, 396, 454, 276, 491, 117, 2, 490, 8, 427, 447, 172, 211, 330, 311, 495, 303, 106, 461, 382, 128, 421, 235, 301, 317, 429, 201, 77, 16, 219, 175, 122, 189, 424, 340, 97, 386, 110, 223, 339, 30, 118, 279, 87, 261, 90, 375, 472, 55, 151, 166, 260, 23, 39, 111, 463, 387, 180, 250, 74, 49, 22, 285, 372, 402, 347, 308, 441, 126, 64, 315, 3, 73, 203, 477, 153, 224, 468, 134, 136, 407, 89, 218, 230, 109, 452, 63, 331, 246, 168, 266, 130, 107, 273, 367, 488, 398, 120, 448, 176, 309, 212, 269, 381, 366, 226, 214, 94, 465, 385, 163, 284, 45, 419, 316, 210, 215, 13, 485, 20, 341, 161, 393, 216, 7, 200, 247, 327, 469, 233, 15, 356, 318, 193, 394, 323, 82, 217, 388, 156, 471, 239, 46, 255, 444, 376, 18, 167, 242, 336, 479, 206, 17, 392, 102, 32, 147, 92, 268, 351, 439, 287, 59, 374, 121, 83, 334, 69, 186, 265, 142, 417, 86, 483, 61, 322, 428, 129, 174, 165, 420, 449, 21, 178, 493, 431, 361, 335, 85, 135, 277, 379, 259, 423, 243, 72, 0, 24, 31, 363, 98, 294, 6, 43, 60, 114, 354, 486, 403, 305, 383, 80, 12, 159, 484, 262, 314, 33, 349, 291, 344, 404, 302, 437, 138, 377, 1, 399, 99, 205, 412, 473, 54, 237, 397, 328, 173, 434, 310, 170, 220, 416, 36, 462, 222, 155, 171, 258, 25, 357, 56, 430, 53, 238, 52, 321, 267, 228, 67, 256, 389, 119, 440, 414, 91, 400, 304, 116, 278, 187, 48, 199, 425, 144, 355, 438, 240, 263, 4, 295, 207, 9, 244, 369, 160, 57, 313, 141, 209, 245, 137, 358, 442, 332, 410, 44, 51, 35, 93, 66, 286, 103, 81, 411, 113, 289, 38, 415, 182, 26, 112, 221, 194, 352, 378, 68, 29, 188, 132, 125, 337, 76, 360, 152, 348, 342, 368, 42, 234, 474, 282, 395, 185, 312, 65, 145, 229, 169, 241, 481, 149, 140, 296, 409, 353, 249, 436, 133, 75, 418, 58, 213, 139, 297, 457, 489, 306, 329, 70, 105, 325, 467, 190, 464, 10, 455, 158, 183, 433, 345, 470, 231, 292, 371, 236, 101, 232, 127, 391, 307, 458, 177, 40, 123, 96, 14, 487, 11, 401, 271, 41, 71, 450, 446, 104, 100, 413, 272, 281, 364, 192, 164, 204, 406, 443, 197, 79, 426, 370, 300, 248, 482, 95, 275, 257, 319, 208, 253, 456, 466, 365, 270, 350, 154, 445, 157, 181, 62, 293, 27, 494, 460, 435, 195, 264, 299, 34, 108, 298, 162, 326, 84, 373, 390, 78, 191, 47, 476, 432, 124, 143, 131, 202, 88, 405, 359, 283, 288, 290, 254, 252, 5, 343, 148, 453, 338, 274, 380, 362, 346, 324, 179, 251, 384, 115, 480, 478, 19]
    
