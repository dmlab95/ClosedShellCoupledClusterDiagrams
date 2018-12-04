from parity import permutation_parity
from functions import *


#Functions for single and consequent contractions

numbers = ["Two", "Three", "Four", "Five", "Six"]


def single_contraction(lst,d): #lst = [up, down] == [fu + su, fl + sl]
 
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
                sign = 0.5 * (-1) ** (distance + permutation_parity(sign_output))
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
                sign = 0.5 * (-1) ** (distance + permutation_parity(sign_output))
                prev = [(k[1],k[2]) for k in lst[:-2]]
		term = sorted(prev+[(i,j)]) + [up+down]
		checklist.append(term)
                ans.append(sorted(lst[:-2]+[(sign,i,j)])+[up+down])
                for_next.append(sorted(lst[:-2]+[(sign,i,j)])+[up]+[down])
    
    return ans, for_next, checklist

                

def next_contraction(from_prev, nth, d):
    result = []
    for_next = []			        
    checklist = []			        
    for i in from_prev:
        store = single_contraction(i, d)
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



