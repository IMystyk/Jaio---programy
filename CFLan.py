# This modules implements generating context-free language from a given grammar
from Chomsky import *
from collections import deque



def lang(nonTerminals, terminals, productionRules, pr=True):
    #  Generates language from a given grammar
    #  TODO don't use it, it's not done!!
    rules = to_list(productionRules)
    remove_useless(nonTerminals, terminals, rules)  # remove useless productions (if any exist)
    productionRules = {}
    for rule in rules:
        productionRules[rule[0]] = rule[1:]
    posIndexes = "abcdefghijklmnopqrstuvwxyz"
    for t in terminals:
        posIndexes = posIndexes.replace(t, '')
    toRemove = []  # list of products that have to be removed
    results = []  # results stored as a list, cuz every 'OR' ('+') creates new element in the list
    #  Search for loops and replace productions if any loops are found
    while True:  # do it until no loops are found
        loopsFound = False
        for nT in reversed(nonTerminals):
            if find_loops(nT, nonTerminals, productionRules):  # found a loop
                loopsFound = True
                for key in productionRules.keys():
                    if key == nT:
                        continue
                    replace_productions(productionRules[key], productionRules[nT], nT)
                recursion = False
                for product in productionRules[nT]:
                    if nT in product:
                        productionRules[nT].remove(product)
                        recursion = True
                if len(productionRules[nT]) == 0 or not recursion:
                    del productionRules[nT]
                    nonTerminals.remove(nT)
                for key in productionRules.keys():
                    for product in productionRules[key]:
                        if product == key:
                            productionRules[key].remove(product)
                break
        if not loopsFound:
            break
    # TODO decide whether to go for one long productions S -> all (if possible) or removing productions individually
    recursions = []  # list of recursive productions of a particular symbol
    language = ""  # our result, follows given pattern: [n] - index
    for key in productionRules.keys():
        current = key
        language += key  # append first non-terminal
        break
    for product in productionRules[current]:
        if current in product:
            recursions.append(product)  # make a list of all recursive productions
    for product in recursions:
        tmp = language.replace(current, product)

    while True:
        # TODO make break condition
        pass






def find_loops(nonTerminal, nonTerminals, productionRules):
    #  Searches for loops like A -> B, B -> A and returns true if any are found for a particular non-terminal
    for key in productionRules.keys():
        if key == nonTerminal:
            continue
        else:
            for product in productionRules[nonTerminal]:
                if key in product:
                    if try_produce(nonTerminal, key, nonTerminals, to_list(productionRules)):
                        return True
    return False


def try_produce(product, producer, nonTerminals, rules):
    #  Tries to produce given product from a given producer
    toUse = deque()
    toUse.append(producer)
    used = []
    while True:
        try:
            p = toUse.popleft()
        except IndexError:  # queue is empty
            break
        if p in used:
            continue
        used.append(p)
        for rule in rules:
            if rule[0] == p:
                for elements in rule:
                    for element in elements:
                        for symbol in element:
                            if symbol in nonTerminals and symbol not in used and symbol != product:
                                toUse.append(symbol)
                            elif symbol == product:
                                return True
    return False


def replace_productions(rule, replacements, target):
    # replaces given symbol (target) in given production rule
    replace = False
    for product in rule:
        if target in product:  # check if there is anything to replace
            replace = True
            break
    if not replace:
        return rule
    recursion = False
    for product in replacements:
        if target in product:  # does target produce itself
            recursion = True  # found recursion
            break
    toRemove = []
    if not recursion:  # replace with no recursions
        for product in rule:
            if target not in product:
                continue
            toRemove.append(product)  # this product is obsolete
            for repl in replacements:  # iterate through all possible productions
                tmp = product.replace(target, repl, 1)  # replace one symbol with one production
                if '^' in tmp and len(tmp) != tmp.count('^'):  # remove lambda production if it's not alone
                    tmp = tmp.replace('^', '')
                elif '^' in tmp and len(tmp) == tmp.count('^'):  # replace multiple lambdas with a single one
                    tmp = '^'
                if tmp not in rule:
                    rule.append(tmp)  # append newly created production if not already in productions
        for product in toRemove:
            try:
                rule.remove(product)
            except ValueError:  # given product has already been removed
                pass
        toRemove.clear()
        return rule
    else:  # replace with recursion (the reason this function came to be)
        maxProducts = len(rule)  # how many products does the given set have
        productCounter = 0  # which product is currently being worked with
        while True:
            if productCounter >= maxProducts:  # all initial products have been checked
                break
            product = rule[productCounter]  # choose current product based on a productCounter
            if target in product:  # check if our target symbol is in given product
                toAppend = []  # products that will be added with the number how many times target occurs due to recursion
                toAppend.append([product, 0])
                toRemove.append(product)
                for element in toAppend:
                    targetOccurrences = element[0].count(target)  # how many times target symbol occurs
                    if targetOccurrences == element[1]:  # target occurrences are only due to recursion (same number)
                        continue
                    for repl in replacements:
                        targetOccurrences = element[1]  # set the number of recursion-created targets
                        targetOccurrences += repl.count(target)  # if target produces itself add a number how many copies it produces
                        tmp = element[0].replace(target, repl, element[1] + 1)  # replace one more target than recursion number
                        tmp = tmp.replace(repl, target, element[1])  # restore recursion-created targets
                        if '^' in tmp and len(tmp) != tmp.count('^'):
                            tmp = tmp.replace('^', '')  # remove lambda production if it's not alone
                        elif '^' in tmp and len(tmp) == tmp.count('^'):  # replace multiple lambdas with a single one
                            tmp = '^'
                        toAppend.append([tmp, targetOccurrences])
                        if target in tmp and targetOccurrences != tmp.count(target):
                            toRemove.append(tmp)
                for element in toAppend:
                    if element[0] not in rule:
                        rule.append(element[0])  # append newly created products (even not complete ones)
            productCounter += 1
        for product in toRemove:
            try:
                rule.remove(product)
            except ValueError:  # given product has already been removed
                pass
        toRemove.clear()
        return rule


