"""

"""


from PyQt5.QtWidgets import (
    QWidget, QLabel, QComboBox, QPushButton, QGridLayout, QHBoxLayout,
    QVBoxLayout, QGroupBox, QFormLayout
)



class BoltShearTensileAnalysisWidget(QWidget):
    def __init__(self, thread_data, material_data):
        super().__init__()

        # variables
        self.thread_data = thread_data
        self.material_data = material_data

        # main layout
        h_layout = QHBoxLayout()
        self.setLayout(h_layout)

        #layout = QGridLayout()
        #self.setLayout(layout)
        left_layout = QVBoxLayout()
        # thread selection
        left_layout.addWidget(self.initThreadMaterialSelection())
        left_layout.addWidget(self.initGeometryCalculationWidget())
        left_layout.addWidget(self.initMaterialDataWidget())
        left_layout.addStretch()
        h_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.initCalculationWidget())
        right_layout.addStretch()
        h_layout.addLayout(right_layout)





    def initThreadMaterialSelection(self):
        # Thread Selection
        selection_groupbox = QGroupBox("Thread and Material Selection")

        # add a form layout
        selection_layout = QFormLayout()
        selection_groupbox.setLayout(selection_layout)
        # add to the form
        self.standard_combo = QComboBox()
        self.screw_size_combo = QComboBox()
        self.threads_per_inch_combo = QComboBox()
        self.thread_class_combo = QComboBox()
        self.thread_material_combo = QComboBox()
        self.calculate_button = QPushButton("Calculate")
        selection_layout.addRow(QLabel("Standard:"),self.standard_combo)
        selection_layout.addRow(QLabel("Screw Size:"),self.screw_size_combo)
        selection_layout.addRow(QLabel("Threads per Inch:"),self.threads_per_inch_combo)
        selection_layout.addRow(QLabel("Thread Class:"),self.thread_class_combo)
        selection_layout.addRow(QLabel("Thread Material:"),self.thread_material_combo)
        selection_layout.addRow(self.calculate_button)
        return selection_groupbox

    def initGeometryCalculationWidget(self):
        # geometry
        geometry_groupbox = QGroupBox("Geometry Calculations")
        # form layout
        geometry_layout = QFormLayout()
        geometry_groupbox.setLayout(geometry_layout)
        # add to the form
        self.basic_diameter_label = QLabel("NaN")
        self.minor_diameter_label = QLabel("NaN")
        self.tensile_area_label = QLabel("NaN")
        self.thread_shear_area_label = QLabel("NaN")
        geometry_layout.addRow(QLabel("Screw Basic Diameter:"), self.basic_diameter_label)
        geometry_layout.addRow(QLabel("Screw Minor Diameter:"), self.minor_diameter_label)
        geometry_layout.addRow(QLabel("Screw Tensile Area:"), self.tensile_area_label)
        geometry_layout.addRow(QLabel("Screw Thread Shear Area:"), self.thread_shear_area_label)
        return geometry_groupbox

    def initMaterialDataWidget(self):
        material_groupbox = QGroupBox("Material Properties")
        material_layout = QFormLayout()
        material_groupbox.setLayout(material_layout)
        self.material_yield_strength = QLabel("NaN")
        self.material_tensile_strength = QLabel("NaN")
        material_layout.addRow(QLabel("Material Yield Strength:"),self.material_yield_strength)
        material_layout.addRow(QLabel("Material Tensile Strength:"),self.material_tensile_strength)
        return material_groupbox

    def initCalculationWidget(self):
        calculation_groupbox = QGroupBox("Force Calculations")
        calculation_layout = QFormLayout()
        calculation_groupbox.setLayout(calculation_layout)
        self.thread_tensile_yield_strength = QLabel("NaN")
        self.thread_tensile_ultimate_strength = QLabel("NaN")
        self.thread_shear_yield_strength = QLabel("NaN")
        self.thread_shear_ultimate_strength = QLabel("NaN")
        calculation_layout.addRow(QLabel("Tensile Yield Strength:"),self.thread_tensile_yield_strength)
        calculation_layout.addRow(QLabel("Tensile Ultimate Strength:"),self.thread_tensile_ultimate_strength)
        calculation_layout.addRow(QLabel("Shear Yield Strength:"),self.thread_shear_yield_strength)
        calculation_layout.addRow(QLabel("Shear Ultimate Strength:"),self.thread_shear_ultimate_strength)
        return calculation_groupbox

    def onCalculatePressed(self):
        pass
