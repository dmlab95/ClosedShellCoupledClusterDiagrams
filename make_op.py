from call_wicks import * 
from operator import mul
from math import factorial as fact
from copy import deepcopy
import os.path

def write_in_tex(list_op):
 
    flag = int(list_op == ['V'])
    f = open("result.tex", "a+" )
    if len(list_op) == 1:
        f.write('\\vskip 0.2in')
        f.write('\centerline{\underline{' + ['F', 'V'][flag] + ' Term}}\n')
        f.write('\t$$' + ['F^{a}_{i}', 'V^{ab}_{ij}'][flag] + '\n$$\n\\vskip 0.5in')
	return [1, [['a', 'b'][: 1 + flag], ['i', 'j'][: 1 + flag]]] 


def make_op(oplst, cctyp, val):   #oplst = ['V', 'T1', 'T1', 'T2']

    print oplst
    dict1 = {'V': 2, 'F': 1, 'T1': 1, 'T2': 2, 'T3': 6, 'T4':8}
    holes = 'klmnot'
    particles = 'cdefgh'
    #actives = 'uvwxyz'
    fu, fl = 'pq'[:dict1[oplst[0]]], 'rs'[:dict1[oplst[0]]]
    operators = [int(i[1]) for i in oplst[1:]]
    cnt = sum(operators)
    temp = [1] + [oplst.count(i) for i in set(oplst[1:]) if oplst.count(i) > 1]
    prefactor = 1. * reduce(mul, [dict1.get(i, 1) for i in oplst]) * reduce(mul, [fact(i) for i in temp])
    su, sl = particles[val: cnt + val], holes[val: cnt + val]
    print '\nprefactor ', prefactor,  '\nfirst operator(up, down) ', fu, fl,  '\nsecond operator(up, down)', \
    su, sl, "\n"
    
    flag = int(oplst == ['V'])
    f = open("result.tex", "a+" )
    book = {i: operators.count(i) for i in set(operators)}
    if os.path.isfile("result.tex"):
        com = '\t$' + oplst[0] + ''.join(['T_{}^{}'.format(i, j), 'T_{}'.format(i)][j == 1] for i, j in book.items()) + '$ '
        statement = '\n\centerline{\underline{' + com + ' Terms}}\n'
        if statement not in f.read():
            f.write(statement)
    
    return operators, prefactor, fu, fl, su, sl


def driver_initial(list_op, cctyp, nbody):

    operators, prefactor, fu, fl, su, sl = make_op(list_op, cctyp, nbody)
    fu, fl, su, sl = arrange_input(fu, fl, su, sl)
    return wicks(prefactor, fu, fl, su, sl, 1, operators, cctyp, nbody)


def driver(list_op, cctyp):
 
    write_in_tex(list_op)
    if len(list_op) == 1:
	return

    rhs_oplst = sum(int(T[1]) for T in list_op[1:]) - (len(list_op) > 2)
    val = max(0, min(rhs_oplst, len(cctyp) - 2) - 2)                   #val => max nbody HT complex can form from this oplst
    print 'val ', val
    for nbody in range(val + 1):
        driver_initial(list_op, cctyp, nbody)


if __name__ == '__main__':
    print driver(['V','T1','T2'], cctyp)
