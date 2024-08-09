from UTILS.load_data import get_data, in_memory
from UTILS import drive
from UTILS.Trigger import derivative_trigger, live_show
import matplotlib.pyplot as plt
import numpy as np
import sys
import multiprocessing

def main():
    files, svc = get_data(max_files=300)

    # Start live_show in a separate process
    live_show_process = multiprocessing.Process(target=live_show, args=('Alignments.txt',))
    live_show_process.start()

    for file in files:
        data = in_memory(file, svc)

        bl = False
        if len(sys.argv) > 1:
            bl = True

        Timestamp = np.linspace(0, len(data), len(data), dtype=int)
        idx = np.array(Timestamp[:int(0.4 * 1e6)])
        T = Timestamp[idx]
        signal = data[idx]

        plt.figure(figsize=(20, 5))
        plt.plot(T, signal)
        plt.title('CUT I SIGNAL')
        plt.ylabel('[V]')
        plt.xlabel('Timestamp')

        a, b, _ = derivative_trigger(signal, 100, plot=bl)

        print(f'{file} done!')

        with open('Alignments.txt', 'a') as file:
            file.writelines(str(b) + '\n')

    # Ensure the live_show process completes
    live_show_process.join()

if __name__ == "__main__":
    main()