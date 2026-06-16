from collections import deque
from shutil import get_terminal_size
from heapq import heappush, heappop
from itertools import count
counter = count()
from random import choice, random
from math import exp
terminal_width, _ = get_terminal_size()
_visualizers = {}
_visualizers2 = {}

class Problem:
    '''
    Abstract base class for problem formulation.
    It declares the expected methods to be used by a search algorithm.
    All the methods declared are just placeholders that throw errors if not overriden by child "concrete" classes!
    '''

    def __init__(self):
        '''Constructor that initializes the problem. Typically used to setup the initial state and, if applicable, the goal state.'''
        self.init_state = None

    def actions(self, state):
        '''Returns an iterable with the applicable actions to the given state.'''
        raise NotImplementedError

    def result(self, state, action):
        '''Returns the resulting state from applying the given action to the given state.'''
        raise NotImplementedError

    def goal_test(self, state):
        '''Returns whether or not the given state is a goal state.'''
        raise NotImplementedError

    def step_cost(self, state, action):
        '''Returns the step cost of applying the given action to the given state.'''
        raise NotImplementedError
    
    def heuristic(self, state):
        '''Returns the heuristic value of the given state, i.e., the estimated number of steps to the nearest goal state.'''
        raise NotImplementedError

class Node:
    '''Node data structure for search space bookkeeping.'''
    
    def __init__(self, state, parent, action, path_cost, heuristic):
        '''Constructor for the node state with the required parameters.'''
        self.state = state
        self.parent = parent
        self.action = action
        self.g = path_cost
        self.h = heuristic
        self.f = path_cost + heuristic

    @classmethod
    def root(cls, problem):
        '''Factory method to create the root node.'''
        init_state = problem.init_state
        return cls(init_state, None, None, 0, problem.heuristic(init_state))

    @classmethod
    def child(cls, problem, parent, action):
        '''Factory method to create a child node.'''
        child_state = problem.result(parent.state, action)
        return cls(
            child_state,
            parent,
            action,
            parent.g + problem.step_cost(parent.state, action),
            problem.heuristic(child_state))

def solution(node):
    '''A method to extract the sequence of actions representing the solution from the goal node.'''
    actions = []
    cost = node.g
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    actions.reverse()
    return actions, cost

def bfs_tree(problem, verbose=False):
    '''Breadth-first tree search implementation.'''
    if problem.goal_test(problem.init_state): return solution(Node.root(problem.init_state))
    frontier = deque([Node.root(problem)])
    if verbose: visualizer = Visualizer(problem)
    while frontier:
        if verbose: visualizer.visualize(frontier)
        node = frontier.pop()
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            #print(child)
            if problem.goal_test(child.state):
                return solution(child)
            frontier.appendleft(child)

def bfs_graph(problem, verbose=False):
    '''Breadth-first graph search implementation.'''
    states = []
    if problem.goal_test(problem.init_state): return states.append(solution(Node.root(problem.init_state))), solution(Node.root(problem.init_state))
    frontier = deque([Node.root(problem)])
    explored = {problem.init_state}
    if verbose: visualizer = Visualizer(problem)
    while frontier:
        if verbose: visualizer.visualize(frontier)
        node = frontier.pop()
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            if child.state not in explored:
                if problem.goal_test(child.state):
                    print("child.state = ", child.state)
                    return states.append(solution(child)), solution(child)
                frontier.appendleft(child)
                explored.add(child.state)

def _default_visualizer(_, state):
    '''Generic visualizer for unknown problems.'''
    print(state)

class Visualizer:
    '''Visualization and printing functionality encapsulation.'''

    def __init__(self, problem):
        '''Constructor with the problem to visualize.'''
        self.problem = problem
        self.counter = 0

    def visualize(self, frontier):
        '''Visualizes the frontier at every step.'''
        self.counter += 1
        states = []
        #print(f'Frontier at step {self.counter}')
        for node in frontier:
            #print()
            newstate = _visualizers.get(type(self.problem), _default_visualizer)(self.problem, node.state)
            states.append(newstate)
        #print('-' * terminal_width)
        return states

def dfs(problem,verbose=False):
    while True:
        if problem.goal_test(problem.init_state): return solution(Node.root(problem.init_state))
        frontier = deque([Node.root(problem)])
        if verbose: visualizer = Visualizer(problem)
        childs=0
        while frontier:
            container=deque()
            if verbose: visualizer.visualize(frontier)
            node=frontier.pop()
            childs=0
            for action in problem.actions(node.state):
                child = Node.child(problem, node, action)
                if problem.goal_test(child.state):
                    return solution(child)
                container.append(child)
                childs+=1
            container.reverse()
            frontier.extendleft(container)

def ids(problem,verbose=False):
    limit=0
    while True:
        if problem.goal_test(problem.init_state): return solution(Node.root(problem.init_state))
        frontier = deque([Node.root(problem)])
        if verbose: visualizer = Visualizer(problem)
        layer=0
        childs=0
        while frontier:
            container=deque()
            if verbose: visualizer.visualize(frontier)
            node=frontier.pop()
            if(layer<=limit+1):
                childs=0
                for action in problem.actions(node.state):
                    child = Node.child(problem, node, action)
                    if problem.goal_test(child.state):
                        return solution(child)
                    container.append(child)
                    childs+=1
                container.reverse()
                frontier.extendleft(container)
                layer+=1
            else:
                childs-=1
                if(childs==0):
                    layer-=1
        limit+=1

def greedy_best_first(problem, verbose=False):
    '''Greedy best-first search implementation.'''
    frontier = [(None, None, Node.root(problem))]
    explored = set()
    if verbose: visualizer = Visualizer(problem)
    while frontier:
        if verbose: visualizer.visualize(frontier)
        _, _, node = heappop(frontier)
        if node.state in explored: continue
        if problem.goal_test(node.state):
            return solution(node)
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            if child.state not in explored:
                heappush(frontier, (child.h, next(counter), child))

def A_star(problem, verbose=False):
    frontier = [(None, None, Node.root(problem))]
    explored = set()
    if verbose: visualizer = Visualizer(problem)
    while frontier:
        if verbose: visualizer.visualize(frontier)
        _, _, node = heappop(frontier)
        if node.state in explored: continue
        if problem.goal_test(node.state):
            return solution(node)
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            if child.state not in explored:
                heappush(frontier, (child.f, next(counter), child))

def hill_climbing(problem, verbose=False):
    '''Hill climbing search implementation.'''
    current_state = problem.init_state
    current_value = problem.heuristic(current_state)
    if verbose: visualizer = Visualizer2(problem)
    while True:
        if verbose: visualizer.visualize([current_state])
        next_state, next_value = None, None
        for action in problem.actions(current_state):
            new_state = problem.result(current_state, action)
            new_value = problem.heuristic(new_state)
            if next_value is None or next_value > new_value:
                next_state, next_value = new_state, new_value
        if current_value <= next_value: return current_state
        current_state, current_value = next_state, next_value

def _default_visualizer2(_, state):
    '''Generic visualizer for unknown problems.'''
    floors={"G":0,"F":1,"S":2,"Z":-1}
    goalbuilding=tuple(_.goalbuilding)
    firsttime=0
    newstate=state
    newbuilding=tuple(_.Map[newstate[0]][newstate[1]])
    if(newbuilding==goalbuilding and firsttime==0):
        firsttime=1
        print(f"Step into {_.buildings[goalbuilding]}")
        if(_.room!=None):
            floor=floors[_.room[3]]
            number=_.room[4:]
            if(floor==-1):
                print(f"Go to Zone {number}")
            elif(floor==0):
                print(f"Your destination is at Ground Floor, Follow the steps")
            elif(floor==1):
                print(f"Your destination is at First Floor, Please use Elivator!")
                print(f"Then follow the steps")
            elif(floor==2):
                print(f"Your destination is at Second Floor, Please use Elivator!")
                print(f"Then follow the steps")
        print(f"move to {newstate}")
        return newstate
    else:
        print(f"move to {newstate}")
        return newstate

class Visualizer2:
    '''Visualization and printing functionality encapsulation.'''

    def __init__(self, problem):
        '''Constructor with the problem to visualize.'''
        self.problem = problem
        self.counter = 0
    
    def visualize(self, frontier):
        '''Visualizes the frontier at every step.'''
        self.counter += 1
        states = []
        #print(f'Frontier at step {self.counter}')
        for state in frontier:
            #print()
            newstate = _visualizers2.get(type(self.problem), _default_visualizer2)(self.problem, state)
            states.append(newstate)
        return states
        #print('-' * terminal_width) 

def simulated_annealing(problem, schedule, verbose=False):
    '''Simulated annealing search implementation.'''
    current_state = problem.init_state
    current_value = problem.heuristic(current_state)
    states = []
    if verbose: visualizer = Visualizer2(problem)
    for t in count():
        if verbose: visualizer.visualize([current_state])
        T = schedule(t)  # A function that determines the "temperature" (acceptability of a bad state) as a function of the step count
        if current_value == 0 or T == 0: return states, current_state  # Return if a goal state is found or if the temperature hits 0
        next_states = [problem.result(current_state, action) for action in problem.actions(current_state)]  # Generate all possible next states
        while True:  # Repeat the following till the current state is updated
            next_state = choice(next_states)  # Choose a random next state
            next_value = problem.heuristic(next_state)
            delta = current_value - next_value
            if delta > 0 or random() < exp(delta / T):  # Accept the randomly chosen state immediately if it is better than the current state or with a probability (exponentially) proportional to the temperature and how bad it is
                current_state, current_value = next_state, next_value
                states.append(current_state)
                break