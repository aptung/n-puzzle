import csv
import copy
import time

def loadFileFrom(filepath):
    if loadFileFrom_helper(filepath)==None:
        return "There was an error"
    else:
        return loadFileFrom_helper(filepath)

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
    nums = [i for i in range(n**2)]
    for line in game:
        for num in line:
            if not str.isdigit(num): # Checking to see if the star is present
                return num=='*'
            else:
                test = int(num)
                if test <0 or test>n**2-1: # Cheking for ints out of bound
                    return False
                if nums[test]==-1: # Checking for repeated elements
                    return False
                nums[test] == -1
    return True

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

def main():
    # Testing code here
    #print(isGoal(loadFileFrom("input.txt")))
    start_time = time.time()
    print(computeNeighbors(loadFileFrom("input.txt")))
    print(time.time()-start_time)

if __name__ == "__main__":
    main()
