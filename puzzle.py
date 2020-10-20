import csv
import copy
import time
# See http://www.artbylogic.com/puzzles/numSlider/numberShuffle.htm for practice problems

def loadFileFrom(filepath):
    file = loadFileFrom_helper(filepath)
    if file==None:
        return "There was an error"
    return file

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
            return game
        return None

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
        new_state = copy.deepcopy(state)
        new_state[row][column], new_state[row-1][column] = new_state[row-1][column], new_state[row][column]
        next_moves.append((new_state[row][column], new_state))
    # Move down
    if row<n-1:
        new_state = copy.deepcopy(state)
        new_state[row][column], new_state[row+1][column] = new_state[row+1][column], new_state[row][column]
        next_moves.append((new_state[row][column], new_state))
    # Move right
    if column<n-1:
        new_state = copy.deepcopy(state)
        new_state[row][column], new_state[row][column+1] = new_state[row][column+1], new_state[row][column]
        next_moves.append((new_state[row][column], new_state))
    # Move left
    if column>0:
        new_state = copy.deepcopy(state)
        new_state[row][column], new_state[row][column-1] = new_state[row][column-1], new_state[row][column]
        next_moves.append((new_state[row][column], new_state))
    return next_moves

def isGoal(state):
    n = len(state)
    goal = [[str(x+1+y) for x in range(n)] for y in range(0,n**2,n)]
    goal[n-1][n-1]='*'
    return goal==state

def BFS(state):
    start_time = time.time()
    state = tuple(map(tuple, state))
    frontier = [state]
    parents = {state: None}
    discovered = set()
    i=0
    while len(frontier) != 0:
        current_state = frontier[0]
        frontier.pop(0)
        discovered.add(tuple(map(tuple, current_state)))
        if isGoal([list(x) for x in current_state]):
            print("done!")
            return backtrack_states(parents, current_state)
        for neighbor in computeNeighbors([list(x) for x in current_state]):
            move = neighbor[0]
            neighbor = neighbor[1]
            neighbor = tuple(map(tuple, neighbor))
            if neighbor not in discovered:
                frontier.append(neighbor)
                discovered.add(neighbor)
                parents[neighbor] = current_state
        i+=1
        if i%10000 == 0:
            print(i)
            print(time.time()-start_time)


def backtrack_states(parents, current_state):
    moves = []
    while parents[current_state] != None:
        list_version_parent = [list(x) for x in parents[current_state]]
        possible_moves = computeNeighbors(list_version_parent)
        for states in possible_moves:
            if states[1]==[list(x) for x in current_state]:
                moves.insert(0, states[0])
        current_state = parents[current_state]
    return moves

def DFS(state):
    start_time = time.time()
    state = tuple(map(tuple, state))
    frontier = [state]
    parents = {state: None}
    discovered = set()
    i=0
    while len(frontier) != 0:
        current_state = frontier[0]
        frontier.pop(0)
        discovered.add(tuple(map(tuple, current_state)))
        if isGoal([list(x) for x in current_state]):
            print("done!")
            return backtrack_states(parents, current_state)
        for neighbor in computeNeighbors([list(x) for x in current_state]):
            move = neighbor[0]
            neighbor = neighbor[1]
            neighbor = tuple(map(tuple, neighbor))
            if neighbor not in discovered:
                frontier.insert(0, neighbor) # Only change from BFS is this line
                discovered.add(neighbor)
                parents[neighbor] = current_state
        i+=1
        if i%10000 == 0:
            print(i)
            print(time.time()-start_time)

def bidirectionalsearch(state):
    pass

def AStar(state):
    pass


def main():
    # Testing code here
    #print(isGoal(loadFileFrom("input.txt")))
    global_start_time = time.time()
    print(loadFileFrom("input.txt"))
    print(time.time()-global_start_time)
    '''
    global_start_time = time.time()
    print(DFS(loadFileFrom("input.txt")))
    print(time.time()-global_start_time)'''


if __name__ == "__main__":
    main()
