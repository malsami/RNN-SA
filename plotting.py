"""File for different plots for visualisation of the results of hyperparameter optimization.

- Single Line Plot: plot the validation accuracy as a function of one hyperparamter
- Correlation: plot correlation matrix between validation accuracy and all hyperparamters
"""


def single_line_plot():
    ### SINGLE LINE PLOT ###
    import csv

    import matplotlib.pyplot as plt

    x = []  # data that should be plotted on the x-axis (a hyperparameter)
    y = []  # data that should be plotted on the y-axis (validation accuracy)

    with open('LSTM_num_cells.csv', 'r') as csvfile:  # open csv file
        plots = csv.reader(csvfile, delimiter=',')
        header = next(plots)  # read header
        for row in plots:  # iterate over all rows and read data
            x.append(int(row[9]))  # hyperparameter to plot
            y.append(float(row[2]))  # validation accuracy

    plt.plot(x, y, 'o')  # line plot of y = f(x)
    # plt.plot([200, 200], [0, 1], 'r--')  # vertical line
    # plt.plot([0, 5000], [0.977, 0.977], 'r')  # horizontal line

    plt.xlabel('hidden_layer_size')  # label of x-axis
    plt.ylabel('val_acc')  # label of y-axis
    plt.axis([0, 1000, 0.88, 0.98])  # limits of x- and y-axis: [min_x, max_x, min_y, max_y]
    # plt.xticks([0, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])    # ticks of x-axis
    # plt.yticks([0.9, 0.92, 0.94, 0.96, 0.98, 1])  # ticks of y-axis

    plt.show()  # show all plots


def correlation():
    ### CORRELATION ###
    # plot correlation between all hyperparameters and the validation accuracy with Talos
    import talos
    import matplotlib.pyplot as plt

    r = talos.Reporting('LSTM_hidden_layer_size.csv')  # open and read csv file

    r.plot_corr()  # plot correlation matrix

    plt.show()  # show all plots


def plot_num_epochs():
    """Plot validation accuracy as function of num_epochs."""
    import csv

    import matplotlib.pyplot as plt

    x = []  # data that should be plotted on the x-axis (a hyperparameter)
    y = []  # data that should be plotted on the y-axis (validation accuracy)

    with open('num_epochs\\LSTM_num_epochs.csv', 'r') as csvfile:  # open csv file
        plots = csv.reader(csvfile, delimiter=',')
        header = next(plots)  # read header
        for row in plots:  # iterate over all rows and read data
            x.append(int(row[7]))  # hyperparameter to plot
            y.append(float(row[2]))  # validation accuracy

    plt.plot(x, y, 'o')  # line plot of y = f(x)
    # plt.plot([128, 128], [0, 1], 'r--')  # vertical line
    plt.plot([0, 200], [0.932, 0.932], 'r')  # horizontal line

    plt.xlabel('num_epochs')  # label of x-axis
    plt.ylabel('val_acc')  # label of y-axis
    plt.axis([0, 200, 0.8, 1])  # limits of x- and y-axis: [min_x, max_x, min_y, max_y]
    # plt.xticks([0, 32, 64, 128, 200, 256, 400, 512, 600, 800, 1024])  # ticks of x-axis
    # plt.yticks([0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96])  # ticks of y-axis

    plt.show()  # show all plots


def plot_batch_size():
    """Plot validation accuracy as function of batch_size."""
    import csv

    import matplotlib.pyplot as plt

    x = []  # data that should be plotted on the x-axis (a hyperparameter)
    y = []  # data that should be plotted on the y-axis (validation accuracy)

    with open('batch_size\\LSTM_batch_size.csv', 'r') as csvfile:  # open csv file
        plots = csv.reader(csvfile, delimiter=',')
        header = next(plots)  # read header
        for row in plots:  # iterate over all rows and read data
            x.append(int(row[6]))  # hyperparameter to plot
            y.append(float(row[2]))  # validation accuracy

    plt.plot(x, y, 'o')  # line plot of y = f(x)
    plt.plot([128, 128], [0, 1], 'r--')  # vertical line
    plt.plot([0, 1050], [0.9574916288153964, 0.9574916288153964], 'r')  # horizontal line

    plt.xlabel('batch_size')  # label of x-axis
    plt.ylabel('val_acc')  # label of y-axis
    plt.axis([0, 1050, 0.9, 0.96])  # limits of x- and y-axis: [min_x, max_x, min_y, max_y]
    plt.xticks([0, 32, 64, 128, 200, 256, 400, 512, 600, 800, 1024])  # ticks of x-axis
    plt.yticks([0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96])  # ticks of y-axis

    plt.show()  # show all plots


def plot_hidden_layer_size():
    """Plot validation accuracy as function of hidden_layer_size."""
    import csv

    import matplotlib.pyplot as plt

    x = []  # data that should be plotted on the x-axis (a hyperparameter)
    y = []  # data that should be plotted on the y-axis (validation accuracy)

    with open('hidden_layer_size\\LSTM_hidden_layer_size.csv', 'r') as csvfile:  # open csv file
        plots = csv.reader(csvfile, delimiter=',')
        header = next(plots)  # read header
        for row in plots:  # iterate over all rows and read data
            x.append(int(row[10]))  # hyperparameter to plot
            y.append(float(row[2]))  # validation accuracy

    plt.figure(1, (12.8, 4.8))  # create figure with specific size

    ### subplot for all data points ###
    plt.subplot(1, 2, 1)
    plt.plot(x, y, 'o')  # line plot of y = f(x)
    plt.plot([0, 5000], [0.977, 0.977], 'r')  # horizontal line

    plt.xlabel('hidden_layer_size')  # label of x-axis
    plt.ylabel('val_acc')  # label of y-axis
    plt.axis([0, 5000, 0.88, 0.98])  # limits of x- and y-axis: [min_x, max_x, min_y, max_y]

    ### subplot for interesting data points ###
    plt.subplot(1, 2, 2)
    plt.plot(x, y, 'o')  # line plot of y = f(x)
    plt.plot([319, 319], [0, 1], 'r--')  # vertical line
    plt.plot([0, 1000], [0.977, 0.977], 'r')  # horizontal line

    plt.xlabel('hidden_layer_size')  # label of x-axis
    plt.ylabel('val_acc')  # label of y-axis
    plt.axis([0, 1000, 0.88, 0.98])  # limits of x- and y-axis: [min_x, max_x, min_y, max_y]
    plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])  # ticks of x-axis
    # plt.yticks([0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96])  # ticks of y-axis

    plt.show()  # show all plots


def plot_num_cells():
    """Plot validation accuracy as function of num_cells."""
    import csv

    import matplotlib.pyplot as plt

    x = []  # data that should be plotted on the x-axis (a hyperparameter)
    y = []  # data that should be plotted on the y-axis (validation accuracy)

    with open('num_cells\\LSTM_num_cells.csv', 'r') as csvfile:  # open csv file
        plots = csv.reader(csvfile, delimiter=',')
        header = next(plots)  # read header
        for row in plots:  # iterate over all rows and read data
            x.append(int(row[9]))  # hyperparameter to plot
            y.append(float(row[2]))  # validation accuracy

    plt.plot(x, y, 'o')  # line plot of y = f(x)
    # plt.plot([128, 128], [0, 1], 'r--')  # vertical line
    plt.plot([0, 11], [0.9847, 0.9847], 'r')  # horizontal line

    plt.xlabel('num_cells')  # label of x-axis
    plt.ylabel('val_acc')  # label of y-axis
    plt.axis([0, 11, 0.95, 1])  # limits of x- and y-axis: [min_x, max_x, min_y, max_y]
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])  # ticks of x-axis
    # plt.yticks([0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96])  # ticks of y-axis

    plt.show()  # show all plots


if __name__ == "__main__":
    plot_num_cells()