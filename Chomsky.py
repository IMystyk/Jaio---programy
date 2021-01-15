#  This module implements Chomsky hierarchy syntax of a given grammar

def to_list(productionRules):
    # Creates list from a given dictionary with non terminal symbol always as it's first element
    # Then returns the entire list
    result = []
    current = []
    for x in productionRules.keys():
        current.append(x)
        if type(productionRules[x]) is tuple:
            for p in productionRules[x]:
                current.append(p)
        else:
            current.append(productionRules[x])
        result.append(current.copy())
        current.clear()
    return result

def to_dic(rules):
    # Creates dictionary from a given list of production rules
    result = {}
    for rule in rules:
        result[rule[0]] = tuple(rule[1:])
    return result

def find_producer(symbol, rules):
    # Finds non-terminal symbol that produces given symbol
    # If no such production is found returns 0
    for x in rules:
        if len(x) == 2:
            if x[1] == symbol:
                return x[0]
    return 0

def remove_useless(nonTerminals, terminals, rules, pr=True):
    # Checks if any production rules are useless and deletes them (and non-terminal symbols) if any are found
    tmp = rules.copy()
    while True:
        produced = 0
        for nT in nonTerminals:
            if nT == nonTerminals[0]:
                produced = 1
            for rule in rules:
                for product in rule:
                    if product == rule[0]:
                        continue
                    else:
                        if nT in product:
                            produced = 1
            if not produced:
                for rule in rules:
                    if rule[0] == nT:
                        if pr:
                            print("Usuwamy: ", end='')
                            for product in rule:
                                if product == rule[0]:
                                    print(product, end=' -> ')
                                elif product != rule[-1]:
                                    print(product, end=' | ')
                                else:
                                    print(product)
                        rules.remove(rule)
                        nonTerminals.remove(nT)
            produced = 0
        prevUsed = []
        for rule in rules:
            prevUsed.append(rule[0])
            if try_escape(rule[0], terminals, rules, prevUsed.copy()):
                continue
            else:
                if pr:
                    print("Usuwamy: ", end='')
                    for product in rule:
                        if product == rule[0]:
                            print(product, end=' -> ')
                        elif product != rule[-1]:
                            print(product, end=' | ')
                        else:
                            print(product)
                rules.remove(rule)
                for x in rules:
                    for p in x:
                        if rule[0] in p:
                            if pr:
                                print("Usuwamy: ", end='')
                                print(x[0], end=' -> ')
                                print(p)
                            x.remove(p)
                nonTerminals.remove(rule[0])
                prevUsed.remove(rule[0])
        if tmp == rules:
            break
        else:
            prevUsed.clear()
            tmp = rules.copy()
    if pr:
        print()


def try_escape(nonTerminal, terminals, rules, prevUsed):
    # Checks if given non-terminal symbol produces terminal symbol
    # Returns True if non-terminal can be "escaped" or False if otherwise
    results = []
    oneResult = []
    for rule in rules:
        if rule[0] == nonTerminal:
            for product in rule:
                if product == rule[0]:
                    continue
                elif len(product) == 1 and product in terminals:
                    return True
                else:
                    for symbol in product:
                        if symbol in terminals:
                            oneResult.append(True)
                        elif symbol == nonTerminal:
                            oneResult.append(False)
                        elif symbol not in prevUsed:
                            prevUsed.append(symbol)
                            oneResult.append(try_escape(symbol, terminals, rules, prevUsed.copy()))
                    results.append(oneResult.copy())
                    oneResult.clear()
    escape = False
    for res in results:
        for x in res:
            escape = x
        if escape:
            return True
    return False




def chomsky(nonTerminals, terminals, productionRules, pr=True):
    # Transforms grammar with given production rules to Chomsky hierarchy
    availableNonTerminals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # Check which non-terminal symbols are really available
    for x in nonTerminals:
        availableNonTerminals = availableNonTerminals.replace(x, '')
    # Create list of production Rules
    rules = to_list(productionRules)
    remove_useless(nonTerminals, terminals, rules)
    ruleCounter = 0
    productCounter = 0
    found = 0
    while True:
        x = rules[ruleCounter]
        while True:
            p = x[productCounter]
            if not productCounter:
                productCounter += 1
                if productCounter == len(x):
                    break
                continue
            if len(p) == 1:
                if p in terminals:
                    productCounter += 1
                    if productCounter == len(x):
                        break
                    continue
                else:
                    if find_producer('^', rules):
                        if pr:
                            print(rules[ruleCounter][0], end=' -> ')
                            print(rules[ruleCounter][productCounter], end=' ')
                            print("Zastepujemy: ", end='')
                            print(rules[ruleCounter][0], end=' -> ')
                            print(p + find_producer('^', rules))
                        rules[ruleCounter][productCounter] = p + find_producer('^', rules)
                    else:
                        nT = availableNonTerminals[0]
                        availableNonTerminals = availableNonTerminals.replace(nT, '')
                        rules.append([nT, '^'])
                        nonTerminals.append(nT)
                        terminals.append('^')
                        if pr:
                            print(rules[ruleCounter][0], end=' -> ')
                            print(rules[ruleCounter][productCounter], end=' ')
                            print("Zastepujemy: ", end='')
                            print(rules[ruleCounter][0], end=' -> ')
                            print(p + nT, ", gdzie:", nT, " -> '^'")
                        rules[ruleCounter][productCounter] = p + nT
            elif len(p) == 2:
                if p[0] in nonTerminals and p[1] in nonTerminals:
                    productCounter += 1
                    if productCounter == len(x):
                        break
                    continue
                else:
                    if p[0] in terminals:
                        if find_producer(p[0], rules):
                            if pr:
                                print(rules[ruleCounter][0], end=' -> ')
                                print(rules[ruleCounter][productCounter], end=' ')
                                print("Zastepujemy: ", end='')
                                print(rules[ruleCounter][0], end=' -> ')
                                print(rules[ruleCounter][productCounter].replace(p[0], find_producer(p[0], rules)), end =' ')
                                print(", gdzie:", find_producer(p[0], rules), " -> ", p[0])
                            rules[ruleCounter][productCounter] = rules[ruleCounter][productCounter].replace(p[0], find_producer(p[0], rules))
                        else:
                            nT = availableNonTerminals[0]
                            availableNonTerminals = availableNonTerminals.replace(nT, '')
                            rules.append([nT, p[0]])
                            nonTerminals.append(nT)
                            if pr:
                                print(rules[ruleCounter][0], end=' -> ')
                                print(rules[ruleCounter][productCounter], end=' ')
                                print("Zastepujemy: ", end='')
                                print(rules[ruleCounter][0], end=' -> ')
                                print(rules[ruleCounter][productCounter].replace(p[0], find_producer(p[0], rules)), end=' ')
                                print(", gdzie: ", nT, " -> ", p[0])
                            rules[ruleCounter][productCounter] = rules[ruleCounter][productCounter].replace(p[0], nT)
                    if p[1] in terminals:
                        if find_producer(p[1], rules):
                            if pr:
                                print(rules[ruleCounter][0], end=' -> ')
                                print(rules[ruleCounter][productCounter], end=' ')
                                print("Zastepujemy: ", end='')
                                print(rules[ruleCounter][0], end=' -> ')
                                print(rules[ruleCounter][productCounter].replace(p[1], find_producer(p[1], rules)), end=' ')
                                print(", gdzie:", find_producer(p[1], rules), " -> ", p[1])
                            rules[ruleCounter][productCounter] = rules[ruleCounter][productCounter].replace(p[1], find_producer(p[1], rules))
                        else:
                            nT = availableNonTerminals[0]
                            availableNonTerminals = availableNonTerminals.replace(nT, '')
                            rules.append([nT, p[1]])
                            nonTerminals.append(nT)
                            if pr:
                                print(rules[ruleCounter][0], end=' -> ')
                                print(rules[ruleCounter][productCounter], end=' ')
                                print("Zastepujemy: ", end='')
                                print(rules[ruleCounter][0], end=' -> ')
                                print(rules[ruleCounter][productCounter].replace(p[1], find_producer(p[1], rules)), end=' ')
                                print(", gdzie: ", nT, " -> ", p[1])
                            rules[ruleCounter][productCounter] = rules[ruleCounter][productCounter].replace(p[1], find_producer(p[1], rules))
            else:
                for symbol in p:
                    if symbol in terminals:
                        if find_producer(symbol, rules):
                            if pr:
                                print(rules[ruleCounter][0], end=' -> ')
                                print(rules[ruleCounter][productCounter], end=' ')
                                print("Zastepujemy: ", end='')
                                print(rules[ruleCounter][0], end=' -> ')
                                print(rules[ruleCounter][productCounter].replace(symbol, find_producer(symbol, rules)), end=' ')
                                print(", gdzie: ", find_producer(symbol, rules), ' -> ', symbol)
                            rules[ruleCounter][productCounter] = rules[ruleCounter][productCounter].replace(symbol, find_producer(symbol, rules))
                        else:
                            nT = availableNonTerminals[0]
                            availableNonTerminals = availableNonTerminals.replace(nT, '')
                            rules.append([nT, symbol])
                            nonTerminals.append(nT)
                            if pr:
                                print(rules[ruleCounter][0], end=' -> ')
                                print(rules[ruleCounter][productCounter], end=' ')
                                print("Zastepujemy: ", end='')
                                print(rules[ruleCounter][0], end=' -> ')
                                print(rules[ruleCounter][productCounter].replace(symbol, nT), end=' ')
                                print(", gdzie: ", nT, ' -> ', symbol)
                            rules[ruleCounter][productCounter] = rules[ruleCounter][productCounter].replace(symbol, nT)
                for n in range(len(p)):
                    if n + 1 == len(p):
                        break
                    else:
                        pair = rules[ruleCounter][productCounter][0] + rules[ruleCounter][productCounter][1]
                        if find_producer(pair, rules):
                            if pr:
                                print(rules[ruleCounter][0], end=' -> ')
                                print(rules[ruleCounter][productCounter], end=' ')
                                print("Zastepujemy: ", end='')
                                print(rules[ruleCounter][0], end=' -> ')
                                print(rules[ruleCounter][productCounter].replace(pair, find_producer(pair, rules), 1), end=' ')
                                print(", gdzie: ", find_producer(pair, rules), " -> ", pair)
                            rules[ruleCounter][productCounter] = rules[ruleCounter][productCounter].replace(pair, find_producer(pair, rules), 1)
                            found = 1
                            break
                if found:
                    found = 0
                    continue
                pair = rules[ruleCounter][productCounter][0] + rules[ruleCounter][productCounter][1]
                nT = availableNonTerminals[0]
                availableNonTerminals = availableNonTerminals.replace(nT, '')
                nonTerminals.append(nT)
                rules.append([nT, pair])
                if pr:
                    print(rules[ruleCounter][0], end=' -> ')
                    print(rules[ruleCounter][productCounter], end=' ')
                    print("Zastepujemy: ", end='')
                    print(rules[ruleCounter][0], end=' -> ')
                    print(rules[ruleCounter][productCounter].replace(pair, nT, 1), end=' ')
                    print(", gdzie: ", nT, ' -> ', pair)
                rules[ruleCounter][productCounter] = rules[ruleCounter][productCounter].replace(pair, nT, 1)
                continue

            productCounter += 1
            if productCounter == len(x):
                break
        ruleCounter += 1
        productCounter = 0
        if len(rules) == ruleCounter:
            break
    result = {}
    for rule in rules:
        result[rule[0]] = tuple(rule[1:])
    return nonTerminals, terminals, result

