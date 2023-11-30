import numpy as np
import matplotlib.pyplot as plt
import logging
import mplcyberpunk

plt.style.use("cyberpunk")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

M = 50  # number of random processes
N = 2 ** 14  # number of process elements


def sigmoid(x, mu, alpha):
    return 0.5 * (1 + np.tanh((x - mu) / (2 * alpha)))


def generate_sigmoid(mu, alpha):
    x = np.random.uniform(-3, 3, N)
    X = sigmoid(x, mu, alpha)
    return X


mu_sigmoid = np.random.uniform(-3, 3, M)
alpha_sigmoid = np.random.uniform(1, 3, M)

xi_sigmoid = [generate_sigmoid(mu_sigmoid[i], alpha_sigmoid[i]) for i in range(M)]
X_sigmoid = np.sum(xi_sigmoid, axis=0)

# Plot the scatter plot with color map
plt.subplot(211)
colors = np.arange(len(X_sigmoid))
scatter = plt.scatter(range(0, N), X_sigmoid, s=np.ones(N), c=colors, cmap='rainbow')
plt.colorbar(scatter, label='Values')
plt.ylabel(r'$X = \sum_i \xi_i$')
plt.title(f'Realizations of the sum of {M} random processes')

plt.subplot(212)
p_sigmoid, bins_sigmoid, patches_sigmoid = plt.hist(X_sigmoid, 400, density=True, color="GREEN")
plt.xlabel('x')
plt.ylabel('p(x)')
plt.title(f'$M = {M}$')
plt.tight_layout()
plt.show()

delta_x_sigmoid = bins_sigmoid[1:] - bins_sigmoid[:-1]
x_sigmoid = bins_sigmoid[:-1]

k_sigmoid = 6
mean_sigmoid = [np.sum(x_sigmoid ** i * p_sigmoid * delta_x_sigmoid) for i in range(k_sigmoid + 1)]
mu_sigmoid = [np.sum((x_sigmoid - mean_sigmoid[1]) ** i * p_sigmoid * delta_x_sigmoid) for i in range(k_sigmoid + 1)]
sem_sigmoid = [0] + [mean_sigmoid[i + 1] for i in range(k_sigmoid)]

norm_mu_sigmoid = [mu_sigmoid[i] / mu_sigmoid[2] ** (i / 2) for i in range(k_sigmoid + 1)]
norm_sem_sigmoid = [sem_sigmoid[i] / mu_sigmoid[2] ** (i / 2) for i in range(k_sigmoid + 1)]

logger.info('\nMoments \n%s', mean_sigmoid[1:])
logger.info('\nCentral moments \n%s', mu_sigmoid[1:])
logger.info('\nCumulants \n%s', sem_sigmoid[1:])
logger.info('\nNormalized central moments \n%s', norm_mu_sigmoid[1:])
logger.info('\nNormalized cumulants \n%s', norm_sem_sigmoid[1:])

# Calculate theoretical mean and variance
theoretical_mean_total = np.sum(mu_sigmoid)
theoretical_variance_total = np.sum(alpha_sigmoid ** 2 / 3)  # Assuming alpha_sigmoid is the parameter of sigmoid

# Print the results
logger.info(f'Theoretical Mean of the Sum: {theoretical_mean_total}')
logger.info(f'Theoretical Variance of the Sum: {theoretical_variance_total}')
