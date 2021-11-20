from numpy import mean, std, around

from .BaseDialog import BaseDialog
from ..helpers import field_must_exist
from ..interface.terratest_dialog_stats_choose import TerratestDialogStatsChoose
from ..interface.terratest_dialog_stats_show import TerratestDialogStatsShow


class StatisticsDialog(BaseDialog):
    def __init__(self, iface):
        super().__init__(iface, TerratestDialogStatsChoose())

        self.dlg_show = TerratestDialogStatsShow()

        self.dlg.countButton.clicked.connect(self.calculate_stats)
        self.dlg.cancelButton.clicked.connect(self.cancel)

    def show(self):
        self.load_vector_layers()
        self.vector_layers_to_list()

        super().show()

    def cancel(self):
        self.dlg.layerList.clear()

        super().cancel()

    def calculate_stats(self):
        selected_layer = self.vector_layers[self.dlg.layerList.currentIndex()]
        fields = selected_layer.fields()

        index = field_must_exist(fields, 'Evd', self.dlg)
        if index == -1:
            return

        evd = []
        features = selected_layer.getFeatures()
        for feature in features:
            evd.append(feature.attributes()[index])

        if self.dlg.meanCheckbox.isChecked():
            mean_value = around(mean(evd), 1)
            self.dlg_show.meanText.setText(str(mean_value))

        if self.dlg.stdDevCheckbox.isChecked():
            std_value = around(std(evd), 3)
            self.dlg_show.stdDevText.setText(str(std_value))

        if self.dlg.coeffVariationCheckbox.isChecked():
            coeff_var = around((std(evd) / mean(evd)) * 100, 1)
            self.dlg_show.coeffVariationText.setText(str(coeff_var) + '%')
            if coeff_var < 30:
                result = 'warstwa jednorodna'
                color = 'green'
            else:
                result = 'warstwa niejednorodna'
                color = 'red'

            self.dlg_show.resultText.setText(result)
            self.dlg_show.resultText.setStyleSheet('color: ' + color)

        self.dlg.close()
        self.dlg_show.show()
