import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
plt.close('all')

df = pd.DataFrame({'mass': [0.330, 4.87, 5.97],
                   'radius': [2439.7, 6051.8, 6378.1]},
                  index=['Mercury', 'Venus', 'Earth'])
plot = df.plot.pie(y='mass', figsize=(5, 5))
plt.show()
