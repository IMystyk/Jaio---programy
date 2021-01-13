#  This program in the future will help you pass jajo exam
#  Now it does nothing
#  Literally


# to check if given symbol can be terminal
posTerminals = "0123456789^abcdefghijklmnopqrstuvwxyz"

if __name__ == "__main__":

    terminals = []
    results = []
    nonTerminals = []
    productionRules = {}

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
        print(x, end=' -> ')
        for y in productionRules[x]:
            if y != productionRules[x][-1]:
                print(y, end=' | ')
            else:
                print(y)
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

