import numpy as np

from sympy import symbols
from sympy import lambdify
from sympy import latex
from sympy import solve
from sympy import Eq

from bokeh.models import ColumnDataSource, DataTable, TableColumn, Span
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


slope_input = TextInput(value="", title="Variable cost")
int_input = TextInput(value="", title="Startup cost")

var_input = TextInput(value="", title="No equipment cost per unit")

button = Button(label="Draw!")

x = symbols('x')

def build_cost(slope, inter=0):
    """ Create the total cost curve.
    
    Returns a sympy equation.
    """
    m, x, b = symbols('m x b')
    COST = m*x + b
    return COST.subs(m, slope).subs(b, inter)


def b_call(event):
    """
    Button functionality stuff
    """
    s = float(slope_input.value)
    i = float(int_input.value)

    v = float(var_input.value)

    ALL = slice(len(df.data['x']))

    df.patch({
      'y':[(ALL, df.data['x']*s + i)],
      'y2':[(ALL, df.data['x']*v)]
    })

    # Solve cost equality here
    fixed = build_cost(slope=s, inter=i)
    variable = build_cost(slope=v)

    # Update vertical line
    solution = solve(Eq(fixed, variable))
    print(f'Solution: {solution}')
    EQ = float(solution[0])

    eq_solve = Span(location=EQ, dimension='height', line_width=2)
    p.add_layout(eq_solve)






button.on_click(b_call)

INPUTS = column(slope_input, int_input, button, p)
my_layout = layout([
  [INPUTS, column(var_input, data_table)]
])

curdoc().add_root(my_layout)
