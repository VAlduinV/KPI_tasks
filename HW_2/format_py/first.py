import matplotlib.pyplot as plt
import numpy as np
import mplcyberpunk


def plot_graph1():
    # Генеруємо 50 випадкових значень для y
    y = np.random.rand(50)

    # Створюємо перший графік
    plt.plot(y)

    # Додаємо горизонтальну лінію y=0.4
    plt.axhline(y=0.4, color='r', linestyle='--', label='y=0.4')

    # Підписи до графіку та легенда
    plt.title('Випадкові значення')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()


def plot_graph2():
    # Генеруємо значення x від -2π до 2π
    x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

    # Створюємо другий графік (синусоїда)
    plt.plot(x, np.sin(x))

    # Додаємо вертикальні лінії x=-π/2 і x=π/2
    plt.axvline(x=-np.pi / 2, color='g', linestyle='--', label='x=-π/2')
    plt.axvline(x=np.pi / 2, color='b', linestyle='--', label='x=π/2')

    # Підписи до графіку та легенда
    plt.title('Синусоїда від -2π до 2π')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()


if __name__ == "__main__":
    plt.style.use("cyberpunk")

    plt.subplot(2, 1, 1)  # Вказуємо, що перший графік буде в верхній підсітці
    plot_graph1()

    plt.subplot(2, 1, 2)  # Вказуємо, що другий графік буде в нижній підсітці
    plot_graph2()

    mplcyberpunk.add_glow_effects()
    plt.tight_layout()

    plt.show()
