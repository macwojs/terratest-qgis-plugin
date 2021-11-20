import os.path

from qgis.PyQt.QtGui import QFont
from qgis.PyQt.QtWidgets import QMessageBox, QDialog
from qgis._core import QgsProject, QgsPrintLayout, QgsLayoutItemPage, QgsLayoutItemMap, QgsLayoutPoint, QgsUnitTypes, \
    QgsLayoutItemLabel, QgsLayoutSize, QgsLayoutItemScaleBar, QgsLayoutItemPicture


class PrintTemplateDialog(object):
    def __init__(self, iface):
        self.iface = iface

    def import_template(self):
        name = "Terratest default"
        manager = QgsProject.instance().layoutManager()
        # for layer in manager.printLayouts():
        #     if layer.name() == name:
        #         QMessageBox.information(self.dlg_is, 'ERROR', 'Już istnieje domyślny szablon wydruku (Terratest '
        #                                                       'default)')
        #         return

        layouts_list = manager.printLayouts()
        for layout in layouts_list:
            if layout.name() == name:
                manager.removeLayout(layout)

        project = QgsProject.instance()
        layout = QgsPrintLayout(project)
        layout.initializeDefaults()

        # Change for portrait
        pc = layout.pageCollection()
        pc.page(0).setPageSize('A4', QgsLayoutItemPage.Orientation.Portrait)

        layout.setName(name)
        project.layoutManager().addLayout(layout)

        map = QgsLayoutItemMap(layout)
        map.setRect(20, 20, 20, 20)
        canvas = self.iface.mapCanvas()
        map.setExtent(canvas.extent())  # sets map extent to current map canvas
        map.setFrameEnabled(True)
        layout.addLayoutItem(map)
        # Move & Resize
        map.attemptMove(QgsLayoutPoint(10, 40, QgsUnitTypes.LayoutMillimeters))
        map.attemptResize(QgsLayoutSize(190, 220, QgsUnitTypes.LayoutMillimeters))

        title = QgsLayoutItemLabel(layout)
        title.setText("Mapa lokalizacji punktów pomiarowych")
        title.setFont(QFont("DejaVu Sans", 24))
        title.adjustSizeToText()
        layout.addLayoutItem(title)
        title.attemptMove(QgsLayoutPoint(21, 27, QgsUnitTypes.LayoutMillimeters))

        att_text = QgsLayoutItemLabel(layout)
        att_text.setText("Zal. ")
        att_text.setFont(QFont("DejaVu Sans", 18))
        att_text.adjustSizeToText()
        layout.addLayoutItem(att_text)
        att_text.attemptMove(QgsLayoutPoint(160, 15, QgsUnitTypes.LayoutMillimeters))

        scalebar = QgsLayoutItemScaleBar(layout)
        scalebar.setLinkedMap(map)
        scalebar.setStyle('Single Box')
        scalebar.setFont(QFont("DejaVu Sans", 18))
        scalebar.applyDefaultSize()
        scalebar.setSegmentSizeMode(1)
        scalebar.setNumberOfSegmentsLeft(0)
        scalebar.setMaximumBarWidth(210 / 3)
        scalebar.update()
        layout.addLayoutItem(scalebar)
        scalebar.attemptMove(QgsLayoutPoint(20, 265, QgsUnitTypes.LayoutMillimeters))

        arrow = QgsLayoutItemPicture(layout)
        arrow.setPicturePath(os.path.join(os.path.dirname(__file__), '../icons/north_arrow.svg'))
        layout.addLayoutItem(arrow)
        arrow.attemptMove(QgsLayoutPoint(15, 45, QgsUnitTypes.LayoutMillimeters))
        arrow.attemptResize(QgsLayoutSize(30, 30, QgsUnitTypes.LayoutMillimeters))

        QMessageBox.information(QDialog(), 'SUCCESS', 'Poprawnie dodano szablon wydruku.')
