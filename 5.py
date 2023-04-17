from tabulate import tabulate

# no_of_prod = int(input("Enter no. of productions : "))
# separator = input("Enter Separator : ")
# epsilon = input("Enter Epsilon : ")
# startSymbol = input("Enter start symbol : ")
no_of_prod = 5
separator = '->'
epsilon = 'e'
startSymbol = 'E'

terminals = [
    'i', '+', '*', '(', ')', '$' 
]
variables = [
    'E', 'L', 'T', 'K', 'F'
]
productions = [
    'E->TL',
    'L->+TL|e',
    'T->FK',
    'K->*FK|e',
    'F->i|(E)'
]

# productions = []
# terminals = []
# variables = []
# for i in range(no_of_prod):
#     temp = input(f"Production {i+1} : ").replace(" ", "").split(separator)
#     if temp[0].isupper() and temp[0] not in variables:
#         variables.append(temp[0])
#     productions.append(f"{temp[0]}{separator}{temp[1]}")

# terminals = input("Enter the terminals : ").replace(" ", "").split(',')

FIRST = {
    'E': ['i', '('],
    'L': ['+', 'e'],
    'T': ['i', '('],
    'K': ['*', 'e'],
    'F': ['i', '('],
}
FOLLOW = {
    'E': [')', '$'],
    'L': [')', '$'],
    'T': ['+', ')', '$'],
    'K': ['+', ')', '$'],
    'F': ['*', '+', ')', '$'],
}

# FIRST = {}
# FOLLOW = {}
# for i in variables:
#     FIRST[i] = input(f'Enter FIRST({i}) : ').replace(" ", "").split(',')
#     FOLLOW[i] = input(f'Enter FOLLOW({i}) : ').replace(" ", "").split(',')

parseTable = []
temp = [''] + terminals
parseTable.append(temp)

for j in FIRST.keys():
    print(j)
    row = ['' for x in terminals]
    row = [j] + row
    for i in FIRST[j]:
        for k in terminals:
            # print(k, '   ', i)
            if (i == epsilon):
                # print('null', terminals.index(k))
                for z in FOLLOW[j]:
                    if z == k:
                        row[terminals.index(k) + 1] = f'{j} {separator} {epsilon}'
            elif(i == k):
                # print('match', terminals.index(k))
                production = ''
                for prod in productions:
                    if prod.startswith(j):
                        production = prod
                        break
                temp = production.split(separator)[1].split('|')
                # print(temp)
                production = temp[0]
                for x in temp:
                    if x.startswith(i):
                        production = x
                row[terminals.index(k) + 1] = f'{j} {separator} {production}'
    parseTable.append(row)

print(tabulate(parseTable, tablefmt="simple_grid"))

valid = True

while valid:
    ipString = input("\nEnter string to parse : ")
    ipString = ipString + '$'
    stack = '$' + startSymbol

    flag = True

    parseString = []
    while flag:
        b = stack[-1]
        a = ipString[0]
        if a == b == '$':
            # parseString.append(['', '', 'String accepted'])
            parseString[-1][2] = 'String accepted'
            flag = False
        elif a == b:
            stack = stack[:-1]
            ipString = ipString[1:]
            parseString.append([stack, ipString, f'Pop {a}'])
        else:
            if (b == epsilon):
                stack = stack[:-1]
                parseString.append([stack, ipString, ''])
            else:
                i = variables.index(b) + 1
                j = terminals.index(a) + 1
                if parseTable[i][j] == '':
                    parseString.append([stack, ipString, 'String rejected'])
                    flag = False
                    valid = False
                else:
                    stack = stack[:-1]
                    stack = stack + parseTable[i][j].replace(" ", "").split(separator)[1][::-1]
                    parseString.append([stack, ipString, parseTable[i][j]])
        
    print(tabulate(parseString, tablefmt="simple_grid"))
