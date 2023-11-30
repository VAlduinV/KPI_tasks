import numpy as np
import matplotlib.pyplot as plt
import logging
import mplcyberpunk

plt.style.use("cyberpunk")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def p_x_theoretical(x):
    return 1 / (np.pi * np.sqrt(1 - x**2))


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

plt.figure(figsize=(10, 6))

# Let's plot the values of the random variable
plt.subplot(211)
plt.plot(t, phi_process, color="GREEN")
mplcyberpunk.add_glow_effects()
mplcyberpunk.add_gradient_fill(alpha_gradientglow=0.5)
plt.xlabel('$t$')
plt.ylabel(r'$\varphi(t)$')
plt.title('Phase')

plt.subplot(212)
scatter = plt.scatter(t, X, s=np.ones(N), c=t, cmap='jet')
plt.ylabel(r'$X(t)$')
plt.xlabel('t')
plt.title(f'Realizations of random processes')
cbar = plt.colorbar(scatter, label='Time')
cbar.set_label('Time', rotation=270, labelpad=15)

# Let's draw a histogram of the distribution
plt.figure()
p, bins, patches = plt.hist(X, 400, density=True, color="RED", label='Experimental')
x_theoretical = np.linspace(-1, 1, 1000)
p_theoretical = p_x_theoretical(x_theoretical)
plt.plot(x_theoretical, p_theoretical, label='Theoretical', color='BLUE')

plt.xlabel('x')
plt.ylabel('p(x)')
plt.title('Experimental and Theoretical Distribution Density')
plt.legend()

# search for moments, central moments, and cumulants
delta_x = bins[1:] - bins[:-1]  # lengths of partition
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

plt.show()
