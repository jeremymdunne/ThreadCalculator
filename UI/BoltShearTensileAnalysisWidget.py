"""

"""


from PyQt5.QtWidgets import (
    QWidget, QLabel, QComboBox, QPushButton, QGridLayout, QHBoxLayout,
    QVBoxLayout, QGroupBox, QFormLayout, QLineEdit
)

from PyQt5.QtGui import QPixmap
from ThreadCalculator import *


class BoltShearTensileAnalysisWidget(QWidget):
    def __init__(self, thread_data, material_data):
        super().__init__()



        # variables
        self.thread_data = thread_data # imported thread data
        self.legible_thread_data = self.sanitizeThreadData(self.thread_data) # thread data that is user selected
        self.material_data = material_data # import material data

        # self.organizeThreadData()
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
        image = self.initImage()
        right_layout.addWidget(image)
        right_layout.addStretch()
        h_layout.addLayout(right_layout)



        # lock the standard to english for now
        # print(thread_data[0])
        self.standard_combo.addItem(thread_data[0]['hint'])
        self.populateThreadSize()


    def sanitizeThreadData(self, thread_data):
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
        return data

    def populateThreadSize(self):
        # populate the thread size options
        choices = [' ']
        # print(self.legible_thread_data)
        standard_index = self.standard_combo.currentIndex()

        for t in self.legible_thread_data[standard_index]['data']:
            choices.append(t['screw_size'])
        # print(choices)
        self.screw_size_combo.clear()
        self.screw_size_combo.addItems(choices)

    def onStandardChange(self):
        # update the screw size, clear everything else
        self.populateThreadSize()


    def onScrewSizeChange(self):
        # only show the available options
        standard_index = self.standard_combo.currentIndex()
        size_index = self.screw_size_combo.currentIndex() - 1

        if self.screw_size_combo.currentText() != ' ':
            # threads per inch
            self.threads_per_inch_combo.clear()
            possible_threads_per_inch = self.legible_thread_data[standard_index]['data'][size_index]['pitch']
            self.threads_per_inch_combo.addItems(self.floatArrayToStringArray(possible_threads_per_inch))

            # thread class
            self.external_thread_class_combo.clear()
            possible_thread_class = self.legible_thread_data[standard_index]['data'][size_index]['external_class']
            self.external_thread_class_combo.addItems(self.floatArrayToStringArray(possible_thread_class))

            # material
            self.external_thread_material_combo.clear()
            self.external_thread_material_combo.addItems(self.material_names)

            # internal data
            # defaults to not selected
            self.internal_thread_class_combo.clear()
            possible_thread_class = self.legible_thread_data[standard_index]['data'][size_index]['internal_class']
            self.internal_thread_class_combo.addItem(' ') # blank option
            self.internal_thread_class_combo.addItems(self.floatArrayToStringArray(possible_thread_class))

            self.internal_thread_material_combo.clear()
            self.internal_thread_material_combo.addItem(' ') # blank option
            self.internal_thread_material_combo.addItems(self.material_names)
        else:
            # clear everything
            self.threads_per_inch_combo.clear()
            self.external_thread_class_combo.clear()
            self.external_thread_material_combo.clear()
            self.internal_thread_class_combo.clear()

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
        self.standard_combo.currentTextChanged.connect(self.onStandardChange)
        self.screw_size_combo.currentTextChanged.connect(self.onScrewSizeChange)
        self.calculate_button.clicked.connect(self.onCalculatePressed)

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
        calculation_layout.addWidget(external_groupbox)

        external_shear_groupbox = QGroupBox("Bolt Shear Loading")
        external_shear_layout = QFormLayout()
        external_shear_groupbox.setLayout(external_shear_layout)
        external_layout.addWidget(external_shear_groupbox)

        external_tensile_groupbox = QGroupBox("Bolt Tensile Loading")
        external_tensile_layout = QFormLayout()
        external_tensile_groupbox.setLayout(external_tensile_layout)
        external_layout.addWidget(external_tensile_groupbox)

        # internal calculations
        internal_groupbox = QGroupBox("Internal Thread Calculations")
        internal_layout = QFormLayout()
        internal_groupbox.setLayout(internal_layout)
        calculation_layout.addWidget(internal_groupbox)


        # quick note about naming
        """
                                      (bolt)
            tensile loading <--->   =======|||
                                        ^ shear loading





        """

        # external bolt, shear loading
        self.external_shear_loading_area = QLabel("NaN")
        self.external_shear_loading_yield = QLabel("NaN")
        self.external_shear_loading_ultimate = QLabel("NaN")

        # external bolt, tensile loading
        self.external_tensile_loading_area = QLabel("NaN")
        self.external_tensile_loading_yield = QLabel("NaN")
        self.external_tensile_loading_ultimate = QLabel("NaN")

        # internal, tensile loading
        self.external_tensile_loading_thread_shear_area = QLabel("NaN")
        self.external_tensile_loading_thread_shear_yield = QLabel("NaN")
        self.external_tensile_loading_thread_shear_ultimate = QLabel("NaN")
        self.internal_tensile_loading_thread_shear_area = QLabel("NaN")
        self.internal_tensile_loading_thread_shear_yield = QLabel("NaN")
        self.internal_tensile_loading_thread_shear_ultimate = QLabel("NaN")

        external_shear_layout.addRow(QLabel("Bolt Shear Loading Area:"), self.external_shear_loading_area)
        external_shear_layout.addRow(QLabel("Bolt Shear Loading Yield Strength:"), self.external_shear_loading_yield)
        external_shear_layout.addRow(QLabel("Bolt Shear Loading Ultimate Strength:"), self.external_shear_loading_ultimate)

        external_tensile_layout.addRow(QLabel("Bolt Tensile Loading Area: "), self.external_tensile_loading_area)
        external_tensile_layout.addRow(QLabel("Bolt Tensile Loading Yield Strength: "), self.external_tensile_loading_yield)
        external_tensile_layout.addRow(QLabel("Bolt Tensile Loading Ultimate Strength: "), self.external_tensile_loading_ultimate)

        external_tensile_layout.addRow(QLabel("Bolt Tensile Loading Thread Shear Area: "), self.external_tensile_loading_thread_shear_area)
        external_tensile_layout.addRow(QLabel("Bolt Tensile Loading Thread Shear Yield Strength: "), self.external_tensile_loading_thread_shear_yield)
        external_tensile_layout.addRow(QLabel("Bolt Tensile Loading Thread Shear Tensile Strength: "), self.external_tensile_loading_thread_shear_ultimate)

        internal_layout.addRow(QLabel("Internal Tensile Loading Thread Shear Area: "), self.internal_tensile_loading_thread_shear_area)
        internal_layout.addRow(QLabel("Internal Tensile Loading Thread Shear Yield Strength: "), self.internal_tensile_loading_thread_shear_yield)
        internal_layout.addRow(QLabel("Internal Tensile Loading Thread Shear Ultimate Strength: "), self.internal_tensile_loading_thread_shear_ultimate)


        # summary
        summary_groupbox = QGroupBox("Calculation Summary")
        summary_layout = QFormLayout()
        summary_groupbox.setLayout(summary_layout)



        calculation_layout.addWidget(summary_groupbox)
        return calculation_groupbox

    def initImage(self):
        # widget = QWidget()
        label = QLabel()
        pixmap = QPixmap('./UI/Loading Diagram.jpg')
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        return label



    def onCalculatePressed(self):
        # check that the required data is provided
        if self.screw_size_combo.currentIndex() == 0:
            print("error!")
            return
        if self.threads_per_inch_combo.currentText() == ' ':
            print("error!")
            return
        if self.external_thread_class_combo.currentText() == ' ':
            print("error!")
            return
        perform_internal_calcs = True
        if self.internal_thread_class_combo.currentText() == ' ':
            perform_internal_calcs = False
        elif self.internal_thread_material_combo.currentText() == ' ':
            perform_internal_calcs = False

        # calculations pass, populate information
        self.populateGeometery(perform_internal_calcs)
        self.populateMaterial(perform_internal_calcs)
        self.populateCalculate(perform_internal_calcs)


    def populateGeometery(self, perform_internal_calcs):
        pass

    def getMaterialProperties(self, material_name):
        dict = {}
        for i in self.material_data:
            if i['material_name'] == material_name:
                dict['yield_strength'] = i['yield_strength']
                dict['tensile_strength'] = i['tensile_strength']
                return dict

    def populateMaterial(self, perform_internal_calcs):
        print(self.external_thread_material_combo.currentText())
        material_name = self.external_thread_material_combo.currentText()
        external_material = self.getMaterialProperties(material_name)
        print(external_material['yield_strength'])
        self.external_material_yield_strength.setText(str(external_material['yield_strength']) + ' psi')
        self.external_material_tensile_strength.setText(str(external_material['tensile_strength']) + ' psi')
        if perform_internal_calcs:
            internal_material = self.getMaterialProperties(self.internal_thread_material_combo.currentText())
            self.internal_material_yield_strength.setText(str(external_material['yield_strength']) + ' psi')
            self.internal_material_tensile_strength.setText(str(external_material['tensile_strength']) + ' psi')
        else:
            self.internal_material_yield_strength.setText("N/A")
            self.internal_material_tensile_strength.setText("N/A")


    def getExternalThreadData(self, thread_size, thread_pitch, thread_class):
        # go through thread_data and return the dict with the appropriate data
        standard_index = self.standard_combo.currentIndex()
        for t in self.thread_data[standard_index]['external_data']:
            if t['screw_size'] == thread_size:
                if float(t['pitch']) == float(thread_pitch):
                    if t['thread_class'] == thread_class:
                        return t



    def populateCalculate(self, perform_internal_calcs):
        # get the thread data

        # run area calcs
        external_thread = self.getExternalThreadData(self.screw_size_combo.currentText(), self.threads_per_inch_combo.currentText(), self.external_thread_class_combo.currentText())
        cross_area = calcThreadTensileArea(external_thread)
        print(cross_area)
