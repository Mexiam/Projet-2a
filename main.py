import matplotlib.pyplot as plt
import matplotlib.transforms as trsf
from Entities import Lapin, Loup, Map, Population
from svgpathtools import svg2paths
from svgpath2mpl import parse_path

lapin_path, attributes = svg2paths('lapin.svg')
lapin_marker = parse_path(attributes[0]['d'])

lapin_marker.vertices -= lapin_marker.vertices.mean(axis=0)
lapin_marker = lapin_marker.transformed(trsf.Affine2D().rotate_deg(180))
lapin_marker = lapin_marker.transformed(trsf.Affine2D().scale(-1,1))

loup_path, attributes = svg2paths('loup.svg')
loup_marker = parse_path(attributes[0]['d'])

loup_marker.vertices -= loup_marker.vertices.mean(axis=0)
loup_marker = loup_marker.transformed(trsf.Affine2D().rotate_deg(180))
loup_marker = loup_marker.transformed(trsf.Affine2D().scale(-1,1))



def update_plot(global_plot, grass, grass_data, prey_population, prey_data, predator_population, pred_data):
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

    ax1.imshow(grass.get_food_map(), cmap='Greens', vmin=0, vmax=1)

    (x_protected_pos, y_protected_pos) = grass.protected_pos()
    ax1.scatter(y_protected_pos, x_protected_pos, color='k', marker='o')
    ax1.scatter(prey_population.y_list(lambda i : i.alive and not i.sane), prey_population.x_list(lambda i : i.alive and not i.sane), color='g', marker='X')
    ax1.scatter(predator_population.y_list(lambda i : i.alive and not i.sane), predator_population.x_list(lambda i : i.alive and not i.sane), color='g', marker='X')
    ax1.scatter(prey_population.y_list(), prey_population.x_list(), color='b', marker=lapin_marker)
    ax1.scatter(predator_population.y_list(), predator_population.x_list(), color='r', marker=loup_marker)
    
    ax2.plot(prey_data, color='b')
    ax2.plot(pred_data, color='r')
    ax2.plot(grass_data, color='g')

    fig.canvas.flush_events()
    fig.canvas.draw()

    plt.pause(0.5) 


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
    predator_population = Population(Loup, predator_init, grass, min_start_energy=2, max_start_energy=6)
    prey_population = Population(Lapin, prey_init, grass, min_start_energy=1, max_start_energy=5)

    grass_data = []
    prey_data = []
    pred_data = []

    global_plot = set_plot()

    for s in range(steps):
        print(f'Step {s}')

        grass.new_day()
        prey_population.new_day()
        predator_population.new_day()

        grass_data.append(grass.get_food_quantity()*prey_init/1000)
        prey_data.append(len(prey_population))
        pred_data.append(len(predator_population))

        update_plot(global_plot, grass, grass_data, prey_population, prey_data, predator_population, pred_data)

    plt.waitforbuttonpress()


if __name__ == "__main__":
    simulation(y=30, x=30, prey_init=120, predator_init=80, steps=500)
