#!/usr/bin/env python
#
# Load in the necessary libraries (importing them as smaller strings for brevity).

import numpy as np
import matplotlib.pyplot as plt

# SN data to plot

blue1 = 'cornflowerblue'
blue2 = 'blue'
blue3 = 'mediumslateblue'
blue4 = 'slateblue'
blue5 = 'darkslateblue'
blue6 = 'deepskyblue'
blue7 = 'darkturquoise'
blue8 = 'steelblue'
blue9 = 'c'
blue10 = 'darkcyan'

red1 = 'red'
red2 = 'salmon'
red3 = 'tomato'
red4 = 'crimson'
red5 = 'orangered'
red6 = 'coral'

green = 'lime'




labels = 'I','Ia', 'Ia-91by-like', 'Ia-91T-like', 'Iax[02cx-like]', 'Ib', 'Ibc', 'Ibn', 'Ic', 'Ic-BL', 'II','II-P', 'II-pec', 'IIb', 'IIn', 'IIn/AGN', 'Unclassified SN' 
sizes = [2,110, 9, 6, 2, 12, 1, 1, 13, 4, 113, 19, 1, 6, 7, 1, 94]
colors = [blue1, blue2, blue3, blue4, blue5, blue6, blue7, blue8, blue9, blue10, red1, red2, red3, red4, red5, red6, green]
explode = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

# Plot
chart = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%.2f%%', shadow=False, labeldistance=1.2, startangle=90)
#plt.legend(chart[0], labels, loc='centre')
plt.axis('equal')
#plt.tight_layout()
plt.show()
