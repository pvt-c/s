from tabulate import tabulate

print("Enter code (Ctrl-Z to save it) : \n")
# contents = [
# 'MACRO INCR &X,&Y,&REG1',
# 'MOVER &REG1,&X',
# 'ADD &REG1,&Y',
# 'MOVEM &REG1,&X',
# 'MEND',
# 'MACRO DECR &A,&B,&REG2',
# 'MOVER &REG2,&A',
# 'SUB &REG2,&B',
# 'MOVEM &REG2,&A',
# 'INCR &A,&B,&REG2',
# 'MEND',
# 'START 100',
# 'READ N1',
# 'READ N2',
# 'READ N3',
# 'DECR N1,N2,N3',
# 'STOP',
# 'N1 DS 1',
# 'N2 DS 2',
# 'N3 DS 3',
# 'END',
# ]
ipCode = []
contents = []
while True:
    try:
        line = input()
    except EOFError:
        break
    contents.append(line)

MNT = []
ALA = []
MDT = []
alaList = []
macroName = False
mntIndex = 0
mdtIndex = 1
alaIndex = 1

for i in contents:
    if i[0:5].upper() == 'MACRO':
        macroName = True
        temp = i.upper().replace('MACRO', '').strip().split()
        MNT.append([mdtIndex, temp[0], mntIndex])
        mdtIndex += 1
       
        # ALA
        alas = temp[1].split('=', 1)[0].split(',')
        for j in alas:
            alaList.append(j)
            ALA.append([f'#{alaIndex}', j])
            alaIndex += 1
        MDT.append([mntIndex, f'{temp[0]} {temp[1]}'])
       
        mntIndex += 1
    elif i[0:4].upper() == 'MEND':
        macroName = False
        MDT.append([mntIndex, 'MEND'])
        mntIndex += 1
    else:
        if macroName == True:
            for j in alaList:
                if j in i:
                    i = i.replace(j, f'#{alaList.index(j)+1}')
            MDT.append([mntIndex, i])
            mntIndex += 1
        else:
            ipCode.append(i)

print('\n===========PASS 1===========')
print('\n-----------MNT-----------')
print(tabulate(MNT, tablefmt="simple_grid", headers=['Index', 'Macro Name', 'MDT Index']))
print('\n-----------ALA-----------')
print(tabulate(ALA, tablefmt="simple_grid", headers=['Positional Arguments', 'Dummy Arguments']))
print('\n-----------MDT-----------')
print(tabulate(MDT, tablefmt="simple_grid", headers=['Index', 'Code']))




























# ipCode = [
#     'START 100',
#     'READ N1',
#     'READ N2',
#     'READ N3',
#     'DECR N1,N2,N3',
#     'STOP',
#     'N1 DS 1',
#     'N2 DS 2',
#     'N3 DS 3',
#     'END',
# ]

i = 0
ala_ip = []
ala_code = []
ala_index = []
while i < len(ipCode):
    j = 0
    while j < len(MNT):
        if ipCode[i].split()[0] == MNT[j][1]:
            startIndex = MNT[j][2]
            try:
                endIndex = MNT[j+1][2] - 1
            except IndexError:
                endIndex = len(MDT) - 1
            ipIndex = i
            ala_ip += ipCode[i].split()[1].split(',')
            ala_code += MDT[startIndex][1].split()[1].split(',')
            for k in MDT[startIndex][1].split()[1].split(','):
                for x in ALA:
                    if x[1] == k:
                        temp = x[0]
                ala_index.append(temp)
            del ipCode[i]
            for k in range(startIndex, endIndex):
                temp = MDT[k][1]
                for x in range(0, len(ala_ip)):
                    temp = temp.replace(ala_index[x], ala_ip[x])
                    temp = temp.replace(ala_code[x], ala_ip[x])
                ipCode.insert(ipIndex, temp)
                ipIndex += 1
            break
        j += 1
    i += 1

pass2 = []
for i, index in enumerate(ipCode):
    pass2.append([i, index])


print('\n===========PASS 2===========')
print(tabulate(pass2, tablefmt="simple_grid", headers=['Index', 'Code']))