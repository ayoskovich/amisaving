import numpy as np

from bokeh.models import ColumnDataSource
from bokeh.layouts import column
from bokeh.models import Button, TextInput
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

x_vals = np.array([0, 1, 2, 3, 4])
y_vals = x_vals.copy()  # This is important

df = ColumnDataSource(data={'x':x_vals,
                            'y':y_vals})

# create a plot and style its properties
p = figure(title="This is a graph of a thing", x_range=(0, 10), y_range=(0, 10), 
           toolbar_location="right")

r = p.line(x='x', y='y', source=df)
dat = r.data_source


def c_slope(attr, old, new):
    xs = df.data['x']
    ALL = slice(len(xs))

    df.patch({
      'y':[(ALL, xs*int(new))]
    })
    print(f"Slope changed, new data: {df.data['y']}")


def c_int(attr, old, new):
    ys = df.data['y']
    ALL = slice(len(ys))

    df.patch({
      'y':[(ALL, ys+int(new))]
    })



slope_input = TextInput(value="", title="Slope")
slope_input.on_change("value", c_slope)


int_input = TextInput(value="", title="Intercept")
int_input.on_change("value", c_int)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(slope_input, int_input, p))
