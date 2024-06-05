import random
import numpy as np
import matplotlib.pyplot as plt
import Entities

petit_lapin = Entities.Lapin()
petit_lapin.kill()

def grass_growth(env, rate=0.05):
    return np.minimum(env + rate, np.ones_like(env))


def update_plot(global_plot, grass, grass_qty, prey_population, prey_pop_size, predator_population, predator_pop_size):
    """Update 2D environment plot and population line plot.

    Args:
        global_plot (tuple): Tuple with the figure container and a tuple with the two subplots.
        grass (array): Numpy array representing the environment.
        grass_qty (list): List with grass quantity for each step of the simulation.
        prey_population (list): List of individuals. Each individual is a dictionary with at least 'x' and 'y' keys.
        prey_pop_size (list): List of number of individuals for each step.
        predator_population (list): List of individuals. Each individual is a dictionary with at least 'x' and 'y' keys.
        predator_pop_size (list): List of number of individuals for each step.
    """

    fig = global_plot[0]
    ax1, ax2 = global_plot[1]

    # Plots
    # clear axis
    ax1.cla()
    ax2.cla()

    ax1.imshow(grass, cmap='Greens', vmin=0, vmax=1)

    preys_x = []
    preys_y = []
    for idx in range(len(prey_population)):
        preys_x.append(prey_population[idx]['x'])
        preys_y.append(prey_population[idx]['y'])
    ax1.scatter(preys_x, preys_y, color='b', marker=4)

    predators_x = []
    predators_y = []
    for idx in range(len(predator_population)):
        predators_x.append(predator_population[idx]['x'])
        predators_y.append(predator_population[idx]['y'])
    ax1.scatter(predators_x, predators_y, color='r', marker=5)

    ax2.plot(grass_qty, color='g')
    ax2.plot(prey_pop_size, color='b')
    ax2.plot(predator_pop_size, color='r')

    grass_qty.append((np.sum(grass)))
    prey_pop_size.append(len(prey_population))
    predator_pop_size.append(len(predator_population))

    fig.canvas.flush_events()
    fig.canvas.draw()

    plt.pause(0.01)


def set_plot(width=25.6, height=13.3):
    """Initialize plot with two empty subplots.

    Args:
        width (float, optional): Width of the plot. Defaults to 25.6 (suits for 2560*1440 screen).
        height (float, optional): Height of the plot. Defaults to 13.3 (suits for 2560*1440 screen).

    Returns:
        tuple: First element of tuple is the figure container. Second element of the tuple is a tuple with the two
        subplots.
    """
    return plt.subplots(1, 2, figsize=(width, height))


def simulation(y, x, prey_init, predator_init):
    grass = np.zeros((x, y))
    grass[0, 3] = 0.8  # A particular point is more grassly than the others
    grass_qty = [np.sum(grass)]  # Size history

    predator_population = []  # List of predotors
    predator_pop_size = [len(predator_population)]  # Size history
    prey_population = [{'x': 5, 'y': 10}]  # List of preys    # One for example
    prey_pop_size = [len(prey_population)]  # Size history

    global_plot = set_plot()

    for s in range(20):
        print(f'Step {s}')
        grass = grass_growth(grass, rate=0.1)

        if len(prey_population) > 0 and prey_population[0]['x'] < 30:  # example of prey moving
            prey_population[0]['x'] += 1

        update_plot(global_plot, grass, grass_qty, prey_population, prey_pop_size, predator_population,
                    predator_pop_size)

    plt.waitforbuttonpress()


if __name__ == "__main__":
    simulation(y=30, x=30, prey_init=1, predator_init=0)
