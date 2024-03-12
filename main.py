import math
import statistics
cols = 6
rows = 13
data = open("hardness_data_1.txt").read()
fill = []
table = []
row = []
column = []

results = {"means": 0, "standard deviations": 0}
broken = data.split(" ")
for character in broken:
    if character != ' ':
        try:
            fill.append(float(character))
        except ValueError:
            continue


for j in range(cols):
    column = []
    for i in range(len(fill)):
        if i % cols == 0:
            if fill[i+j] != 0:
                column.append(fill[i+j])
    table.append(column)
data = table

means = []
sds = []
medians = []
for k in range(len(table)):
    c = table[k]
    some = 0
    num = 0
    for i in c:
        some += i
    means.append(some / len(c))
    for i in range(len(c)):
        num += (c[i]-means[k])**2
    sds.append(math.sqrt(num/len(c)))
    medians.append(statistics.median(c))
results["means"] = means
results["standard deviations"] = sds
results["medians"] = medians


print(results)
