import random
import numpy as np
import matplotlib.pyplot as plt
from Entities import Lapin, Loup, Case, Map, Population


def update_plot(global_plot, grass, prey_population, predator_population):
    """Update 2D environment plot and population line plot.

    Args:
        global_plot (tuple): Tuple with the figure container and a tuple with the two subplots.
        grass : instance of Map class
        prey_population : instance of Lapin class
        predator_population : instance of Loup class
    """

    fig = global_plot[0]
    ax1, ax2 = global_plot[1]

    # Plots
    # clear axis
    ax1.cla()
    ax2.cla()

    grass_map = [[case.quantity_food for case in line] for line in grass]

    ax1.imshow(grass_map, cmap='Greens', vmin=0, vmax=1)

    ax1.scatter(prey_population.x_list(), prey_population.y_list(), color='b', marker=4)

    ax1.scatter(predator_population.x_list(), predator_population.y_list(), color='r', marker=5)

    print(grass.get_food_quantity())

    ax2.plot(grass.get_food_quantity(), color='g')
    ax2.plot(len(prey_population), color='b')
    ax2.plot(len(predator_population), color='r')

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


def simulation(y, x, prey_init, predator_init, steps):
    grass = Map(x, y)
    predator_population = Population(Loup, predator_init, grass)
    prey_population = Population(Lapin, prey_init, grass)

    global_plot = set_plot()

    for s in range(steps):
        print(f'Step {s}')

        grass.new_day()
        prey_population.new_day()
        predator_population.new_day()

        update_plot(global_plot, grass, prey_population, predator_population)

    plt.waitforbuttonpress()


if __name__ == "__main__":
    simulation(y=30, x=30, prey_init=15, predator_init=5, steps=500)
