import numpy as np

from bokeh.layouts import column
from bokeh.models import Button, TextInput
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

x_vals = np.linspace(0, 10, 20)
y_vals = x_vals*2


# create a plot and style its properties
p = figure(title="testing!", x_range=(0, 100), y_range=(0, 100), 
           toolbar_location="right")

r = p.circle(x_vals, y_vals)
dat = r.data_source
i = 0

def callback(attr, old, new):
    global i 

    new_data = dict()
    new_data['x'] = dat.data['x']
    new_data['y'] = dat.data['x']*10*(i + 1)
    p.title.text = f"Iteration: {i}"
    i = i + 1
    print(slope_input.value_input)
    print(f'Attr: {attr}')
    print(f'old: {old}')
    print(f'new: {new}')

    dat.data = new_data

# add a button widget and configure with the call back
button = Button(label="Press Me")
# button.on_click(callback)

slope_input = TextInput(value="Enter fixed cost here", title="Fixed cost:")
slope_input.on_change("value", callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(slope_input, p))
