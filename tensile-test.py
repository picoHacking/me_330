import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker

col_no = 4  # number of columns to read from data file

# Use this program for tensile test data .csv files from mtil website https://mtil.illinois.edu
# Modifications are required for use with other sorts of data


def csv_to_list(filename):
    # convert csv file to python list
    cols = []
    for c in range(col_no):
        cols.append([])
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            new_row = (','.join(row)).split(',')
            for c in range(len(row)):
                cols[c].append(new_row[c])
    return cols


def get_title(fn):
    # obtain heat treatment type
    title_elements = {"AN":"Annealed","NM":"Normalized","OQ":"Oil Quenched","WQ":"Water Quenched",
                      "T300C":"Tempered, 300$^\circ$C", "T550C":"Tempered, 550$^\circ$C"}
    title = csv_to_list(fn)[2][3][8:]
    for key in title_elements:
        if key in title:
            title = title_elements[key]
    return title


def get_ss(fn):
    # get stress and strain out of the data
    forces = csv_to_list(fn)[2][30:]
    forces = [float(i) for i in forces]
    strains = csv_to_list(fn)[3][5:]
    strains = [float(i) for i in strains]

    while forces[-1] < 20:
        forces.remove(forces[-1])
        strains.remove(strains[-1])

    min_strain = np.min(strains)
    #print(min_strain)

    if min_strain < -0.002:
        strains = [i-np.min(strains) for i in strains]

    stresses = []
    #print(forces)
    area = 0.25*np.pi*((float(csv_to_list(fn)[2][14]))**2)
    for force in forces:
        stresses.append(1000*force/area)

    return stresses, strains


def set_up_plot(folder_name, legend=True, xticks=10):
    # generate subplot with serif font
    font = {"family": "serif", "size": 12}
    fig = plt.figure(figsize=(10, 4))
    ax = fig.add_subplot()
    x_ticks = ticker.MaxNLocator(xticks)
    stress2, strain2 = get_ss('tensile_data/M01C4340AN_1.csv')
    x = np.linspace(0.002, 0.01, 100)
    y = offset_yield(x, approx_e(stress2, strain2))
    ax.plot(x,y)

    for f_name in os.listdir(folder_name):
        f_name = folder_name + "/" + f_name
        stress = get_ss(f_name)[0]
        strain = get_ss(f_name)[1]
        ax.plot(strain, stress, label=get_title(f_name))
        print(max(stress), f_name)
        offset_yield_strength = 0

        # Finding 0.2% offset yield (there might be a faster way to do this).
        for s in range(len(strain)):
            if strain[s] < 0.25:
                for i in x:
                    if abs(strain[s]-i)/strain[s] < 0.001:
                        offset_yield_strength = round(stress[s], 1)
                        break

        #print('0.2% offset yield strength', offset_yield_strength, 'MPa', f_name)
        print(offset_yield_strength)


        #print(approx_e(stress,strain), "MPa", f_name)
        ax.xaxis.set_major_locator(x_ticks)

    if legend:
        ax.legend(bbox_to_anchor=(1.1, 1.1), facecolor='white', framealpha=1, prop={'family': 'serif'})
    ax.set_xlabel("Strain (mm/mm)", fontdict=font)
    ax.set_ylabel("Stress (MPa)", fontdict=font)
    for tick in ax.get_xticklabels():
        tick.set_fontname("DejaVu Serif")
    for tick in ax.get_yticklabels():
        tick.set_fontname("DejaVu Serif")
    return ax


def get_hardness(fn):
    # convert Rockwell B to Brinell
    hardness = float(csv_to_list(fn)[2][16])
    bhn = 33.22*np.exp(0.0192*hardness)

    #print(get_title(fn), "\n", hardness, "HRB", "\n", bhn, "BHN")


def approx_e(stresses, strains, max_stress=500):
    # approximate elasticity modulus
    x = 1
    y = 1
    for i in range(len(stresses)):
        if stresses[i] > max_stress:
            y = stresses[i]
            x = strains[i]
            break
    #print(y/x)
    return y/x


def offset_yield(x, e, offset=0.002):
    # function used for plotting offset yield line
    return e*(x-offset)


def offset_yield_plot(fn='tensile_data/M01C4340AN_1.csv'):
    # create 0.2% offset line with slope equal to modulus of elasticity of annealed steel (about the same as the rest)
    stress2, strain2 = get_ss(fn)
    x = np.linspace(0.002, 0.01, 10)
    y = offset_yield(x, approx_e(stress2, strain2))
    print(x, y)
    return x, y


# runs hardness function on the data in "tensile_data"
for fname in os.listdir("tensile_data"):
    fname = "tensile_data" + "/" + fname
    get_hardness(fname)


# running and debugging
#print(get_ss('tensile_data/M01A4340AN_1.csv'))
plot = set_up_plot("tensile_data")
#plot = set_up_plot("tensile_data2", legend=False)

plt.grid(color='lightgray')
#plt.xlim(-0.01,0.2)
plt.show()


