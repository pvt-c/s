from tabulate import tabulate

no_of_prod = int(input("Enter no. of productions : "))
startSymbol = input("Enter start symbol : ")
productions = []
# no_of_prod = 3
# startSymbol = 'E'
# productions = [
#     'E->E+E',
#     'E->E*E',
#     'E->id'
# ]

for i in range(no_of_prod):
    temp = input(f"Production {i+1} : ").replace(" ", "").split('->')
    try:
        vals = temp[1].split('|')
        for j in vals:
            productions.append(f"{temp[0]}->{j}")
    except Exception as e:
        print(e)
        
operators = input('Enter all operators separated by commas : ')
operatorsList = operators.replace(" ", "").split(",")
operatorsList.append('$')
# operatorsList = ['E', 'id', '+', '*', '$']

operatorPrecedenceTable = []
for i in range(0, len(operatorsList)):
    temp = []
    for j in range(0, len(operatorsList)):
        temp.append(input(f'Operator precedence of {operatorsList[i]}, {operatorsList[j]} : '))
    operatorPrecedenceTable.append(temp)

# operatorPrecedenceTable = [
#     ['', '', '<', '<', ''],
#     ['', '', '>', '>', '>'],
#     ['<', '<', '>', '<', '>'],
#     ['<', '<', '>', '>', '>'],
#     ['<', '<', '<', '<', ''],
# ]
temp = []
for i in operatorPrecedenceTable:
    temp.append([operatorsList[operatorPrecedenceTable.index(i)]] + i)
print('\n---------Operator Precedence Table---------')
print(tabulate(temp, tablefmt="simple_grid", headers=operatorsList))

ip = input('\nEnter string to parse : ')
# ip = 'id,+,id,*,id'
ip += ',$'

ip = ip.split(',')

prodRHS = [x.split('->')[1] for x in productions]

stack = ['$']
track = []
flag = True
while flag:
    x = stack[-1]
    y = ip[0]
    op = operatorPrecedenceTable[operatorsList.index(x)][operatorsList.index(y)]
    
    if x == startSymbol and y == '$':
        if len(stack) == 2:
            track.append([''.join(stack), ''.join(ip), 'ACCEPT'])
            break
        else:
            for j in reversed(range(1, len(stack))):
                eq = ''.join(stack[j:len(stack)])
                if eq in prodRHS:
                    temp = prodRHS.index(eq)
                    track.append([''.join(stack), ''.join(ip), f'Reduce {productions[temp]}'])
                    stack[j:len(stack)] = productions[temp].split('->')[0]
                    break

    else:
        if op == '<' or op == '=':
            track.append([''.join(stack), ''.join(ip), 'Shift'])
            stack.append(y)
            ip = ip[1:]
        elif op == '>':
            for j in reversed(range(1, len(stack))):
                eq = ''.join(stack[j:len(stack)])
                if eq in prodRHS:
                    temp = prodRHS.index(eq)
                    track.append([''.join(stack), ''.join(ip), f'Reduce {productions[temp]}'])
                    stack[j:len(stack)] = productions[temp].split('->')[0]
                    break
                    # flag = False
        else:
            track.append([''.join(stack), ''.join(ip), 'REJECT'])
            break

print('\n---------Parse Table---------')
print(tabulate(track, tablefmt="simple_grid", headers=['Stack', 'Input Tape', 'Action']))
