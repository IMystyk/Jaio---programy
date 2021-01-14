#  This program in the future will help you pass jajo exam
#  Now it does nothing
#  Literally
import Chomsky

def print_production(productionRules):
    # Prints production rules
    for x in productionRules.keys():
        print(x, end=' -> ')
        for y in productionRules[x]:
            if y != productionRules[x][-1]:
                print(y, end=' | ')
            else:
                print(y)
def print_grammar(terminals, nonTerminals):
    # Prints given grammar
    print("G = <{", end='')
    for x in nonTerminals:
        print(x, end=', ')
    for x in terminals:
        if x != terminals[-1]:
            print(x, end=', ')
        else:
            print(x, end='}, { ')
    for x in terminals:
        if x != terminals[-1]:
            print(x, end=', ')
        else:
            print(x, '}, P,', nonTerminals[0], ' >')

def readFile():
    # Reads production rules from a file
    with open("source.txt", 'r') as read:
        # TO DO
        pass

# to check if given symbol can be terminal
posTerminals = "0123456789^abcdefghijklmnopqrstuvwxyz"

if __name__ == "__main__":

    # Test values
    # terminals = ['x', 'y', 'z']
    # nonTerminals = ['S', 'X', 'Y', 'Z']
    # productionRules = {'S': ('SY', 'Xy', 'xZ'), 'X': ('Xx', 'z'), 'Y': ('Zy', 'Yy'), 'Z': ('y', 'Zx', 'z')}
    terminals = ['x', 'y']
    nonTerminals = ['S', 'A', 'B', 'C', 'D']
    productionRules = {'S': ('x', 'AD', 'C', 'BD'), 'C': ('y'), 'A': ('x'), 'D': ('xD')}


    #rules = Chomsky.to_list(productionRules)
    #Chomsky.remove_useless(nonTerminals, terminals, rules)

    print_production(productionRules)
    print('------Chomsky------')
    t, n, pr = Chomsky.chomsky(nonTerminals, terminals, productionRules)
    print_production(pr)
    input()

    terminals = []
    nonTerminals = []
    productionRules = {}

    results = []


    # Get production rules from user
    while True:
        nT = input("Enter new non-terminal symbol ('/OK' to finish): \n")
        if nT.upper() == "/OK":
            break
        elif len(nT) != 1:
            continue
        else:
            nT = nT.upper()
            print("Enter new production results ('/OK' to finish, '^' for lambda): ")
            for x in productionRules.keys():
                print(x, end=' -> ')
                for y in productionRules[x]:
                    if y != productionRules[x][-1]:
                        print(y, end=' | ')
                    else:
                        print(y)
            while True:
                print(nT, end=' -> ')
                for y in results:
                    print(y, end=' | ')
                r = input()
                if r.upper() == "/OK":
                    break
                else:
                    results.append(r)
                    for symbol in r:
                        if symbol in posTerminals and symbol not in terminals:
                            terminals.append(symbol)
            if len(results) != 0:
                productionRules[nT] = tuple(results.copy())
            results.clear()
    for x in productionRules.keys():
        nonTerminals.append(x)
    print_production(productionRules)
    print_grammar(terminals, nonTerminals)

    Chomsky.chomsky(nonTerminals.copy(), terminals.copy(), productionRules)