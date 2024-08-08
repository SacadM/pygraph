import plotly.io as pio

class Exporter:
    def export_plot(self, plot, format, filename='plot'):
        if format == 'png':
            pio.write_image(plot, f'{filename}.png')
        elif format == 'svg':
            pio.write_image(plot, f'{filename}.svg')
        elif format == 'pdf':
            pio.write_image(plot, f'{filename}.pdf')