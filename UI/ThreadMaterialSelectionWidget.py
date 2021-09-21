from PyQt5.QtWidgets import (
QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel)
from PyQt5.QtCore import pyqtSignal


class ThreadMaterialSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        # variables
        self.thread_material_options = {}

        # signals
        thread_size_change = pyqtSignal()
        # labels
        screw_size_label = QLabel("Screw Size:")
        threads_per_inch_label = QLabel("Threads per Inch:")
        external_thread_class_label = QLabel("External Thread Class:")
        external_material_label = QLabel("External Thread Material:")
        internal_material_label = QLabel("")

        # combo boxes
        self.screw_size_combo = QComboBox()
        self.threads_per_inch_combo = QComboBox()
        self.thread_class_combo = QComboBox()
        self.material_combo = QComboBox()

        # layout
        layout = QGridLayout()
        self.setLayout(layout)
        # labels
        layout.addWidget(screw_size_label, 0, 0)
        layout.addWidget(threads_per_inch_label, 0, 1)
        layout.addWidget(thread_class_label, 0, 2)
        layout.addWidget(material_label, 0, 3)
        layout.addWidget(self.screw_size_combo, 1,0)
        layout.addWidget(self.threads_per_inch_combo, 1, 1)
        layout.addWidget(self.thread_class_combo, 1, 2)
        layout.addWidget(self.material_combo, 1, 3)

        # signals
        self.screw_size_combo.currentTextChanged.connect(self.onThreadSizeChange)

    def onThreadSizeChange(self):
        print("hallo!")
        self.thread_size_change.emit()

    def getValues(self):
        dict = {}
        dict['screw_size'] = self.screw_size_combo.currentText()
        dict['threads_per_inch'] = self.threads_per_inch_combo.currentText()
        dict['thread_class'] = self.thread_class_combo.currentText()
        dict['material'] = self.material_combo.currentText()
        return dict

    # helper functions
    def setOptions(self, options):
        self.thread_material_options = options
        # spark an update


    def setScrewSizeOptions(self, options):
        # expect a list of unique sizes
        self.screw_size_combo.clear()
        self.screw_size_combo.addItems(options)

    def setThreadsPerInchOptions(self, options):
        # expect a list of tpis
        self.threads_per_inch_combo.clear()
        self.threads_per_inch_combo.addItems(options)

    def setThreadClassOptions(self, options):
        # expect a list of classes
        self.thread_class_combo.clear()
        self.thread_class_combo.addItems(options)
