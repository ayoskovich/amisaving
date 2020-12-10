from bokeh.plotting import figure
from bokeh.embed import components 

plot = figure()
plot.circle([1,2], [3,4])

script, div = components(plot)

with open("script.html", "w") as file:
  file.write(script)

with open("div.html", "w") as file:
  file.write(div)
