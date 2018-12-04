from parity import permutation_parity
from totex import *


    
fu, fl, su, sl = ['i1', 'u1', 'v1'], ['a0', 'u0', 'v0'], ['a1', 'u1', 'v1'], ['i0', 'u0', 'v0'] 
#fu, fl, su, sl = ['i1', 'j1', 'k1'], ['a0', 'b0', 'c0'], ['a1', 'c1', 'b1'], ['i0', 'j0', 'k0'] 
#fu = ['i1', 'u1']; fl = ['v0', 'a0']; su = ['v1','a1']; sl = ['i0', 'u0']

d = distinguish_2strings(fu, fl, su, sl)

numbers = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight"]

#===========NOTE: for VT, take V^pq_rs (1st string) & T^cd_kl
#-----------for VT^2, 1st take V^kl_cd & T^pq_rs
#-----------get its VT (doubly contr.) terms
#-----------doubly contract it with T^ef_mn


def single_contraction(lst): #lst = [up, down] == [fu + su, fl + sl]
   
    ans = []
    checklist = []
    for_next = []
    up = lst[-2]
    down = lst[-1]
    up_ = up[:]
    down_ = down[:]
    for index_i, i in enumerate(up_):
        up = up_[:]
        up.remove(i)
        for index_j, j in enumerate(down_):
            down = down_[:]
	    if d[i] == 1 and d[j] == -1:
	        down[index_j], down[index_i] = down[index_i], down[index_j]
                down.remove(j)
                sign_input = up_ + down_[::-1]
                distance = sign_input.index(j) - sign_input.index(i) - 1
                sign_input.remove(i)
                sign_input.remove(j)
                sign_output = up + down[::-1]
                sign_output = [sign_input.index(k) for k in sign_output]
                sign = 1#0.5 * (-1) ** (distance + permutation_parity(sign_output))
                prev = [(k[1],k[2]) for k in lst[:-2]]
		term = sorted(prev+[(i,j)]) + [up+down]
		checklist.append(term)
                ans.append(sorted(lst[:-2]+[(sign,i,j)])+[up+down])
                for_next.append(sorted(lst[:-2]+[(sign,i,j)])+[up]+[down])
               
     
    for index_i, i in enumerate(down_):
        for index_j, j in enumerate(up_):
            up = up_[:]
            up.remove(j)
            down = down_[:]
	    if d[i] == 1 and d[j] == -1:
	        down[index_j], down[index_i] = down[index_i], down[index_j]
                down.remove(i)
                sign_input = up_ + down_[::-1]
                distance = sign_input.index(j) - sign_input.index(i)
                sign_input.remove(i)
                sign_input.remove(j)
                sign_output = up + down[::-1]
                sign_output = [sign_input.index(k) for k in sign_output]
                sign = 1#0.5 * (-1) ** (distance + permutation_parity(sign_output))
                prev = [(k[1],k[2]) for k in lst[:-2]]
		term = sorted(prev+[(i,j)]) + [up+down]
		checklist.append(term)
                ans.append(sorted(lst[:-2]+[(sign,i,j)])+[up+down])
                for_next.append(sorted(lst[:-2]+[(sign,i,j)])+[up]+[down])
    
    return ans, for_next, checklist

                
#==================include 2 for loops
#------------------last: fully contracted, no E i.e. list left

def loopcheck(lst, last = False):

    for k in lst:
        if k[-1] == []:
            k.remove(k[-1])  #no [] left after full contraction
    signed = lst[:]
    for k in lst:
        taken = []
        if last:
            tmp = k[:]
        else:
            tmp = k[:-1]
	for index_i,i in enumerate(k[:-1]): 
	    for j in k[index_i+1:]:
                if i[1] in fu:   
                    if j[1] in fl:   
			if i not in taken and j not in taken:
                            try:
 			        if fu.index(i[1]) == fl.index(j[1]) and \
                                sl.index(i[2]) == su.index(j[2]):
			            taken.append(i)  
			            taken.append(j)
                                    tmp.remove(i)
                                    tmp += [(2*i[0],i[1],i[2])]
                	    except:
				pass
		elif i[1] in fl:   
                    if j[1] in fu:   
			if i not in taken and j not in taken:
                            try:
 			        if fl.index(i[1]) == fu.index(j[1]) and \
                                su.index(i[2]) == sl.index(j[2]):
                                    #print 'hello'
			            taken.append(i)  
			            taken.append(j)  
                                    tmp.remove(i)
                                    tmp += [(2*i[0],i[1],i[2])]
			    except:
				pass
        tmp = sorted(tmp)
        if not last:
            tmp += [k[-1]] 
        signed.remove(k)
    	signed.append(tmp)
    return signed


def next_contraction(from_prev, nth):
    result = []
    for_next = []			        
    checklist = []			        
    for i in from_prev:
        store = single_contraction(i)
        for j, k, l in zip(store[2], store[0], store[1]):
            if j not in checklist:
                checklist.append(j)
                result.append(k)
                for_next.append(l)

    #result = loopcheck(result)   
    #print "\n" + "-" * 115 + "\n" + nth + " contractions..." + "\n" + "-" * 115

    #for index,k in enumerate(result, 1):
      # print "{}.  {}".format(index, k)  
    return for_next, result


#=========================Single Contraction

l = single_contraction([fu + su, fl + sl])[0]
#print "\n" + "-" * 115 + "\n" + "Single contractions..." + "\n" + "-" * 115
#for index,i in enumerate(l, 1):
    #print "{}.  {}".format(index, i)
    
for_second = single_contraction([fu + su, fl + sl])[1]

#=========================Multiple Contractions

cnt = 0
length = 2 * min(len(fu),len(su))
#length = 10
VT = []
try:
    for i in range(length - 1):
        for_second, result =  next_contraction(for_second, numbers[cnt])
        if not i:
	    VT = result   #save doubly contracted terms
        l += result
        cnt += 1
except:
    'count is : ', cnt
    pass

#========================Get the prefactor and sign

ans = prefactor(l)
ans = remove_open_inactives(ans)
ans = remove_particle_destruction(ans)
ans = check_index(ans)
for i in ans:
    print i
f_col, s_col = cols(fu, fl, su, sl)
ans = factor(ans, f_col, s_col)
print '\n\n\n' 
for i in ans:
    print i
print '\n\n'
#ans = totex(ans)


'''
for index, j in enumerate(vtt, 1): print index, '.   ', j  #20 * 20 = 400 terms
lst = validate_vtt(vtt)
for index, i in enumerate(lst, 1): print 'vtt ', index, '.  ', i #72 valid VT^2 terms

'''

#=====================Convert to teX

'''
#=========================VT^2 terms
T2 = ['e1', 'f1', 'm0', 'n0']
su = T2[:2]; sl = T2[2:]
vtt = []
for i in VT:
    fu = i[-1][: len(i[-1])//2]
    fl = i[-1][len(i[-1])//2: ]
    d = distinguish_2strings(fu, fl, su, sl)
    front = i[:-1]
    vtt_lst, for_next, x = single_contraction([fu + su, fl + sl])
    for_second = []
    for j, k in zip(vtt_lst, for_next):
	j = front + j
        for_second.append(front + k)
#    for k in for_second: print 'k', k
    VTT =  next_contraction(for_second, 'two')[1]
    VTT = prefactor(VTT)
    vtt += VTT
#    for index, j in enumerate(VTT, 1): print index, '.   ', j


f = open('res.txt', 'w')
for i in ans:
    #print i
    f.write(str(i)+"\n")
#totex(ans)
#diagrams(ans)
#vt_totex()
'''



