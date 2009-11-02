import plugin
from util import prepare_for_display, window_manager, GuiLockError

import numpy as np
import sys


try:
    # We try to aquire the gui lock first or else the gui import might
    # trample another GUI's PyOS_InputHook.
    window_manager.acquire('qt')

except GuiLockError, gle:
    print gle

else:
    try:
        from PyQt4.QtGui import (QApplication, QMainWindow, QImage, QPixmap,
                                 QLabel)

    except ImportError:
        print 'PyQT4 libraries not installed.  Plugin not loaded.'
        window_manager._release('qt')

    else:

        app = None

        class ImageWindow(QMainWindow):
            def __init__(self, arr, mgr):
                QMainWindow.__init__(self)
                self.mgr = mgr
                img = QImage(arr.data, arr.shape[1], arr.shape[0],
                             QImage.Format_RGB888)
                pm = QPixmap.fromImage(img)

                label = QLabel()
                label.setPixmap(pm)
                label.show()

                self.label = label
                self.setCentralWidget(self.label)
                self.mgr.add_window(self)

            def closeEvent(self, event):
                # Allow window to be destroyed by removing any
                # references to it
                self.mgr.remove_window(self)

        def qt_imshow(arr):
            global app

            if not app:
                app = QApplication([])

            arr = prepare_for_display(arr)

            iw = ImageWindow(arr, window_manager)
            iw.show()

        def qt_show():
            global app
            if app and window_manager.has_windows():
                app.exec_()
            else:
                print 'No images to show.  See `imshow`.'

        plugin.register('qt', show=qt_imshow, appshow=qt_show)
