from choice import Choice
import numpy as np

from bokeh.models import ColumnDataSource, Span, Div, Range1d
from bokeh.layouts import column, layout
from bokeh.models import Button, TextInput
from bokeh.plotting import figure, curdoc
from bokeh.embed import components

x_vals = np.arange(0, 1000)
y_vals = x_vals.copy()  # This is important

df = ColumnDataSource(data={'x':x_vals,
                            'y':y_vals,
                            'y2':y_vals.copy()
})

PAGE_WIDTH = 800

# create a plot and style its properties
p = figure(title="Cost Comparison", x_range=(0, 1000), y_range=(0, 1000), 
           tools = "wheel_zoom, pan, reset", toolbar_location="right",
           plot_width=PAGE_WIDTH, plot_height=400, name="main_fig")

p.xaxis.axis_label = "# of units purchased"
p.yaxis.axis_label = "Total Cost"

wid = 2
p.line(x='x', y='y', line_width=wid, color="red", source=df)
p.line(x='x', y='y2', line_width=wid, color="blue", source=df)

eq_solve = Span(location=0, dimension='height', line_width=2)
p.add_layout(eq_solve)

slope_input = TextInput(value="1", title="Cost per unit with equipment:")
var_input = TextInput(value="3", title="Cost per unit without equipment:", width=PAGE_WIDTH)
int_input = TextInput(value="60", title="Cost of equipment:")
button = Button(label="Draw!")


def b_call(event):
    """
    Button functionality stuff
    """
    a = Choice('purchasing equipment', slope_input.value, int_input.value)
    b = Choice('not purchasing equipment', var_input.value)

    ALL = slice(len(df.data['x']))

    df.patch({
      'y':[(ALL, df.data['x']*a.slope + a.inter)],
      'y2':[(ALL, df.data['x']*b.slope)]
    })

    try:
      diff = Choice.when_equal(a, b)
      BUF = 10
      SOL = diff['sol']['x']
      eq_solve.location = SOL
      answer.text = diff['descr']

      p.x_range.start = SOL - BUF
      p.x_range.end = SOL + BUF

      p.y_range.start = diff['sol']['y'] - BUF
      p.y_range.end = diff['sol']['y'] + BUF

    except ValueError:
      eq_solve.location = 0
      answer.text = 'There isnt a solution'


answer = Div()

button.on_click(b_call)

my_layout = layout([
  [column(int_input, slope_input, var_input)],
  [column(button, answer, p)]
])

vale = figure(name='hehe')
vale.circle([1,2], [3,4])

curdoc().add_root(p)
curdoc().add_root(vale)

