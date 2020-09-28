LECTURE 03 - SEARCH PROBLEMS

--------------- Meanings of search in CS --------------

- Search or store data
- Search for web documents
- Search for paths or routes
- Search for solutions

--------------- Search in AI -------------

Search for paths and routes -----------

Finding a set of actions that will bring us from an initial state to a goal state.
Algorithms:

- Depth first search
- Breadth first search
- Branch and bound
- A\*
- Monte Carlo tree search

Search for Solutions -----------

Find a solution in a large space of camdidate solutions
Algorithms:

- Evolutionary algorithms
- Metaheuristics
- Simulated annealing
- Ant colony optimisation

** More interested in the end product/solution

--------------------------------------------------------
Some examples of search problems:

- Robot vehicle would search for a route to a given destination.

- Air traffic control

--------------------------------------------------------
INTELLIGENT AGENTS
------------------

A rational agent chooses actions to maximise the expected utility.

Today; Agents that have a goal, and a cost (REach the goal at a lower cost)

** An agent perceives its environment through sensors and acts upon it` through actuators.

--------------------------------------------------------

Solving a problem by searching -------------------------

- Finding sequences of actions that lead to desirable   states

PROBLEM: A GOAL and a set of means to achive it
SOLUTION: A sequence of ACTIONS to achieve a goal

- Given a precise definition(a model of the problem) of a problem, it is possible to construct a search process for finding solutions.

--------- AN EXAMPLE --------

Environment: Maze, ghosts and dots 

To use search methods we need to use abstraction.

A SEARCH STATE keeps omnly the details needed for solving the problem.

A search problem consists of:

- A set of states (state space)
- A set of actions (transitions, costs)

A START STATE and a GOAL TEST.

******Abstraction*****
- STATES consider the only Pac-man immediate neighbourhood (3x3)
- ACTIONS: 4 moves with arrow keys(u, d, l, r)

-------------------------
A solution is a sequence of actions (a plan) which 3
transforms the start state to a goal state.

------ Pac man as a search problem ----

Problem: Find paths 
    - States: (x, y) ocation (3x3)
    - Actions: u, d, l, r
    - Successor: update location only
    - Goal test: (x,y) = END

Problem: Eat all dots
    - States: {(x, y), dot Booleans}
    - Actions; u, d, l, r
    - Successor: Update location and eat the dot
    - Goal test: Dots are all eaten

