Uninformed Tree based search -------------

- A solution is an action sequence

- Search algorithms work by considering various possible action sequences(plans)

Two types of tree-based search algorithms:
- Uninformed(blind) algorithms
- Informed algorithms

---- State space graphs -----

A mathematical representation of a search problem.

- Nodes are (abstracted) world configurations
- Arcs represent successors (action results)
- The goal test is a given node or set of nodes.

IN A STATE SPACE GRAPH, EACH STATE ONLY APPEARS ONCE!

--------------------------------------------------------

State space graph: Pac-man
---------------------------

How many states? 
- Pacman positions: 5x5 = 25
- Pacman Heading: N, S, E, W = 4
- Food pellets: 9, two states(eaten or not) so it becomes 9^2
- TOTAL STATES: 25*4*81 = 8100

In general the state space graph is too big to have in memory.
--------------------------------------------------------
Search Trees --------------------
---------------------------------
- Starting with a root node and applying the possible   actions to move to the next node.
- Children correspond to successors
- Nodes show states, but correspond to PLANS that achieve those states.
- For most problems, we can never actually build the whole tree.
--------------------------------------------------------
Searching with a search tree
----------------------------

- Expand out potential plans (tree nodes)
- Maintain a FRINGE of partial plans under construction 
- Try to expand as few tree nodes as possible.

--------------------------------------------------------
General Tree Search 
-------------------

General tree search function: 

![Function for a general search tree](https://github.com/[DTROONEY29]/[CSCU9YE]/Notes/[GenTreeSearchFunction]/.jpg?raw=true)
--------------------------------------------------------
Uninformed (Blind) search strategies
-------------------------------------
Use only the information available in the problem definition. Systematically generate new states, and test them against the goal.

Main strategies:
- Breadth First Search (BFS)
- Depth-First Search (DFS)

Improvements:
- Uniform cost search
- Depth-limited search
- Iterative deepening search

--------------------------------------------------------Breadth First Search 
--------------------

Strategy - Expand a shallowest node first 
Implementation - Fringe is a FIFO Queue

Depth First Search 
-------------------

Strategy - expand a deepest node first 
Implementation - Fringe is a LIFO stack 

IMPROVEMENTS ------------------------------

Uniform Cost Search
--------------------
- Improves BFS by always selecting the lowest cost fringe node from the start node for expansion

Depth Limited Search 
--------------------
- Avoid problems of DFS by imposing a maximum depth of path

Iterative Deepening Search
--------------------------
- Sidesteps teh issue of choosing the depth limit 
- Tries all possible depth limits: 0,1,1 etc.
-Combines the benefits of DFS nd BFS.

--------------------------------------------------------
Comparing search strategies - IMPORTANT!
---------------------------
- Completeness - does it always find a solution if one exists ?
- Time complexity - Number of nodes generated 
- Space complexity - Maximum number of nodes in memory 
- Optimality - Does it always find a least-cost solution?

------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Informed Tree based Search
--------------------------

- Use problem-specific knowledge 
- Knowledge is given by a HEURISTIC FUNCTION that returns a number describing the desirability (or lack thereof) of expanding a node.

Search Heuristics
-----------------
A HEURISTIC is:
- A function that estimates how close a state is to a goal
- Designed for a particular search problem.
- Examples: manhattan distance, euclidean distance.

--------------------------------------------------------

- Strategy: expand a node that you think is closest to a goal state.
- Idea: use a HEURISTIC FUNCTION for each node - estimate of "Desirability" ---> Expand most desirable unexpanded node.
- Implementation : A queue sorted in a decreasing order if desirability.

--------------------------------------------------------

Informed search - Algorithms
----------------------------

Greedy Search
-------------
- Chooses (expands) teh node that takes us closest to the goal at each branch of the tree(according to heuristic)

A* Search
----------
- Chooses (expands) on the least-cost solution path
- Combines; The cost of the path so far an dthe estimation of what is the node that takes us closer to the goal.