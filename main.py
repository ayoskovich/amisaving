import numpy as np

from bokeh.layouts import column
from bokeh.models import Button, TextInput
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

# x_vals = np.linspace(0, 10, 20)
x_vals = np.array([0, 1, 2, 3, 4])
y_vals = x_vals

df = ColumnDataSource(data={'x':x_vals,
                            'y':y_vals})

# create a plot and style its properties
p = figure(title="This is a graph of a thing", x_range=(0, 10), y_range=(0, 10), 
           toolbar_location="right")

r = p.line(x='x', y='y', source=df)
dat = r.data_source


def callback(attr, old, new):
    new_data = dict()
    new_data['x'] = dat.data['x']
    try:
        new_data['y'] = dat.data['x']*int(new)
    except:
        pass

    dat.data = new_data


def callback2(attr, old, new):
    new_data = dict()
    new_data['x'] = dat.data['x']
    try:
        new_data['y'] = int(new) + dat.data['x']
    except:
        pass

    dat.data = new_data



slope_input = TextInput(value="", title="Slope")
slope_input.on_change("value", callback)


int_input = TextInput(value="", title="Intercept")
int_input.on_change("value", callback2)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(slope_input, int_input, p))
