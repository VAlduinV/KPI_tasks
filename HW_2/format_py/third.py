import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
# Збереження анімації у HTML
from matplotlib.animation import PillowWriter


# Функція для створення 3D-поверхні з параметром
def generate_surface(parameter):
    # Ваша формула для створення поверхні залежно від параметра
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x, y = np.meshgrid(x, y)
    z = np.sin(np.sqrt(x ** 2 + y ** 2) + parameter)
    return x, y, z


# Функція для оновлення анімації
def animate(parameter):
    ax.cla()  # Очищення попередньої поверхні
    x, y, z = generate_surface(parameter)
    surface = ax.plot_surface(x, y, z, cmap='viridis')
    ax.set_title(f'Параметр: {parameter:.2f}')
    return surface


# Створення фігури та 3D-поверхні
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Задайте діапазон параметра і створіть анімацію
parameter_range = np.linspace(0, 2 * np.pi, 100)
ani = FuncAnimation(fig, animate, frames=parameter_range, interval=100)

# Збереження анімації в GIF
ani.save('animated_surface.gif', writer='pillow')

ani.save('animated_surface.html', writer=PillowWriter(fps=10))

plt.show()
