#  This program in the future will help you pass jajo exam
import Chomsky
import Greibach
import Regular
import CFLan
import RemoveStart

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

def read_from_file():
    # Reads production rules from a file
    posTerminals = "0123456789^abcdefghijklmnopqrstuvwxyz"
    terminals = []
    nonTerminals = []
    productionRules = {}
    rules = []
    file = open("source.txt", 'r')
    for line in file:
        data = line.split()
        data.remove('->')
        try:
            while True:
                data.remove('|')
        except ValueError:
            pass
        nonTerminals.append(data[0])
        rules.append(data.copy())
        data.clear()
    for x in rules:
        for p in x:
            for s in p:
                if s in posTerminals and s not in terminals:
                    terminals.append(s)
    productionRules = Chomsky.to_dic(rules)
    return nonTerminals, terminals, productionRules

def read_from_string(string):
    # Reads production rules from the string
    posTerminals = "0123456789^abcdefghijklmnopqrstuvwxyz"
    terminals = []
    nonTerminals = []
    productionRules = {}
    rules = []
    data = string.split()
    nextP = False
    for x in data:
        if x == '->':
            nextP = True
            continue
        elif x == '|':
            nextP = True
            continue
        elif not nextP:
            nonTerminals.append(x)
            rules.append([x])
            nextP = True
            continue
        elif nextP:
            for s in x:
                if s in posTerminals and s not in terminals:
                    terminals.append(s)
            rules[-1].append(x)
            nextP = False
    productionRules = Chomsky.to_dic(rules)
    return nonTerminals, terminals, productionRules


# to check if given symbol can be terminal
posTerminals = "0123456789^abcdefghijklmnopqrstuvwxyz"

if __name__ == "__main__":

    # testString = "S -> aS | bS | cS | 2R\nmabda -> lambd3"
    # read_from_string(testString)
    # Test values
    # terminals = ['x', 'y', 'z']
    # nonTerminals = ['S', 'X', 'Y', 'Z']
    # productionRules = {'S': ('SY', 'Xy', 'xZ'), 'X': ('Xx', 'z'), 'Y': ('Zy', 'Yy'), 'Z': ('y', 'Zx', 'z')}
    # terminals = ['x', 'y']
    # nonTerminals = ['S', 'A', 'B', 'C', 'D']
    # productionRules = {'S': ('x', 'AD', 'C', 'BD'), 'C': ('y'), 'A': ('x'), 'D': ('xD')}

    #terminals, nonTerminals, productionRules = read_from_file()

    # rules = Chomsky.to_list(productionRules)
    # Chomsky.remove_useless(nonTerminals, terminals, rules)
    # Chomsky.print_production(Chomsky.to_dic(rules))
    #Chomsky.remove_singles(nonTerminals, terminals, Chomsky.to_list(productionRules), pr=True)
    #Chomsky.chomsky(nonTerminals, terminals, productionRules, pr=True)

    #rules = Chomsky.to_list(productionRules)
    #print(rules)
    #pr = Chomsky.to_dic(rules)
    #print(pr)
    #Chomsky.remove_useless(nonTerminals, terminals, rules)
    #Chomsky.print_production(productionRules)
    #n, t, pr = Chomsky.chomsky(nonTerminals, terminals, productionRules, pr=False)
    #Chomsky.print_production(pr)
    nonTerminals, terminals, productionRules = read_from_file()
    RemoveStart.remove_start(nonTerminals, terminals, productionRules)
    # Chomsky.remove_useless(nonTerminals,terminals,Chomsky.to_list(productionRules))
    # print("Najpier na chowmkyego")
    # n, t, pr = Chomsky.chomsky(nonTerminals.copy(), terminals.copy(), productionRules.copy())
    # n, t, pr = Greibach.greibach(nonTerminals.copy(), terminals.copy(), productionRules.copy())
    # Chomsky.print_production(pr)
    # TODO CFLan.lang(nonTerminals, terminals, productionRules)
    #Regular.to_deterministic(nonTerminals, terminals, productionRules)
    #Regular.to_deterministic(nonTerminals, terminals, productionRules)
#    nonTerminals, terminals, productionRules = Regular.to_complete(nonTerminals.copy(), terminals.copy(), productionRules.copy())
    #Chomsky.print_production(productionRules)
    # rule = ['ASA', 'y']
    # replacements = ['0']
    # target = 'A'
    #CFLan.replace_productions(rule, replacements, target)
    input()

    # Chomsky.print_production(productionRules)
    # n, t, pr = Chomsky.chomsky(nonTerminals.copy(), terminals.copy(), productionRules.copy(), pr=False)
    # Chomsky.print_production(pr)
    # n, t, pr = Greibach.greibach(nonTerminals.copy(), terminals.copy(), productionRules.copy())
    # Chomsky.print_production(pr)
    # input()

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