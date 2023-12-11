import math
import mplcyberpunk
import numpy as np
import matplotlib.pyplot as plt
import logging

plt.style.use("cyberpunk")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def logistic_density(x, m, alpha):
    return (1 / alpha) * np.exp(-(x - m) / alpha) / (1 + np.exp(-(x - m) / alpha)) ** 2


def theoretical_logistic_density(x, m, alpha):
    return (1 / alpha) * np.exp(-(x - m) / alpha) / (1 + np.exp(-(x - m) / alpha)) ** 2


def cumulative_logistic_distribution(x, m, alpha):
    return 0.5 * (1 + np.tanh((x - m) / (2 * alpha)))


def generate_logistic_distribution(N, m, alpha):
    u = np.random.uniform(0, 1, N)
    X = m + alpha * np.log(u / (1 - u))
    return X


def plot_process_realizations(X):
    plt.subplot(211)
    colors = np.arange(len(X))
    plt.scatter(range(0, len(X)), X, s=np.ones(len(X)), c=colors, cmap='rainbow')
    plt.ylabel(r'$X$')
    plt.title('Process realizations')
    plt.colorbar(label='Index')


def plot_experimental_distribution(X, alpha):
    plt.subplot(212)
    count, bins, _ = plt.hist(X, 400, density=True, alpha=0.7, color="RED", label='Empirical density')

    # Use the theoretical logistic density function for the plot
    theoretical_density = theoretical_logistic_density(bins, m, alpha)
    plt.plot(bins, theoretical_density, 'b--', label='Theoretical density (Logistic)')

    plt.xlabel('x')
    plt.ylabel('p(x)')
    plt.title('Experimental distribution density')
    plt.legend()
    plt.tight_layout()
    mplcyberpunk.add_glow_effects()
    mplcyberpunk.add_gradient_fill(alpha_gradientglow=0.5)

    return count, bins


def plot_cumulative_distribution(count, bins, alpha):
    plt.figure()
    cumulative_density = np.cumsum(count) * np.diff(bins)[0]

    # Use the theoretical cumulative distribution function for the plot
    norm_cdf = cumulative_logistic_distribution(bins, m, alpha)

    plt.plot(bins[:-1], cumulative_density, 'r', label='Empirical cumulative distribution')
    plt.plot(bins, norm_cdf, 'b--', label='Theoretical cumulative distribution (Logistic)')
    plt.xlabel('x')
    plt.ylabel('Cumulative Probability')
    plt.title('Empirical vs Theoretical Cumulative Distribution')
    plt.legend()
    plt.tight_layout()
    mplcyberpunk.add_glow_effects()
    mplcyberpunk.add_gradient_fill(alpha_gradientglow=0.5)
    plt.show()


def calculate_moments_cumulants(X, bins, k=6):
    delta_x = bins[1] - bins[0]
    x = bins[:-1]

    count, _ = np.histogram(X, bins=bins, density=True)

    mean_values = [np.sum(x ** i * count * delta_x) for i in range(k + 1)]
    central_moments = [np.sum((x - mean_values[1]) ** i * count * delta_x) for i in range(1, k + 1)]
    cumulants = [central_moments[i - 1] / math.factorial(i - 1) for i in range(1, k + 1)]

    norm_central_moments = central_moments / central_moments[1] ** (np.arange(1, k + 1) / 2)
    norm_cumulants = cumulants / central_moments[1] ** (np.arange(1, k + 1) / 2)

    return mean_values, central_moments, cumulants, norm_central_moments, norm_cumulants



def log_theoretical_values(alpha):
    m1_teor = m
    mu2_teor = (np.pi ** 2 / 3) * alpha ** 2
    asym_teor = 0
    exces_teor = 1.2

    logger.info(f'm1_teor = {m1_teor}')
    logger.info(f'mu2_teor = {mu2_teor}')
    logger.info(f'asym_teor = {asym_teor}')
    logger.info(f'exces_teor = {exces_teor}')


def log_moments_cumulants(mean, mu, sem, norm_mu, norm_sem):
    logger.info('\nMoments \n %s', mean)  # Змінено тут
    logger.info('\nCentral moments \n %s', mu[1:])
    logger.info('\nCumulants \n %s', sem[1:])
    logger.info('\nNormalized central moments \n %s', norm_mu[1:])
    logger.info('\nNormalized cumulants \n %s', norm_sem[1:])


# Set the number of elements and distribution parameters
N = 2 ** 14
m, alpha = -5, 2

# Generate Logistic distribution
X = generate_logistic_distribution(N, m, alpha)

# Plot process realizations and experimental distribution
plt.figure(figsize=(10, 6))
plot_process_realizations(X)
count, bins = plot_experimental_distribution(X, alpha)

# Calculate and log moments, central moments, and cumulants
mean, mu, sem, norm_mu, norm_sem = calculate_moments_cumulants(X, bins)
log_theoretical_values(alpha)
log_moments_cumulants(mean, mu, sem, norm_mu, norm_sem)

# Plot cumulative distribution
plot_cumulative_distribution(count, bins, alpha)
