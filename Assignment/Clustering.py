#!/usr/bin/env python
# coding: utf-8

# ## Clustering Methods

# In[1]:


import numpy as np      # Numerical library, used keeing the list of colours and computing the Euclidean distance

# Read in the color data file 
# Input: string with file name
# Oputput: the number of colours (integer), and a list numpy arrays with all the colours
def read_data(fname):
    cols = np.loadtxt(fname, skiprows = 4) # The first 4 lines have text information, and are ignored     
    ncols = len(cols)     # Total number of colours and list of colours
    return ncols,cols


# In[2]:


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
    


# In[3]:


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


# ### Converting the data into a Dataframe

# After calling the load_data function - load_dataframe converts the numpy array into a dataframe so that it can be easily explored and manipulated using the pandas and scikit learn libraries. The function assigns headers to the data corresponding to each colour column and returns the data with a generated index.
# 
# NOTE: To run the different color files just uncomment desired file below and comment out the files not in use.

# In[4]:


import pandas as pd
import numpy as np


ncolors, colors = read_data("col100.txt")
#ncolors, colors = read_data("col500.txt")

def load_dataframe(colors):
    data = pd.DataFrame(np.array(colors), columns=['Red', 'Green', 'Blue'])
    return data

data = load_dataframe(colors)

print(data)


# 

# ### Hierarchical Clustering 

# Aggolmerative clustering is a common Hierarchical bottom up approach that starts with an observation at each point in the data ( if there are 500 points in the data, it will start with 500 observations). From here, at each point it uses a proximity function (in our case- the Euclidean distance) to determine its closest neighbour. After determining it's closest neighbour, it expands the observation to include that closet point. Therefore creating a cluster of two points. The algorithm then repeats this process for each new observation - taking it's central point and calculating the euclidean distances of the surrounding neighbours to determine the next nearest point, each time adding the closest neighbour to the cluster. A Dendrogram provides a method of visualising the change in each cluster and the increase in size. Number of clusters to be produced can be specified, and the algorithm will stop once all points have been grouped into the specified number of clusters.
# 
# The decision to use hierarchical agglomerative clustering was made as it is more flexible when manipulating data, as it does not necessarily have to use a distance value and can be used on non numerical data. Even though both of those conditions are satisfied in this experiment, due to it's popularity and relatively good performance, and multiple use cases in real-world application - we chose to employ hierarchical agglomerative when organising the color palettes.

# In[5]:


import scipy.cluster.hierarchy as shc
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering 

def agglomerative(number_of_clusters, linkage, data):
    acluster = AgglomerativeClustering(n_clusters = number_of_clusters, linkage=linkage)
    agg_clusters = acluster.fit_predict(data)
    return agg_clusters


# ### Sorting data by cluster

# Assigns each colour to a cluster and appends cluster column to dataframe. Dataframe columns are then sorted by cluster and the reordered indexes produce the solution.

# In[6]:


def organise_by_cluster(data, ncolors, agg_clusters):

    data['Cluster'] = agg_clusters 
    data.groupby('Cluster').size()
    agg_data_ordered = data.sort_values('Cluster')
    agg_data_top = agg_data_ordered.head(ncolors)
    agg_solution = list(agg_data_top.index.values)
    return agg_solution


# ### Running the model

# Specify data, number of desired clusters (float, int) and linkage type(String) - e.g. 'ward', 'single', 'complete'. Returns colour palette and euclidean distance evaluation metric.

# In[7]:



def run_model(data, clusters, linkage):

    linkage_method = linkage
    Agg_clusters = agglomerative(clusters, linkage_method, data)
    solution = organise_by_cluster(data, ncolors, Agg_clusters)
    evaluation_metric = evaluate(colors, solution)
    
    return evaluation_metric, solution


# ### Running the model multiple times

# Multi_tries function loops the clustering algorithm multiple times, specified by the parameter 'tries'(int). 
# Assigns produced metric and solution parameters each time to "best" variables, and compares each iteration result with the 
# previous, if the metric of an iteration is found to be lower than the previous iteration metric, the former is assigned to 
# the best_metric variable and the solution assigned to the best_solution variable. The number of clusters of the best solution is also recorded. The function then returns the best solution, metric and cluster number. It is also important to note that linkage must be specified as a parameter - as done previously.

# In[8]:



def multi_tries(tries, bsol, bmet, linkage):
    best_metric = bmet
    best_solution = bsol
    for x in range(tries):
        current_metric, current_solution = run_model(data, x+1, linkage)
    #Compare initial metric to current metric
        if current_metric < best_metric:
            best_metric = current_metric
            best_solution = current_solution.copy()
            clusters = x
            
    return best_solution, best_metric, clusters


# In[9]:


# Running the clustering algorithm on a small even amount of clusters with linkage ward to 
# get an intial base solution.

init_metric, init_solution = run_model(data, 8, 'ward')
print('Initial solution evaluation metric: ' + str(init_metric))
print('Initial Solution palette: ')
plot_colors(colors, init_solution, 60)






# ### Results

# Below are the best found evaluation metrics taken from runs on diffrent linkage methods on the 10, 100 and 500 color files:
# 
# COL100
# -----------
# With 80 runs
# 
# Best evaluation was found with ward linkage: 26.760 - 22 clusters
# 
# COL500
# -----------
# With 200 runs
# 
# Best evaluation was found with ward linkage : 102.743 - 53 clusters 
# 
# 

# ### Visualising Linkage

# Below are the different dendrograms for the different linkage methods:

# In[10]:


plt.title('Ward Linkage Diagram')
shc.dendrogram(shc.linkage(data, method='ward'))
plt.xlabel('Colors'), plt.ylabel('Depth')


# In[11]:


plt.title('Single Linkage Diagram')
shc.dendrogram(shc.linkage(data, method='single'))
plt.xlabel('Colors'), plt.ylabel('Depth')


# In[12]:


plt.title('Complete Linkage Diagram')
shc.dendrogram(shc.linkage(data, method='complete'))
plt.xlabel('Colors'), plt.ylabel('Depth')


# In[13]:


plt.title('Average Linkage Diagram')
shc.dendrogram(shc.linkage(data, method='average'))
plt.xlabel('Colors'), plt.ylabel('Depth')


# ### Running on different linkages 

# Below are multiple algorithm runs (200 runs) on four diffrent linkage types and their results: 

# In[14]:


sol, metric, clusters = multi_tries(80, init_solution, init_metric, 'ward')

print('RAN ON WARD LINKAGE')
print('Best evaluation metric is: ' + str(metric))
print('Best number of clusters is: ' + str(clusters))
plot_colors(colors, sol, 60)


# In[15]:


sol, metric, clusters = multi_tries(80, init_solution, init_metric, 'single')

print('RAN ON SINGLE LINKAGE')
print('Best evaluation metric is: ' + str(metric))
print('Best number of clusters is: ' + str(clusters))
plot_colors(colors, sol, 60)


# In[16]:


sol, metric, clusters = multi_tries(80, init_solution, init_metric, 'complete')

print('RAN ON COMPLETE LINKAGE')
print('Best evaluation metric is: ' + str(metric))
print('Best number of clusters is: ' + str(clusters))
plot_colors(colors, sol, 60)


# In[17]:


sol, metric, clusters = multi_tries(80, init_solution, init_metric, 'average')

print('RAN ON AVERAGE LINKAGE')
print('Best evaluation metric is: ' + str(metric))
print('Best number of clusters is: ' + str(clusters))
plot_colors(colors, sol, 60)


# In[18]:


#run_model(data, 46, 'complete')


# In[ ]:




