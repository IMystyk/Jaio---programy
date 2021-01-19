# This module implements an algorithm to transform given grammar to Greibach's form

from Chomsky import *

def find_productions(nonTerminal, rules):
    #  Returns list of products produced by given non-terminal symbol
    products = []
    for rule in rules:
        if rule[0] == nonTerminal:
            for product in rule:
                if product == rule[0]:
                    continue
                products.append(product)
    return products
def greibach(nonTerminals, terminals, productionRules, pr=True):
    # This function transforms given grammar, nonTerminals: non-terminal symbols list, terminals: terminal symbols list
    # productionRules: dictionary with production rules, pr:checks if user wants an output printed (default - True)
    nonTerminals, terminals, productionRules = chomsky(nonTerminals, terminals, productionRules, pr=False) # transform
    # given grammar to The Chomsky hierarchy (because that's how the programmer decided to proceed)
    rules = to_list(productionRules) # create list out of a dictionary (first element in each list is a key from ditionary)
    availableNonTerminals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # list af all possible symbols that can be non-terminal symbols
    for x in nonTerminals:
        availableNonTerminals = availableNonTerminals.replace(x, '') # Check which symbols are already in use and remove them
    alfas = []  # list to store alfas
    betas = []  # list to store betas
    #  Trying to use 2nd lemma if possible
    ruleCounter = 0
    productCounter = 0
    while True:
        if ruleCounter >= len(rules):
            break
        rule = rules[ruleCounter]
        while True:
            if productCounter >= len(rule):
                break
            product = rule[productCounter]
            if product == rule[0]:
                productCounter += 1
                continue
            if product[0] == rule[0]:  # found symbol at the first place on the right side
                alfas.append(product[1:])
            else:
                betas.append(product)
            productCounter += 1
        if len(alfas) == 0:
            betas.clear()
        else:
            if pr:
                print("Usuwamy produkcje zawierające wyrazy alfa w", rules[ruleCounter][0])
            for alfa in alfas:
                rules[ruleCounter].remove(rules[ruleCounter][0] + alfa)  # remove productions with alfas
                if pr:
                    print("Z", rules[ruleCounter][0], end=' -> ')
                    print("usuwamy", end=' ')
                    if alfa == alfas[-1]:
                        print(alfa)
                    else:
                        print(alfa, end=' | ')
            nT = availableNonTerminals[0]
            availableNonTerminals = availableNonTerminals.replace(nT, '')
            nonTerminals.append(nT)
            if pr:
                print("Dodajemy produkcje:", rules[ruleCounter][0], end=" -> ")
            for beta in betas:
                if pr:
                    if beta == betas[-1]:
                        print(beta)
                    else:
                        print(beta, end=' | ')
                rules[ruleCounter].append(beta + nT)  # add new production to beta productions
            newRule = [nT]  # create new production rule
            if pr:
                print("Dodajemy nowa regule produkcji", nT, end=' -> ')
            for alfa in alfas:
                if pr:
                    if alfa == alfas[-1]:
                        print(alfa, "|", alfa + nT)
                    else:
                        print(alfa, "|", alfa + nT, end=" | ")
                newRule.append(alfa)
                newRule.append(alfa + nT)
            rules.append(newRule.copy())
            betas.clear()
            alfas.clear()
        print_production(to_dic(rules))
        ruleCounter += 1
        productCounter = 0
    #  Now use 1st lemma
    done = []  # create list with already done productions
    notDone = []  # create list with to-be-done productions
    ready = True
    for rule in rules:
        for product in rule:
            if product == rule[0]:
                continue
            if product[0] in nonTerminals:
                notDone.append(rule[0])
                ready = False
                break
        if ready:
            done.append(rule[0])
        ready = True
    ruleCounter = len(rules) - 1
    productCounter = 0
    tmp = []  # used to contain temporary rules
    while True:
        if ruleCounter < 0:
            if len(notDone) == 0:
                break
            else:
                ruleCounter = len(rules) - 1
                continue
        rule = rules[ruleCounter]
        if rule[0] in done:  # just a small optimization
            ruleCounter -= 1
            continue
        if pr:
            repeat = []
            message = "W "
            message += rules[ruleCounter][0]
            message += ' zamieniamy '
        while True:
            if productCounter >= len(rule):
                break
            product = rule[productCounter]
            if product == rule[0]:
                tmp.append(product)
                productCounter += 1
                continue
            if product[0] in nonTerminals:  # product starts with non-terminal symbol
                if product[0] not in done:  # impossible to transform yet
                    productCounter = len(rule)
                    tmp.clear()
                    continue
                else:
                    products = find_productions(product[0], rules)
                    for res in products:
                        tmp.append(res + product[1:])
                    if pr:
                        if product[0] not in repeat:
                            repeat.append(product[0])
                            message += product[0]
                            message += " na "
                            message += str(products)
                            message += " "
            else:
                tmp.append(product)
            productCounter += 1
        if len(tmp) > 1:  # we were able to fully transform given productions
            rules[ruleCounter] = tmp.copy()
            tmp.clear()
            done.append(rules[ruleCounter][0])
            notDone.remove(rules[ruleCounter][0])
            if pr:
                print(message)
            print_production(to_dic(rules))
        tmp.clear()
        ruleCounter -= 1
        productCounter = 0
    remove_useless(nonTerminals, terminals, rules)

