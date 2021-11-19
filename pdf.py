import imghdr

import PIL.Image
from PyPDF2 import PdfFileMerger, PdfFileReader
from PyQt5.QtWidgets import QMessageBox
from fpdf import FPDF
import os.path
from numpy import mean, std, around, array, save, load, append

from qgis._core import QgsProject, QgsLayoutExporter, QgsMessageLog


class PDF(FPDF):

    def __init__(self, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation, unit, format)

        self.y_own = 20

    def accept_page_break(self):
        self.y_own = 20
        return super().accept_page_break()

    def field_must_exist(self, fields, field, dlg):
        index = fields.indexFromName(field)
        if index == -1:
            QMessageBox.information(dlg, 'ERROR', 'Wybrana przez Ciebie warstwa nie zawiera kolumny Evd')

        return index

    def init(self):
        self.add_page()
        self.set_margins(10, 20)
        self.add_font('DejaVu', '', os.path.join(os.path.dirname(__file__), 'DejaVuSansCondensed.ttf'), uni=True)

    def report_pdf(self, dlg, layer):
        # Add logo
        image_file = dlg.imageFileText.text()
        if image_file != '' and image_file is not None:
            if not imghdr.what(image_file):
                QMessageBox.information(dlg, 'ERROR', 'Logo musi być grafiką rastrową')
                return

            image = PIL.Image.open(image_file)
            width, height = image.size
            image.close()
            if height / width >= 3 / 7:
                self.image(image_file, x=20, y=30, h=30)
            else:
                self.image(image_file, x=20, y=30, w=70)

        # Date and place
        self.set_xy(20, self.y_own)
        self.set_font('DejaVu', '', 11)
        text = dlg.cityLine.text() + ', ' + dlg.dateLine.text()
        self.cell(w=60, h=8, align='L', txt=text, border=0)

        # attachment
        self.set_xy(160, self.y_own)
        self.set_font('DejaVu', '', 11)
        text = 'Zal. ' + dlg.attachLine.text()
        self.cell(w=30, h=8, align='R', txt=text, border=0)

        self.y_own = self.y_own + 10
        self.set_xy(90, self.y_own)
        self.set_font('DejaVu', '', 16)
        self.cell(w=120, h=8, align='C', txt="Protokół badania", border=0)

        self.y_own = self.y_own + 8
        self.set_xy(90, self.y_own)
        self.set_font('DejaVu', '', 14)
        self.cell(w=120, h=5, align='C', txt="dynamicznego modułu odkształcenia Evd", border=0)

        self.set_font('DejaVu', '', 12)

        fields = layer.fields()
        features = layer.getFeatures()

        self.y_own = self.y_own + 12
        elements = [
            'Producent',
            'Numer seryjny',
            'Waga młota'
        ]

        feature = features.__next__()
        elements_values = [
            'Terratest GmbH',
        ]

        if fields.indexFromName('serial_number') != -1:
            elements_values.append(feature['serial_number'])
        else:
            elements_values.append('')

        if fields.indexFromName('hammer_weight') != -1:
            elements_values.append(feature['hammer_weight'] + 'kg')
        else:
            elements_values.append('')

        for i in range(len(elements)):
            self.set_xy(90, self.y_own)
            self.write(5, elements[i] + ': ' + elements_values[i])
            self.y_own = self.y_own + 5

        # Dane badania
        elements = [
            'Obiekt',
            'Lokalizacja',
            'Zleceniodawca',
            'Pogoda',
            'Warstwa',
            'Badany materiał',
            'Grunt równoważny',
            'Uziarnienie',
            'Badanie wykonał',
            'Opracował'
        ]
        element_values = [
            dlg.testObjectLine.text(),
            dlg.locationLine.text(),
            dlg.buyerLine.text(),
            dlg.weatherLine.text(),
            dlg.layerLine.text(),
            dlg.soilTestLine.text(),
            dlg.soilEqualLine.text(),
            dlg.granularityLine.text(),
            dlg.testerLine.text(),
            dlg.creatorLine.text()
        ]
        self.y_own = self.y_own + 5  # distance 10 from last element
        y_temp = self.y_own
        for i in range(len(elements)):
            self.set_xy(40, self.y_own)
            self.cell(w=20, h=5, align='R', txt=elements[i] + ':', border=0)
            self.cell(w=110, h=5, align='C', txt=element_values[i], border=0)
            self.y_own = self.y_own + 6
            self.line(60, self.y_own - 0.5, 185, self.y_own - 0.5)
        self.rect(15, y_temp - 2, 180, self.y_own - y_temp + 5)

        # Wyniki badania
        if dlg.resultCheckbox.isChecked():
            features = layer.getFeatures()
            columns_name = [
                'Pkt',
                'Data',
                'Osiadanie\nS1\n[mm]',
                'Osiadanie\nS2\n[mm]',
                'Osiadanie\nS3\n[mm]',
                'Osiadanie\nśrednie\n[mm]',
                'Evd\n[MPa]',
                'E2\n[MPa]',
                'Is\n[-]',
                'Id\n[-]'
            ]
            columns_width = [
                8,
                40,
                20,
                20,
                20,
                20,
                15,
                20,
                15,
                15
            ]
            header_height = 15
            header_heights = [
                header_height,
                header_height,
                header_height / 3,
                header_height / 3,
                header_height / 3,
                header_height / 3,
                header_height / 2,
                header_height / 2,
                header_height / 2,
                header_height / 2
            ]
            keys = [
                'Pkt',
                'date',
                's1max',
                's2max',
                's3max',
                'average_s',
                'Evd',
                'E2',
                'Is',
                'Id'
            ]

            indexes = {}

            total_width = 0
            for i in range(len(keys)):
                index = fields.indexFromName(keys[i])
                indexes[keys[i]] = [index, columns_name[i], columns_width[i], header_heights[i]]
                if index != -1:
                    total_width = total_width + columns_width[i]

            # Center table
            x = (210 - total_width) / 2
            x_temp = x

            # Header
            self.y_own = self.y_own + 5
            self.set_xy(x, self.y_own)
            self.set_font('DejaVu', '', 11)
            self.set_fill_color(240)
            for key, value in indexes.items():
                if value[0] != -1:
                    self.multi_cell(value[2], value[3], value[1], 1, align='C', fill=True)
                x_temp = x_temp + value[2]
                self.set_xy(x_temp, self.y_own)

            self.y_own = self.y_own + header_height
            self.set_font('DejaVu', '', 10)
            for feature in features:
                self.set_xy(x, self.y_own)
                for key, value in indexes.items():
                    if value[0] != -1:
                        data = feature.attributes()[value[0]]
                        if key == 'date':
                            data = data.toString('dd.MM.yyyy  hh:mm')
                        if key == 's1max' or key == 's2max' or key == 's3max' or key == 'average_s':
                            data = '%.3f' % round(data, 3)
                        if key == 'Evd' or key == 'E2':
                            data = '%.1f' % round(data, 1)
                        if key == 'Is' or key == 'Id':
                            data = '%.2f' % round(data, 2)

                        self.cell(value[2], 5, str(data), 1, align='C')

                self.y_own = self.y_own + 5

        # Statystyki
        if dlg.statsCheckbox.isChecked():
            features = layer.getFeatures()
            evd_index = self.field_must_exist(fields, 'Evd', dlg)
            if evd_index == -1:
                return
            evd = []
            for feature in features:
                evd.append(feature.attributes()[evd_index])

            self.y_own = self.y_own + 5
            x = 30
            self.set_font('DejaVu', '', 12)

            mean_value = mean(evd)
            self.set_xy(x, self.y_own)
            self.cell(w=60, h=10, align='R', txt="Średnia arytmetyczna Evd:", border=0)
            self.cell(w=20, h=10, align='C', txt=str(around(mean_value, 1)), border=0)
            self.cell(w=20, h=10, align='C', txt="[MPa]", border=0)

            std_value = std(evd)
            self.y_own = self.y_own + 10
            self.set_xy(x, self.y_own)
            self.cell(w=60, h=10, align='R', txt="Odchylenie standardowe Evd:", border=0)
            self.cell(w=20, h=10, align='C', txt=str(around(std_value, 3)), border=0)
            self.cell(w=20, h=10, align='C', txt="[MPa]", border=0)

            coeff_var = (std_value / mean_value) * 100
            self.y_own = self.y_own + 10
            self.set_xy(x, self.y_own)
            self.cell(w=60, h=10, align='R', txt="Współczynnik zmienności Evd:", border=0)
            self.cell(w=20, h=10, align='C', txt=str(around(coeff_var, 3)), border=0)
            self.cell(w=20, h=10, align='C', txt="[%]", border=0)

            self.y_own = self.y_own + 10
            self.set_xy(x, self.y_own)
            self.cell(w=60, h=10, align='R', txt="Kryterium jakości:", border=0)
            if coeff_var < 30:
                text = 'Spełnione - warstwa jednorodna'
                self.set_text_color(0, 255, 0)
            else:
                text = 'Niespełnione - warstwa niejednorodna'
                self.set_text_color(255, 0, 0)
            self.cell(w=80, h=10, align='C', txt=text, border=0)

    def save(self, output_file, map_name):
        self.output(output_file, 'F')

        head, tail = os.path.split(output_file)  # head is path, tail is file name

        # Generowanie mapy
        if map_name:
            manager = QgsProject.instance().layoutManager()
            layout = manager.layoutByName(map_name)
            exporter = QgsLayoutExporter(layout)
            temp_path = os.path.join(head, 'temp_asdasdasdasd.pdf')
            exporter.exportToPdf(temp_path, QgsLayoutExporter.PdfExportSettings())

            merge_file = PdfFileMerger()
            merge_file.append(PdfFileReader(output_file))
            merge_file.append(PdfFileReader(temp_path))
            merge_file.write(output_file)
            os.remove(temp_path)
