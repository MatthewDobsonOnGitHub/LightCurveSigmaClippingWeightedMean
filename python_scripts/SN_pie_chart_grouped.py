#!/usr/bin/env python
#
# Load in the necessary libraries (importing them as smaller strings for brevity).

import numpy as np
import matplotlib.pyplot as plt

# SN data to plot

blue_I = 'midnightblue'
blue_Ia = 'blue'
blue_Ib = 'deepskyblue'
blue_Ibn = 'dodgerblue'
blue_Ic = 'darkturquoise'
blue_Ic_BL = 'turquoise'
blue_Ibc = 'steelblue'

red_II = 'red'
red_IIb = 'crimson'
red_IIn = 'orangered'
red_IIn_AGN = 'coral'

#purple_SN = 'violet'

labels = 'I','Ia', 'Ib', 'Ibn', 'Ic', 'Ic-BL', 'Ibc', 'II', 'IIb', 'IIn', 'IIn/AGN'
sizes = [2, 127, 12, 1, 13, 4, 1, 133, 6, 7, 1]
colors = [blue_I, blue_Ia, blue_Ib, blue_Ibn, blue_Ic, blue_Ic_BL, blue_Ibc, red_II, red_IIb, red_IIn, red_IIn_AGN]
explode = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)


# Plot
chart = plt.pie(sizes, explode=explode, colors=colors, autopct='%.2f%%', shadow=False, labeldistance=1.2, pctdistance=1.2, startangle=90)
plt.legend(chart[0], labels, loc='right')
plt.axis('equal')
plt.savefig("SN_pie_chart_sans_unclassified.pdf")
plt.tight_layout()
plt.show()
