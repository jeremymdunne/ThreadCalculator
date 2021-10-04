from PyQt5.QtWidgets import (
    QWidget, QLabel, QComboBox, QPushButton, QGridLayout, QHBoxLayout,
    QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QErrorMessage, QCheckBox
)
from PyQt5.QtGui import QPixmap, QDoubleValidator

from UI.UnitLabel import UnitLabel

from ThreadCalculator import *

class BoltedConnectionAnalysisWidget(QWidget):

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
        # setup
        self.thread_data = thread_data
        self.material_data = material_data
        self.thread_naming_data = self.parseThreadNamingData(self.thread_data)
        self.material_naming_data = []
        for m in self.material_data:
            self.material_naming_data.append(m['material_name'])

        ## init ui
        self.initUI()


    """! init the UI elements
    @param self object pointer
    """
    def initUI(self):
        # main format is a hbox layout
        layout = QHBoxLayout()
        self.setLayout(layout)
        # left & right pane
        left_pane_layout = QVBoxLayout()
        right_pane_layout = QVBoxLayout()

        # left pane inits
        self.selection_widget = self.initSelectionWidget()
        left_pane_layout.addWidget(self.selection_widget)
        self.geometry_widget = self.initGeometryMaterialWidget()
        left_pane_layout.addWidget(self.geometry_widget)
        self.deformation_widget = self.initDeformationWidget()
        left_pane_layout.addWidget(self.deformation_widget)
        self.tearout_widget = self.initTearOutWidget()
        left_pane_layout.addWidget(self.tearout_widget)
        left_pane_layout.addStretch()

        # right pane
        self.image_widget = self.initImageWidget()
        right_pane_layout.addWidget(self.image_widget)
        right_pane_layout.addStretch()

        layout.addLayout(left_pane_layout)
        layout.addLayout(right_pane_layout)

        self.populateThreadStandards()
        self.populateMaterialOptions()


    ### UI functions

    """! init the selection widget
    @param self object pointer
    """
    def initSelectionWidget(self):
        selection_groupbox = QGroupBox("Input Selection")

        selection_layout = QFormLayout()
        selection_groupbox.setLayout(selection_layout)

        # members
        self.thread_standard_combo = QComboBox()
        self.thread_size_combo = QComboBox()
        self.material_combo = QComboBox()
        self.material_thickness = QLineEdit()
        self.hole_offset = QLineEdit()
        self.calculate_button = QPushButton("Calculate")

        # add members
        selection_layout.addRow(QLabel('Thread Standard'), self.thread_standard_combo)
        selection_layout.addRow(QLabel('Screw Size'), self.thread_size_combo)
        selection_layout.addRow(QLabel('Plate Material'), self.material_combo)
        selection_layout.addRow(QLabel('Plate Thickness (T)'), self.material_thickness)
        selection_layout.addRow(QLabel('Hole Offset (A)'), self.hole_offset)
        selection_layout.addRow(self.calculate_button)

        # actions
        self.thread_standard_combo.currentTextChanged.connect(self.onStandardChange)
        self.calculate_button.clicked.connect(self.onCalculatePressed)



        return selection_groupbox

    def initGeometryMaterialWidget(self):
        geometry_groupbox = QGroupBox("Thread Geomerty and Material Data")
        geometry_layout = QFormLayout()
        geometry_groupbox.setLayout(geometry_layout)

        # members
        self.hole_diameter = UnitLabel(unit_label = 'in')
        self.hole_engagement_area = UnitLabel(unit_label = 'in^2')
        self.hole_tearout_area = UnitLabel(unit_label = 'in^2')
        self.material_yield_strength = UnitLabel(unit_label = 'psi')
        self.material_tensile_strength = UnitLabel(unit_label = 'psi')

        # add members
        geometry_layout.addRow(QLabel('Hole Diameter'), self.hole_diameter)
        geometry_layout.addRow(QLabel('Deformation Area'), self.hole_engagement_area)
        geometry_layout.addRow(QLabel('Tearout Area'), self.hole_tearout_area)
        geometry_layout.addRow(QLabel('Material Yield Strength'), self.material_yield_strength)
        geometry_layout.addRow(QLabel('Material Tensile Strength'), self.material_tensile_strength)



        return geometry_groupbox

    """! init the deformation widget
    @param self object pointer
    """
    def initDeformationWidget(self):
        deformation_groupbox = QGroupBox("Hole Deformation Calculations")
        deformation_layout = QFormLayout()
        deformation_groupbox.setLayout(deformation_layout)

        # members
        self.hole_deformation_yield_force = UnitLabel(unit_label = 'lb')
        self.hole_deformation_tensile_force = UnitLabel(unit_label = 'lb')

        # add members


        return deformation_groupbox

    """! init the tear out widget
    @param self object pointer
    """
    def initTearOutWidget(self):
        tearout_groupbox = QGroupBox("Hole Tearout Calculations")

        return tearout_groupbox

    """! init image widget
    @param self object pointer
    """
    def initImageWidget(self):
        widget = QWidget()
        widget_layout = QVBoxLayout()
        widget.setLayout(widget_layout)

        shear_loading = QLabel()
        shear_loading.setPixmap(QPixmap('./UI/Single Double Shear.jpg'))
        shear_loading.setScaledContents(True)
        widget_layout.addWidget(shear_loading)

        hole_failure = QLabel()
        hole_failure.setPixmap(QPixmap('./UI/Hole Deformation Tearout.jpg'))
        hole_failure.setScaledContents(True)
        widget_layout.addWidget(hole_failure)

        return widget


    ### UI Actions


    def onCalculatePressed(self):
        #
        pass

    """! on standard change
    prompts for selection updates when a new standard is selected
    @param self object pointer
    """
    def onStandardChange(self):
        # update the screw size options
        standard = self.thread_standard_combo.currentText()
        self.thread_size_combo.clear()
        available_screw_sizes = []
        for s in self.thread_naming_data:
            if s['standard_hint'] == standard:
                for d in s['data']:
                    available_screw_sizes.append(d['screw_size'])
                self.thread_size_combo.addItems(available_screw_sizes)
                return available_screw_sizes

    """! populate material options
    @param self object pointer
    """
    def populateMaterialOptions(self):
        self.material_combo.addItems(self.material_naming_data)

    """! populate standard options
    @param self object pointer
    """
    def populateThreadStandards(self):
        options = []
        for s in self.thread_naming_data:
            options.append(s['standard_hint'])
        self.thread_standard_combo.addItems(options)

    ### Helper Functions

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
    def getThreadData(self, standard, screw_size, pitch, thread_class):
        for s in self.thread_data:
            if s['hint'] == standard:
                for t in s['external_data']:
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
