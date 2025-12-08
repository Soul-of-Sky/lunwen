import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np

# Data provided by the user
categories = ['空闲', 'SQLite', 'OpenCV', 'YOLO', 'TinyLlama', '7zip']
p64 = [5.45, 93.68, 96.67, 28.0, 23.95, 94.31]
p256 = [13.69, 95.47, 98.48, 36.31, 37.03, 95.44]
p1024 = [37.65, 97.24, 99.41, 55.84, 61.53, 96.96]
p2048 = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0]

# Plotting the data
x = np.arange(len(categories))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots(figsize=(8, 3))
rects1 = ax.bar(x - 1.5 * width, p64, width, label='64 KB', hatch='///', edgecolor='green', color='white')
rects2 = ax.bar(x - 0.5 * width, p256, width, label='256 KB', hatch='...', edgecolor='blue', color='white')
rects3 = ax.bar(x + 0.5 * width, p1024, width, label='1024 KB', hatch='xxxx', edgecolor='red', color='white')
rects4 = ax.bar(x + 1.5 * width, p2048, width, label='4096 KB', hatch='++', edgecolor='orange', color='white')

# Adding labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Compression Ratio (%)', fontname='Times New Roman', fontsize=20)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontname='Times New Roman', fontsize=20)

ax.tick_params(axis='y', which='both', labelsize=20, labelfontfamily='Times New Roman')

font_prop = font_manager.FontProperties(family='Times New Roman', size=14)
ax.legend(loc='upper center', prop=font_prop, frameon=False, ncol=4)

# Adjust the y-axis limits and ticks
# ax.locator_params(axis='y', nbins=6)
ax.set_yticks([0, 20, 40, 60, 80, 100])
plt.ylim(0, 125)

# Save the plot as a PDF file
plt.savefig('gran.pdf', format='pdf', bbox_inches='tight')
plt.show()