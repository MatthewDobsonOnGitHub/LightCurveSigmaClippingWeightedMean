#!/usr/bin/env python
#
# Load in the necessary libraries (importing them as smaller strings for brevity).

import numpy as np
import matplotlib.pyplot as plt

# SN data to plot

I = 2
Ia = 110
Ia_91bg_like = 9
Ia_91T_like = 6
Iax_02cx_like = 2
Ib = 12
Ibn = 1
Ic = 13
Ic_BL = 4
Ibc = 1
II = 113
II_P = 19
II_pec = 1
IIb = 6
IIn = 7
IIn_AGN = 1

blue_I = 'midnightblue'
blue_Ia = 'blue'
blue_Ia_91bg_like = 'mediumblue'
blue_Ia_91T_like = 'royalblue'
blue_Iax_02cx_like = 'navy'
blue_Ib = 'deepskyblue'
blue_Ibn = 'dodgerblue'
blue_Ic = 'darkturquoise'
blue_Ic_BL = 'turquoise'
blue_Ibc = 'steelblue'

red_II = 'red'
red_II_P = 'indianred'
red_II_pec = 'lightcoral'
red_IIb = 'crimson'
red_IIn = 'orangered'
red_IIn_AGN = 'maroon'

#purple_SN = 'violet'

labels_1 = 'II','Ia','Ibc','I'
sizes_1 = [II+II_P+II_pec+IIb+IIn+IIn_AGN, Ia+Ia_91bg_like+Ia_91T_like+Iax_02cx_like, Ib+Ibn+Ic+Ic_BL+Ibc, I]
colors_1 = [red_II, blue_Ia, blue_Ib, blue_I]
explode_1 = (0, 0, 0, 0)

labels_2 = 'Ia Normal','Ia 91bg like','Ia 91T like','Iax[02cx like]'
sizes_2 = [Ia, Ia_91bg_like, Ia_91T_like, Iax_02cx_like]
colors_2 = [blue_Ia, blue_Ia_91bg_like, blue_Ia_91T_like, blue_Iax_02cx_like]
explode_2 = (0, 0, 0, 0)

labels_3 = 'Ic','Ibc','Ib'
sizes_3 = [Ic+Ic_BL, Ibc, Ib+Ibn]
colors_3 = [blue_Ic, blue_Ibc, blue_Ib]
explode_3 = (0, 0, 0)

labels_4 = 'II P','II pec','IIb','IIn'
sizes_4 = [II_P, II_pec, IIb, IIn+IIn_AGN]
colors_4 = [red_II_P, red_II_pec, red_IIb, red_IIn]
explode_4 = (0, 0, 0, 0)


# Plot
plt.figure("Supernovae")
plt.subplots_adjust(hspace=0.7, wspace=0)

plt.subplot(141)
chart_1 = plt.pie(sizes_1, explode=explode_1, colors=colors_1, labels=labels_1, autopct='%.2f%%', shadow=False, labeldistance=0.5, pctdistance=1.5, startangle=90, counterclock=True)
plt.legend(chart_1[0], labels_1, loc='best')
plt.axis('equal')

plt.subplot(142)
chart_2 = plt.pie(sizes_2, explode=explode_2, colors=colors_2, labels=labels_2, autopct='%.2f%%', shadow=False, labeldistance=0.5, pctdistance=1.5, startangle=90, counterclock=True)
plt.legend(chart_2[0], labels_2, loc='best')
plt.axis('equal')

plt.subplot(143)
chart_3 = plt.pie(sizes_3, explode=explode_3, colors=colors_3, labels=labels_3, autopct='%.2f%%', shadow=False, labeldistance=0.5, pctdistance=1.5, startangle=90, counterclock=True)
plt.legend(chart_3[0], labels_3, loc='best')
plt.axis('equal')

plt.subplot(144)
chart_4 = plt.pie(sizes_4, explode=explode_4, colors=colors_4, labels=labels_4, autopct='%.2f%%', shadow=False, labeldistance=0.5, pctdistance=1.5, startangle=90, counterclock=True)
plt.legend(chart_4[0], labels_4, loc='best')
plt.axis('equal')


plt.savefig("SN_pie_chart_sans_unclassified.pdf")
#plt.tight_layout()
plt.show()
