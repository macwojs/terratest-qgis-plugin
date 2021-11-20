from qgis._core import QgsProject, QgsVectorLayer


class BaseDialog(object):
    def __init__(self, iface, dlg):
        self.iface = iface
        self.dlg = dlg

        self.vector_layers = None

    def show(self):
        self.dlg.show()
        self.dlg.exec_()

    def cancel(self):
        self.dlg.close()

    def load_vector_layers(self):
        self.vector_layers = [layer for layer in QgsProject.instance().mapLayers().values() if
                              layer.type() == QgsVectorLayer.VectorLayer]

    def vector_layers_to_list(self):
        self.dlg.layerList.clear()
        self.dlg.layerList.addItems([layer.name() for layer in self.vector_layers])
