from contractions import *
from functions import *
from latex import *
from transform_gen_indices import *
from compare import *
from math import factorial 


#=========================Differentiate b/w creation & annh. operations

def arrange_input(fu, fl, su, sl):
    
    actives = 'uvwxyz'
    flag = len(set(fu + fl)) != len(fu + fl) or len(set(su + sl)) != len(su + sl)
    fu = [[i,i.upper()][flag and i in actives]  + '1' for i in fu]
    fl = [[i,i.upper()][flag and i in actives] + '0' for i in fl]
    #if one active orbital repeats in 1st/2nd operator, change it to uppercase
    su = [i + '1' for i in su]
    sl = [i + '0' for i in sl]
    return fu, fl, su, sl



#============================Single Contraction

def wicks(num, fu, fl, su, sl, sector, operators, cctyp, val=0):
    
    global d
    d = distinguish_2strings(fu, fl, su, sl)
    l = single_contraction([fu + su, fl + sl],d)[0]
    
    for_second = single_contraction([fu + su, fl + sl], d)[1]

    #=========================Multiple Contractions

    cnt = 0
    length = 2 * min(len(fu), len(su))
    for i in range(length - 1):
        for_second, result =  next_contraction(for_second, numbers[cnt], d)
        l += result
        cnt += 1

    #========================Get the prefactor and sign

    ans = prefactor(l)
    #for i in ans:
    #    print i
    #ans = remove_open_inactives(ans) #A must for overlap, not otherwise
    if sector == 1:
        ans = remove_hole_creation(ans)
    if sector == 2:
        ans = remove_particle_destruction(ans)
    ans = check_index(ans)
    print 'returning transform_gen_indices function\n'
    ans_lst, indices = transform_gen_indices(ans, fu, fl, su, sl, cctyp, val)
    
    #print '\n' 
    #for i, j in enumerate(indices, 1):
        #print i, ".  ", j
    #print '\n\n'

    #======================Compare and keep unique expressions

    ans, expressions, checklist_pool = create_final_list(ans_lst, indices, operators, cctyp, sector)

    lst_nb = []
    for cnt, checklist_pool_nb in enumerate(checklist_pool, 1):  
        index = 0 
        temp = []
        print '{} body terms:\n'.format(cnt)
        for i, j in checklist_pool_nb.items():
            if j[-1]:
                index += 1
	        print index, ".  ", i, "\n     ", [j[0]/num] + j[1:], "\n"
                temp.append([j[0]/num] + j[1:])
        print '\n\n'
        lst_nb.append(temp)
        if temp:
            convert_to_tex(temp, cnt)
    return ans

#ans = totex(ans)
