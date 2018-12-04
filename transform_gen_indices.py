#  input:     [1, ('p1', 'j0'), ['b1', 'q0']]
#----> output: [1, ('j1', 'j0'), ['a1', 'i0']]
# fu, fl, su, sl = 'p', 'q', 'b', 'j' --> 'j', 'i', 'b', 'j'
#[0.25, ('p1', 'k0'), ('q1', 'l0'), ['c1', 'd1', 'r0', 's0']]   --->  [0.25, ('k1', 'k0'), ('l1', 'l0'), ['a1', 'b1', 'i0', 'j0']]
'''
fu = p, q   fl = r, s  su = c, d  sl = k, l
   = k, l      = i, j     = a, b 0
#[('c', 'a'), ('d', 'b'), ('p', 'k'), ('q', 'l'), ('r', 'i'), ('s', 'j')])
'''

from copy import deepcopy
from collections import OrderedDict

def transform_gen_indices(lst, fu_, fl_, su_, sl_, cctyp, val):

    ans = []
    indices = []
    pqrs = 'pqrs'
    holes, particles = set('ijklmno'), set('abcdefg')
    #val_ = min(len(su_), len(cctyp) - 2)
    print 'val is: ', val
    for term in lst:
	#if type(term[-1]) == tuple or len(term[-1]) > 4+ max(0, 2 *(val_- 2)):#Ignore fully contracted terms+nbody or more excitations,true if call driver once for all terms
 
        flag = 0
        if val:   #HT complex can be max 2b i.e. can have max 4 open indices
	    flag = 4
	if type(term[-1]) == tuple or len(term[-1]) > 4 + 2 * val:   #Ignore fully contracted terms + nbody or more excitations
	    pass
        elif flag == len(term[-1]) or flag//2 == len(term[-1]):      #Ignore 1b & 2b terms if max possible exc > 2
	    pass
	else:
            d_gen = dict()
            exc =  len(term[-1])//2
            exc_level = ['a1', 'b1','c1','d1'][:exc] + ['i0', 'j0','k0','l0'][:exc]
            term1 = deepcopy(term)
            fu = deepcopy(fu_)
            fl = deepcopy(fl_)
            su = deepcopy(su_)
            sl = deepcopy(sl_)
	    for index, contraction in enumerate(term[1:-1], 1):
                if contraction[0][0] in pqrs:
                    d_gen[contraction[0][0]] = term[index][1][0]
		    term[index] = (term[index][1][0] + term[index][0][1], term[index][1])
		else:
                    d_gen[contraction[1][0]] = term[index][0][0]
		    contraction[1][0] = contraction[0][0]
            for index, item in enumerate(term[-1]):
		d_gen[item[0]] = exc_level[index][0]
	    ans.append(term[:-1] + [exc_level])
            print "\n", term1, '  ---> ', ans[-1]
            
#---------------------rename the gen indices on F/V and inactive indices as needed on T
#                     len(d_gen) = no of contractions + exc. level (2, 4, 6 or 8)
#                                
            for key, value in d_gen.items():
		for j in range(len(fu)):
                    if key in fu[j]:
			fu[j] = value + '1'
		    if key in fl[j]:
	         	fl[j] = value + '0'
		for j in range(len(su)):
		    if key in su[j]:
			su[j] = value + '1'
	            if key in sl[j]:
			sl[j] = value + '0'

            indices.append([fu, fl, su, sl])
            #print "new fu, fl, su, sl ", fu, fl, su, sl

            #if len(fu) == 1:    #Discard terms if F is not class-diagonal
		#if set(fu[0][0] + fl[0][0]) & holes  and set(fu[0][0] + fl[0][0]) & particles:
		    #print 'discarding above term as F is not class diagonal\n'
                    #del ans[-1]
                    #del indices[-1]
       
    return ans, indices


#transform_gen_indices(lst, fu, fl, su, sl,cctyp)
