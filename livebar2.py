import matplotlib; matplotlib.use("MacOSX")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import numpy as np
import csv

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):
    inputfile = open('tweetdata2.csv')
    rows = csv.reader(inputfile)
    xs = ['blank']
    ys1 = []  # positive
    ys2 = []  # neutral
    ys3 = []  # negative
    bar_width = 0.85
    next(rows)
    for row in rows:
        xs.append(row[0])
        if int(row[4]):
            ys1.append(int(row[1])*100/int(row[4]))
            ys2.append(int(row[2])*100/int(row[4]))
            ys3.append(int(row[3])*100/int(row[4]))
        else:
            ys1.append(0)
            ys2.append(0)
            ys3.append(0)

    ax1.clear()
    y_pos = np.arange(0, len(xs)-1)
    ax1.bar(y_pos, ys1, color='#b5ffb9', label='positive', edgecolor='white', width=bar_width)
    ax1.bar(y_pos, ys2, bottom=ys1, color='#f9bc86', label='neutral', edgecolor='white', width=bar_width)
    ax1.bar(y_pos, ys3, bottom=[i+j for i, j in zip(ys1, ys2)], color='#a3acff', label='negative', edgecolor='white', width=bar_width)
    ax1.set_xticklabels(xs)
    pos = mpatches.Patch(color='#b5ffb9', label='Positive')
    neu = mpatches.Patch(color='#f9bc86', label='Neutral')
    neg = mpatches.Patch(color='#a3acff', label='Negative')
    plt.legend(handles=[pos, neu, neg])
    plt.draw()


anim = animation.FuncAnimation(fig, animate, repeat=False, blit=False, interval=2000)
plt.show()
