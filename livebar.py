import matplotlib; matplotlib.use("MacOSX")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import csv

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):
    inputfile = open('tweetdata.csv')
    rows = csv.reader(inputfile)
    xs = ['blank']
    ys = []
    for row in rows:
        xs.append(row[0])
        ys.append(int(row[1]))
    y_pos = np.arange(0, len(xs)-1)
    ax1.bar(y_pos, ys, align='center')
    ax1.set_xticklabels(xs)
    plt.draw()


anim = animation.FuncAnimation(fig, animate, repeat=False, blit=False, interval=2000)
plt.show()
