import cairo

from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg

from . import Constants
from .components.canvas.colors import FLOWGRAPH_BACKGROUND_COLOR

def get_rotated_coordinate(coor, rotation):
    """
    Rotate the coordinate by the given rotation.
    Args:
        coor: the coordinate x, y tuple
        rotation: the angle in degrees
    Returns:
        the rotated coordinates
    """
    # handles negative angles
    rotation = (rotation + 360) % 360
    if rotation not in Constants.POSSIBLE_ROTATIONS:
        raise ValueError('unusable rotation angle "%s"'%str(rotation))
    # determine the number of degrees to rotate
    cos_r, sin_r = {
        0: (1, 0), 90: (0, 1), 180: (-1, 0), 270: (0, -1),
    }[rotation]
    x, y = coor
    return x * cos_r + y * sin_r, -x * sin_r + y * cos_r

def make_screenshot(fg_view, file_path, transparent_bg=False):
    if not file_path:
        return
    if file_path.endswith(".png"):
        rect = fg_view.viewport().rect()

        pixmap = QtGui.QPixmap(rect.size())
        painter = QtGui.QPainter(pixmap)

        fg_view.render(painter, QtCore.QRectF(pixmap.rect()), rect)
        pixmap.save(file_path,"PNG")
        painter.end()
    elif file_path.endswith(".svg"):
        rect = fg_view.viewport().rect()

        generator = QtSvg.QSvgGenerator()
        generator.setFileName(file_path)
        generator.setSize(rect.size())
        painter = QtGui.QPainter(generator)
        fg_view.render(painter)
        painter.end()
    elif file_path.endswith(".pdf"):
        return # TODO