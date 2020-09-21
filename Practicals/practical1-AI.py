# Calculate the volume of a sphere with radius 5

import math
import random as rnd 


# r = 5 

# volume = (4*math.pi)*(r**3)
# volume = volume//3

# print(str(volume))
# -------------------------------------------------- TASK 2 -----------------------------------------------------------------
# Your task is to implement a function called distance, that receives four paramenters the coordinates of 
# two points in the order:𝑥1,𝑦1,𝑥2,𝑦2, and calculates the Euclidean distance between the points (𝑥1,𝑦1) and (𝑥2,𝑦2)


#def distance(x1, y1, x2, y2):

 #   s1 = (x2 - x1)**2
  #  s2 = (y2 - y2)**2

   # output = math.sqrt(s1+s2)

    #print(str(output))

 # distance(1, 3, 6, 4)

# ------------------------------------------------------ TASK 3 -------------------------------------------------------------
# Your task is to create a list of numbers with the hypothetical ages of a group of people. 
# The ages will be randomly-generated, and we assume that the minimum age is 1 and the maximum 120. 
# You should create a function that creates the list, and also keeps the sum of all elements in the list.
# The sum is required to be able to compute the average age. Your function should receive as a parameter 
# the size of the group, and should return two values: a list of ages, and its average.

# Your function should print out the numbers as they are added to the list. 
# When calling your function, you should receive the two returning values as two separate variables.
# You should then also print out the two variables.

# Finally to test that your average computation is correct, you should compare your value with computing 
#the average using the predefined list function sum() which computes the sum of the elements in a list. 
# Whenever you print a variable, please include text to describe what the number represents.



def ages(size):
    
    listOfAges = [] * size
    count = 0

    while count <= size:
        randomAge = rnd.randint(1, 120)
        listOfAges.append(randomAge)
        print(str(randomAge))
        count = count + 1
    print(listOfAges)
    average = sum(listOfAges)//size
    print("Average age is: " + str(average))


ages(50)
