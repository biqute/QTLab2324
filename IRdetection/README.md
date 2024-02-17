# Folder architecture 
Good whatever part of the day it is to everyone!

IRdetection
    │  
    └── HDF5
    │     └── h5_and.py # Python class for writing to and reading from a hdf5 file  
    │
    └── Instruments     
    │      └── Gas_Handler22    # Folder for cryostat handler communication and manipulation, liveplots
    │      │          │
    │      │          │── handler.py   # Python class for cryostat handler communication and manipulation
    │      │          │── live_plot_P14 # Real time plot for sensor 14
    │      │          │── live_plot_P15 # Real time plot for sensor 14
    │      │          └── test.ipynb    # Notebook for handler.py test
    │      │
    │      └── Manuals # Contains manuals for cryo and VNA handling
    │      │
    │      │
    │      └── Test data
    │      │         │── fitprova      # iMinuit tests
    │      │         │── fits.ipynb    # Notebook for fitting $\frac{1}{Q}$ vs $T$
    │      │         │── psweep.ipynb  # Notebook for TAKING DATA
    │      │         └── Fitted.csv    # CSV file with columns $T$ , $\frac{1}{Q}$ , $\sigma_{\frac{1}{Q}}$
    │      │         └── init.csv      # CSV file with columns $T$ , $\frac{1}{Q}$ , $\sigma_{\frac{1}{Q}}$
    │      └── VNA GUI
    │               │── HP8753E.py    # Python class for VNa comunication and handling
    │               │── mainwindow.py # GUI main window
    │               │── par dialog.py # GUI dialog popup
    │               └── FindRes.py    # GUI window for finding resonances
    │               └── Params.py     # GUI 
    └── Notebooks
         │── bessel2.ipynb # Notebook for fitting resonances
         │── fits.ipynb    # Notebook for fitting $\frac{1}{Q}$ vs $T$
         │── psweep.ipynb  # Notebook for TAKING DATA
         └── Fitted.csv    # CSV file with columns $T$ , $\frac{1}{Q}$ , $\sigma_{\frac{1}{Q}}$
