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
        return game

def testArray(game):
    pass
    #Add more testing of array
    #Test to make sure all numbers 1-n^2-1 are included
    #Test to make sure the space character is "*"

def main():
    # Testing code here
    print(loadFileFrom("input.txt"))

if __name__ == "__main__":
    main()
