"""
Custom PyQt5 widget that includes a unit label on a value
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QHBoxLayout)

"""! UnitLabel PyQt5 Widget
creates a QLabel with a specified unit label
also supports formating and data recall
"""
class UnitLabel(QLabel):
    """! constructor
    @param self object pointer
    @param kwargs supports the following:
        unit_label : str
        decimals : int
    """
    def __init__(self, **kwargs):
        super().__init__()

        # basic layout is a right alligned
        #layout.setSpacing(0)
        if kwargs['unit_label']:
            self.unit_str = kwargs.get('unit_label')
        else:
            self.unit_str = ""
        if 'decimals' in kwargs:
            self.decimals = kwargs.get('decimals')
        else:
            self.decimals = 2
        self.value_str = ""
        self.display()


    def display(self):
        self.setText(self.value_str + ' ' + self.unit_str)

    """! clear the value
    sets the label to a blank string
    @param self object pointer
    """
    def clearValue(self):
        self.value_str = ''
        self.display()

    """! clear the unit
    sets the unit to a blank string
    @param self object pointer
    """
    def clearUnit(self):
        self.unit_str = ''
        self.display()

    """! get the value
    @param self object pointer
    @return float value
    """
    def getValue(self):
        return float(self.value_str)

    """! set the value
    @param self object pointer
    @param value float value
    """
    def setValue(self, value):
        self.value_str = self.formatValue(value)
        self.display()

    """! set the unit label
    @param self object pointer
    @param unit str unit label
    """
    def setUnit(self, unit):
        self.unit_str = unit
        self.display()


    """! format the value
    @param self object pointer
    @param value float value
    @return str formatted value
    """
    def formatValue(self, value):
        format_str = "{:." + str(self.decimals) + "f}"
        return format_str.format(value)
