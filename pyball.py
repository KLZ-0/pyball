#!/usr/bin/python3

import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import random

class Window(QMainWindow):
    _msecdelay = 1

    def __init__(self):
        super(Window, self).__init__()
        self.app = app

        self.up = False
        self.down = False
        self.left = False
        self.right = False

        self.setupUi()
        # self.setupShortcuts()
        self.setTimers()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setGeometry(200, 200, 200, 120)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.main_scene = QGraphicsScene(self)

        self.ball = QGraphicsEllipseItem()
        self.ball.setRect(0, 0, 20, 20)
        pen = self.ball.pen()
        pen.setColor(QtGui.QColor("#ffffff"))
        self.ball.setPen(pen)
        brush = self.ball.brush()
        brush.setColor(QtGui.QColor("#ffffff"))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.ball.setBrush(brush)
        self.main_scene.addItem(self.ball)

        self.target = QGraphicsEllipseItem()
        self.target.setRect(0, 0, 50, 50)
        pen = self.target.pen()
        pen.setColor(QtGui.QColor("#00ff00"))
        self.target.setPen(pen)
        brush = self.target.brush()
        brush.setColor(QtGui.QColor("#00ff00"))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.target.setBrush(brush)
        self.main_scene.addItem(self.target)

        self.hits = 0
        self.hitCountItem = QGraphicsTextItem()
        self.hitCountItem.setPlainText("0")
        font = self.hitCountItem.font()
        font.setPixelSize(100)
        self.hitCountItem.setFont(font)
        self.main_scene.addItem(self.hitCountItem)

        self.main_view = QGraphicsView(self.main_scene, self)
        self.main_view.setRenderHint(QtGui.QPainter.Antialiasing)

        self.grabKeyboard()

    def setTimers(self):
        self.mainTimer = QtCore.QTimer()
        self.mainTimer.timeout.connect(self.moveBall)
        self.mainTimer.start(self._msecdelay)

    def moveBall(self):
        if self.up:
            self.ball.moveBy(0, -1)
        if self.down:
            self.ball.moveBy(0, 1)
        if self.left:
            self.ball.moveBy(-1, 0)
        if self.right:
            self.ball.moveBy(1, 0)
        if self.ball.x() > self.main_scene.width():
            self.ball.setPos(0, self.ball.y())
        if self.ball.y() > self.main_scene.height():
            self.ball.setPos(self.ball.x(), 0)
        if self.ball.x() < 0:
            self.ball.setPos(self.main_scene.width(), self.ball.y())
        if self.ball.y() < 0:
            self.ball.setPos(self.ball.x(), self.main_scene.height())

        ballPolygon = QtGui.QPolygonF(QtCore.QRectF(self.ball.pos().x(), self.ball.pos().y(), self.ball.rect().width(), self.ball.rect().height()))
        targetpolygon = QtGui.QPolygonF(QtCore.QRectF(self.target.pos().x(), self.target.pos().y(), self.target.rect().width(), self.target.rect().height()))
        if ballPolygon.intersects(targetpolygon):
            self.moveTarget()

        # if self.ball.pos() == self.target.pos():
        # if self.target.isVisibleTo(self.ball):
        #     self.moveTarget()


        return False

    def moveTarget(self):
            self.target.setPos(random.randrange(self.main_scene.width()), random.randrange(self.main_scene.height()))
            self.hits += 1
            self.hitCountItem.setPlainText(str(self.hits))

    def keyPressEvent(self, event):
        if not self.mainTimer.isActive(): self.mainTimer.start()

        key = event.text()
        if "w" in key or event.key() == 16777235:
            self.up = True
        if "s" in key or event.key() == 16777237:
            self.down = True
        if "a" in key or event.key() == 16777234:
            self.left = True
        if "d" in key or event.key() == 16777236:
            self.right = True
        if "q" in key:
            self.app.exit()
        if "r" in key or event.key() == 32:
            self.ball.setPos(0, 0)

    def keyReleaseEvent(self, event):
        key = event.text()
        if "w" in key or event.key() == 16777235:
            self.up = False
        if "s" in key or event.key() == 16777237:
            self.down = False
        if "a" in key or event.key() == 16777234:
            self.left = False
        if "d" in key or event.key() == 16777236:
            self.right = False

        if not (self.up or self.down or self.left or self.right): self.mainTimer.stop()


    def resizeEvent(self, event):
        self.main_view.setGeometry(self.rect())
        self.main_scene.setSceneRect(QtCore.QRectF(self.main_view.contentsRect()))
        self.hitCountItem.setPos(self.main_scene.sceneRect().width()/2-self.hitCountItem.boundingRect().width()/2, self.main_scene.sceneRect().height()/2-self.hitCountItem.boundingRect().height()/2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
