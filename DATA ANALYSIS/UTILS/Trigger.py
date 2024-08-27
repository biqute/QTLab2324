import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks
from scipy.ndimage import convolve
from matplotlib.animation import FuncAnimation

def vertex_parabola(x2, y1, y2, y3):
    x1 = x2 - 1
    x3 = x2 + 1
    b = x3 * x3 * (y2 - y1) + x2 * x2 * (y1 - y3) + x1 * x1 * (y3 - y2)
    a = (y2 - y3) * x1 + (y3 - y1) * x2 + (y1 - y2) * x3
    #den = (x1-x2)*(x1-x3)*(x3-x2)
    return -b/(2*a)

def coeff_parabola(x2, y1, y2, y3):
    x1 = x2 - 1
    x3 = x2 + 1
    den = (x1 - x2) * (x1 - x3) * (x3 - x2)
    b = (x3 * x3 * (y2 - y1) + x2 * x2 * (y1 - y3) + x1 * x1 * (y3 - y2)) / den
    a = ((y2 - y3) * x1 + (y3 - y1) * x2 + (y1 - y2) * x3) / den
    c = ((x2 * x3 * y1 * (x3 - x2) + x3 * x1* y2  * (x1 - x3) + x1 * x2 * y3 * (x2 - x1))) / den

    return a, b, c

def derivative_trigger(sample, window_ma, a = 10, b = 5, n=2, plot=False):
    # Initialize an empty list to store moving averages
    weights = np.full(window_ma, 1/window_ma)
    moving_averages = convolve(sample, weights, mode='mirror')

    time = np.linspace(0,len(sample), len(sample))

    first_derivative = np.gradient(moving_averages)
    std = np.std(first_derivative[0:100])/2 
    index_min = first_derivative.argmin()
    
    rise_points = 0
    while first_derivative[index_min - rise_points] < -std:
        rise_points += 1
        
    a = a #to have a window_length of 21, in this way all the windows are equal
    b = b
    start = index_min - rise_points

    if start < a:
        start = a
    if start > len(sample)-a:
        start = len(sample)-1-a
    
    end = start + a + 1     # +1 to avoid the error: "window_length must be odd."
    begin = start - a if start - a > 0 else 0 # To avoid negative values for begin
    
    #print('hint start = %d, begin = %d, end = %d' %(start, begin, end))
    
    window_length = len(sample[begin:end]) #-1 if len(sample[begin:end]) % 2 == 0 else len(sample[begin:end])

    #print(window_length)

    #poly_order = window_length-1 if window_length < 14 else 12
    
    derivative_func = savgol_filter(sample[begin:end], window_length, 8, n, delta=1) #8 is the best in the tests done

    # we have to drop the first b points and the last b points of the array
    # since sth strange happens here with the derivative due to the polinomial fitting of sav_gol
    time = np.linspace(0,len(sample), len(sample))

    if plot:
        plt.figure(figsize=(20,8))
        #plt.scatter(time[begin:end], savgol_filter(sample[begin:end], window_length, 8, 0, delta=1), color='red',label='savgol')
        plt.scatter(time[begin:end], derivative_func, color="forestgreen",label='derivative')
        plt.xlabel(r'Time [$\mu$s]')
        plt.ylabel(r'Voltage [mV]')
        plt.legend()

    x2 = begin+b+(derivative_func[b:-b].argmin())
    y1 = derivative_func[b+derivative_func[b:-b].argmin() - 1]
    y2 = derivative_func[b+derivative_func[b:-b].argmin()]
    y3 = derivative_func[b+derivative_func[b:-b].argmin() + 1]
    min = vertex_parabola(x2, y1, y2, y3)
    aa, bb, cc = coeff_parabola(x2, y1, y2, y3)
    if plot:
        t = time[begin:end]
        plt.scatter(t, aa*t*t + bb*t +cc, color='dodgerblue')
        plt.xlabel(r'Time [$\mu$s]')
        plt.ylabel(r'Voltage [mV]')
        plt.grid()
        plt.show()
    #min = begin+b+(derivative_func[b:-b].argmin())

    return min, x2, derivative_func[b+derivative_func[b:-b].argmin()]
    #return print('start: ', time[begin+b+derivative_func[b:-b].argmin()])


def align_signal(signal, window_ma, points_before_trigger=1000, points_after_trigger=20000, plot=False):
    # Align a single signal using the derivative_trigger function
    min_point, x2, _ = derivative_trigger(signal, window_ma, plot=plot)

    # Calculate the start and end indices for the aligned signal
    start = int(min_point - points_before_trigger)
    end = int(min_point + points_after_trigger)

    # Adjust start and end to ensure they are within the valid range
    if start < 0:
        start = 0
    if end > len(signal):
        end = len(signal)
        start = int(end - points_before_trigger - points_after_trigger)
    
    # Ensure that we don't go out of bounds
    if start < 0:
        start = 0

    aligned_signal = signal[start:end]

    if plot:
        plt.figure(figsize=(12, 6))
        plt.plot(signal, label='Original Signal', alpha=0.5)
        plt.plot(np.arange(start, end), aligned_signal, label='Aligned Signal', alpha=0.75)
        plt.xlabel('Sample')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.title('Original vs Aligned Signal')
        plt.show()

    return aligned_signal, min_point

def weighted_moving_average(data, window_size):
    # Converti i dati in un array numpy
    data = np.array(data)
    
    # Crea i pesi come un array numpy
    weights = np.arange(1, window_size + 1)
    
    # Calcola la somma dei pesi
    weight_sum = weights.sum()
    
    # Calcola la media mobile ponderata utilizzando la funzione di convoluzione
    wma = np.convolve(data, weights[::-1], mode='valid') / weight_sum
    
    return wma

def exponential_moving_average(data, window_size):
    # Converti i dati in un array numpy
    data = np.array(data)
    
    # Calcola il coefficiente di ammortamento
    alpha = 2 / (window_size + 1)
    
    # Inizializza un array per l'EMA con lo stesso formato dei dati
    ema = np.zeros_like(data, dtype=float)
    
    # Imposta il primo valore dell'EMA uguale al primo valore dei dati
    ema[0] = data[0]
    
    # Calcola l'EMA usando la formula ricorsiva
    for i in range(1, len(data)):
        ema[i] = alpha * data[i] + (1 - alpha) * ema[i - 1]
    
    return ema

def simple_moving_average(data, window_size):
    # Converti i dati in un array numpy
    data = np.array(data)
    
    # Crea un array di pesi per la finestra (tutti uguali)
    weights = np.ones(window_size) / window_size
    
    # Calcola la SMA usando la funzione di convoluzione
    sma = np.convolve(data, weights, mode='valid')
    
    return sma


def align_definitive(signal,window=180,polyorder=8,derivorder=1,plot=False):

    signal_derivative = savgol_filter(signal,window,polyorder,derivorder)

    idxs, props = find_peaks(signal_derivative[1:-1],0)

    try:
        max(props['peak_heights']) > 5 * np.std(signal_derivative)
    except Exception as e:
        print(f"Could not find maximum of derivative -> {e}")

    bw = 0
    mean = max(signal_derivative)

    while(mean > np.std(signal_derivative[:1000]) or mean < -1*np.std(signal_derivative[:1000])):
        bw += 1
        dacalcolare = (signal_derivative[idxs[np.argmax(props['peak_heights'])]-bw:idxs[np.argmax(props['peak_heights'])]])
        mean = np.mean(dacalcolare)

    xmin = idxs[np.argmax(props['peak_heights'])]-bw
    x_alignment = xmin + np.argmin(signal_derivative[xmin:idxs[np.argmax(props['peak_heights'])]])

    if plot:
        fig,axs = plt.subplots(2,1, figsize=(15,10))
        axs[0].plot(signal_derivative,label='signal_derivative DErivative')
        axs[0].scatter(signal_derivative,signal_derivative['peak_heights'],marker='x',color='black')
        axs[0].scatter(signal_derivative[np.argmax(signal_derivative['peak_heights'])],max(signal_derivative['peak_heights']),marker='x',color='red',label='Maximum')
        axs[0].axhline(np.std(signal_derivative[:1000]),linestyle='-.',color='red',label=r'$\sigma$')
        axs[0].axhline(-1*np.std(signal_derivative[:1000]),linestyle='-.',color='red',label=r'$-\sigma$')
        axs[0].axvline(signal_derivative[np.argmax(signal_derivative['peak_heights'])],0,1, linestyle='-.',color='green')
        axs[0].set_xlim([signal_derivative[np.argmax(signal_derivative['peak_heights'])]-800,signal_derivative[np.argmax(signal_derivative['peak_heights'])]+800])

        axs[1].plot(signal_derivative[signal_derivative[np.argmax(signal_derivative['peak_heights'])]-bw:signal_derivative[np.argmax(signal_derivative['peak_heights'])]])
        axs[0].scatter(xmin,signal_derivative[xmin],marker='x',color='orange',label='Stable point')
        axs[0].scatter(x_alignment,signal_derivative[x_alignment],marker='+',color='green',label='Alignment point')
        axs[1].set_title('Alignment')
        axs[0].legend()
        plt.show()

    final = signal[x_alignment-1000:x_alignment+19000]

    return xmin,x_alignment, final

def initialize_canvas():
    # Initialize the plot
    fig, ax = plt.subplots()
    bins = np.linspace(50000, 350000, 60)  # Adjust the range and number of bins as needed
    hist_data, _ = np.histogram([], bins=bins)
    bars = ax.bar(bins[:-1], hist_data, width=bins[1] - bins[0], color='blue', edgecolor='black')

    ax.set_xlim(bins[0], bins[-1])
    ax.set_ylim(0, 10)  # Adjust this based on the expected distribution
    return fig, ax, bars, bins

# Function to update the plot
def update(frame, file_path, ax, bars, bins):
    # Read the file and extract the numbers
    try:
        with open(file_path, 'r') as f:
            data = f.readlines()
            data = [float(line.strip()) for line in data]#if float(line.strip())>190000 and float(line.strip())<210000]# Convert lines to floats
    except FileNotFoundError:
        data = []

    if data:
        # Update histogram data
        hist_data, _ = np.histogram(data, bins=bins)
        for bar, height in zip(bars, hist_data):
            bar.set_height(height)
        ax.set_ylim(0, max(hist_data) + 5)  # Adjust y-limits dynamically

    return bars

def live_show(file_path):
    # Create the animation
    fig, ax, bars, bins = initialize_canvas()
    _ = FuncAnimation(fig, update, fargs=(file_path, ax, bars, bins), interval=1000,cache_frame_data=False)  # Update every 1 second

    # Show the plot
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Live Data Distribution')
    plt.show()