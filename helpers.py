from PyQt5.QtWidgets import QMessageBox


def field_must_exist(fields, field, dlg):
    index = fields.indexFromName(field)
    if index == -1:
        QMessageBox.information(dlg, 'ERROR', 'Wybrana przez Ciebie warstwa nie zawiera kolumny Evd')

    return index
