# %% Imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, norm
from iminuit.cost import LeastSquares
from iminuit import Minuit
import sys

# %% Load OFF data
OFF = np.genfromtxt(r'/home/drtofa/OneDrive/QTLab2324/DATA ANALYSIS/OPTIMUM/TXT/OFF_Tension.txt')

# %% Function to compute the sum of Poisson and Gaussian distributions
import numpy as np
from scipy.stats import poisson, norm

def compute_sum_poisson_gaussian(amplitudes, A, mu, sigma, delta, Egamma):
    Nmax = 200
    """
    Compute the model function for the given data.
    
    Parameters:
    - amplitudes: Array of observed amplitudes (OFF) in volts.
    - A: Normalization factor.
    - mu: Mean of the Poisson distribution.
    - sigma: Standard deviation of the Gaussian distribution.
    - delta: Global shift of the fit function from zero.
    - Egamma: Energy of a single photon in eV.
    - Nmax: Maximum number of photons considered in the sum.
    
    Returns:
    - Array of computed values for the given amplitudes.
    """
    result = np.zeros_like(amplitudes)
    
    # Array of possible photon numbers
    photon_numbers = np.arange(0, Nmax + 1, dtype=int)
    
    # Compute Poisson probabilities for all photon numbers
    poisson_probs = poisson.pmf(photon_numbers, mu)
    
    # Compute the Gaussian PDF for each photon number and sum up
    for n in photon_numbers:
        # Compute Gaussian PDF for the current number of photons
        gaussian_values = norm.pdf(amplitudes, loc=n * Egamma + delta, scale=sigma)
        
        # Update result array
        result += poisson_probs[n] * gaussian_values
    
    return A * result



# %% Plotting function
def plot(OFF, bin_centers, hist, m, func):
    idx = OFF > 0.001
    fig, ax = plt.subplots(figsize=(15, 6))
    fig.tight_layout()
    
    # Plot data
    ax.errorbar(bin_centers, hist, np.sqrt(hist + 1), alpha=0.5, label='Data', fmt='ko', color='blue')
    
    # Plot fit result
    fit_values = func(bin_centers, *m.values)
    ax.errorbar(bin_centers, fit_values, np.sqrt(fit_values + 1), color='black', fmt='ko', linestyle='-', label='Fit')
    
    # Histogram
    ax.hist(OFF[idx], 80, histtype='stepfilled', color='lightblue', density=False, alpha=0.5)
    
    # Axes labels and title
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Counts')
    ax.set_title('OFF Fit')
    ax.grid(True)
    
    # Add chi-squared and parameters to legend
    title = [f"{par} = {m.values[par]:.5f} +/- {m.errors[par]:.5f}" for par in m.parameters]
    title.append(r'$\chi^{2}_{0} = $' + f"{m.fval/m.ndof:.2f}")
    legend = ax.legend(title="\n".join(title), fontsize=10)
    legend.get_title().set_fontsize(10)  # Adjust font size
    plt.savefig('plot'+sys.argv[1]+'.png')


# %% Data processing
idx = OFF > 0.001
bins = 80  # Number of bins
hist, bin_edges = np.histogram(OFF[idx], bins=bins, density=False)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2


# %% Plot raw histogram with grid and vertical lines
fig, ax = plt.subplots(figsize=(15, 10))
fig.tight_layout()
ax.errorbar(bin_centers, hist, np.sqrt(hist), fmt='ko')
for k in np.arange(-2, 15, 1):
    ax.axvline(0.001152 + k * (0.001318 - 0.001152) / 2, 0, 1, linestyle='--', color='red')
ax.hist(OFF[idx], bins=bins, density=False)
ax.set_title('OFF Histogram')
ax.set_xlabel('Data')
ax.set_ylabel('Counts')
ax.grid(True)
ax.legend()
plt.savefig('vertical'+sys.argv[1]+'.png')

# Set initial parameter values
A_initial = 1
mu_initial = 4
delta_initial = 0.00115
sigma_initial = float(sys.argv[1])
Egamma_initial = (0.001318 - 0.001152) / 2

p0 = [A_initial, mu_initial, sigma_initial, delta_initial, Egamma_initial]

# Use keyword argument for Nmax
lsq = LeastSquares(bin_centers, hist, np.sqrt(hist+1), compute_sum_poisson_gaussian)
m = Minuit(lsq, *p0)  # Initial parameter values as positional arguments
m.fixed['sigma'] = True  # Optional: Fix sigma during fitting
m.migrad(ncall=1000)



# %% Plot fit result
plot(OFF, bin_centers, hist, m, compute_sum_poisson_gaussian)

# %% Find peaks in the fitted data
from scipy.signal import find_peaks
fit_values = compute_sum_poisson_gaussian(bin_centers, *m.values)
peaks, _ = find_peaks(fit_values, 0)

for peak in peaks:
    plt.axvline(bin_centers[peak], 0, fit_values[peak] / max(fit_values), linestyle='-.', color='red')

x_center = np.sum(bin_centers * fit_values) / np.sum(fit_values)
print(f"x_center: {x_center}")

# %% Calculate skewness
y = compute_sum_poisson_gaussian(OFF[idx], *m.values)
Num = np.sum((y - m.values['mu']) ** 3)
Den = np.sum((y - m.values['mu']) ** 2) ** 1.5
F = np.sqrt(len(y)) * Num / Den

print(f'Skewness: {F:.2f}')
