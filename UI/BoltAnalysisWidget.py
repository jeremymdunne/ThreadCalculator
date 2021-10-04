"""
Second attempt at a widget

"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QComboBox, QPushButton, QGridLayout, QHBoxLayout,
    QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QErrorMessage, QCheckBox
)
from PyQt5.QtGui import QPixmap, QDoubleValidator

from UI.UnitLabel import UnitLabel

from ThreadCalculator import *

class BoltAnalysisWidget(QWidget):

    """!    class constructor
    @param self object pointer
    @param thread_data array of dicts containing:
        standard : str
        hint : str
        external_data : array of dicts containing:
            screw_size : float
            pitch : float. Note: for english standard, this is actually tpi
            thread_class : str
            basic_diameter : float
            max_major_diameter : float
            min_major_diameter : float
            max_pitch_diameter : float
            min_pitch_diameter : float
            max_minor_diameter : float
        internal_data : array of dicts containing:
            screw_size : float
            pitch : float. Note: for english standard, this is actually tpi
            thread_class : str
            basic_diameter : float
            min_minor_diameter : float
            max_minor_diameter : float
            min_pitch_diameter : float
            max_pitch_diameter : float
            max_major_diameter : float
    @ param material_data array of dicts containing:
            material_name : str
            yield_strength : float
            tensile_strength : float
    """
    def __init__(self, thread_data, material_data):
        super().__init__()

        # extract naming & identification data from thread_data and material_data
        self.thread_data = thread_data
        self.thread_naming_data = self.parseThreadNamingData(self.thread_data)
        self.material_data = material_data
        self.material_naming_data = []
        for m in self.material_data:
            self.material_naming_data.append(m['material_name'])

        # init ui
        self.initUI()


    ### UI functions


    """!    init the UI elements
    @param self object pointer
    """
    def initUI(self):
        # main layout is a H Box layout with nested V Boxes
        # don't ask why its not just a grid
        top_level_layout = QHBoxLayout()
        self.setLayout(top_level_layout)
        # left pane will include selection, geometry, material data
        left_pane_layout = QVBoxLayout()
        # right pane will include calculated values, image, and possible equation data
        right_pane_layout = QVBoxLayout()

        # left pane inits
        self.selection_widget = self.initSelectionWidget()
        left_pane_layout.addWidget(self.selection_widget)
        self.geometry_widget = self.initGeometryMaterialWidget()
        left_pane_layout.addWidget(self.geometry_widget)
        left_pane_layout.addStretch()

        # right pane
        self.calculation_widget = self.initCalculationWidget()
        right_pane_layout.addWidget(self.calculation_widget)

        self.image_widget = self.initImageWidget()
        right_pane_layout.addWidget(self.image_widget)
        right_pane_layout.addStretch()

        # add to the main
        top_level_layout.addLayout(left_pane_layout)
        top_level_layout.addLayout(right_pane_layout)
        self.populateStandardOptions()
        self.populateMaterialOptions()




    """!    init the selection widget
    """
    def initSelectionWidget(self):
        # main layout is a QGroupBox
        selection_groupbox = QGroupBox("Thread and Material Selection")
        # form layout seems visibly clean for this
        selection_layout = QVBoxLayout()
        selection_groupbox.setLayout(selection_layout)
        # bolt selection (external)
        external_selection_groupbox = QGroupBox("External Thread Selection (Required)")
        external_selection_layout = QFormLayout()
        external_selection_groupbox.setLayout(external_selection_layout)
        selection_layout.addWidget(external_selection_groupbox)
        # members
        self.thread_standard_combo = QComboBox()
        self.external_thread_size_combo = QComboBox()
        self.external_thread_pitch_combo = QComboBox()
        self.external_thread_class_combo = QComboBox()
        self.external_thread_material_combo = QComboBox()
        # add members
        external_selection_layout.addRow(QLabel("Standard"),self.thread_standard_combo)
        external_selection_layout.addRow(QLabel("Screw Size"),self.external_thread_size_combo)
        external_selection_layout.addRow(QLabel("Screw Pitch (or TPI)"),self.external_thread_pitch_combo) # note, need to figure this one out...
        external_selection_layout.addRow(QLabel("Screw Thread Class"),self.external_thread_class_combo)
        external_selection_layout.addRow(QLabel("Screw Material"),self.external_thread_material_combo)

        # internal selection
        internal_selection_groupbox = QGroupBox("Internal Thread Selection (Optional)")
        internal_selection_layout = QFormLayout()
        internal_selection_groupbox.setLayout(internal_selection_layout)
        selection_layout.addWidget(internal_selection_groupbox)
        # members
        self.engagement_length_line_edit = QLineEdit()
        self.engagement_length_line_edit.setValidator(QDoubleValidator())
        self.internal_thread_class_combo = QComboBox()
        self.internal_thread_material_combo = QComboBox()
        self.adjust_thread_engagement_length = QCheckBox('Remove 2 Threads From Engagement Length')
        self.adjust_thread_engagement_length.setChecked(True)

        # add members
        internal_selection_layout.addRow(QLabel("Internal Thread Class"),self.internal_thread_class_combo)
        internal_selection_layout.addRow(QLabel("Internal Thread Material"),self.internal_thread_material_combo)
        internal_selection_layout.addRow(QLabel("Thread Engagement"),self.engagement_length_line_edit)
        internal_selection_layout.addRow(self.adjust_thread_engagement_length)


        self.calculate_button = QPushButton("Calculate")
        selection_layout.addWidget(self.calculate_button)

        # signals
        self.calculate_button.clicked.connect(self.onCalculatePressed)
        self.thread_standard_combo.currentTextChanged.connect(self.onStandardChange)
        self.external_thread_size_combo.currentTextChanged.connect(self.onScrewSizeChange)

        return selection_groupbox



    """! init thread geometry and material widget
    """
    def initGeometryMaterialWidget(self):
        # main layout is a QGroupBox
        geometry_groupbox = QGroupBox("Thread Geometry and Material Data")
        geometry_layout = QVBoxLayout()
        geometry_groupbox.setLayout(geometry_layout)

        # external thread geometry
        external_thread_groupbox = QGroupBox("External Thread")
        external_thread_layout = QFormLayout()
        external_thread_groupbox.setLayout(external_thread_layout)
        geometry_layout.addWidget(external_thread_groupbox)
        # members
        self.external_thread_basic_diameter = UnitLabel(unit_label = 'in')
        self.external_thread_minor_diamter = UnitLabel(unit_label = 'in')
        self.external_thread_stress_area = UnitLabel(unit_label = 'in^2')
        self.external_thread_thread_area = UnitLabel(unit_label = 'in^2')
        self.used_engagement_length = UnitLabel(unit_label = 'in')
        self.external_thread_material_yield_strength = UnitLabel(unit_label = 'psi')
        self.external_thread_material_tensile_strength = UnitLabel(unit_label = 'psi')
        # add members
        external_thread_layout.addRow(QLabel("Screw Basic Diameter"), self.external_thread_basic_diameter)
        external_thread_layout.addRow(QLabel("Screw Minor Diameter"), self.external_thread_minor_diamter)
        external_thread_layout.addRow(QLabel("Screw Stress Area"), self.external_thread_stress_area)
        external_thread_layout.addRow(QLabel("Screw Thread Area"), self.external_thread_thread_area)
        external_thread_layout.addRow(QLabel("Engagement Length Used"),self.used_engagement_length)
        external_thread_layout.addRow(QLabel("Screw Material Yield Strength"), self.external_thread_material_yield_strength)
        external_thread_layout.addRow(QLabel("Screw Material Tensile Strength"), self.external_thread_material_tensile_strength)


        # internal thread geometry
        internal_thread_groupbox = QGroupBox("Internal Thread")
        internal_thread_layout = QFormLayout()
        internal_thread_groupbox.setLayout(internal_thread_layout)
        geometry_layout.addWidget(internal_thread_groupbox)
        # members
        self.internal_thread_major_diameter = UnitLabel(unit_label = 'in')
        self.internal_thread_minor_diameter = UnitLabel(unit_label = 'in')
        self.internal_thread_thread_area = UnitLabel(unit_label = 'in^2')
        self.internal_thread_material_yield_strength = UnitLabel(unit_label = 'psi')
        self.internal_thread_material_tensile_strength = UnitLabel(unit_label = 'psi')
        # add members
        internal_thread_layout.addRow(QLabel("Internal Thread Major Diameter"), self.internal_thread_major_diameter)
        internal_thread_layout.addRow(QLabel("Internal Thread Minor Diameter"), self.internal_thread_minor_diameter)
        internal_thread_layout.addRow(QLabel("Internal Thread Area"), self.internal_thread_thread_area)
        internal_thread_layout.addRow(QLabel("Internal Thread Material Yield Strength"), self.internal_thread_material_yield_strength)
        internal_thread_layout.addRow(QLabel("Internal Thread Material Tensile Strength"), self.internal_thread_material_tensile_strength)

        return geometry_groupbox

    """! init the calculation widget
    @param self object pointer
    """
    def initCalculationWidget(self):
        calculation_groupbox = QGroupBox("Calculations")
        calculation_layout = QVBoxLayout()
        calculation_groupbox.setLayout(calculation_layout)

        external_thread_groupbox = QGroupBox("External Thread Calculations")
        external_thread_layout = QFormLayout()
        external_thread_groupbox.setLayout(external_thread_layout)
        calculation_layout.addWidget(external_thread_groupbox)
        # members
        self.external_thread_shear_yield_strength = UnitLabel(unit_label = 'lb')
        self.external_thread_shear_tensile_strength = UnitLabel(unit_label = 'lb')
        self.external_thread_tensile_yield_strength = UnitLabel(unit_label = 'lb')
        self.external_thread_tensile_tensile_strength = UnitLabel(unit_label = 'lb')
        self.external_thread_thread_shear_yield_strength = UnitLabel(unit_label = 'lb')
        self.external_thread_thread_shear_tensile_strength = UnitLabel(unit_label = 'lb')
        # add
        external_thread_layout.addRow(QLabel('Shear Loading Yield Strength:'), self.external_thread_shear_yield_strength)
        external_thread_layout.addRow(QLabel('Shear Loading Tensile Strength:'), self.external_thread_shear_tensile_strength)
        external_thread_layout.addRow(QLabel('Tensile Loading Yield Strength:'), self.external_thread_tensile_yield_strength)
        external_thread_layout.addRow(QLabel('Tensile Loading Tensile Strength:'), self.external_thread_tensile_tensile_strength)
        external_thread_layout.addRow(QLabel('Tensile Loading Thread Shear Yield Strength:'), self.external_thread_thread_shear_yield_strength)
        external_thread_layout.addRow(QLabel('Tensile Loading Thread Shear Tensile Strength:'), self.external_thread_thread_shear_tensile_strength)

        internal_thread_groupbox = QGroupBox("Internal Thread Calculations")
        internal_thread_layout = QFormLayout()
        internal_thread_groupbox.setLayout(internal_thread_layout)
        calculation_layout.addWidget(internal_thread_groupbox)
        # members
        self.internal_thread_thread_shear_yield_strength = UnitLabel(unit_label = 'lb')
        self.internal_thread_thread_shear_tensile_strength = UnitLabel(unit_label = 'lb')
        # add
        internal_thread_layout.addRow(QLabel('Tensile Loading Thread Shear Yield Strength:'), self.internal_thread_thread_shear_yield_strength)
        internal_thread_layout.addRow(QLabel('Tensile Loading Thread Shear Tensile Strength:'), self.internal_thread_thread_shear_tensile_strength)

        summary_groupbox = QGroupBox("Calculation Summary")
        summary_layout = QFormLayout()
        summary_groupbox.setLayout(summary_layout)
        calculation_layout.addWidget(summary_groupbox)
        # members
        self.shear_loading_yield_strength = UnitLabel(unit_label = 'lb')
        self.shear_loading_tensile_strength = UnitLabel(unit_label = 'lb')
        self.tensile_loading_yield_strength = UnitLabel(unit_label = 'lb')
        self.tensile_loading_tensile_strength = UnitLabel(unit_label = 'lb')
        self.tensile_loading_limiting_label = QLabel('')
        # add
        summary_layout.addRow(QLabel('Shear Loading Yield Strength:'), self.shear_loading_yield_strength)
        summary_layout.addRow(QLabel('Shear Loading Tensile Strength:'), self.shear_loading_tensile_strength)
        summary_layout.addRow(QLabel('Tensile Loading Yield Strength:'), self.tensile_loading_yield_strength)
        summary_layout.addRow(QLabel('Tensile Loading Tensile Strength:'), self.tensile_loading_tensile_strength)
        summary_layout.addRow(QLabel('Tensile Loading Limiting Factor:'), self.tensile_loading_limiting_label)



        return calculation_groupbox


    def initImageWidget(self):
        label = QLabel()
        label.setPixmap(QPixmap('./UI/Bolt Loading Diagram.jpg'))
        label.setScaledContents(True)

        return label


    ### UI actions
    """! on standard change
    prompts for selection updates when a new standard is selected
    @param self object pointer
    """
    def onStandardChange(self):
        # update the screw size options
        standard = self.thread_standard_combo.currentText()
        self.external_thread_size_combo.clear()
        available_screw_sizes = []
        for s in self.thread_naming_data:
            if s['standard_hint'] == standard:
                for d in s['data']:
                    available_screw_sizes.append(d['screw_size'])
                self.external_thread_size_combo.addItems(available_screw_sizes)
                return available_screw_sizes

    """! on screw size change
    updates available internal & external options
    @param self object pointer
    """
    def onScrewSizeChange(self):
        standard = self.thread_standard_combo.currentText()
        size = self.external_thread_size_combo.currentText()
        # clear
        self.external_thread_class_combo.clear()
        self.external_thread_pitch_combo.clear()
        self.internal_thread_class_combo.clear()

        for s in self.thread_naming_data:
            if s['standard_hint'] == standard:
                for d in s['data']:
                    if d['screw_size'] == size:
                        self.external_thread_class_combo.addItems(d['external_thread_class'])
                        self.internal_thread_class_combo.addItems([''] + d['internal_thread_class'])
                        self.external_thread_pitch_combo.addItems(self.floatArrayToStringArray(d['pitch']))

    """! populate material options
    @param self object pointer
    """
    def populateMaterialOptions(self):
        self.external_thread_material_combo.addItems(self.material_naming_data)
        self.internal_thread_material_combo.addItem('')
        self.internal_thread_material_combo.addItems(self.material_naming_data)

    """! populate standard options
    @param self object pointer
    """
    def populateStandardOptions(self):
        options = []
        for s in self.thread_naming_data:
            options.append(s['standard_hint'])
        self.thread_standard_combo.addItems(options)

    """! handle calculate button press
    @param self object pointer
    """
    def onCalculatePressed(self):
        # first clear all calculations to prevent confusion
        self.clearValues()
        # first validate input
        if not self.validateExternalInput():
            msg = QErrorMessage()
            msg.showMessage('Not all inputs found')
            msg.exec_()
            return
            # cause an error message here
        using_internal_calcs = self.validateInternalInput()
        # run geometry calculations
        external_thread_data = self.getExternalThreadData(
            self.thread_standard_combo.currentText(),
            self.external_thread_size_combo.currentText(),
            self.external_thread_pitch_combo.currentText(),
            self.external_thread_class_combo.currentText())
        print(external_thread_data)
        external_material_data = self.getMaterialData(self.external_thread_material_combo.currentText())
        external_tensile_calcs = calcFailureThreadTensileForce(external_thread_data, external_material_data)
        external_shear_calcs = calcFailureThreadShearForce(external_thread_data, external_material_data)
        if using_internal_calcs:
            internal_thread_data = self.getInternalThreadData(
                self.thread_standard_combo.currentText(),
                self.external_thread_size_combo.currentText(),
                self.external_thread_pitch_combo.currentText(),
                self.internal_thread_class_combo.currentText())
            internal_material_data = self.getMaterialData(self.internal_thread_material_combo.currentText())
            engagement_length = float(self.engagement_length_line_edit.text())
            if self.adjust_thread_engagement_length.isChecked():
                engagement_length -= 2 * 1 / external_thread_data['pitch']
            self.used_engagement_length.setValue(engagement_length)
            internal_thread_calcs = calcFailureThreadEngagement(
                external_thread_data,
                external_material_data,
                internal_thread_data,
                internal_material_data,
                engagement_length)
        # geometry
        self.external_thread_basic_diameter.setValue(external_thread_data['basic_diameter'])
        self.external_thread_minor_diamter.setValue(external_thread_data['max_minor_diameter'])
        self.external_thread_stress_area.setValue(external_tensile_calcs['area'])
        self.external_thread_material_yield_strength.setValue(external_material_data['yield_strength'])
        self.external_thread_material_tensile_strength.setValue(external_material_data['tensile_strength'])

        if using_internal_calcs:
            self.external_thread_thread_area.setValue(internal_thread_calcs['internal_thread_area'])
            self.internal_thread_major_diameter.setValue(internal_thread_data['max_major_diameter'])
            self.internal_thread_minor_diameter.setValue(internal_thread_data['min_minor_diameter'])
            self.internal_thread_thread_area.setValue(internal_thread_calcs['internal_thread_area'])
            self.internal_thread_material_yield_strength.setValue(internal_material_data['yield_strength'])
            self.internal_thread_material_tensile_strength.setValue(internal_material_data['tensile_strength'])

        # populate calculations
        self.external_thread_shear_yield_strength.setValue(external_shear_calcs['yield_strength'])
        self.external_thread_shear_tensile_strength.setValue(external_shear_calcs['tensile_strength'])
        self.external_thread_tensile_yield_strength.setValue(external_tensile_calcs['yield_strength'])
        self.external_thread_tensile_tensile_strength.setValue(external_tensile_calcs['tensile_strength'])

        if using_internal_calcs:
            self.external_thread_thread_shear_yield_strength.setValue(internal_thread_calcs['external_yield_strength'])
            self.external_thread_thread_shear_tensile_strength.setValue(internal_thread_calcs['external_tensile_strength'])
            self.internal_thread_thread_shear_yield_strength.setValue(internal_thread_calcs['internal_yield_strength'])
            self.internal_thread_thread_shear_tensile_strength.setValue(internal_thread_calcs['internal_tensile_strength'])

        # extra logic
        self.shear_loading_yield_strength.setValue(external_shear_calcs['yield_strength'])
        self.shear_loading_tensile_strength.setValue(external_shear_calcs['tensile_strength'])

        if using_internal_calcs:
            if internal_thread_calcs['external_yield_strength'] > internal_thread_calcs['internal_yield_strength']:
                self.tensile_loading_yield_strength.setValue(internal_thread_calcs['internal_yield_strength'])
                self.tensile_loading_tensile_strength.setValue(internal_thread_calcs['internal_tensile_strength'])
                self.tensile_loading_limiting_label.setText("Internal Thread")
            else:
                self.tensile_loading_yield_strength.setValue(internal_thread_calcs['external_yield_strength'])
                self.tensile_loading_tensile_strength.setValue(internal_thread_calcs['external_yield_strength'])
                self.tensile_loading_limiting_label.setText("External Thread")

    """! validate input for internal calculations
    @param self object pointer
    @return boolean for if input is valid
    """
    def validateInternalInput(self):
        if self.internal_thread_class_combo.currentText() != '':
            if self.internal_thread_material_combo.currentText() != '':
                if self.engagement_length_line_edit.text() != '':
                    return True
        return False


    """! validate input for external calculations
    @param self object pointer
    @return boolean for if input is valid
    """
    def validateExternalInput(self):
        # as of now, all the external thread has default inputs
        return True

    """! clear all values
    clears all values in preperation for new calculations
    @param self object pointer
    """
    def clearValues(self):
        # geometry
        self.external_thread_basic_diameter.clearValue()
        self.external_thread_minor_diamter.clearValue()
        self.external_thread_stress_area.clearValue()
        self.external_thread_thread_area.clearValue()
        self.external_thread_material_yield_strength.clearValue()
        self.external_thread_material_tensile_strength.clearValue()
        self.internal_thread_major_diameter.clearValue()
        self.internal_thread_minor_diameter.clearValue()
        self.internal_thread_thread_area.clearValue()
        self.internal_thread_material_yield_strength.clearValue()
        self.internal_thread_material_tensile_strength.clearValue()
        self.used_engagement_length.clearValue()
        # calculations
        self.external_thread_shear_yield_strength.clearValue()
        self.external_thread_shear_tensile_strength.clearValue()
        self.external_thread_tensile_yield_strength.clearValue()
        self.external_thread_tensile_tensile_strength.clearValue()
        self.external_thread_thread_shear_yield_strength.clearValue()
        self.external_thread_thread_shear_tensile_strength.clearValue()

        self.internal_thread_thread_shear_yield_strength.clearValue()
        self.internal_thread_thread_shear_tensile_strength.clearValue()
        self.shear_loading_yield_strength.clearValue()
        self.shear_loading_tensile_strength.clearValue()
        self.tensile_loading_yield_strength.clearValue()
        self.tensile_loading_tensile_strength.clearValue()
        self.tensile_loading_limiting_label.setText('')


    ### helper functions

    """! float array to str array
    @param self object pointer
    @param floats array of floats
    @return array of str
    """
    def floatArrayToStringArray(self, floats):
        arr = []
        for f in floats:
            arr.append(str(f))
        return arr


    """! get external thread data
    returns the screw data from an identifier
    @param self object pointer
    @param standard : str screw standard
    @param screw_size : str screw size
    @param pitch : float screw pitch (or tpi in english)
    @param thread_class : str
    @return thread_data entry line (see constructor)
    """
    def getExternalThreadData(self, standard, screw_size, pitch, thread_class):
        for s in self.thread_data:
            if s['hint'] == standard:
                for t in s['external_data']:
                    if t['screw_size'] == screw_size:
                        if float(t['pitch']) == float(pitch):
                            if t['thread_class'] == thread_class:
                                return t


    """! get internal thread data
    returns the screw data from an identifier
    @param self object pointer
    @param standard : str screw standard
    @param screw_size : str screw size
    @param pitch : float screw pitch (or tpi in english)
    @param thread_class : str
    @return thread_data entry line (see constructor)
    """
    def getInternalThreadData(self, standard, screw_size, pitch, thread_class):
        for s in self.thread_data:
            if s['hint'] == standard:
                for t in s['internal_data']:
                    if t['screw_size'] == screw_size:
                        if float(t['pitch']) == float(pitch):
                            if t['thread_class'] == thread_class:
                                return t

    """! get material data
    returns the material data from an identifier
    @param self object pointer
    @param material_name : str material name (identifier)
    @return material_data entry (see constructor)
    """
    def getMaterialData(self, material_name):
        for m in self.material_data:
            if m['material_name'] == material_name:
                return m

    """!  parse thread data to get naming information
    @param self object pointer
    @param thread_data dict containing thread data to parse. See constructor for more information
    @return array of named dicts containing the following:
        standard_name : str
        standard_hint : str
        data : array of dicts containing
            screw_size : str
            pitch : array of floats. Note: in standard ('english') this is actually the tpi
            external_thread_class : array of str
            internal_thread_class : array of str
    """
    def parseThreadNamingData(self, thread_data):
        data = [] # return array
        for t in thread_data:
            standard_data = {} # data for this standard
            standard_data['standard_name']  = t['standard']
            standard_data['standard_hint'] = t['hint']
            standard_data['data'] = []
            for d in t['external_data']:
                # check if need to add new screw_size or just append thread_class
                if (len(standard_data['data']) > 0) and (standard_data['data'][-1]['screw_size'] == d['screw_size']):
                    if d['pitch'] not in standard_data['data'][-1]['pitch']:
                        standard_data['data'][-1]['pitch'].append(d['pitch'])
                    if d['thread_class'] not in standard_data['data'][-1]['external_thread_class']:
                        standard_data['data'][-1]['external_thread_class'].append(d['thread_class'])
                # not contained
                else:
                    standard_data['data'].append({
                        'screw_size':d['screw_size'],
                        'pitch':[d['pitch']],
                        'external_thread_class':[d['thread_class']],
                        'internal_thread_class':[]})
            # add internal thread class
            for d in t['internal_data']:
                for s in standard_data['data']:
                    if s['screw_size'] == d['screw_size']:
                        if d['thread_class'] not in s['internal_thread_class']:
                            s['internal_thread_class'].append(d['thread_class'])
                            break
            data.append(standard_data)
        return data
