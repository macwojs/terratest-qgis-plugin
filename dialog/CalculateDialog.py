from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import QMessageBox
from qgis._core import QgsField

from .BaseDialog import BaseDialog
from ..libs.terratest.TerratestLib import TerratestCalculate
from ..helpers import field_must_exist
from ..interface.terratest_dialog_is import TerratestDialogIS


class CalculateDialog(BaseDialog):
    def __init__(self, iface):
        super().__init__(iface, TerratestDialogIS())

        self.dlg.countButton.clicked.connect(self.calculate_is_e2)
        self.dlg.cancelButton.clicked.connect(self.cancel)

        self.dlg.soilList.addItems([soil for soil in TerratestCalculate.SOILS])
        self.dlg.granularityList.addItems([granularity for granularity in TerratestCalculate.GRANULARITIES])
        self.dlg.idMethodList.addItems([id_type for id_type in TerratestCalculate.ID_METHOD])

    def show(self):
        self.load_vector_layers()
        self.vector_layers_to_list()

        super().show()

    def calculate_is_e2(self):
        selected_layer = self.vector_layers[self.dlg.layerList.currentIndex()]
        fields = selected_layer.fields()

        index = field_must_exist(fields, 'Evd', self.dlg)
        if index == -1:
            return

        if not fields[index].type() == QVariant.Double:
            QMessageBox.information(self.dlg, 'ERROR', 'Kolumna w wybranej przez Ciebie warstwie nie jest typu '
                                                       'Double')
            return

        soil = self.dlg.soilList.currentIndex()
        granularity = self.dlg.granularityList.currentIndex()

        layer_provider = selected_layer.dataProvider()

        selected_layer.startEditing()

        if self.dlg.isCheckbox.isChecked():
            index_is = fields.indexFromName('Is')
            if index_is == -1:
                layer_provider.addAttributes([QgsField('Is', QVariant.Double)])
                selected_layer.updateFields()
                fields = selected_layer.fields()
                index_is = fields.indexFromName('Is')

            features = selected_layer.getFeatures()
            for feature in features:
                is_value = TerratestCalculate.calculate_is(TerratestCalculate.GRANULARITIES[granularity],
                                                           TerratestCalculate.SOILS[soil],
                                                           feature.attributes()[index])
                selected_layer.changeAttributeValue(feature.id(), index_is, round(is_value, 3))

        if self.dlg.e2Checkbox.isChecked():
            index_e2 = fields.indexFromName('E2')
            if index_e2 == -1:
                layer_provider.addAttributes([QgsField('E2', QVariant.Double)])
                selected_layer.updateFields()
                fields = selected_layer.fields()
                index_e2 = fields.indexFromName('E2')

            features = selected_layer.getFeatures()
            for feature in features:
                e2_value = TerratestCalculate.calculate_e2(TerratestCalculate.GRANULARITIES[granularity],
                                                           TerratestCalculate.SOILS[soil],
                                                           feature.attributes()[index])
                selected_layer.changeAttributeValue(feature.id(), index_e2, round(e2_value, 3))

        if self.dlg.idCheckbox.isChecked():
            index_id = fields.indexFromName('Id')
            if index_id == -1:
                layer_provider.addAttributes([QgsField('Id', QVariant.Double)])
                selected_layer.updateFields()
                fields = selected_layer.fields()
                index_id = fields.indexFromName('Id')

            features = selected_layer.getFeatures()
            id_type = self.dlg.idMethodList.currentIndex()
            for feature in features:
                id_value = TerratestCalculate.calculate_id(TerratestCalculate.GRANULARITIES[granularity],
                                                           TerratestCalculate.SOILS[soil],
                                                           feature.attributes()[index],
                                                           TerratestCalculate.ID_METHOD[id_type])
                selected_layer.changeAttributeValue(feature.id(), index_id, round(id_value, 3))

        selected_layer.commitChanges()

        self.cancel()

    def cancel(self):
        self.dlg.layerList.clear()

        super().cancel()
