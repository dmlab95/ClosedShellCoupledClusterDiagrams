

#========================Differentiate b/w 1st & 2nd operator string

def distinguish_2strings(fu, fl, su, sl):
    d1 = {i: 1 for i in fu + fl}
    d2 = {k: -1 for k in su + sl}
    d = d1.copy()
    d.update(d2)
    return d

#========================Get the prefactor and sign

'''[(-0.5, 'p1', 'k0'), (-0.5, 'q1', 'l0'), ['c1', 'd1', 'r0', 's0']]
---> [0.25, ('p1', 'k0'), ('q1', 'l0'), ['c1', 'd1', 'r0', 's0']] '''

def prefactor(l):
    ans = []
    for i in l:
        cnt = 1
        temp = []
        lst = []
        for j in i:
            if type(j) == tuple:
                temp.append((j[1], j[2]))
                cnt *= j[0]
        lst.append(cnt)
        lst += temp + [i[-1]] * (type(i[-1]) == list) 
        ans.append(lst)
    return ans


#=========================Validate contractions

'''Keep only those contractions where all inactive indices are contracted
e.g. for 1 pair of uncontracted indices (they come at the last, in a list, whereas 
all first brackets indicate contractions), [-0.125, ('u1', 'u0'), ('a0', 'a1'), ('v0', 'v1'), ['i1', 'i0']]
this term is invalid as E^i_i remains. The next one is fully contracted, so no need to check:
[0.25, ('a0', 'v1'), ('u1', 'u0'), ('i1', 'i0'), ('v0', 'a1')]
'''
def remove_open_inactives(lst):
    ans = []
    for term in lst:
        if type(term[-1]) == list:
	    if set('ijklmnotabcdefgh') & set(''.join(term[-1])): #inactive index open
		pass
	    else:
		ans.append(term)
	else:
	    ans.append(term)
    return ans


#======================Discard u^dagger u type contraction if u is particle

'''also true for v, w, x, y
'''
def remove_particle_destruction(lst):
    ans = []
    for term in lst:
	for contraction in term[1:]:
	    if type(contraction) == tuple:
		if contraction[0][0].lower() in 'uvwxyz' and contraction[1][1] == '0':
		    break
	    if contraction == term[-1]:
		ans.append([1.0] + term[1:])  #give 1.0 for all factors
    return ans


#======================Discard u u^dagger type contraction if u is hole

'''also true for v, w, x, y, z
'''
def remove_hole_creation(lst):
    ans = []
    for term in lst:
	for contraction in term[1:]:
	    if type(contraction) == tuple:
		if contraction[0][0].lower() in 'uvwxyz' and contraction[0][1] == '0':
		    break
	    if contraction == term[-1]:
		ans.append([term[0]] + term[1:])  #same as giving 1.0 for all factors, after factor()
    return ans


#======================Discard ('a0', 'v1') type contractions
#                      but keep all contractions with generic indices
#                      also transform ('U0','u1') ---> ('u0','u1')

def check_index(lst):
    ans = []
    pqrs = 'pqrs'
    for term in lst:
        for index, contraction in enumerate(term[1:]):
            lenc = len(contraction)
            if lenc == 2:
                a, b = contraction[0][0].lower(), contraction[1][0].lower()
	        if (a or b) not in pqrs and type(contraction) == tuple and a != b:
		    break
	    if contraction == term[-1]:
                term[index + 1] = list(i.lower() for i in contraction)
                if term[-1] == []:
                    term = term[:-1]          #for [0.25, ('p1', 'j0'), ('q0', 'b1'), []]
		ans.append(term)
            else:
                term[index + 1] = tuple(i.lower() for i in contraction)
    return ans


#===================The penultimate step of generating overlap, next symm check
#===================How many direct/exchange loops & internal holelines

'''input: [ [1.0, ('i1', 'i0'), ('a0', 'a1'), ['u1', 'v1', 'u0', 'v0']], 
   [1.0, ('i1', 'i0'), ('v0', 'v1'), ('a0', 'a1'), ['u1', 'u0']] ]
   output: [ [-1, ['u1', 'v1', 'u0', 'v0']], [2, ['u1', 'u0']] ]
   <E^iu_va|E^va_iu>, i.e. fu = ['i1', 'u1'], fl = ['v0', a0'], su = ['v1', 'a1'], sl = ['i0', 'u0']
'''
#-------------------Create two columns from columns of first & second Es'

'''Needed to trace the path of the loop'''

def cols(fu, fl, su, sl): 
    f_col = [[i[0], j[0]] for i, j in zip(fu, fl)]
    s_col = [[i[0], j[0]] for i, j in zip(su, sl)]
    return f_col, s_col


#-------------Check for direct and exchange loop
#-------------Start with 1st inactive index on 1st E

def count_loop(contracted_indices, f_col1_, s_col1_, loops):

    for i in contracted_indices:
	if i in 'ijklmnotabcdefgh':
	    start = i
	    break
 
#-------------Trace the path that ends in start

    path = [None]
    #print 'start ', start, 'contracted indices', contracted_indices, '\n', f_col1_, s_col1_
    cnt = 0
    while path[-1] != start:
        path[0] = start
        if cnt > 5:
	    break
	cnt += 1
	for i in f_col1_:
	    if i[0] == path[-1]:
		path.append(i[-1])
                break
	for i in s_col1_:
	    if i[0] == path[-1]:
	        path.append(i[-1])
                break
	if start in path[-2:] and len(path) > 2: #1 loop
	    loops += 1
            break
            #if len(path) < 4: 
                #print 'path ', path, 'this is a direct loop'
            #else:
                #print 'path ', path, 'this is an exchange loop'
    #print 'count ', cnt, 'path ', path, 'total loops ', loops
    contracted_indices = [i for i in contracted_indices if i not in path]
    #print 'remaining contracted_indices ', contracted_indices 
    return loops, contracted_indices


def factor(term, f_col, s_col, sector):

    f_col1 = [i[::-1] for i in f_col]
    s_col1 = [i[::-1] for i in s_col]
    #collection of vertices of 1st & 2nd (may be composite) operators
    f_col1_ = map(lambda x: x.lower(), map(''.join, f_col1))  
    s_col1_ = map(lambda x: x.lower(), map(''.join, s_col1))

    factor, loops = 1, 0
    contracted_indices = list(c[0][0].lower() for c in term if type(c) == tuple) 
    contractions = len(contracted_indices)
    hole_lines = sum(c in 'ijklmnot' for c in contracted_indices) + (sector == 1) * (len(set(contracted_indices) & set('uvwxyz')))
    #print '\nterm', term, "\ncontractions ", contractions, contracted_indices, 'hole_lines ', hole_lines, "fcol, scol ", f_col, s_col
    for i in range((1 + contractions)//2):
        if len(contracted_indices) >= 2:
            loops, contracted_indices = count_loop(contracted_indices, f_col1_, s_col1_, loops)
            
    factor = (2 ** loops) * ((-1) ** (loops + hole_lines))
    ans = [factor] + term[1:]
    return ans
        


f_col, s_col = [['l', 'd'], ['k', 'c']], [['a', 'i'], ['d', 'l'], ['c', 'k'], ['b', 'j']]
term = [0.0625, ('l1', 'l0'), ('k1', 'k0'), ('d0', 'd1'), ('c0', 'c1'), ['a1', 'b1', 'i0', 'j0']] 
#print factor(term, f_col, s_col, 2)  #4 <-- from 2 direct loops

term= [-0.0625, ('l1', 'l0'), ('k1', 'k0'), ('c0', 'c1'), ('d0', 'd1'), ['a1', 'b1', 'i0', 'j0']] 
f_col, s_col =  [['l', 'c'], ['k', 'd']], [['c', 'k'], ['d', 'l'], ['a', 'i'], ['b', 'j']]
#print factor(term, f_col, s_col, 2)   #-2 <-- from 1 exchange loop

term = [1, ('k1', 'k0'), ('l1', 'l0'), ('d0', 'd1'), ['a1', 'b1', 'i0', 'j0']]
f_col, s_col = [['k', 'i'], ['l', 'd']], [['a', 'k'], ['d', 'l'], ['b', 'j']]
#print factor(term, f_col, s_col, 2)   #-2 <-- from 1 direct loop

