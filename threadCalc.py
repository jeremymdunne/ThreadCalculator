from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
QApplication, QMainWindow, QWidget, QComboBox, QVBoxLayout, QHBoxLayout,
QGridLayout, QLabel, QTabWidget)

from ThreadCalculator import *
from threaddatReader import *
from materialdatReader import *
from UI.BoltAnalysisWidget import *
from UI.BoltedConnectionAnalysisWidget import *


class ThreadCalcUI(QMainWindow):
    def __init__(self, thread_data, material_data):
        super().__init__()

        self.setWindowTitle("Thread Calc V0.1")
        self.setFixedSize(800,900)

        # main widget

        tab_widget = QTabWidget()
        self.BoltShearTensileAnalysis = BoltAnalysisWidget(thread_data, material_data)
        self.BoltedConnectionAnalysis = BoltedConnectionAnalysisWidget(thread_data, material_data)
        tab_widget.addTab(self.BoltShearTensileAnalysis, "Bolt Shear and Tensile Analysis")
        tab_widget.addTab(self.BoltedConnectionAnalysis, "Bolted Connection Analysis")

        self.setCentralWidget(tab_widget)




def main():
    # read in the threads
    threadFiles = getThreadDataFiles()
    materialFiles = getMaterialdatFiles()
    materials = []
    for m in materialFiles:
        materials += readMaterialdat(m)
    threads = []
    for f in threadFiles:
        threads.append(readThreaddat(f))

    # print(threads)
    app = QApplication([])

    window = ThreadCalcUI(threads, materials)
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()
