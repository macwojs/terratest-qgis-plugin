# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Terratest
                                 A QGIS plugin
 Read data from terratest dynamic plate
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-10-19
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Maciej Nikiel
        email                : m.nikiel@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt import QtGui
from qgis.PyQt.QtWidgets import QFileDialog, QAbstractItemView
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from qgis._core import QgsMessageLog, QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsPointXY

from .resources import *
# Import the code for the dialog
from .terratest_dialog import TerratestDialog
import os.path

from .terratest_lib import Terratest as TerraLib


class Terratest:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Terratest_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Terratest')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Terratest', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/terratest/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Terratest'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Terratest'),
                action)
            self.iface.removeToolBarIcon(action)

    def choose_files(self):
        files, selected_filter = QFileDialog.getOpenFileNames(self.dlg, "Select terratest files")

        for i in files:
            item = QtGui.QStandardItem(str(i))
            self.dlg.filesView.model().appendRow(item)

    def cancel(self):
        self.delete_all()
        self.dlg.close()

    def generate(self):
        model = self.dlg.filesView.model()
        if model.rowCount():
            vl = QgsVectorLayer("Point", "temporary_points", "memory")
            pr = vl.dataProvider()
            pr.addAttributes([
                QgsField("name", QVariant.String),
                QgsField("serial_number", QVariant.String),
                QgsField("calibration", QVariant.Date),
                QgsField("date", QVariant.DateTime),
                QgsField("X", QVariant.Double),
                QgsField("Y", QVariant.Double),
                QgsField("s1", QVariant.Double),
                QgsField("v1max", QVariant.Double),
                QgsField("s1max", QVariant.Double),
                QgsField("s2", QVariant.Double),
                QgsField("v2max", QVariant.Double),
                QgsField("s2max", QVariant.Double),
                QgsField("s3", QVariant.Double),
                QgsField("v3max", QVariant.Double),
                QgsField("s3max", QVariant.Double),
            ])

            for row in range(model.rowCount()):
                index = model.takeItem(row)

                data = TerraLib(index.text())

                # TODO czytanie danego pliku z wykorzystaniem TerraLib

                # TODO Zapis do warstwy wektorowej
                fet = QgsFeature()
                fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(10, 10)))
                # fet.setAttributes([
                #     "Johny",
                #     2,
                #     0.3
                # ])
                pr.addFeatures([fet])

        self.delete_all()

    def delete(self):
        selected_list = self.dlg.filesView.selectedIndexes()
        selected_list = sorted(selected_list, key=lambda x: -x.row())
        for i in selected_list:
            self.dlg.filesView.model().takeRow(i.row())

    def delete_all(self):
        self.dlg.filesView.model().clear()

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start:
            self.first_start = False
            self.dlg = TerratestDialog()

            model = QtGui.QStandardItemModel()
            self.dlg.filesView.setModel(model)
            self.dlg.filesView.setSelectionMode(QAbstractItemView.ExtendedSelection)

            self.dlg.openButton.clicked.connect(self.choose_files)
            self.dlg.cancelButton.clicked.connect(self.cancel)
            self.dlg.generateButton.clicked.connect(self.generate)
            self.dlg.deleteButton.clicked.connect(self.delete)
            self.dlg.deleteAllButton.clicked.connect(self.delete_all)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
