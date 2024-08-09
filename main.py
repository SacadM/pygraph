from plotter import Plotter
from math_ops import MathOps
from export import Exporter
from annotations import Annotations
from cli import parse_cli_args
import sympy as sp

def main():
    args = parse_cli_args()

    plotter = Plotter()
    math_ops = MathOps()
    exporter = Exporter()
    annotations = Annotations()

    function = args.function
    plot_type = args.plot_type
    x_range = args.x_range
    y_range = args.y_range
    num_points = args.num_points
    show_plots = not args.no_show

    if plot_type == '2D':
        plotter.plot_2d(function, x_range, num_points)
    elif plot_type == '3D':
        plotter.plot_3d(function, x_range, y_range, num_points)
    elif plot_type == 'parametric':
        x_func, y_func = function.split(',')
        plotter.plot_parametric(x_func.strip(), y_func.strip(), x_range, num_points)
    elif plot_type == 'polar':
        plotter.plot_polar(function, x_range, num_points)

    if args.derivative:
        math_ops.plot_derivative(function, x_range, num_points)
    if args.integral:
        math_ops.plot_integral(function, x_range, num_points)
    if args.taylor:
        math_ops.plot_taylor_series(function, x_range, num_points, n=args.taylor)

    if args.export:
        exporter.export_plot(plotter.current_plot, args.export)
    
    if args.annotate:
        if args.annotate is True:  # No condition provided, use default behavior
            annotate_condition = None
        else:
            # Convert the string condition into a function
            def condition_func_factory(cond_str):
                x, y = sp.symbols('x y')
                return eval(f"lambda x, y: {cond_str}")

            annotate_condition = condition_func_factory(args.annotate)

        annotations.add_annotations(function, plotter.current_plot, x_range, num_points, annotate_on_condition=annotate_condition)

    if show_plots:
        if plotter.current_plot:
            plotter.current_plot.show()
        if math_ops.current_plot:
            math_ops.current_plot.show()

if __name__ == "__main__":
    main()