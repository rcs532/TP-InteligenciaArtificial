# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    util.raiseNotDefined()


#python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs  comando para ejecutar
 

def breadthFirstSearch(problem):
    node = {'state':problem.getStartState(), 'cost':0} #Me posiciono en el nodo inicial, y llevo registro del costo
    if(problem.isGoalState(node['state'])): 
        return [] #si comienzo en la meta entonces no retorno acciones para hacer
    frontier = util.Queue()
    frontier.push(node) # Se crea un queue FIFO con node como el unico elemento
    explored=set() #declaramos un set vacio para llevar registro de que exploramos

    while True:
        if frontier.isEmpty():
            raise Exception("Search failed")

        node= frontier.pop()

        explored.add(node['state'])
        #ahora empezamos a ver a los sucesores
        successors = problem.getSuccessors(node['state'])
        for successor in successors:
            #creamos un nodo hijo y manejamos su estado, accion, costo y su nodo padre
            child = {'state':successor[0], 'action':successor[1], 'cost':successor[2], 'parent':node}
            #si el estado del hijo no esta en explorados
            if(child['state'] not in explored):
                #si llegamos a la meta
                if(problem.isGoalState(child['state'])):
                    actions = []
                    node = child
                    while 'parent' in node:
                        actions.append(node['action'])
                        node = node['parent']
                    actions.reverse()    
                    return actions
                #sino insertamos al hijo a la frontera
                frontier.push(child)



    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
