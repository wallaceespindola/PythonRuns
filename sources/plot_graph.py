import matplotlib.pyplot as plt
import numpy as np


def plot_graph_1():
    print("Plotting a graph with 3 subplots: sin, cos, tan")

    # Create sample data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.tan(x)

    # Create a figure with 1 row and 3 columns of subplots
    fig, ax = plt.subplots(1, 3, figsize=(12, 8))

    # Plot data on each subplot
    ax[0].plot(x, y1)
    ax[0].set_title("Sine")

    ax[1].plot(x, y2)
    ax[1].set_title("Cosine")

    ax[2].plot(x, y3)
    ax[2].set_title("Tangent")

    # Display the figure
    plt.tight_layout()  # Adjust subplots to fit into the figure area.
    plt.show()

def plot_graph_2():
    print("Plotting a graph with 3 subplots: sinh, cosh, tanh")

    # Create sample data
    x = np.linspace(0, 10, 100)
    y1 = np.sinh(x)
    y2 = np.cosh(x)
    y3 = np.tanh(x)

    # Create a figure with 1 row and 3 columns of subplots
    fig, ax = plt.subplots(1, 3, figsize=(12, 8))

    # Plot data on each subplot
    ax[0].plot(x, y1)
    ax[0].set_title("Sine Hyperbolic")

    ax[1].plot(x, y2)
    ax[1].set_title("Cosine Hyperbolic")

    ax[2].plot(x, y3)
    ax[2].set_title("Tangent Hyperbolic")

    # Display the figure
    plt.tight_layout()  # Adjust subplots to fit into the figure area.
    plt.show()

def plot_graph_3():
    print("Plotting a graph with 3 subplots: arcsin, arccos, arctan")

    # Create sample data
    x = np.linspace(0, 10, 100)
    y1 = np.arcsin(x)
    y2 = np.arccos(x)
    y3 = np.arctan(x)

    # Create a figure with 1 row and 3 columns of subplots
    fig, ax = plt.subplots(1, 3, figsize=(12, 8))

    # Plot data on each subplot
    ax[0].plot(x, y1)
    ax[0].set_title("Arc Sin")

    ax[1].plot(x, y2)
    ax[1].set_title("Arc Cosin")

    ax[2].plot(x, y3)
    ax[2].set_title("Arc Tangent")

    # Display the figure
    plt.tight_layout()  # Adjust subplots to fit into the figure area.
    plt.show()

if __name__ == "__main__":
    plot_graph_1()
    plot_graph_2()
    plot_graph_3()
