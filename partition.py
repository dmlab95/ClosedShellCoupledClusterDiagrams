

def sum_to_n(n, size, limit=None):
    """Produce all lists of `size` positive integers in decreasing order
    that add up to `n`."""
    if size == 1:
        yield [n]
        return
    if limit is None:
        limit = n
    start = (n + size - 1) // size
    stop = min(limit, n - size + 1) + 1
    for i in range(start, stop):
        for tail in sum_to_n(n - i, size - 1, i):
            yield [i] + tail


def create_V_T_list(cctyp):

    num = len(cctyp)  #V is 2b, i.e. max possible Hamiltonian, so for CCSD, VTn composite can be max 2b, for CCSDT 5b, for CCSDTQ 6b
    lst = []
    for j in range(1, num + 1):
        for i in range(1, j + 1):
            for x in sum_to_n(j, i):
                if len(x) <= 4:     #[V,T,T,T,T]: V is 2b, so can maximally connect to 4 operators
                    x =  sorted(x)
                    #print x

                    if cctyp == 'CCSD':
                        if max(x) <= 2:   #as max T is T2
                            lst.append(x)

                    elif cctyp == 'CCSDT':
                        if max(x) <= 3:    #as max T is T3
                            lst.append(x)

                    elif cctyp == 'CCSDTQ':
                        if max(x) <= 4:   #as max T is T4
                            lst.append(x)
        #print "\n"
    return lst


def create_F_T_list(cctyp):

    num = len(cctyp) - 1  #F is 1b, so for CCSD, FTn composite can be max 3b, for CCSDT 4b, for CCSDTQ 5b
    lst = []                   #num: CCSD: 2, CCSDT: 3, CCSDTQ: 4
    for j in range(1, num + 1):
        for i in range(1, j + 1):
            for x in sum_to_n(j, i):
                if len(x) <= 2:     #[F,T,T]: F is 2b, so can maximally connect to 2 operators
                    x =  sorted(x)
                    print x

                    if cctyp == 'CCSD':
                        if max(x) <= 2:   #as max T is T2
                            lst.append(x)

                    elif cctyp == 'CCSDT':
                        if max(x) <= 3:    #as max T is T3
                            lst.append(x)

                    elif cctyp == 'CCSDTQ':
                        if max(x) <= 4:   #as max T is T4
                            lst.append(x)
        print "\n"
    return lst


def create_call_list(cctyp):

    calls = [['F']]
    F_T_list = create_F_T_list(cctyp)
    for i in F_T_list:
        calls.append(['F'] + ['T' + str(j) for j in i])
    calls += [['V']]
    V_T_list = create_V_T_list(cctyp)
    for i in V_T_list:
        calls.append(['V'] + ['T' + str(j) for j in i])
    #print "   Possible operator call list for cctyp = ", cctyp, '\n'
    for index, item in enumerate(calls, 1):
        print index, ". ", item
    return calls

if __name__ == '__main__':
    print create_call_list('CCSD')
    print '=' * 50 + '\n\n'
    print create_call_list('CCSDT')
    print '=' * 50 + '\n\n'
    print create_call_list('CCSDTQ')
