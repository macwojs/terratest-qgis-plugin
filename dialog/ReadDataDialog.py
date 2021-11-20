import os.path

from qgis.PyQt import QtGui
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QAbstractItemView, QFileDialog
from qgis._core import QgsRasterLayer, QgsProject, QgsField, QgsFeature, QgsGeometry, QgsPointXY, QgsPalLayerSettings, \
    QgsTextFormat, QgsTextBufferSettings, QgsVectorLayerSimpleLabeling

from .BaseDialog import BaseDialog
from ..libs.terratest.TerratestLib import TerratestRead as TerraLib
from ..interface.terratest_dialog_base import TerratestDialog


class ReadDataDialog(BaseDialog):
    def __init__(self, iface):
        super().__init__(iface, TerratestDialog())

        self.wms_maps = [
            {
                "url": "type=xyz&url=https://tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0&crs"
                       "=EPSG3857",
                "name": "OpenStreetMap"
            },
            {
                "url": "contextualWMSLegend=0&crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png8&layers=RZab"
                       "&layers=TPrz&layers=SOd2&layers=SOd1&layers=GNu2&layers=GNu1&layers=TKa2&layers=TKa1&layers"
                       "=TPi2&layers=TPi1&layers=UTrw&layers=TLes&layers=RKr&layers=RTr&layers=ku7&layers=ku6&layers"
                       "=ku5&layers=ku4&layers=ku3&layers=ku2&layers=ku1&layers=Mo&layers=Szu&layers=Pl3&layers=Pl2"
                       "&layers=Pl1&layers=kanOkr&layers=rzOk&layers=row&layers=kan&layers=rz&layers=RowEt&layers"
                       "=kanEt&layers=rzEt&layers=WPow&layers=LBrzN&layers=LBrz&layers=WPowEt&layers=GrPol&layers=Rez"
                       "&layers=GrPK&layers=GrPN&layers=GrDz&layers=GrGm&layers=GrPo&layers=GrWo&layers=GrPns&layers"
                       "=PRur&layers=ZbTA&layers=BudCm&layers=TerCm&layers=BudSp&layers=Szkl&layers=Kap&layers=SwNch"
                       "&layers=SwCh&layers=BudZr&layers=BudGo&layers=BudPWy&layers=BudP2&layers=BudP1&layers=BudUWy"
                       "&layers=BudU&layers=BudMWy&layers=BudMJ&layers=BudMW&layers=Bzn&layers=BHydA&layers=BHydL"
                       "&layers=wyk&layers=wa6&layers=wa5&layers=wa4&layers=wa3&layers=wa2&layers=wa1&layers=IUTA"
                       "&layers=ObOrA&layers=ObPL&layers=Prom&layers=PomL&layers=MurH&layers=PerA&layers=PerL&layers"
                       "=Tryb&layers=UTrL&layers=LTra&layers=LKNc&layers=LKBu&layers=LKWs&layers=TSt&layers=LKNelJ"
                       "&layers=LKNelD&layers=LKNelW&layers=LKZelJ&layers=LKZelD&layers=LKZelW&layers=Scz&layers=Al"
                       "&layers=AlEt&layers=Sch2&layers=Sch1&layers=DrDGr&layers=DrLGr&layers=JDrLNUt&layers=JDLNTw"
                       "&layers=JDrZTw&layers=JDrG&layers=DrEk&layers=JDrEk&layers=AuBud&layers=JAu&layers=NazDr"
                       "&layers=NrDr&layers=Umo&layers=PPdz&layers=Prze&layers=TunK&layers=TunD&layers=Klad&layers"
                       "=MosK&layers=MosD&layers=UTrP&layers=ObKom&layers=InUTP&layers=ZbTP&layers=NazUl&layers=ObOrP"
                       "&layers=WyBT&layers=LTel&layers=LEle&layers=ObPP&layers=DrzPomP&layers=e13&layers=e12&layers"
                       "=e11&layers=e10&layers=e9&layers=e8&layers=e7&layers=e6&layers=e5&layers=e4&layers=e3&layers"
                       "=e2&layers=e1&layers=s19&layers=s18&layers=s17&layers=s16&layers=s15&layers=s14&layers=s13"
                       "&layers=s12&layers=s11&layers=s10&layers=s9&layers=s8&layers=s7&layers=s6&layers=s5&layers=s4"
                       "&layers=s3&layers=s2&layers=s1&styles&styles&styles&styles&styles&styles&styles&styles&styles"
                       "&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles"
                       "&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles"
                       "&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles"
                       "&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles"
                       "&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles"
                       "&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles"
                       "&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles"
                       "&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles"
                       "&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles"
                       "&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles"
                       "&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles"
                       "&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles&styles"
                       "&url=http://mapy.geoportal.gov.pl/wss/service/pub/guest/kompozycja_BDOT10k_WMS/MapServer"
                       "/WMSServer",
                "name": "Geoportal - BDOT10K"
            },
            {
                "url": "contextualWMSLegend=0&crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png8&layers=Raster"
                       "&styles&url=http://mapy.geoportal.gov.pl/wss/service/img/guest/TOPO/MapServer/WMSServer",
                "name": "Geoportal - Topo"
            },
            {
                "url": "type=xyz&url=http://mt0.google.com/vt/lyrs%3Ds%26hl%3Den%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D"
                       "%7Bz%7D&zmax=18&zmin=0",
                "name": "Google - Satelite"
            },
        ]

        model = QtGui.QStandardItemModel()
        self.dlg.filesView.setModel(model)
        # self.dlg.filesView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.dlg.filesView.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.dlg.filesView.selectionModel().currentChanged.connect(self.show_details)

        self.dlg.openButton.clicked.connect(self.choose_files)
        self.dlg.cancelButton.clicked.connect(self.cancel)
        self.dlg.generateButton.clicked.connect(self.generate)
        self.dlg.deleteButton.clicked.connect(self.delete)
        self.dlg.deleteAllButton.clicked.connect(self.delete_all)

        self.dlg.wmsList.addItems([map["name"] for map in self.wms_maps])

    def choose_files(self):
        files, selected_filter = QFileDialog.getOpenFileNames(self.dlg, "Select terratest files")

        for i in files:
            item = QtGui.QStandardItem(os.path.basename(i))
            terratest_data = TerraLib(i)
            item.setData(terratest_data)
            self.dlg.filesView.model().appendRow(item)

    def cancel(self):
        self.delete_all()

        super().cancel()

    def generate(self):
        if self.dlg.wmsCheckbox.isChecked():
            wms_index = self.dlg.wmsList.currentIndex()
            map = self.wms_maps[wms_index]
            wms_layer = QgsRasterLayer(map["url"], map["name"], "wms")
            QgsProject.instance().addMapLayer(wms_layer)

        model = self.dlg.filesView.model()
        if model.rowCount():
            vl = self.iface.addVectorLayer("Point?crs=epsg:4326", "terratest_points", "memory")
            pr = vl.dataProvider()
            pr.addAttributes([
                QgsField("Pkt", QVariant.Int),
                QgsField("name", QVariant.String),
                QgsField("serial_number", QVariant.String),
                QgsField("hammer_weight", QVariant.String),
                QgsField("calibration", QVariant.Date),
                QgsField("date", QVariant.DateTime),
                QgsField("X", QVariant.Double),
                QgsField("Y", QVariant.Double),
                QgsField("s1", QVariant.String),
                QgsField("v1max", QVariant.Double),
                QgsField("s1max", QVariant.Double),
                QgsField("s2", QVariant.String),
                QgsField("v2max", QVariant.Double),
                QgsField("s2max", QVariant.Double),
                QgsField("s3", QVariant.String),
                QgsField("v3max", QVariant.Double),
                QgsField("s3max", QVariant.Double),
                QgsField("Evd", QVariant.Double),
                QgsField("average_s", QVariant.Double),
                QgsField("s/v", QVariant.Double)
            ])
            vl.updateFields()

            data = []
            for row in range(model.rowCount()):
                item = model.takeItem(row).data()
                data.append(item)

            lp = 1
            data.sort(key=lambda x: x.test_datetime)
            for item in data:
                cords = item.coordinates_g()

                fet = QgsFeature()
                fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(cords[1], cords[0])))
                fet.setAttributes([lp] + item.atr_for_layer())
                pr.addFeatures([fet])

                lp = lp + 1

                vl.updateExtents()

            # LABEL FOR LAYER
            pal_layer = QgsPalLayerSettings()
            pal_layer.fieldName = "Pkt"

            # Text format and buffer
            text_format = QgsTextFormat()
            text_format.setSize(12)
            buffer_settings = QgsTextBufferSettings()
            buffer_settings.setEnabled(True)
            buffer_settings.setSize(1)
            buffer_settings.setColor(QColor("white"))
            text_format.setBuffer(buffer_settings)
            pal_layer.setFormat(text_format)

            # Label offset
            pal_layer.placement = 1
            pal_layer.quadOffset = 4
            pal_layer.xOffset = 2.0
            pal_layer.yOffset = -3.0

            labeler = QgsVectorLayerSimpleLabeling(pal_layer)
            vl.setLabeling(labeler)
            vl.setLabelsEnabled(True)
            vl.triggerRepaint()

            # FIXME Zoom to loaded layer
            # canvas = self.iface.mapCanvas()
            # vl.selectAll()
            # canvas.zoomToSelected()
            # self.iface.actionZoomToSelected().trigger()
            # vl.removeSelection()
            # canvas.refresh()

        self.cancel()

    def show_details(self, current, previous):
        item = self.dlg.filesView.model().itemFromIndex(current).data()
        text = "Nazwa: " + item.name + "\n" \
               + "Data: " + item.test_datetime.strftime("%d.%m.%Y") + "\n" \
               + "Godzina: " + item.test_datetime.strftime("%H:%M:%S") + "\n" \
               + "Evd: " + "{:.3f}".format(item.evd)
        self.dlg.detailsText.setPlainText(text)

    def delete(self):
        selected_list = self.dlg.filesView.selectedIndexes()
        selected_list = sorted(selected_list, key=lambda x: -x.row())
        for i in selected_list:
            self.dlg.filesView.model().takeRow(i.row())

    def delete_all(self):
        self.dlg.filesView.model().clear()
