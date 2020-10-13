from choice import Choice
import numpy as np

from bokeh.models import ColumnDataSource, Span, Div
from bokeh.layouts import column, layout
from bokeh.models import Button, TextInput
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

slope_input = TextInput(value="", title="Cost per unit with equipment:")
var_input = TextInput(value="", title="Cost per unit without equipment:", width=PAGE_WIDTH)
int_input = TextInput(value="", title="Cost of equipment:")
button = Button(label="Draw!")


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
description = Div(text="""
<h3>
Should I invest in equipment to brew coffee at home, or is it cheaper to just buy coffee at Starbucks? Should I purchase a car or Uber everywhere? This calculator is meant to help you make these types of decisions.
</h3>
<p>
In order to describe how to use this tool let's focus on the coffee example and let's say I have 2 options: 
</p>
<ol>
  <li>Purchase equipment and brew at home.</li>
  <li>Skip the equipment and purchase a cup of coffee at Starbucks.</li>
</ol>
<p>
For option 1, I would need to purchase equipment, and let's say that costs $60. Then, once I have the equipment, for each additional cup of coffee I only need to pay for the beans. Let's say that one cup of coffee takes $1 worth of beans.
For option 2, I spend $0 on equipment, but each cup costs me the price at Starbucks, and let's say that's $3.
</p>
<p>
That's a lot of words! In summary...
<ul>
  <li><span class='bold'>Cost of equipment:</span> The $60 I would spend on coffee equipment (filters, coffee machine, kettle, etc.).</li>
  <li><span class='bold'>Cost per unit with equipment:</span> The $1 I need to spend for each cup of coffee, if I buy equipment.</li>
  <li><span class='bold'>Cost per unit without equipment:</span> The $3 I need to spend for each cup of coffee I'd buy at Starbucks.</li>
</ul>
</p>
""", width=PAGE_WIDTH)

answer = Div()

button.on_click(b_call)

my_layout = layout([
  [header],
  [description],
  [column(int_input, slope_input, var_input)],
  [column(button, answer, p)]
])

curdoc().add_root(my_layout)
