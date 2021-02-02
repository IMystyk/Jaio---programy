from CFLan import replace_productions
from Chomsky import to_dic, to_list, print_production

def remove_start(nonTerminals, terminals, productionRules, pr=True):
    # removes starting symbol from the right start
    rules = to_list(productionRules)
    productionRules = {}
    for rule in rules:
        productionRules[rule[0]] = rule[1:]
    for key in productionRules.keys():
        startSymbol = key  # find starting symbol
        break
    availableNonTerminals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # Check which non-terminal symbols are really available
    for x in nonTerminals:
        availableNonTerminals = availableNonTerminals.replace(x, '')
    nT = availableNonTerminals[0]
    availableNonTerminals = availableNonTerminals.replace(nT, '')
    productionRules[nT] = productionRules[startSymbol].copy()
    for key in productionRules.keys():
        replace_productions(productionRules[key], nT, startSymbol)
    if pr:
        print("Tworzymy nowa produkcje", nT, end=' -> ')
        for product in productionRules[nT]:
            if product == productionRules[nT][-1]:
                print(product)
            else:
                print(product, end=' | ')
        print("Zamieniamy symbol poczatkowy", startSymbol, "we wszystkich produkcjach na", nT)
        tmp = {}
        for key in productionRules.keys():
            tmp[key] = tuple(productionRules[key])
        print_production(tmp)
    return nonTerminals, terminals, tmp
