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


#comando para ejecutar dfs python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
def depthFirstSearch(problem):
   #en frontier guardamos los estados a ser explorados
    frontier = util.Stack()
    #en explored vamos a ir llevando a quienes ya exploramos
    exploredNodes = []
    #definimos un nodo inicial
    startState = problem.getStartState()
    startNode = (startState, [])
    
    frontier.push(startNode) #empezamos explorando el primero
    
    while not frontier.isEmpty():
        currentState, actions = frontier.pop()
        
        if currentState not in exploredNodes:
            #marcamos el nodo actual como explorado
            exploredNodes.append(currentState)

            if problem.isGoalState(currentState):
                return actions
            else:
                #obtenemos la lista de todos los sucesores del nodo en forma de tupla (successor, action, stepCost)
                
                successors = problem.getSuccessors(currentState)
                
                #empujamos cada sucesor a la tupla ya que hay que explorarlo
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newNode = (succState, newAction)
                    frontier.push(newNode)

    return actions  
    
    util.raiseNotDefined()


#python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs  comando para ejecutar
def breadthFirstSearch(problem):
    node = {'state':problem.getStartState(), 'cost':0} #Me posiciono en el nodo inicial, y llevo registro del costo
    if(problem.isGoalState(node['state'])): 
        return [] #si comienzo en la meta entonces no retorno acciones para hacer
    frontier = util.Queue() #aqui guardamos los que todavia no hemos explorado
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



#comando para ejecutar : python pacman.py -l tinyMaze -p SearchAgent -a fn=ucs
def uniformCostSearch(problem):
    #Fifo queue para llevar registro de nodos no explorados
    frontier = util.PriorityQueue()

    #guarda los estados previamente explorados (para evitar ciclos), guarda stat:cost
    exploredNodes = {}
    
    startState = problem.getStartState()
    startNode = (startState, [], 0) #(state, action, cost)
    
    frontier.push(startNode, 0)
    
    while not frontier.isEmpty():
        #Empezamos explorando el primer nodo de costo mas bajo en la frontera
        currentState, actions, currentCost = frontier.pop()
       
        if (currentState not in exploredNodes) or (currentCost < exploredNodes[currentState]):
            #ponemos ese nodo en la lista de explorados
            exploredNodes[currentState] = currentCost

            if problem.isGoalState(currentState):
                return actions
            else:
                #lista de (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)
                
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newCost = currentCost + succCost
                    newNode = (succState, newAction, newCost)

                    frontier.update(newNode, newCost)

    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# python pacman.py -l trickySearch -p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=foodHeuristic
def aStarSearch(problem, heuristic=nullHeuristic):
     #nodos a explorar: tendra un item, costo+heuristica
    frontier = util.PriorityQueue()
    #nodos a explorar
    exploredNodes = [] #tendra (state, cost)

    startState = problem.getStartState()
    startNode = (startState, [], 0) #(state, action, cost)

    frontier.push(startNode, 0)

    while not frontier.isEmpty():

        #se comienza explorando el nodo (mas bajo combinando (cost+heuristic) )  en frontier
        currentState, actions, currentCost = frontier.pop()

        #se pone nodo actual en la lista de explorados
        currentNode = (currentState, currentCost)
        exploredNodes.append((currentState, currentCost))

        if problem.isGoalState(currentState):
            return actions

        else:
            #lista de (successor, action, stepCost)
            successors = problem.getSuccessors(currentState)

            #examina cada sucesor
            for succState, succAction, succCost in successors:
                newAction = actions + [succAction]
                newCost = problem.getCostOfActions(newAction)
                newNode = (succState, newAction, newCost)

                #se revisa si el sucesor ya fue explorado
                already_explored = False
                for explored in exploredNodes:
                    #se revisa la tupla de cada nodo explorado
                    exploredState, exploredCost = explored

                    if (succState == exploredState) and (newCost >= exploredCost):
                        already_explored = True

                #si el sucesor no ha sido explorado,se pone en la frontera y lista de explorado
                if not already_explored:
                    frontier.push(newNode, newCost + heuristic(succState, problem))
                    exploredNodes.append((succState, newCost))

    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
