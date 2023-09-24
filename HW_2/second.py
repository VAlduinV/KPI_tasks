import numpy as np
import matplotlib.pyplot as plt
import mplcyberpunk

plt.style.use("cyberpunk")

# Параметри зарядів (+) і (-)
q_positive = 1.0  # Позитивний заряд
q_negative = -1.0  # Негативний заряд

# Позиції зарядів
position_positive = np.array([2.0, 2.0])  # Позитивний заряд розташований в точці (2, 2)
position_negative = np.array([-1.0, -1.0])  # Негативний заряд розташований в точці (-1, -1)

# Початкова позиція частинки, яка рухатиметься
initial_position = np.array([0.0, 0.0], dtype=np.float64)  # Зміна типу на float64


# Функція для обчислення електричного поля від заряду в точці (x, y)
def electric_field(charge_position, point):
    r = point - charge_position
    r_magnitude = np.linalg.norm(r)
    electric_field_strength = q_positive / (r_magnitude ** 2) if q_positive > 0 else 0
    electric_field_direction = r / r_magnitude
    electric_field_vector = electric_field_strength * electric_field_direction
    return electric_field_vector


# Функція для обчислення траєкторії руху частинки
def calculate_trajectory(initial_position, num_steps, step_size):
    trajectory = [initial_position]
    current_position = initial_position.copy()  # Зміна для забезпечення правильного типу
    for _ in range(num_steps):
        total_electric_field = np.zeros(2)
        total_electric_field += electric_field(position_positive, current_position)
        total_electric_field += electric_field(position_negative, current_position)
        current_position += step_size * total_electric_field
        trajectory.append(current_position)
    return np.array(trajectory)


# Параметри для обчислення траєкторії
num_steps = 100
step_size = 0.05

# Обчислення траєкторії руху
trajectory = calculate_trajectory(initial_position, num_steps, step_size)

# Побудова графіка векторного поля
x = np.linspace(-3, 3, 20)
y = np.linspace(-3, 3, 20)
X, Y = np.meshgrid(x, y)
Ex = np.zeros_like(X)
Ey = np.zeros_like(Y)
for i in range(len(x)):
    for j in range(len(y)):
        point = np.array([X[i, j], Y[i, j]])
        electric_field_vector = electric_field(position_positive, point) + electric_field(position_negative, point)
        Ex[i, j], Ey[i, j] = electric_field_vector

plt.figure(figsize=(8, 8))
plt.quiver(X, Y, Ex, Ey, scale=20, scale_units='inches')
plt.scatter(position_positive[0], position_positive[1], c='red', marker='o', label='Позитивний заряд (+) в (2, 2)')
plt.scatter(position_negative[0], position_negative[1], c='blue', marker='o', label='Негативний заряд (-) в (-1, -1)')
plt.plot(trajectory[:, 0], trajectory[:, 1], 'g-', label='Траєкторія руху', linewidth=2)
plt.xlabel('X-ось')
plt.ylabel('Y-ось')
plt.title('Векторне поле та траєкторія руху')
plt.legend()
plt.grid(True)
mplcyberpunk.add_glow_effects()
plt.show()
