import numpy as np
import matplotlib.pyplot as plt
import logging
import mplcyberpunk
from scipy.special import gamma

plt.style.use("cyberpunk")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def p_x_theoretical(x):
    mask = np.logical_and(-1 <= x, x <= 1)
    result = np.zeros_like(x)
    result[mask] = 1 / (np.pi * np.sqrt(1 - x[mask]**2))
    return result


def Rinv_phi(n, k, N):
    phi = np.zeros(N)
    phi[0] = np.random.choice([k, -k])

    invert_prob = n / N
    invert_array = np.random.choice([1, -1], N, p=[1 - invert_prob, invert_prob])

    for i in range(1, N):
        phi[i] = phi[i - 1] * invert_array[i]

    return phi


# parameters from condition
N = 2 ** 14  # number of process elements
n = 512
omega_0 = np.pi / 64
delta = 0.002

# moments of time
t = np.linspace(0, 1000, N)

# generation random process
phi_process = Rinv_phi(n, delta, N)
X = np.sin(omega_0 * t + phi_process)

# Use numpy.histogram to get values p and bins
p, bins = np.histogram(X, bins=400, density=True)

# Normalize the histogram
delta_x = bins[1] - bins[0]
p = p / (np.sum(p) * delta_x)

# Plot the histogram and the theoretical density
plt.figure()
plt.plot(bins[:-1], p, color="RED", label='Experimental', linewidth=2)
x_theoretical = np.linspace(-1, 1, 1000)
p_theoretical = p_x_theoretical(x_theoretical)
plt.plot(x_theoretical, p_theoretical, label='Theoretical', color='BLUE')

plt.xlabel('x')
plt.ylabel('p(x)')
plt.title('Experimental and Theoretical Distribution Density')
plt.legend()

# search for moments, central moments, and cumulants
x = bins[:-1]  # beginnings of intervals
k = 6  # maximum order of moments from the condition

mean = [np.sum(x ** i * p * delta_x) for i in range(k + 1)]  # the first k moments
mu = [np.sum((x - mean[1]) ** i * p * delta_x) for i in range(k + 1)]  # the first k central moments
sem = [0, mean[1], mu[2], mu[3], mu[4] - 3 * mu[2] ** 2,
       mu[5] - 10 * mu[3] * mu[2], mu[6] - 15 * mu[4] * mu[2] + 30 * mu[2] ** 3]  # the first k cumulants
norm_mu = [mu[i] / mu[2] ** (i / 2) for i in range(k + 1)]  # normalized central moments
norm_sem = [sem[i] / mu[2] ** (i / 2) for i in range(k + 1)]  # normalized cumulants

# Logging the results
logger.info('\nMoments: \n%s', mean[1:])
logger.info('\nCentral moments: \n%s', mu[1:])
logger.info('\nCumulants: \n%s', sem[1:])
logger.info('\nNormalized central moments: \n%s', norm_mu[1:])
logger.info('\nNormalized cumulants: \n%s', norm_sem[1:])

# Calculate moments using the formulas
alpha = beta = 1 / 2

moment_n_alpha_beta = gamma(1 + alpha + beta) / (gamma(1 + alpha) * gamma(beta))
moment_alpha_beta = gamma(alpha + beta) / (gamma(alpha) * gamma(beta))

logger.info('\nMoment B(n+alpha, beta) / B(alpha, beta): %.4f', moment_n_alpha_beta / moment_alpha_beta)

# Calculate skewness (κ3)
s = 5  # for example, you can replace it with the actual value
skewness_denominator = alpha * beta * 2 * (beta - alpha) * (alpha + beta + 2)

if skewness_denominator != 0:
    skewness = (s * (alpha + beta + 1)) / skewness_denominator
    logger.info('\nSkewness (κ3): %.4f', skewness)
else:
    logger.warning('\nSkewness (κ3) is undefined due to division by zero.')


# Calculate kurtosis (κ4)
kurtosis = (6 * alpha**3 + alpha**2 * (1 - 2 * beta) - 2 * alpha * beta * (beta + 2) + beta**2 * (beta + 1)) / (
        alpha * beta * (alpha + beta + 2) * (alpha + beta + 3))
logger.info('\nKurtosis (κ4): %.4f', kurtosis)

plt.show()
