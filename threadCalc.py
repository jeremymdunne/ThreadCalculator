from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
QApplication, QMainWindow, QWidget, QComboBox, QVBoxLayout, QHBoxLayout,
QGridLayout, QLabel, QTabWidget)

from ThreadCalculator import *
from threaddatReader import *
from materialdatReader import *
from UI.BoltShearTensileAnalysisWidget import *



class ThreadCalcUI(QMainWindow):
    def __init__(self, thread_data, material_data):
        super().__init__()

        self.setWindowTitle("Thread Calc V0.1")
        self.setFixedSize(800,800)

        # main widget

        tab_widget = QTabWidget()
        self.BoltShearTensileAnalysis = BoltShearTensileAnalysisWidget(thread_data, material_data)
        tab_widget.addTab(self.BoltShearTensileAnalysis, "Bolt Shear and Tensile Analysis")

        self.setCentralWidget(tab_widget)


def sanitizeThreadData(thread_data):
    # collapse the data into an array of dicts
    # [{standard, hint, data:[{screw_size, pitch, external_classes, internal_classes}]}]
    data = []
    # print(thread_data)
    for f in thread_data:
        standard_data = {}
        standard_data['standard'] = f['standard']
        standard_data['hint'] = f['hint']
        standard_data['data'] = []
        for t in f['external_data']:
            if (len(standard_data['data']) > 0) and (standard_data['data'][-1]['screw_size'] == t['screw_size']):
                # append pitch, external_class
                if t['pitch'] not in standard_data['data'][-1]['pitch']:
                    standard_data['data'][-1]['pitch'].append(t['pitch'])
                if t['thread_class'] not in standard_data['data'][-1]['external_class']:
                    standard_data['data'][-1]['external_class'].append(t['thread_class'])
            # not contained, add
            else:
                standard_data['data'].append({'screw_size':t['screw_size'], 'pitch':[t['pitch']], 'external_class':[t['thread_class']], 'internal_class':[]})
        for t in f['internal_data']:
            # find the entry
            for e in standard_data['data']:
                if e['screw_size'] == t['screw_size']:
                    # append class
                    if t['thread_class'] not in e['internal_class']:
                        e['internal_class'].append(t['thread_class'])
        data.append(standard_data)
    return thread_data


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
    sanitizeThreadData(threads)
    return
    # print(threads)
    app = QApplication([])

    window = ThreadCalcUI(threads, materials)
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()
