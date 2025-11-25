#!/usr/bin/python3
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QWidget
from pysca.helpers import register_user_widgets
from qtpy.QtDesigner import QPyDesignerCustomWidgetPlugin 

register_user_widgets('ui/widgets',ctx=globals(),include='customplugin')
# Пример пользовательского плагина для Qt Designer