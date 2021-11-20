import os.path

from numpy import array, save, load
from qgis.PyQt.QtWidgets import QMessageBox, QFileDialog
from qgis._core import QgsProject, QgsApplication

from .BaseDialog import BaseDialog
from ..interface.terratest_dialog_report import TerratestDialogReport
from ..libs.pdf.pdf import PDF


class ReportDialog(BaseDialog):
    def __init__(self, iface):
        super().__init__(iface, TerratestDialogReport())

        self.dlg.generateButton.clicked.connect(self.generate_report)
        self.dlg.cancelButton.clicked.connect(self.cancel)
        self.dlg.outputFileButton.clicked.connect(self.output_file_report)
        self.dlg.imageFileButton.clicked.connect(self.image_file_report)

        self.settings_path = QgsApplication.qgisSettingsDirPath()

    def show(self):
        self.load_vector_layers()
        self.vector_layers_to_list()

        manager = QgsProject.instance().layoutManager()
        self.dlg.mapsList.clear()
        self.dlg.mapsList.addItems([layer.name() for layer in manager.printLayouts()])

        # Load settings
        try:
            report_settings_array = load(os.path.join(self.settings_path, 'report_form.npy'))
        except:
            pass
        else:
            elements = [
                self.dlg.testObjectLine,
                self.dlg.locationLine,
                self.dlg.buyerLine,
                self.dlg.weatherLine,
                self.dlg.layerLine,
                self.dlg.soilTestLine,
                self.dlg.soilEqualLine,
                self.dlg.granularityLine,
                self.dlg.testerLine,
                self.dlg.creatorLine,
                self.dlg.cityLine,
                self.dlg.dateLine,
                self.dlg.attachLine
            ]
            for i in range(report_settings_array.size):
                elements[i].setText(report_settings_array[i])

        super().show()

    def cancel(self):
        self.dlg.mapsList.clear()
        self.dlg.outputFileText.clear()

        super().cancel()

    def generate_report(self):
        output_file = self.dlg.outputFileText.text()
        if output_file == '' or output_file is None:
            QMessageBox.information(self.dlg, 'ERROR', 'Musisz określić miejsce zapisu raportu')
            return

        pdf = PDF(format='A4')
        pdf.init()
        pdf.report_pdf(self.dlg, self.vector_layers[self.dlg.layerList.currentIndex()])
        if self.dlg.mapCheckbox.isChecked():
            map_name = self.dlg.mapsList.currentText()
        else:
            map_name = None
        pdf.save(output_file, map_name)

        # Zapisywanie danych z formularza na przyszlosc
        np_array = array([
            self.dlg.testObjectLine.text(),
            self.dlg.locationLine.text(),
            self.dlg.buyerLine.text(),
            self.dlg.weatherLine.text(),
            self.dlg.layerLine.text(),
            self.dlg.soilTestLine.text(),
            self.dlg.soilEqualLine.text(),
            self.dlg.granularityLine.text(),
            self.dlg.testerLine.text(),
            self.dlg.creatorLine.text(),
            self.dlg.cityLine.text(),
            self.dlg.dateLine.text(),
            self.dlg.attachLine.text()
        ])
        settings_path = os.path.join(self.settings_path, 'report_form.npy')
        save(settings_path, np_array)

        self.cancel()

    def output_file_report(self):
        filename, _filter = QFileDialog.getSaveFileName(
            self.dlg, "Select output file ", "", '*.pdf')
        self.dlg.outputFileText.setText(filename)

    def image_file_report(self):
        filename, _filter = QFileDialog.getOpenFileName(
            self.dlg, "Select logo file ", "", '*.png,*.jpg')
        self.dlg.imageFileText.setText(filename)
