import sys
sys.path.append(r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\DATA ANALYSIS')
from UTILS.drive import run_script

folders = ['12Cq--BfZONfpXNnzqw1xnwpKd4HLN5QY','1EZwnzFDOlW20t1Ufkj66OG_oNNCVGLGK']

for fol in folders:
    run_script(r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\DATA ANALYSIS\ALIGNMENT\Alignment.py', fol)