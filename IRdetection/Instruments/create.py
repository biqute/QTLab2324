import IPython
import HP8753E as HP
import numpy as np

def main():
     VNA = HP.HP8753E()
     print("VNA object created!")
     IPython.embed()
     return

main()
