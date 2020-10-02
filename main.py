import numpy as np

from bokeh.models import ColumnDataSource, DataTable, TableColumn
from bokeh.layouts import column
from bokeh.models import Button, TextInput
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

x_vals = np.array([0, 1, 2, 3, 4])
y_vals = x_vals.copy()  # This is important

df = ColumnDataSource(data={'x':x_vals,
                            'y':y_vals})

columns = [
  TableColumn(field="x", title="X value"),
  TableColumn(field="y", title="Y value")
]
data_table = DataTable(source=df, columns=columns)


# create a plot and style its properties
p = figure(title="Cost Comparison", x_range=(0, 10), y_range=(0, 10), 
           tools = "wheel_zoom, pan, reset", toolbar_location="right")

p.xaxis.axis_label = "X label"
p.yaxis.axis_label = "Y label"

r = p.line(x='x', y='y', source=df)

slope_input = TextInput(value="", title="Slope")
int_input = TextInput(value="", title="Intercept")
button = Button(label="Draw!")


def b_call(event):
    s = int(slope_input.value)
    i = int(int_input.value)

    ALL = slice(len(df.data['x']))

    df.patch({
      'y':[(ALL, df.data['x']*s + i)]
    })


button.on_click(b_call)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(slope_input, int_input, button, p, data_table))
