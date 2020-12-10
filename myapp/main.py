from choice import Choice
import numpy as np

from bokeh.models import ColumnDataSource, Span, Div, Range1d
from bokeh.layouts import column, layout
from bokeh.models import Button, TextInput
from bokeh.plotting import figure, curdoc

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
           plot_width=PAGE_WIDTH, plot_height=400)

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


header = Div(text="<h1>Am I Saving?</h1>")
description = Div(text="""
<h3>
Should I invest in equipment to brew coffee at home, or is it cheaper to just buy coffee at Starbucks? Should I purchase a car or Uber everywhere? This calculator is meant to help you make these types of decisions.
</h3>
<p>
Let's focus on the coffee example. I have 2 options: 
</p>
<ol>
  <li>Purchase equipment and brew at home.</li>
  <li>Don't buy any equipment and purchase a cup of coffee at Starbucks.</li>
</ol>
<p>
For option 1, I would need to buy things like a kettle, a french press, and maybe some filters (let's say this all costs $60). Then, for each additional cup of coffee my only cost would be the coffee beans themselves (let's say $1 per cup). 
For option 2, I spend $0 on equipment but need to pay Starbucks for each cup of coffee (let's say $3).
</p>
<p>
That's a lot of words! In summary...
<ul>
  <li><span class='bold'>Cost of equipment:</span> The $60 I would spend on coffee equipment (filters, coffee machine, kettle, etc.).</li>
  <li><span class='bold'>Cost per unit with equipment:</span> The $1 I need to spend for each cup of coffee, if I buy equipment.</li>
  <li><span class='bold'>Cost per unit without equipment:</span> The $3 I need to spend for each cup of coffee I'd buy at Starbucks.</li>
</ul>
</p>
<p>
Click the 'Draw!' button below to compare these two options! (If you'd like to autopopulate the numbers from the coffee example, simply refresh the page.)
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
