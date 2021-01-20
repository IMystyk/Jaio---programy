#  This module implements transformations of a given grammar to regular, deterministic and complete
from collections import deque
from Chomsky import *


def check_regular(nonTerminals, terminals, productionRules):
    #  Checks if given grammar is regular
    rules = to_list(productionRules)
    for rule in rules:
        for product in rule:
            if product == rule[0]:
                continue
            if len(product) > 2:
                return False
            elif len(product) == 1:
                if product not in terminals:
                    return False
            elif len(product) == 2:
                if product[0] not in terminals:
                    return False
                elif product[1] not in nonTerminals:
                    return False
    return True


def replace_finals(nonTerminals, terminals, rules, pr=True):
    #  Replaces A -> a productions with A -> aB, where B -> lambda
    if pr:
        print("Usuwamy symbole koncowe (jesli jakiekolwiek znajdziemy)")
    availableNonTerminals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for nT in nonTerminals:
        availableNonTerminals = availableNonTerminals.replace(nT, '')
    lambdaProduction = find_producer('^', rules)
    added = False
    used = False
    if lambdaProduction == 0:
        nT = availableNonTerminals[0]
        availableNonTerminals = availableNonTerminals.replace(nT, '')
        lambdaProduction = nT
        rules.append([nT, '^'])
        nonTerminals.append(nT)
        if '^' not in terminals:
            terminals.append('^')
        added = True
    ruleCounter = 0
    productCounter = 0
    for rule in rules:
        for product in rule:
            if product == rule[0] or len(product) == 2 or product == '^':
                productCounter += 1
                continue
            else:
                if pr:
                    print(rules[ruleCounter][0], " -> ", rules[ruleCounter][productCounter], end=' ')
                    print("zastepujemy:", rules[ruleCounter][0], " -> ", product + lambdaProduction, end='')
                    print(", gdzie", lambdaProduction, " -> ^'")
                rules[ruleCounter][productCounter] = product + lambdaProduction
                used = True
            productCounter += 1
        productCounter = 0
        ruleCounter += 1
    if added and not used:  # never used added lambda production
        rules.remove(rules[-1])
        nonTerminals.remove(lambdaProduction)
        terminals.remove('^')
    if pr:
        print("---------------------")
        print("Po usunieciu:")
        print_production(to_dic(rules))
        print("---------------------")


def to_deterministic(nonTerminals, terminals, productionRules, pr=True):
    #  Transforms given regular grammar to deterministic form
    if not check_regular(nonTerminals, terminals, productionRules):  # check if given grammar is even regular
        print("Podana gramatyka nie jest gramatyka regularna")
        return nonTerminals, terminals, productionRules
    rules = to_list(productionRules)
    replace_finals(nonTerminals, terminals, rules)
    fixprint = []  # cuz print doesn't work properly
    #  TODO add print
    if pr:
        print("Tworzymy nowe symbole terminalne, ktore reprezentuja grupy poprzednich symboli")
    newNonTerminals = []
    newProductions = []
    queue = deque([])  # productions that are yet to be resolved
    routes = {}  # terminal symbols that are labels for routes and their destinations
    for t in terminals:
        if t == '^':
            continue
        routes[t] = []
    availableNonTerminals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for nT in nonTerminals:
        availableNonTerminals = availableNonTerminals.replace(nT, '')
    nT = availableNonTerminals[0]  # create new starting symbol
    availableNonTerminals = availableNonTerminals.replace(nT, '')
    newProductions.append([nT])  # add new starting production rule
    newNonTerminals.append(nT)
    fixprint.append([nT, rules[0][0]])
    newNames = []  # new non-terminals producing old non-terminals
    for product in rules[0]:  # prepare first productions
        if product == rules[0][0]:
            continue
        elif product == '^':  # if lambda production found add it
            newProductions[0].append(product)
        routes[product[0]].append(product[1])
    for key in routes.keys():
        products = routes[key]
        if len(products) == 0:
            continue
        if find_producer(products, newNames):  # if new production already exists add it
            newProductions[0].append(key + find_producer(products, newNames))
        else:  # no existing production found, create a new one
            nT = availableNonTerminals[0]
            availableNonTerminals = availableNonTerminals.replace(nT, '')
            newProductions[0].append(key + nT)
            newNames.append([nT, [rules[0][0]]])
            fixprint.append([nT])
            for x in products:
                fixprint[-1].append(x)
            newProductions.append([nT])
            newNonTerminals.append(nT)
            queue.append([nT, routes[key].copy()])
        routes[key].clear()
    counter = 0
    while True:
        try:
            newRule = queue.popleft()  # pick first element from the queue
        except IndexError:  # queue is empty
            break
        for rule in rules:
            if rule[0] not in newRule[1]:  # given production is not among current products
                continue
            else:  # found production that is our new product
                for product in rule:
                    if product == rule[0]:
                        continue
                    elif product == '^':
                        newProductions[-(counter + 1)].append('^')
                    else:
                        if product[1] not in routes[product[0]]:
                            routes[product[0]].append(product[1])
        for key in routes.keys():
            products = routes[key]
            if len(products):
                if find_producer(products, newNames):
                    newProductions[-(counter + 1)].append(key + find_producer(products, newNames))
                else:
                    nT = availableNonTerminals[0]
                    availableNonTerminals = availableNonTerminals.replace(nT, '')
                    newProductions[-(counter + 1)].append(key + nT)
                    newProductions.append([nT])
                    newNames.append([nT, routes[key].copy()])
                    counter += 1
                    newNonTerminals.append(nT)
                    queue.append([nT, routes[key].copy()])
            routes[key].clear()
        counter -= 1
    if pr:
        for rule in fixprint:
            for product in rule:
                if product == rule[0]:
                    print(product, end=' = { ')
                elif product == rule[-1]:
                    print(product, "}")
                else:
                    print(product, end=', ')
        counter = 0
        for rule in newNames:
            if counter < len(fixprint) - 1:
                counter += 1
                continue
            for product in rule:
                if product == rule[0]:
                    print(product, end=' = { ')
                else:
                    for el in product:
                        if len(product) == 1:
                            print(el, " }")
                        else:
                            if el == product[-1]:
                                print(el, "}")
                            else:
                                print(el, end=', ')
        print_production(to_dic(newProductions))

    return newNonTerminals, terminals, to_dic(newProductions)






def to_complete(nonTerminals, terminals, productionRules, pr=True):
    #  Transforms given regular grammar to complete form (if it's even called complete)
    if not check_regular(nonTerminals, terminals, productionRules):  # check if given grammar is even regular
        print("Podana gramatyka nie jest gramatyka regularna")
        return nonTerminals, terminals, productionRules
    rules = to_list(productionRules)
    replace_finals(nonTerminals, terminals, rules)
    availableNonTerminals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for nT in nonTerminals:
        availableNonTerminals = availableNonTerminals.replace(nT, '')
    ruleCounter = 0
    productCounter = 0
    used = False  # check if trap was ever used
    toAdd = terminals.copy()  # list of terminals that were not used in current rule
    try:  # remove lambda if added
        toAdd.remove('^')
    except ValueError:
        pass
    trap = availableNonTerminals[0]  # trap point
    trapProductions = [trap]
    for t in toAdd:
        trapProductions.append(t+trap)
    rules.append(trapProductions)
    nonTerminals.append(trap)
    availableNonTerminals = availableNonTerminals.replace(trap, '')
    for rule in rules:
        if rule == rules[-1]:
            break
        for product in rule:
            if product == rule[0]:
                continue
            try:
                toAdd.remove(product[0])
            except ValueError:  # trying to remove lambda
                pass
            productCounter += 1
        if len(toAdd) == 0:  # no additional productions needed
            ruleCounter += 1
            toAdd = terminals.copy()
            try:  # remove lambda if added
                toAdd.remove('^')
            except ValueError:
                pass
            continue
        else:  # trap must be added
            for t in toAdd:
                rules[ruleCounter].append(t + trap)
                if pr:
                    print("Dodajemy", rules[ruleCounter][0], "->", t+trap)
            used = True
        toAdd = terminals.copy()
        try:  # remove lambda if added
            toAdd.remove('^')
        except ValueError:
            pass
        ruleCounter += 1
    if not used:
        rules.remove(rules[-1])
        nonTerminals.remove(trap)
    if pr and used:
        print("Dodajemy", rules[-1][0], end=' -> ')
        for product in rules[-1]:
            if product == rules[-1][0]:
                continue
            elif product == rules[-1][-1]:
                print(product)
            else:
                print(product, end=' | ')
    return nonTerminals, terminals, to_dic(rules)

