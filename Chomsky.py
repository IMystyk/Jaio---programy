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
    possibleNonTerminals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    tmp = rules.copy()
    while True:
        try:
            rule = rules[0]
        except IndexError:
            return -1
        for product in rule:
            for symbol in product:
                if symbol in possibleNonTerminals and symbol not in nonTerminals:
                    try:
                        rules[0].remove(product)
                    except ValueError:
                        pass
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
            if try_escape(rule[0], terminals, rules, []):  # prevUsed should be left empty for the first call
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
    for t in terminals:
        obseleteTerminal = True
        for rule in rules:
            for product in rule:
                if t in product:
                    obseleteTerminal = False
        if obseleteTerminal:
            terminals.remove(t)
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


def remove_singles(nonTerminals, terminals, rules, lam=False, pr=False):
    # Removes single-length productions, nonTerminals: non-terminal symbols list, terminals: terminal symbols list
    # rules: all production rules as a list (first element of each list is a "producer")
    remove_useless(nonTerminals, terminals, rules)  # remove useless productions
    currentSingles = []  # productions of a single symbol from the current rule
    replaceAll = False  # marks that there will be no productions of given non-Terminal left
    history = []  # stores previous versions of production rules, prevents infinite loops
    skip = False

    while True:
        for rule in reversed(rules):  # iterate through all rules from bottom to the top
            replaceAll = False
            currentSingles.append(rule[0])  # append current producer to the list (so that later we'll know what to remove)
            for product in rule:  # iterate through all products of a single rule
                if product == rule[0]:
                    continue  # skip first "product", which in fact is a "producer"
                if len(product) == 1:  # check if singular symbol is produced
                    if not lam:  # remove all singular productions
                        currentSingles.append(product)  # append singular symbol to the list of singular productions
                    elif product == '^':  # remove only lambda productions
                        currentSingles.append(product)
            if len(currentSingles) == 1:  # no singular productions found
                currentSingles.clear()
                continue
            else:
                if pr:
                    print("Usuwamy: ", end='')
                    for s in currentSingles:
                        if s == currentSingles[0]:
                            print(currentSingles[0], end=' -> ')
                        elif s == currentSingles[-1]:
                            print(s)
                        else:
                            print(s, end=' | ')
                if len(currentSingles) == len(rule):
                    replaceAll = True
                    nonTerminals.remove(currentSingles[0])
                ruleCounter = 0  # counts which rule is currently being worked with
                if currentSingles[0] == rules[0][0]:  # Removing singular productions from S (starting symbol)
                    for cS in currentSingles:
                        if cS == currentSingles[0]:
                            continue
                        if cS in terminals:
                            rules[0].remove(cS)
                            continue
                        for rule3 in rules:
                            if rule3[0] == cS:
                                for p in rule3:
                                    if p == rule3[0]:
                                        if pr:
                                            print("Wstawiamy do", rule[0][0], end=' -> ')
                                        continue
                                    if p not in rules[0]:
                                        rules[0].append(p)
                                        if pr:
                                            if p == rule3[-1]:
                                                print(p)
                                            else:
                                                print(p, end=' | ')
                                rules[0].remove(cS)
                    skip = True  # skip next part since it's already done
                while True:
                    if skip:
                        skip = False
                        ruleCounter += 1
                    if len(rules) <= ruleCounter:
                        break
                    rule2 = rules[ruleCounter]  # iterate through all the rules
                    productCounter = 0  # counts which product is currently being worked with
                    while True:
                        if productCounter >= len(rule2):
                            break
                        product = rule2[productCounter]  # iterate through all products in given rule
                        if rule2[0] == currentSingles[0] and product in currentSingles:  # found product which we want to replace with
                            if product == currentSingles[0]:  # this one stays (producer)
                                productCounter += 1
                                if productCounter >= len(rule2):
                                    break
                                continue
                            rules[ruleCounter].remove(product)  # remove singular symbol production
                            if len(rules[ruleCounter]) == 1:
                                rules.remove(rules[ruleCounter])
                            else:
                                productCounter -= 1
                        # elif rule2[0] == currentSingles[0]:
                        #     productCounter += 1
                        #     if productCounter >= len(rule2):
                        #         break
                        #     continue
                        else:
                            place = 1
                            for symbol in product:
                                if symbol == currentSingles[0]:  # found symbol we want to replace
                                    if replaceAll:
                                        try:
                                            rules[ruleCounter].remove(product)  # remove product, cuz later we'll be adding it with replacements
                                        except ValueError:
                                            pass
                                    for x in currentSingles:  # iterate through all possible productions
                                        if x == currentSingles[0]:  # skip first (producer)
                                            continue
                                        if not replaceAll:
                                            tmp = product.replace(symbol, x, place)
                                            tmp = tmp.replace(x, symbol, (place-1))
                                            if '^' in tmp and len(tmp) > 1:
                                                tmp = tmp.replace('^', '')
                                        else:
                                            tmp = product.replace(symbol, x, place)
                                            tmp = tmp.replace('^', '')
                                        if tmp not in rules[ruleCounter]:
                                            rules[ruleCounter].insert(productCounter, tmp)
                                            if pr:
                                                print("W", rule2[0], "zamieniamy", product, "na", tmp)
                                if symbol == currentSingles[0]:
                                    place += 1  # used to replace symbol only an one particular position

                        productCounter += 1  # next product
                    ruleCounter += 1  # next rules
                    if len(rules) <= ruleCounter:
                        currentSingles.clear()
                        break
                    if pr:
                        test = to_dic(rules)
                        print_production(test)
        currentSingles.clear()
        if rules not in history:
            history.append(rules)
        else:
            break

    try:  # try removing lambda
        terminals.remove('^')
    except ValueError:
        pass
    if remove_useless(nonTerminals.copy(), terminals.copy(), rules.copy(), pr=False) == -1:  # check if given grammar makes sense
        for x in history:  # x - rules set in history
            y = x[0]  # S productions from a given set
            for e in y:  # products in S productions
                for s in e:  # symbols in S products
                    if s in terminals and s not in rules[0]:  # singular terminal production was deleted, but should exist
                        rules[0].append(s)
    remove_useless(nonTerminals, terminals, rules, pr=False)


def print_production(productionRules):
    # Prints production rules
    for x in productionRules.keys():
        print(x, end=' -> ')
        if type(productionRules[x]) is tuple:
            for y in productionRules[x]:
                if y != productionRules[x][-1]:
                    print(y, end=' | ')
                else:
                    print(y)
        else:
            print(productionRules[x])




def chomsky(nonTerminals, terminals, productionRules, pr=True):
    # Transforms grammar with given production rules to Chomsky hierarchy
    availableNonTerminals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # Check which non-terminal symbols are really available
    for x in nonTerminals:
        availableNonTerminals = availableNonTerminals.replace(x, '')
    # Create list of production Rules
    rules = to_list(productionRules)
    remove_singles(nonTerminals, terminals, rules, lam=True, pr=True)
    #  remove_useless(nonTerminals, terminals, rules)  # no longer needed, remove_singles calls it anyway
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
                else: # TO DO found non-terminal symbol as a product
                    if pr:
                        print(rules[ruleCounter][0], end=' -> ')
                        print(rules[ruleCounter][productCounter], end=' ')
                        print("Zastepujemy: ", end='')
                        print(rules[ruleCounter][0], end=' -> ')
                    rules[ruleCounter].remove(p)
                    for a in rules:
                        if a[0] == p:
                            for b in a:
                                if b == a[0]:
                                    continue
                                if b == a[-1]:
                                    print(b, end=' ')
                                else:
                                    print(b, end=' | ')
                                rules[ruleCounter].insert(productCounter+1, b)
                    if pr:
                        print(', bo', p, end=' -> ')
                        for a in rules:
                            if a[0] == p:
                                for b in a:
                                    if b == a[0]:
                                        continue
                                    if b == a[-1]:
                                        print(b, end=' ')
                                    else:
                                        print(b, end=' | ')
                        print()
                    continue
                    # Producing lambda, cannot do that in Chomsky
                    # if find_producer('^', rules):
                    #     if pr:
                    #         print(rules[ruleCounter][0], end=' -> ')
                    #         print(rules[ruleCounter][productCounter], end=' ')
                    #         print("Zastepujemy: ", end='')
                    #         print(rules[ruleCounter][0], end=' -> ')
                    #         print(p + find_producer('^', rules))
                    #     rules[ruleCounter][productCounter] = p + find_producer('^', rules)
                    # else:
                    #     nT = availableNonTerminals[0]
                    #     availableNonTerminals = availableNonTerminals.replace(nT, '')
                    #     rules.append([nT, '^'])
                    #     nonTerminals.append(nT)
                    #     terminals.append('^')
                    #     if pr:
                    #         print(rules[ruleCounter][0], end=' -> ')
                    #         print(rules[ruleCounter][productCounter], end=' ')
                    #         print("Zastepujemy: ", end='')
                    #         print(rules[ruleCounter][0], end=' -> ')
                    #         print(p + nT, ", gdzie:", nT, " -> '^'")
                    #     rules[ruleCounter][productCounter] = p + nT
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
                                print(", gdzie:", nT, " -> ", p[0])
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
                                print(", gdzie:", find_producer(symbol, rules), ' -> ', symbol)
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
                                print(", gdzie:", nT, ' -> ', symbol)
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
                                print(", gdzie:", find_producer(pair, rules), " -> ", pair)
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
                    print(", gdzie:", nT, ' -> ', pair)
                rules[ruleCounter][productCounter] = rules[ruleCounter][productCounter].replace(pair, nT, 1)
                continue

            productCounter += 1
            if productCounter == len(x):
                break
        ruleCounter += 1
        productCounter = 0
        if len(rules) == ruleCounter:
            break
    remove_useless(nonTerminals, terminals, rules)
    result = {}
    for rule in rules:
        result[rule[0]] = tuple(rule[1:])
    return nonTerminals, terminals, result

