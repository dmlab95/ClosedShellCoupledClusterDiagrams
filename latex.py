
    

#=================CONVERT HT terms to tex

import os.path

def open_tec_file(cctyp):

    #delete old result.tex if it exists
    if os.path.isfile("result.tex"):
        os.remove("result.tex")
    f = open("result.tex", "a+" )
    if os.path.isfile("result.tex"):
        f.write('\documentclass[a4paper,10pt]{article}\n')
        f.write('\usepackage{amsmath}\n')
        f.write('\usepackage{braket}\n')
        f.write('\\begin{document}\n')
        x = 'Diagrams for ' + cctyp + ' Amplitude Equation in Orbital Basis'
        f.write('\centerline{\underline{\\textbf{' + x + '}}}\n')


def convert_to_tex(lst, term):

    print '  nbody, lst: ', term,'\n',lst    
    f = open("result.tex", "a+" )
    f.write('\\vskip 0.1in')
    f.write("\n\centerline{\underline{" + str(term) + " body terms}}")
    for index, i in enumerate(lst, 1):
        f.write('$$\t')
        f.write('{})     '.format(index))
        if i[0] == 0.5:
            f.write('  ' + '  \\frac{1}{2} ')
        elif i[0] == -0.5:
            f.write('  -' + '  \\frac{1}{2} ')
        elif i[0] == 1.0:
            f.write('  +')
        elif i[0] == -1.0:
            f.write('  -')
        elif i[0] < 0:
            f.write('  {}'.format(i[0]))
        elif i[0] > 0:
            f.write('  +{}'.format(i[0] * (i[0] != 1)))
        else:
            f.write('{}'.format(i[0]))
   
         
        x = max(0, term - 2)
        contracted_indices = ''.join(sorted(set([m for j in i[1:] for k in j for m in k if m not in 'abcd'[:2+x] + 'ijkl'[:2+x]])))
        f.write('\displaystyle\sum_{' + contracted_indices + ' } ')
  
        if len(i[1]) == 1:
            f.write('F^{{{}}}_{{{}}}'.format(i[1][0][0], i[1][0][1]))
        elif len(i[1]) == 2:
            f.write('V^{{{}{}}}_{{{}{}}}'.format(i[1][0][0], i[1][1][0], i[1][0][1], i[1][1][1]))
        elif len(i[1]) == 3:
            f.write('V^{{{}{}{}}}_{{{}{}{}}}'.format(i[1][0][0], i[1][1][0], i[1][2][0], i[1][0][1], i[1][1][1], i[1][2][1]))
        for j in i[2:]:
            print 'j is: ', j
            j = sorted(j)
            if len(j) == 1:
	        f.write('T^{{{}}}_{{{}}}'.format(j[0][0], j[0][1]))
            elif len(j) == 2:
	        f.write('T^{{{}{}}}_{{{}{}}}'.format(j[0][0], j[1][0],  j[0][1], j[1][1]))
            elif len(j) == 3:
                f.write('T^{{{}{}{}}}_{{{}{}{}}}'.format(j[0][0], j[1][0], j[2][0], j[0][1], j[1][1], j[2][1]))
            elif len(j[1]) == 4:
                f.write('T^{{{}{}{}}}_{{{}{}{}}}'.format(j[0][0], j[1][0], j[2][0], j[3][0], \
                j[0][1], j[1][1], j[2][1], j[3][1]))

        f.write('$$\n\n')
    if term == 1:
        f.write("\\vskip 0.2in")
    else:
        f.write("\\vskip 0.5in")
    
def close_tec_file():      
    f = open("result.tex", "a+" )
    f.write('\n\n')          
    f.write('\end{document}')
        

