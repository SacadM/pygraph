import argparse
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from mpl_toolkits.mplot3d import Axes3D

def parse_function(func_str):
    x, y = sp.symbols('x y')
    func = sp.sympify(func_str)
    return func

def evaluate_function(func, x_vals, y_vals=None):
    x, y = sp.symbols('x y')
    if y_vals is not None:
        f = sp.lambdify((x, y), func, 'numpy')
        return f(x_vals, y_vals)
    else:
        f = sp.lambdify(x, func, 'numpy')
        return f(x_vals)

def plot_2d_function(func_str, x_range=(-10, 10), num_points=1000):
    func = parse_function(func_str)
    x_vals = np.linspace(x_range[0], x_range[1], num_points)
    y_vals = evaluate_function(func, x_vals)

    plt.plot(x_vals, y_vals, label=func_str)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'Plot of {func_str}')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_3d_function(func_str, x_range=(-10, 10), y_range=(-10, 10), num_points=100):
    func = parse_function(func_str)
    x_vals = np.linspace(x_range[0], x_range[1], num_points)
    y_vals = np.linspace(y_range[0], y_range[1], num_points)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = evaluate_function(func, X, Y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('f(x, y)')
    ax.set_title(f'3D Plot of {func_str}')
    plt.show()

def plot_derivative(func_str, x_range=(-10, 10), num_points=1000):
    func = parse_function(func_str)
    x = sp.symbols('x')
    derivative = sp.diff(func, x)
    x_vals = np.linspace(x_range[0], x_range[1], num_points)
    y_vals = evaluate_function(derivative, x_vals)

    plt.plot(x_vals, y_vals, label=f'd({func_str})/dx')
    plt.xlabel('x')
    plt.ylabel(f"f'(x)")
    plt.title(f"Derivative of {func_str}")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_integral(func_str, x_range=(-10, 10), num_points=1000):
    func = parse_function(func_str)
    x = sp.symbols('x')
    integral = sp.integrate(func, x)
    x_vals = np.linspace(x_range[0], x_range[1], num_points)
    y_vals = evaluate_function(integral, x_vals)

    plt.plot(x_vals, y_vals, label=f'∫{func_str} dx')
    plt.xlabel('x')
    plt.ylabel('F(x)')
    plt.title(f"Integral of {func_str}")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Plot mathematical functions.")
    parser.add_argument('function', type=str, help="Mathematical function to plot (e.g., 'x**2', 'sin(x)', 'x**2 + y**2').")
    parser.add_argument('plot_type', type=str, choices=['2D', '3D'], help="Type of plot: '2D' or '3D'.")
    parser.add_argument('--x_range', type=float, nargs=2, default=[-10, 10], help="Range of x values (default: [-10, 10]).")
    parser.add_argument('--y_range', type=float, nargs=2, default=[-10, 10], help="Range of y values for 3D plot (default: [-10, 10]).")
    parser.add_argument('--num_points', type=int, default=1000, help="Number of points to plot (default: 1000).")
    parser.add_argument('--derivative', action='store_true', help="Plot the derivative of the function.")
    parser.add_argument('--integral', action='store_true', help="Plot the integral of the function.")

    args = parser.parse_args()

    if args.plot_type == '2D':
        if args.derivative:
            plot_derivative(args.function, x_range=args.x_range, num_points=args.num_points)
        elif args.integral:
            plot_integral(args.function, x_range=args.x_range, num_points=args.num_points)
        else:
            plot_2d_function(args.function, x_range=args.x_range, num_points=args.num_points)
    elif args.plot_type == '3D':
        plot_3d_function(args.function, x_range=args.x_range, y_range=args.y_range, num_points=args.num_points)

if __name__ == "__main__":
    main()