import numpy as np

from bokeh.models import ColumnDataSource, DataTable, TableColumn
from bokeh.layouts import column, layout
from bokeh.models import Button, TextInput
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

x_vals = np.array([0, 1, 2, 3, 4])
y_vals = x_vals.copy()  # This is important

df = ColumnDataSource(data={'x':x_vals,
                            'y':y_vals,
                            'y2':y_vals.copy()
})

columns = [
  TableColumn(field="x", title="X value"),
  TableColumn(field="y", title="Y value"),
  TableColumn(field="y2", title="Second Y value")
]
data_table = DataTable(source=df, columns=columns)


# create a plot and style its properties
p = figure(title="Cost Comparison", x_range=(0, 10), y_range=(0, 10), 
           tools = "wheel_zoom, pan, reset", toolbar_location="right")

p.xaxis.axis_label = "X label"
p.yaxis.axis_label = "Y label"

wid = 2
r = p.line(x='x', y='y', line_width=wid, color="red", source=df)
r = p.line(x='x', y='y2', line_width=wid, color="blue", source=df)

slope_input = TextInput(value="", title="Slope")
int_input = TextInput(value="", title="Intercept")

var_input = TextInput(value="", title="Variable Slope")

button = Button(label="Draw!")


def b_call(event):
    """
    Button functionality stuff
    """
    s = int(slope_input.value)
    i = int(int_input.value)

    v = int(var_input.value)

    ALL = slice(len(df.data['x']))

    df.patch({
      'y':[(ALL, df.data['x']*s + i)],
      'y2':[(ALL, df.data['x']*v)]
    })

    # Solve cost equality here





button.on_click(b_call)

INPUTS = column(slope_input, int_input, button, p)
my_layout = layout([
  [INPUTS, column(var_input, data_table)]
])

curdoc().add_root(my_layout)