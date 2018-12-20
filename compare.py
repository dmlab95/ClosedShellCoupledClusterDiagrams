from functions import *
from collections import OrderedDict
from copy import deepcopy

#========================Policy for comparison of terms with similar factor & h, p contractions
#--------------------------------create a five argument check list for each term
'''
EXAMPLE: V T2
i) contracted term: [1, ('k1', 'k0'), ('l1', 'l0'), ['a1', 'b1', 'i0', 'j0']], [factor, H, T] = [1, ('k', 'l', 'i', 'j'), ('a', 'b', 'k', 'l')]'''
#H^kl_ij T^ab_kl ==> fu = ['k', 'l'], fl = ['i', j], su = ['a', 'b'], sl = ['k', 'l']
'''
ii)contracted term: [-1, ('k1', 'k0'), ('c0', 'c1'), ['a1', 'b1', 'i0', 'j0']], [factor, H, T] = [-1, ('k', 'a', 'i', 'c'), ('c', 'b', 'k', 'j')]'''
#H^ka_ic T^cb_kj ==> fu = ['k', 'a'], fl = ['i', 'c'], su = ['c', 'b'], sl = ['k', 'j']

#get  [factor, #holes_contr., #part. contr., sorted(fcol1, fcol2), sorted(scol1, scol2, ...), connectivity b/w each pair of vertices] 
#For i) [1.0,        2,             0,            (h,    h),              (p,   p)     ]                
'''                  k,l                           i     j                 a    b
For ii)[-1.0,        1              1,            (h,    p),              (0,   hp)     '''
#                    k              c              i     a                 -    jb
'''
fcol1 = vertex 1 of first operator i.e. H                         
scol1 = vertex 1 of second operator i.e. composite T
'''

#create op1, op2, op3, op4
#as fcol, scol will not suffice for VT1^4 type of terms
#here if (factor, V, T2, T2) i.e. len() > 3
#(factor, 'V', 'T1', 'T1', 'T2') --> 
#scol = [['c', 'k'], ['d', 'l'], ['a', 'i'], ['b', 'j']]

def get_vertices1(operators, s_col, val):
   
    dict1 = {i: 1 for i in 'abcd'[:val] + 'ijkl'[:val]}
    op1_col, op2_col, op3_col, op4_col = [], [], [], []
    rhs_op_lst = [op1_col, op2_col, op3_col, op4_col][:len(operators)][::-1]
    count = [0, 0, 0, 0][:len(operators)][::-1]
    #will've to create these from s_col
    cnt = 0
    for i in s_col:
        if cnt >= sum(operators):
            break
        for index, op_col in enumerate(rhs_op_lst):
            if cnt >= sum(operators):
	        break
	    op_col.append(s_col[cnt])
            count[index] += sum(dict1.get(i, 0) for i in s_col[cnt])
            cnt += 1

    flag = False
    for i, j in zip(count, operators[::-1]):
	if i >= 2 * j:
	    flag = True
                        #i, a or j, b or i, j, a, b on same operator
    #print 'rhs_op_lst ',  rhs_op_lst[::-1], flag, count[::-1], "\n"
    return rhs_op_lst[::-1], flag



def get_vertices(operators, s_col, val):          
   
    dict1 = {i: 1 for i in 'abcd'[:val] + 'ijkl'[:val]}
    op1_col, op2_col, op3_col, op4_col = [], [], [], []
    rhs_op_lst = [op1_col, op2_col, op3_col, op4_col][:len(operators)][::-1]
    count = [0, 0, 0, 0][:len(operators)][::-1]
    #will've to create these from s_col

    for index, op_col in enumerate(rhs_op_lst):
        if index == 0:
	    k = index
	else:
	    k += len(rhs_op_lst[index - 1])
	rhs_op_lst[index] = s_col[k : k + operators[index]]
	count[index] += sum(dict1.get(j, 0) for i in s_col[k : k + operators[index]] for j in i)
    flag = False
    for i, j in zip(count, operators):
	if i >= 2 * j:                #if jth operator has all lines not connected to H
	    flag = True               #=> (i, a) or (j, b) or (i, j, a, b) or more on same operator

    #print 's_col ',  s_col
    print 'rhs_op_lst ',  rhs_op_lst, count, "\n"
    return rhs_op_lst, flag

operators = [1,2]   #i.e. operators == ['H', 'T1', 'T2'], H = F or V
scol = [['a', 'i'], ['b', 'l'], ['e', 'm']]
#print get_vertices(operators, scol, 2)

#-------------------------Create connectivity between lhs & rhs operators
'''                     list of contr.(#h, #p, #loops, rank_of_operator) b\w each vertices of H(=Fcol) & all Ts'(=Rhs_oplst1)
input:    Fcol, Rhs_oplst1 = [['k', 'c'], ['l', 'd']], [['d', 'l'], ['b', 'j']], [['c', 'k'], ['a', 'i']]
output:   lst = sorted(sorted ((0, 0, 0, 2), (1, 1, 1, 2)), sorted((1, 1, 1, 2), (0, 0, 0, 2)) )
'''
def connectivity(fcol, rhs_op_lst1):
    
    lst = []
    for vertex in fcol:
        temp = []
        for op in rhs_op_lst1:
            rhs = set([j for i in op for j in i])
	    contracted_holes = len(set(vertex) & rhs & set('ijklmnot'))
	    contracted_particles = len(set(vertex) & rhs & set('abcdefgh'))           
	    loops = any(set(vertex) == set(op[i]) for i in range(len(op))) #for all n in Tn 
	    temp.append(tuple([contracted_holes, contracted_particles, int(loops), len(op)]))
	lst.append(tuple(sorted(temp)))
    return tuple(sorted(lst))


#======================create a five argument check list for each term
'''                       Will NOT be this simple for open shell!!!
'''
def checklist(term, operators, fcol, scol, sector = 2):       # expression = [factor, H, T]
                                                              # operators = [2, 2] for VT2^2, [2, 2]-->[T2, T2]
    holes_contracted, particles_contracted = 0, 0            
    for contraction in term[1:-1]:
	if contraction[0][0] in 'ijklmnot' + 'uvwxyz' * (sector == 1):
	    holes_contracted += 1
	elif contraction[0][0] in 'abcdefgh' + 'uvwxyz' * (sector == 2):
	    particles_contracted += 1

#    d1 = {('a',): 'P', ('b',): 'P', ('i',): 'H', ('j',): 'H', ('b', 'j'): 'HP', \
#    ('a', 'i'): 'HP', ('a', 'j'): 'HP', ('b', 'i'): 'HP'}          #for CCSD
#-------for 1b and 2b HT complex, val is 2, i.e. iajb
#-------but from CCSDT 3B terms, val = 3 etc

    val = max(2, len(term[-1])//2)            #no of open lines in a term
    d1 = {tuple(x): ('H' if x in 'ijkl'[:val] else 'P') for x in 'abcd'[:val] + 'ijkl'[:val]}
    d = {(y, x): 'HP' for x in 'ijkl'[:val] for y in 'abcd'[:val]}
    d1.update(d)

    first_op_open_indices = [tuple(sorted(set(i) & set('ijkl'[:val] + 'abcd'[:val]))) for i in fcol]
    f = tuple(sorted([d1.get(i, None) for i in first_op_open_indices]))

    if len(operators) == 1:                    #CASE 1. linear T
        second_op_open_indices = [tuple(sorted(set(i) & set('ijkl'[:val] + 'abcd'[:val]))) for i in scol]
        s = [d1.get(i, None) for i in second_op_open_indices]
        return [scol], tuple([term[0], holes_contracted, particles_contracted, f, tuple(sorted(s))])

    rhs_op_lst, flag = get_vertices(operators, scol, val)
    if flag:
	return [None], (None,)

    rhs_op_lst1 = deepcopy(rhs_op_lst)    
    for index, op in enumerate(rhs_op_lst):
        op = [tuple(sorted(set(i) & set('ijkl'[:val] + 'abcd'[:val]))) for i in op]
        op = [tuple(set(i) & set('ijkl'[:val] + 'abcd'[:val])) for i in op]
        rhs_op_lst[index] = tuple([d1.get(i, None) if i else None for i in op])

                                             #CASE 2. H has open lines
    if f != (None, None):
        return rhs_op_lst1, tuple([term[0], holes_contracted, particles_contracted, f, \
        tuple(sorted([tuple(sorted(op)) for op in rhs_op_lst])), connectivity(fcol, rhs_op_lst1)])
   
                                             #CASE 3. H is fully contracted

    return rhs_op_lst1, tuple([term[0], holes_contracted, particles_contracted, tuple(sorted([tuple(sorted(op)) for op in rhs_op_lst])), \
    connectivity(fcol, rhs_op_lst1)])



operators = [1,1,2]
fcol = [['k','c'], ['l','d']]
scol = [['j', 'c'], ['a', 'l'], ['b', 'k'],['d','i']]
term = [1,('k1', 'k0'), ('c0', 'c1'), ('l0','l1'), ('d0','d1'), ('a1','b1','i0','j0')]
#print checklist(term, operators, fcol, scol, sector = 2)

#======================differentiate b/w 1b, 2b, 3b & 4b excitations, store in 4 dictionaries
#----------------------using 5 arg. checklist as key, add prefactors up if repeated
#--------------------- cctyp not needed as argument, pool has same info
'''                    pool = pool_1b, ... pool_nb, n = {'CCSD': 2, 'CCSDT':3, 'CCSDTQ':4}'''

def create_uniq_expressions(term, expressions, operators, f_col, s_col, pool):
    
    rhs_op_lst, chk = checklist(term, operators, f_col, s_col, sector = 2) 
    #print "rhs_op_lst, chk, term ", rhs_op_lst, chk, term
    if not chk:
	for pool_nb in pool:
	    pool_nb[chk] = None 
        return pool

    for index, pool_nb in enumerate(pool, 1):
        if len(term[-1]) == 2 * index:    #for 1b, 2 indices are open & so on
            if chk not in pool_nb.keys():
                pool_nb[chk] = [term[0]] + [f_col] + rhs_op_lst
            else: 
                pool_nb[chk] = [pool_nb[chk][0] + term[0]] + pool_nb[chk][1:]
            #print 'pool_' + str(index) + 'b ', pool_nb.items()
    return pool



#===================finalize 2 dictionaries as output after comparing each terms
'''----------------------dict.values() are the 1b & 2b final expressions       
'''

def create_final_list(ans_lst, indices, operators, cctyp='CCSD', sector=2):

    ans = []             #Store [factor, (contractions).., [open indices]] == term
    expressions = []     #Store [factor, H(?,?,?,?), T(?,?,?,?)] ---> Actually needed
    checklist_pool_1b = OrderedDict()
    checklist_pool_2b = OrderedDict()              #for cctyp='CCSD' onwards
    checklist_pool_3b = OrderedDict()              #for cctyp='CCSDT' onwards
    checklist_pool_4b = OrderedDict()              #for cctyp='CCSDTQ'
    checklist_pool = [checklist_pool_1b, checklist_pool_2b, checklist_pool_3b, checklist_pool_4b][:len(cctyp)-2]
    for term, indices_for_term in zip(ans_lst, indices):
        fu, fl, su, sl = indices_for_term
        f_col, s_col = cols(fu, fl, su, sl)
        ans.append(factor(term, f_col, s_col, sector))
        term = ans[-1]
        H = tuple([i[0] for i in fu + fl])
        T = tuple([i[0] for i in su + sl])
        expressions.append([ans[-1][0], H, T])
        #print 'expression ', expressions[-1]
        checklist_pool = create_uniq_expressions(term, expressions, operators, f_col, s_col, checklist_pool)
    
    return ans, expressions, checklist_pool
