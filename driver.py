from partition import *
from latex import *
from make_op import *
import time


start_time = time.time()

cctyp = "CCSDT"

open_tec_file(cctyp)

call_list = create_call_list(cctyp)

#driver(['F','T2','T2'], cctyp)

for i in call_list:
    driver(i, cctyp)

'''
driver(['F'], cctyp)
driver(['F','T1'], cctyp)
driver(['F','T2'], cctyp)
driver(['F','T1','T1'], cctyp)
driver(['F','T1','T2'], cctyp)
driver(['V'], cctyp)
driver(['V','T1'], cctyp)
driver(['V','T2'], cctyp)
driver(['V','T1','T1'], cctyp)
driver(['V','T1','T2'], cctyp)                 #OK  
driver(['V','T1','T1','T1'], cctyp)           #OK
driver(['V','T2','T2'], cctyp)                #OK
driver(['V','T1','T1','T2'], cctyp)          #OK
driver(['V','T1','T1','T1','T1'], cctyp)    #OK
'''
close_tec_file()

print"\n\tElapsed Time --- %s seconds ---" % (time.time() - start_time)
