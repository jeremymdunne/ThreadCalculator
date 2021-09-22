"""

"""


from PyQt5.QtWidgets import (
    QWidget, QLabel, QComboBox, QPushButton, QGridLayout, QHBoxLayout,
    QVBoxLayout, QGroupBox, QFormLayout, QLineEdit
)



class BoltShearTensileAnalysisWidget(QWidget):
    def __init__(self, thread_data, material_data):
        super().__init__()



        # variables
        self.thread_data = thread_data
        self.material_data = material_data

        self.organizeThreadData()
        self.organizeMaterialData()

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


        # lock the standard to english for now
        # print(thread_data[0])
        self.standard_combo.addItem(thread_data[0]['hint'])
        self.populateThreadSize()



    def populateThreadSize(self):
        # populate the thread size options
        choices = []
        for t in self.organized_thread_data[0]:
            choices.append(t['screw_size'])
        # print(choices)
        self.screw_size_combo.clear()
        self.screw_size_combo.addItems(choices)

    def onScrewSizeChange(self):
        # only show the available options
        size_index = self.screw_size_combo.currentIndex()

        # threads per inch
        self.threads_per_inch_combo.clear()
        possible_threads_per_inch = self.organized_thread_data[0][size_index]['possible_threads_per_inch']
        self.threads_per_inch_combo.addItems(self.floatArrayToStringArray(possible_threads_per_inch))

        # thread class
        self.external_thread_class_combo.clear()
        possible_thread_class = self.organized_thread_data[0][size_index]['possible_thread_class']
        self.external_thread_class_combo.addItems(self.floatArrayToStringArray(possible_thread_class))

        # material
        self.external_thread_material_combo.clear()
        self.external_thread_material_combo.addItems(self.material_names)

        # internal data
        # defaults to not selected
        self.internal_thread_class_combo.clear()
        possible_thread_class = self.organized_thread_data[0][size_index]['possible_thread_class']
        self.external_thread_class_combo.addItems(self.floatArrayToStringArray(possible_thread_class))

    def getThreadData(self, thread_size, thread_pitch, thread_class):
        # go through thread_data and return the dict with the appropriate data
        for t in thread_data:
            if t['screw_size'] == thread_size:
                if float(t['threads_per_inch']) == float(thread_pitch):
                    if t['thread_class'] == thread_class:
                        return t

    def floatArrayToStringArray(self, float):
        str_arr = []
        for f in float:
            str_arr.append(str(f))
        return str_arr


    def organizeMaterialData(self):
        self.material_names = []
        for m in self.material_data:
            self.material_names.append(m['material_name'])

    def organizeThreadData(self):
        # organize the thread data and sort by size & options
        # organize the thread data
        new_thread_data = []
        for set in self.thread_data:
            data = []
            #entry = {
            #    'screw_size':None, 'possible_threads_per_inch' : [], 'possible_thread_class' : []
            #}
            for d in set['external_data']:
                # check if a new entry is desired
                found = False
                for e in data:
                    if e['screw_size'] == d['screw_size']:
                        # add
                        if d['threads_per_inch'] not in e['possible_threads_per_inch']:
                            e['possible_threads_per_inch'].append(d['threads_per_inch'])
                        if d['thread_class'] not in e['possible_thread_class']:
                            e['possible_thread_class'].append(d['thread_class'])
                        found = True
                        break
                if not found:
                    entry = {}
                    entry['screw_size'] = d['screw_size']
                    entry['possible_threads_per_inch'] = [d['threads_per_inch']]
                    entry['possible_thread_class'] = [d['thread_class']]
                    data.append(entry)
            new_thread_data.append(data)
        self.organized_thread_data = new_thread_data
        # print(self.organized_thread_data)


    def initThreadMaterialSelection(self):
        # Thread Selection
        selection_groupbox = QGroupBox("Thread and Material Selection")

        # add a form layout
        selection_layout = QVBoxLayout()
        selection_groupbox.setLayout(selection_layout)

        self.standard_combo = QComboBox()
        #

        # extra form layout
        external_groupbox = QGroupBox("External Thread Selection (Required)")
        external_layout = QFormLayout()
        external_groupbox.setLayout(external_layout)

        # add to the form
        self.screw_size_combo = QComboBox()
        self.threads_per_inch_combo = QComboBox()
        self.external_thread_class_combo = QComboBox()
        self.external_thread_material_combo = QComboBox()


        self.calculate_button = QPushButton("Calculate")

        external_layout.addRow(QLabel("Standard:"),self.standard_combo)
        external_layout.addRow(QLabel("Screw Size:"),self.screw_size_combo)
        external_layout.addRow(QLabel("Threads per Inch:"),self.threads_per_inch_combo)
        external_layout.addRow(QLabel("External Thread Class:"),self.external_thread_class_combo)
        external_layout.addRow(QLabel("External Thread Material:"),self.external_thread_material_combo)

        # internal
        internal_groupbox = QGroupBox("Internal Thread Selection (Optional)")
        internal_layout = QFormLayout()
        internal_groupbox.setLayout(internal_layout)

        self.internal_thread_class_combo = QComboBox()
        self.internal_thread_material_combo = QComboBox()
        self.thread_engagement_length_input = QLineEdit()


        internal_layout.addRow(QLabel("Internal Thread Class:"),self.internal_thread_class_combo)

        internal_layout.addRow(QLabel("Internal Thread Material:"),self.internal_thread_material_combo)





        selection_layout.addWidget(external_groupbox)
        selection_layout.addWidget(internal_groupbox)
        selection_layout.addWidget(self.calculate_button)

        # connections
        self.screw_size_combo.currentTextChanged.connect(self.onScrewSizeChange)

        return selection_groupbox

    def initGeometryCalculationWidget(self):
        # geometry
        geometry_groupbox = QGroupBox("Geometry Data")
        # form layout
        geometry_layout = QVBoxLayout()
        geometry_groupbox.setLayout(geometry_layout)

        # external
        external_groupbox = QGroupBox("External Thread Data")
        external_layout = QFormLayout()
        external_groupbox.setLayout(external_layout)
        # add to the form
        self.screw_basic_diameter_label = QLabel("NaN")
        self.screw_minor_diameter_label = QLabel("NaN")
        self.internal_minor_diameter_label = QLabel("NaN")
        self.internal_maximum_pitch_diameter_label = QLabel("NaN")
        external_layout.addRow(QLabel("Screw Basic Diameter:"), self.screw_basic_diameter_label)
        external_layout.addRow(QLabel("Screw Minor Diameter:"), self.screw_minor_diameter_label)

        # internal
        internal_groupbox = QGroupBox("Internal Thread Data")
        internal_layout = QFormLayout()
        internal_groupbox.setLayout(internal_layout)

        # add to the form
        # todo

        geometry_layout.addWidget(external_groupbox)
        geometry_layout.addWidget(internal_groupbox)
        # geometry_layout.addRow()
        return geometry_groupbox

    def initMaterialDataWidget(self):
        material_groupbox = QGroupBox("Material Properties")
        material_layout = QVBoxLayout()
        material_groupbox.setLayout(material_layout)

        # external material
        external_groupbox = QGroupBox("External Material Properties")
        external_layout = QFormLayout()
        external_groupbox.setLayout(external_layout)

        self.external_material_yield_strength = QLabel("NaN")
        self.external_material_tensile_strength = QLabel("NaN")
        external_layout.addRow(QLabel("External Material Yield Strength:"),self.external_material_yield_strength)
        external_layout.addRow(QLabel("External Material Tensile Strength:"),self.external_material_tensile_strength)


        # internal material
        internal_groupbox = QGroupBox("Internal Material Properties")
        internal_layout = QFormLayout()
        internal_groupbox.setLayout(internal_layout)

        self.internal_material_yield_strength = QLabel("NaN")
        self.internal_material_tensile_strength = QLabel("NaN")
        internal_layout.addRow(QLabel("Internal Material Yield Strength:"),self.internal_material_yield_strength)
        internal_layout.addRow(QLabel("Internal Material Tensile Strength:"),self.internal_material_tensile_strength)

        material_layout.addWidget(external_groupbox)
        material_layout.addWidget(internal_groupbox)
        return material_groupbox

    def initCalculationWidget(self):
        # three sections
        # external calculations
        # internal calculations
        # summary (min)

        calculation_groupbox = QGroupBox("Force Calculations")
        calculation_layout = QVBoxLayout()
        calculation_groupbox.setLayout(calculation_layout)

        # external calculations
        external_groupbox = QGroupBox("External Thread Calculations")
        external_layout = QFormLayout()
        external_groupbox.setLayout(external_layout)

        self.external_thread_tensile_area = QLabel("NaN")
        self.external_thread_shear_area = QLabel("NaN")
        self.external_thread_shear_yield_strength = QLabel("NaN")
        self.external_thread_shear_ultimate_strength = QLabel("NaN")
        self.external_thread_tensile_yield_strength = QLabel("NaN")
        self.external_thread_tensile_ultimate_strength = QLabel("NaN")
        external_layout.addRow(QLabel("Thread Shear Area:"), self.external_thread_shear_area)
        external_layout.addRow(QLabel("Thread Shear Tensile:"), self.external_thread_shear_yield_strength)
        external_layout.addRow(QLabel("Thread Shear Ultimate:"), self.external_thread_shear_ultimate_strength)
        external_layout.addRow(QLabel("Thread Tensile Area:"), self.external_thread_tensile_area)
        external_layout.addRow(QLabel("Thread Tensile Yield:"), self.external_thread_tensile_yield_strength)
        external_layout.addRow(QLabel("Thread Tensile Ultimate:"), self.external_thread_tensile_ultimate_strength)



        # internal calculations
        internal_groupbox = QGroupBox("Internal Thread Calculations")
        internal_layout = QFormLayout()
        internal_groupbox.setLayout(internal_layout)

        self.internal_thread_shear_area = QLabel("NaN")


        # summary
        summary_groupbox = QGroupBox("Calculation Summary")
        summary_layout = QFormLayout()
        summary_groupbox.setLayout(summary_layout)


        calculation_layout.addWidget(external_groupbox)
        calculation_layout.addWidget(internal_groupbox)
        calculation_layout.addWidget(summary_groupbox)
        return calculation_groupbox

    def onCalculatePressed(self):
        pass
