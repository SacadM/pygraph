import argparse

def parse_cli_args():
    parser = argparse.ArgumentParser(description="Plot mathematical functions or CSV data.")
    parser.add_argument('function', type=str, nargs='?', default=None, help="Mathematical function to plot (e.g., 'x**2', 'sin(x)', 'x**2 + y**2'). For parametric, provide 'x(t), y(t)'. If --csv is provided, this argument is optional.")
    parser.add_argument('plot_type', type=str, choices=['2D', '3D', 'parametric', 'polar', 'csv'], help="Type of plot: '2D', '3D', 'parametric', 'polar', 'csv'.")
    parser.add_argument('--csv', type=str, help="Path to CSV file containing data points to plot.")
    parser.add_argument('--increment', type=float, default=1, help="Increment between each item of the CSV data (default: 1).")
    parser.add_argument('--forecast', type=int, default=0, help="Number of points to forecast (default: 0).")
    parser.add_argument('--x_range', type=float, nargs=2, default=[-10, 10], help="Range of x values (default: [-10, 10]).")
    parser.add_argument('--y_range', type=float, nargs=2, default=[-10, 10], help="Range of y values for 3D plot (default: [-10, 10]).")
    parser.add_argument('--num_points', type=int, default=1000, help="Number of points to plot (default: 1000).")
    parser.add_argument('--derivative', action='store_true', help="Plot the derivative of the function.")
    parser.add_argument('--integral', action='store_true', help="Plot the integral of the function.")
    parser.add_argument('--taylor', type=int, help="Plot the Taylor series approximation of the function up to n terms.")
    parser.add_argument('--export', type=str, choices=['png', 'svg', 'pdf'], help="Export plot format.")
    parser.add_argument('--annotate', nargs='?', const=True, help="Add mathematical annotations. Optionally, provide a condition (e.g., 'x>0').")
    parser.add_argument('--multiplot', nargs='+', help="List of functions to plot in a multiplot layout.")
    parser.add_argument('--rows', type=int, default=1, help="Number of rows in multiplot layout.")
    parser.add_argument('--cols', type=int, default=1, help="Number of columns in multiplot layout.")
    parser.add_argument('--no_show', action='store_true', help="Do not show plots interactively.")

    return parser.parse_args()