import csv
import copy
import time
from queue import PriorityQueue
# See http://www.artbylogic.com/puzzles/numSlider/numberShuffle.htm for practice problems

def loadFileFrom(filepath):
    file = loadFileFrom_helper(filepath)
    if file==None:
        return "There was an error"
    return file

# Returns a 2d tuple of the input, or None if there is an error
def loadFileFrom_helper(filepath):
    with open (filepath, newline='') as input:
        reader = csv.reader(input)
        input = list(reader)
        n = int(input[0][0])
        input.remove([str(n)])
        if len(input) is not n:
            return None
        game = []
        for line in input:
            line = line[0].split("\t")
            if len(line) is not n:
                return None
            game.append(line)
        if testArray(game, n):
            return tuple(map(tuple, game))
        return None

# Tests a 2d array, given the (correct) size of the array
def testArray(game, n):
    nums = [i for i in range(n**2-1)]
    for line in game:
        for num in line:
            if not str.isdigit(num): # Checking to see if the star is present
                if not num=='*':
                    return False
            else:
                int_num = int(num)
                if int_num <0 or int_num>n**2-1: # Cheking for ints out of bound
                    return False
                if nums[int_num-1]==-1: # Checking for repeated elements
                    return False
                nums[int_num-1] = -1
    return (nums==[-1 for i in range(n**2-1)])

# Takes in a 2d tuple as a state
# Returns a tuple of the next moves, written as a tuple containing the thing to
# to be swapped and the state (written as a 2d tuple)
def computeNeighbors(state):
    n = len(state)
    row = 0
    column = 0
    for i in range(n):
        for j in range(n):
            if state[i][j]=='*':
                row = i
                column = j

    next_moves = []
    # Move up
    if row>0:
        new_state = copy.copy(state)
        new_state = [list(x) for x in new_state]
        new_state[row][column], new_state[row-1][column] = new_state[row-1][column], new_state[row][column]
        next_moves.append((new_state[row][column], tuple(map(tuple, new_state))))
    # Move down
    if row<n-1:
        new_state = copy.copy(state)
        new_state = [list(x) for x in new_state]
        new_state[row][column], new_state[row+1][column] = new_state[row+1][column], new_state[row][column]
        next_moves.append((new_state[row][column], tuple(map(tuple, new_state))))
    # Move right
    if column<n-1:
        new_state = copy.copy(state)
        new_state = [list(x) for x in new_state]
        new_state[row][column], new_state[row][column+1] = new_state[row][column+1], new_state[row][column]
        next_moves.append((new_state[row][column], tuple(map(tuple, new_state))))
    # Move left
    if column>0:
        new_state = copy.copy(state)
        new_state = [list(x) for x in new_state]
        new_state[row][column], new_state[row][column-1] = new_state[row][column-1], new_state[row][column]
        next_moves.append((new_state[row][column], tuple(map(tuple, new_state))))
    return next_moves

# Takes in a 2d tuple of the state
# Returns a boolean value whether it is the goal
def isGoal(state):
    n = len(state)
    goal = [[str(x+1+y) for x in range(n)] for y in range(0,n**2,n)]
    goal[n-1][n-1]='*'
    goal = tuple(map(tuple, goal))
    return goal==state

def search(state, type):
    start_time = time.time()
    frontier = [state]
    parents = {state: None}
    discovered = set()
    while len(frontier) != 0:
        current_state = frontier[0]
        frontier.pop(0)
        discovered.add(current_state)
        if isGoal(current_state):
            return backtrack_states(parents, current_state)
        for neighbor in computeNeighbors(current_state):
            neighbor = neighbor[1]
            if neighbor not in discovered:
                if type=="BFS":
                    frontier.append(neighbor)
                elif type=="DFS":
                    frontier.insert(0, neighbor)
                discovered.add(neighbor)
                parents[neighbor] = current_state

# Takes tuples in all inputs
def backtrack_states(parents, current_state):
    moves = []
    while parents[current_state] != None:
        parent = parents[current_state]
        possible_moves = computeNeighbors(parent)
        for states in possible_moves:
            if states[1]==current_state:
                moves.insert(0, states[0])
        current_state = parents[current_state]
    return moves

# Takes in a 2d tuple of a state and does BFS on it
# Does not check improper input
def BFS(state):
    return search(state, "BFS")

def DFS(state):
    return search(state, "DFS")

def bidirectionalsearch(state):
    start_time = time.time()
    n=len(state)
    frontier_forward = [state]
    parents_forward = {state: None}
    discovered_forward = set()

    goal = [[str(x+1+y) for x in range(n)] for y in range(0,n**2,n)]
    goal[n-1][n-1]='*'
    goal = tuple(map(tuple, goal))
    frontier_reverse = [goal]
    parents_reverse = {goal: None}
    discovered_reverse = set()
    while len(frontier_forward) != 0 and len(frontier_reverse) !=0:
        current_state_forward = frontier_forward[0]
        frontier_forward.pop(0)
        discovered_forward.add(current_state_forward)
        if isGoal(current_state_forward):
            return backtrack_states(parents_forward, current_state_forward)

        current_state_reverse = frontier_reverse[0]
        frontier_reverse.pop(0)
        discovered_reverse.add(current_state_reverse)
        if current_state_reverse==state:
            return backtrack_states(parents_reverse, current_state_reverse)[::-1]

        new_states_forward = set()
        for neighbor_forward in computeNeighbors(current_state_forward):
            neighbor_forward = neighbor_forward[1]
            new_states_forward.add(neighbor_forward)
            if neighbor_forward not in discovered_forward:
                frontier_forward.append(neighbor_forward)
                discovered_forward.add(neighbor_forward)
                parents_forward[neighbor_forward] = current_state_forward

        intersection = new_states_forward.intersection(discovered_reverse)
        if len(intersection)>0:
            return backtrack_states(parents_forward, intersection.pop()) + backtrack_states(parents_reverse, current_state_reverse)[::-1]

        new_states_reverse = set()
        for neighbor_reverse in computeNeighbors(current_state_reverse):
            neighbor_reverse = neighbor_reverse[1]
            new_states_reverse.add(neighbor_reverse)
            if neighbor_reverse not in discovered_reverse:
                frontier_reverse.append(neighbor_reverse)
                discovered_reverse.add(neighbor_reverse)
                parents_reverse[neighbor_reverse] = current_state_reverse

        intersection = new_states_forward.intersection(new_states_reverse)
        if len(intersection)>0:
            return backtrack_states(parents_forward, current_state_forward) + backtrack_states(parents_reverse, intersection.pop())[::-1]

def AStar(state):
    start_time = time.time()
    frontier = PriorityQueue()
    frontier.put((h(state), state))
    parents = {state: None}
    discovered = set()
    while not frontier.empty():
        current_state = frontier.get()[1]
        discovered.add(current_state)
        if isGoal(current_state):
            return backtrack_states(parents, current_state)
        for neighbor in computeNeighbors(current_state):
            neighbor = neighbor[1]
            if neighbor not in discovered:
                frontier.put((h(neighbor), neighbor))
                discovered.add(neighbor)
                parents[neighbor] = current_state

# Returns a heuristic for how close a state is to the goal, lower if "better"
# Counts how many numbers are not in the correct place
def h(state):
    n = len(state)
    h = 0
    for i in range(n):
        for j in range(n):
            if state[i][j]=="*":
                if i!=n-1 or j!=n-1:
                    h+=1
            else:
                if not int(state[i][j]) == j+1+n*i:
                    h += 1
    return h

def main():
    pass

if __name__ == "__main__":
    main()
