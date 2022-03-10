import numpy as np
from PyQt6.QtCore    import Qt
from PyQt6.QtGui     import QPainter, QPen, QPixmap, QColor, QImage, QCursor
from PyQt6.QtWidgets import QLabel

# vtag imports
from .colors        import colorsets
from .utils         import drawCross

class VTFrame(QLabel):
    '''
    display centroids and contour
    '''

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.image = None

        # mouse moving events
        self.mx = -1
        self.my = -1

        # plotted labels
        self.labels = None
        # idx which label is assgined
        self.idx_lbs = 0
        # user options
        self.alpha       = 200   # opacity of the annotation
        self.show_lbs    = False # whether to show labels (centroids)
        self.show_motion = True  # whether to show motion (contour)

    def set_labels(self, labels):
        """
        should be vtag.DATA["track"][i]
        """
        self.labels = labels

    def set_image(self, image):
        """
        parameters
        ---
        image: numpy 3D-array for the RGB image (w, h, c)
        """
        try:
            self.image = getGrayQImg(image)
        except Exception as e:
            print(e)
            self.image = None

    def set_predict(self, img):
        self.img_detect = getIdx8QImg(img,  int(np.max(img)), alpha=self.alpha)

    def set_label(self, lb_x, lb_y):
        self.lb_x, self.lb_y = lb_x, lb_y

    def paintEvent(self, event):
        super().paintEvent(event)
        # open painter
        painter = QPainter(self)

        # ---draw background image
        if self.image is not None:
            self.setPixmap(self.image)

        # ---draw labels
        if self.show_lbs:
            draw_labels(self.labels, painter)

        # close painter
        painter.end()

        # cursor
        cursor = get_QCursor(self.idx_lbs)
        self.setCursor(cursor)

    def mouseMoveEvent(self, evt):
        pt = evt.position().toPoint()
        self.mx, self.my = pt.x(), pt.y()


def get_QCursor(i, size=15):
    # create transparent background
    img_cur = QPixmap(size * 2, size * 2)
    img_cur.fill(QColor(0, 0, 0, 0))
    # create painter
    paint_cur = QPainter(img_cur)
    paint_cur.drawPixmap(0, 0, img_cur)
    # create pen
    pen = QPen()
    pen.setStyle(Qt.PenStyle.SolidLine)
    # ---border (black)
    pen.setWidth(10)
    pen.setColor(colorsets[0])
    paint_cur.setPen(pen)
    drawCross(size, size, paint_cur, size=6)
    # ---filled (color)
    pen.setWidth(8)
    pen.setColor(colorsets[i + 1])
    paint_cur.setPen(pen)
    drawCross(size, size, paint_cur, size=6)
    # close painter
    paint_cur.end()
    # return
    return QCursor(img_cur)

def draw_labels(labels, painter):
    pen = QPen()
    pen.setStyle(Qt.PenStyle.SolidLine)
    for i, (x, y) in enumerate(labels):
        # border (black)
        pen.setWidth(10)
        pen.setColor(colorsets[0])
        painter.setPen(pen)
        drawCross(x, y, painter, size=6)
        # filled (color)
        pen.setWidth(8)
        pen.setColor(colorsets[i + 1])
        painter.setPen(pen)
        drawCross(x, y, painter, size=6)

def getRGBQImg(img):
    h, w = img.shape[0], img.shape[1]
    qImg = QImage(img.astype(np.uint8).copy(), w, h, w*3, QImage.Format.Format_RGB888)
    return QPixmap(qImg)

def getBinQImg(img):
    h, w = img.shape[0], img.shape[1]
    qImg = QImage(img.astype(np.uint8).copy(), w,
                  h, w*1, QImage.Format.Format_Indexed8)
    qImg.setColor(0, colorsets[0])
    qImg.setColor(1, colorsets[1])
    return QPixmap(qImg)

def getIdx8QImg(img, k, alpha=200):  # k=20
    h, w = img.shape[0], img.shape[1]
    qImg = QImage(img.astype(np.uint8).copy(), w,
                  h, w*1, QImage.Format.Format_Indexed8)
    nc = len(colorsets) - 1  # exclude 0: background color
    # background color
    qImg.setColor(0, QColor(0, 0, 0, alpha).rgba())
    # cluster color
    for i in range(k):
        # use '%' to iterate the colormap
        qImg.setColor(i + 1, colorsets[(i % nc) + 1].rgba())
    return QPixmap(qImg)

def getGrayQImg(img):
    h, w = img.shape[0], img.shape[1]
    qImg = QImage(img.astype(np.uint8).copy(), w,
                  h, w*1, QImage.Format.Format_Grayscale8)
    return QPixmap(qImg)
