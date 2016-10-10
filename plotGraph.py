# Plots a graph of a function and outputs it using matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Set font for matplotlib
font = {'family' : 'serif',
        #'weight': 'bold' ,
        'size'   : 10}

matplotlib.rc('font', **font)

# Create array with table of values between -2.0 and 8.0
x = np.arange(-2.0, 8.0, 0.01)

# Calculate the function f(x) = (x - 4 - ln(x))^2
y = (x - 4 - np.log(x)) ** 2

# Initialise plot
plt.plot(x, y, '-k', lw=1)
plt.ylim([0,10])

# Set axes so that are centred on the origin
ax = plt.subplot(111)
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')
ax.spines['left'].set_smart_bounds(True)
ax.spines['bottom'].set_smart_bounds(True)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Manually set axis tick values to prevent the number zero being shown on top of the axes
ax.xaxis.set_ticks([-2, -1, 1, 2, 3, 4, 5, 6, 7, 8])
ax.yaxis.set_ticks([-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Show the graph. It can be saved as an image once the window opens
plt.show()
