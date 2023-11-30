import mplcyberpunk
import numpy as np
import matplotlib.pyplot as plt
import logging

plt.style.use("cyberpunk")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def logistic_density(x, m, alpha):
    return (1 / alpha) * np.exp(-(x - m) / alpha) * (1 + np.exp(-(x - m) / alpha)) ** -2


def generate_logistic_distribution(N, m, alpha):
    r = np.random.uniform(0, 1, N)
    phi = np.random.uniform(0, 1, N)
    z = np.cos(2 * np.pi * phi) * np.sqrt(-2 * np.log(r))
    X = m + alpha * z
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
    theoretical_density = logistic_density(bins, m, alpha)
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
    plt.plot(bins[:-1], cumulative_density, 'r', label='Empirical cumulative distribution')

    # Add logistic distribution line
    norm_cdf = (1 + np.tanh((bins - m) / (2 * alpha))) / 2  # Cumulative distribution function for logistic distribution
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
    delta_x = bins[1:] - bins[:-1]
    x = bins[:-1]

    count, _, _ = plt.hist(X, bins, density=True)

    mean = [np.sum(x ** i * count * delta_x) for i in range(k + 1)]
    mu = [np.sum((x - mean[1]) ** i * count * delta_x) for i in range(k + 1)]
    sem = [0, mean[1], mu[2], mu[3], mu[4] - 3 * mu[2] ** 2, mu[5] - 10 * mu[3] * mu[2],
           mu[6] - 15 * mu[4] * mu[2] + 30 * mu[2] ** 3]

    norm_mu = [mu[i] / mu[2] ** (i / 2) for i in range(k + 1)]
    norm_sem = [sem[i] / mu[2] ** (i / 2) for i in range(k + 1)]

    return mean, mu, sem, norm_mu, norm_sem


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
    logger.info('\nMoments \n %s', mean[1:])
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
