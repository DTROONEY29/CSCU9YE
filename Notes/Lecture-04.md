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

![alt text](http://![alt text](http://url/to/img.png)
)
