


#==================================================================================================

#Run automatic ccsd/ccsdt amplitude terms generator python program 
#closed shell, orbital basis
#from orbital based spinfree Wick's theorem
#which stores final result in result.tex
#in latex input mode
#get detailed output along with final terms in ans
#change latex.py for specific output format

#==================================================================================================

    echo 
    read -p "For Closed Shell CCSD diagrams give input as 1, for CCSDT give 2:   " prompt
    case $prompt in
        1) echo 'Here are the diagrams for CCSD'; sed -i 's/"CCSDT"/"CCSD"/g' driver.py;;
        2) echo 'Here are the diagrams for CCSDT'; sed -i 's/"CCSD"/"CCSDT"/g' driver.py;;
        * ) echo "Please answer 1 or 2, run the script again";;
    esac

python driver.py > ans


#Convert: result.tex --> result.pdf

pdflatex result.tex &&


#Open result.pdf on terminal

evince result.pdf 
