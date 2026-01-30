import matplotlib.pyplot as plt
import numpy as np

# times measurement for the 3 versions, from protocol_figX.py
# {set_size : [pub_time, verify_time]} in millisecond
v1 = {100: [378, 948], 200: [757, 1901], 300: [1142, 2865], 400: [1527, 3829], 500: [1908, 4782]}
v2 = {100: [198, 303], 200: [394, 575], 300: [593, 897], 400: [794, 1139], 500: [990, 1394]}
v3 = {100: [594, 99], 200: [1181, 203], 300: [1788, 317], 400: [2366, 391], 500: [2949, 503]}

assert v1.keys() == v2.keys() == v3.keys()
x_labels = v1.keys()
x = np.arange(len(x_labels))

pub_times = [[v1[k][0]/1000, v2[k][0]/1000, v3[k][0]/1000] for k in x_labels]
verif_times = [[v1[k][1]/1000, v2[k][1]/1000, v3[k][1]/1000] for k in x_labels]

bar_width = 0.18
spacing = bar_width + 0.02
offsets = [-spacing, 0, spacing]

fig, ax = plt.subplots(figsize=(6, 5))

for i in range(3):
    positions = x + offsets[i]
    pub = [pub_times[j][i] for j in range(len(x))]
    ver = [verif_times[j][i] for j in range(len(x))]

    match i:
        case 0:
            ax.bar(positions, pub, width=bar_width, color='none', edgecolor='green', hatch='/////', label='V1 Publication')
            ax.bar(positions, ver, bottom=pub, width=bar_width, color='none', edgecolor='blue', hatch='/////', label='V1 Verifications')
        case 1:
            ax.bar(positions, pub, width=bar_width, color='none', edgecolor='green', hatch='oo', label='V2 Publication')
            ax.bar(positions, ver, bottom=pub, width=bar_width, color='none', edgecolor='blue', hatch='oo', label='V2 Verifications')
        case 2:
            ax.bar(positions, pub, width=bar_width, color='green', label='V3 Publication')
            ax.bar(positions, ver, bottom=pub, width=bar_width, color='blue', label='V3 Verifications')

ax.set_xticks(x, labels=x, fontsize=14)
ax.set_xticklabels(x_labels, fontsize=14)
ax.set_xlabel("Bob's set size", fontsize=18)
ax.set_ylabel("Time (s)", fontsize=18)
ax.legend(fontsize=13.5)

plt.tight_layout()
plt.grid(True, axis='y', linestyle='--', alpha=0.5)
plt.savefig("times_plot.png")
