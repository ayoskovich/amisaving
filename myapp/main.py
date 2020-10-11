from choice import Choice
import numpy as np


from bokeh.models import ColumnDataSource, DataTable, TableColumn, Span
from bokeh.models import Div
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

PAGE_WIDTH = 800

# create a plot and style its properties
p = figure(title="Cost Comparison", x_range=(0, 10), y_range=(0, 10), 
           tools = "wheel_zoom, pan, reset", toolbar_location="right",
           plot_width=PAGE_WIDTH, plot_height=400)

p.xaxis.axis_label = "# of units purchased"
p.yaxis.axis_label = "Total Cost"

wid = 2
p.line(x='x', y='y', line_width=wid, color="red", source=df)
p.line(x='x', y='y2', line_width=wid, color="blue", source=df)

eq_solve = Span(location=0, dimension='height', line_width=2)
p.add_layout(eq_solve)

slope_input = TextInput(value="", title="Cost per unit with equipment")
var_input = TextInput(value="", title="Cost per unit without equipment")
int_input = TextInput(value="", title="Cost of equipment", width=PAGE_WIDTH)
button = Button(label="Draw!", css_classes=["my_button"])


def b_call(event):
    """
    Button functionality stuff
    """
    a = Choice('Purchasing equipment', slope_input.value, int_input.value)
    b = Choice('No equipment', var_input.value)

    ALL = slice(len(df.data['x']))

    df.patch({
      'y':[(ALL, df.data['x']*a.slope + a.inter)],
      'y2':[(ALL, df.data['x']*b.slope)]
    })

    try:
      diff = Choice.when_equal(a, b)
      eq_solve.location = diff['sol']
      answer.text = diff['descr']
      
    except ValueError:
      eq_solve.location = 0
      answer.text = 'There isnt a solution'


header = Div(text="<h1>Am I Saving?</h1>")

description = Div(text="""<p>
This website is meant to help you make informed spending decisions.
More specifically, it will aid you when your asking questions about whether or not it's worth it
to spend money on equipment. 
</p>
""", width=PAGE_WIDTH)

w_start = Div(text="<h3>Purchasing equipment</h3>", width=int(PAGE_WIDTH / 2))
no_start = Div(text="<h3>No equipment</h3>", width=int(PAGE_WIDTH / 2))
answer = Div()

button.on_click(b_call)

my_layout = layout([
  [header],
  [description],
  [column(int_input, slope_input, var_input, button)],
  [column(answer, p)]
])

curdoc().add_root(my_layout)
