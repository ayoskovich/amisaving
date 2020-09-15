#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np

import sympy
from sympy import symbols
from sympy import lambdify
from sympy import latex

def build_cost(slope, inter=0):
    """ Create the total cost curve.
    
    Returns a sympy equation.
    """
    m, x, b = symbols('m x b')
    COST = m*x + b
    return COST.subs(m, slope).subs(b, inter)


fixed = build_cost(slope=2, inter=24)
variable = build_cost(slope=4)


# In[ ]:


lam_a = lambdify(x, fixed, modules=['numpy'])
lam_b = lambdify(x, variable, modules=['numpy'])

x_vals = np.linspace(0, 20, 100)
y_vals1 = lam_a(x_vals)
y_vals2 = lam_b(x_vals)

plt.plot(x_vals, y_vals1, label=latex(fixed));
plt.plot(x_vals, y_vals2, label=latex(variable));
plt.title('Cost curves');
plt.legend();


# In[ ]:


a = pd.DataFrame({
    'name':['anthony', 'bob', 'vale'],
    'age':[23, 100, 22]
})
b = pd.DataFrame({
    'name':['bob'],
    'food':['tacos']
})


# In[ ]:


a


# In[ ]:


b


# In[ ]:


pd.merge(a, b, how='outer', on='name')


# In[ ]:


SELECT a.*, b.* 
FROM names AS a 
LEFT JOIN foods AS b 
ON a.name = UPCASE(b.name)

