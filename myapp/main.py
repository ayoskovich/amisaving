from choice import Choice
import numpy as np

from bokeh.models import ColumnDataSource, Span, Div, Range1d
from bokeh.layouts import column, layout, row
from bokeh.models import Button, TextInput, BoxAnnotation, Label
from bokeh.plotting import figure, curdoc
from bokeh.embed import components

x_vals = np.arange(0, 1000)
y_vals = x_vals.copy()  # This is important

df = ColumnDataSource(data={'x':x_vals,
                            'y':y_vals,
                            'y2':y_vals.copy()
})

# create a plot and style its properties
p = figure(title="Cost Comparison", x_range=(0, 1000), y_range=(0, 1000), 
           tools = "wheel_zoom, pan, reset", toolbar_location="right",
           name="main_fig")

# Region Highlighting
AL = .15
left_box = BoxAnnotation(fill_color='yellow', fill_alpha=AL)
right_box = BoxAnnotation(fill_color='green', fill_alpha=AL)

left_lab = Label()
right_lab = Label()

p.xaxis.axis_label = "# of units purchased"
p.yaxis.axis_label = "Total Cost"

wid = 2
p.line(x='x', y='y', line_width=wid, color="red", legend_label="Cost when buying equipment", source=df)
p.line(x='x', y='y2', line_width=wid, color="blue", legend_label="Cost without equipment", source=df)


eq_solve = Span(location=0, dimension='height', line_width=2)


p.add_layout(left_box)
p.add_layout(right_box)
p.add_layout(eq_solve)
p.add_layout(left_lab)
p.add_layout(right_lab)

slope_input = TextInput(value="1", sizing_mode="stretch_width", name="slope_input")
var_input = TextInput(value="3", sizing_mode="stretch_width", name="var_input")
int_input = TextInput(value="60", sizing_mode="stretch_width", name="int_input")

curdoc().add_root(slope_input)
curdoc().add_root(var_input)
curdoc().add_root(int_input)

button = Button(label="Draw!", name="myButton")


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
      SOLY = diff['sol']['y']
      eq_solve.location = SOL
      answer.text = diff['descr']

      p.x_range.start = SOL - BUF
      p.x_range.end = SOL + BUF

      p.y_range.start = diff['sol']['y'] - BUF
      p.y_range.end = diff['sol']['y'] + BUF

      left_box.right = SOL
      right_box.left = SOL 

      left_lab.text = diff['bef']
      left_lab.x = SOL - 5
      left_lab.y = SOLY + 5

      right_lab.text = diff['aft']
      right_lab.x = SOL + 5
      right_lab.y = SOLY - 5

    except ValueError:
      eq_solve.location = 0
      answer.text = 'There isnt a solution'


answer = Div()

button.on_click(b_call)


plot_int = column(button, answer, p, sizing_mode="stretch_width", name='plot')
curdoc().add_root(plot_int)

curdoc().title = "Am I Saving?"
