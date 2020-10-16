import csv
import statistics


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

def main():
    # Testing code here
    print(loadFileFrom("input.txt"))

if __name__ == "__main__":
    main()
