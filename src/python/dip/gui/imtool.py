import sys
import numpy as np

from PySide2 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
import cv2


if __name__ == "__main__":

    target_image = sys.argv[1]

    app = QtWidgets.QApplication(sys.argv)
    wid = QtWidgets.QWidget()
    wid.resize(250, 150)
    grid = QtWidgets.QVBoxLayout(wid)
    fig = Figure(figsize=(7, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
    gs = fig.add_gridspec(1, 1)
    ax = fig.add_subplot(gs[0, 0])
    # d = np.array([[i+j for i in range(-5, 6)] for j in range(-5, 6)])
    d = cv2.imread(target_image)
    im = ax.imshow(d[:,:,[2,1,0]])

    canvas = FigureCanvas(fig)
    toolbar = NavigationToolbar(canvas, None)
    grid.addWidget(canvas)
    grid.addWidget(toolbar)

    # Mouse tooltip
    from PySide2 import QtGui, QtCore, QtWidgets
    mouse_tooltip = QtWidgets.QLabel()
    mouse_tooltip.setFrameShape(QtWidgets.QFrame.StyledPanel)
    mouse_tooltip.setWindowFlags(QtCore.Qt.ToolTip)
    mouse_tooltip.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
    mouse_tooltip.show()

    def show_tooltip(msg):
        msg = msg.replace(', ', '\n')
        mouse_tooltip.setText(msg)

        pos = QtGui.QCursor.pos()
        mouse_tooltip.move(pos.x() + 20, pos.y() + 15)
        mouse_tooltip.adjustSize()
    toolbar.message.connect(show_tooltip)

    wid.show()
    sys.exit(app.exec_())

# import matplotlib
# matplotlib.use("Qt4Agg")
# matplotlib.rcParams["backend.qt4"] = "PySide"




# fig, ax = plt.subplots()

# d = np.array([[i+j for i in range(-5, 6)] for j in range(-5, 6)])
# im = ax.imshow(d)
# im.set_extent((-5, 5, -5, 5))

# def format_coord(x, y):
#     """Format the x and y string display."""
#     imgs = ax.get_images()
#     if len(imgs) > 0:
#         for img in imgs:
#             try:
#                 array = img.get_array()
#                 extent = img.get_extent()

#                 # Get the x and y index spacing
#                 x_space = np.linspace(extent[0], extent[1], array.shape[1])
#                 y_space = np.linspace(extent[3], extent[2], array.shape[0])

#                 # Find the closest index
#                 x_idx= (np.abs(x_space - x)).argmin()
#                 y_idx= (np.abs(y_space - y)).argmin()

#                 # Grab z
#                 z = array[y_idx, x_idx]
#                 return 'x={:1.4f}, y={:1.4f}, z={:1.4f}'.format(x, y, z)
#             except (TypeError, ValueError):
#                 pass
#         return 'x={:1.4f}, y={:1.4f}, z={:1.4f}'.format(x, y, 0)
#     return 'x={:1.4f}, y={:1.4f}'.format(x, y)
# # end format_coord

# ax.format_coord = format_coord

# fig, ax = plt.subplots()


# # Show the plot
# plt.show()
