import random as rnd
import matplotlib.pyplot as plt 


# Read the data given a file name. Returns: n = no. items, 
# c = capacity, vs: list of item values, ws: list of item weights

def read_knapsack_data(fname):
           
    with open(fname, 'r') as kfile:
        lines = kfile.readlines()     # reads the whole file
    n = int(lines[0])
    c = int(lines[n+1])
    vs = []
    ws = []
    lines = lines[1:n+1]              # Removes the first and last line
    for l in lines:
        numbers = l.split()           # Converts the string into a list
        vs.append(int(numbers[1]))    # Appends value, need to convert to int
        ws.append(int(numbers[2]))    # Appends weight, need to convert to int
    return n, c, vs, ws

# Reading data from a file, in this example the instance with 5 items
knapfile = "knap5.txt"     # filename, should be located in the same directory
n, c, values, weights = read_knapsack_data(knapfile)
print(f'values:  {values}\nweights: {weights}\nNumber of items: {n}. Weight Capacity: {c}')

# Reading data from a file
knapfile = "knap20.txt"     # filename, should be located in the same directory
n, c, values, weights = read_knapsack_data(knapfile)
# Print only the number of items and capacity
print(f'Number of items: {n}. Weight Capacity: {c}')

sol = rnd.choices([0,1], k=n)  # this create a random binary list of n elements, where n comes from the cell above
print(sol)



x = [weights]
y = [values]
plt.scatter(x, y, label="Dataset of 20", color="k")


#plt.label('x')
#plt.label('y') 
plt.title('Set of 5 Items')
plt.legend()
plt.show()

#This function should receive as input an integer number size and returns
#  a list of binary (1 and 0)  numbers of length size, generated uniformly at random.


def randomsol(size):

    random_generated_sol = rnd.choices([0,1], k=size)

    return random_generated_sol

#This function receives as input a binary list sol and returns two values,
#  tval, twei corresponding to the total sum of values and weights of the items,
#  respectively for the input solution.  Your function should detect whether the
#  input solution is invalid (i.e. if the total weight is greater than the capacity of the sack W).
#  If that is the case, then the function should return tval = 0.



def evaluate(sol):
    i = 0
    if sol[i] = "0":
        







#print(randomsol(10))
