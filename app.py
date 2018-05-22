import psutil
import sys
import pyqtgraph as pg
from PyQt4.QtGui import (QApplication, QMainWindow)
from PyQt4.QtCore import QTimer, QProcess
import ramyCaracteristicas #archivo ramyCaracteristicas.py interface

class MainWindow(QMainWindow, ramyCaracteristicas.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)#linea para jalar todos componente de la interfaz

        # crear la grafica y sus propiedades
        self.crear_grafica()# funcion
        self.grafica_datos_x = []
        self.grafica_datos_y = []
        self.contador_x = 0
        self.inicializar_timer()#funcion

        self.pushButton.clicked.connect(self.funcionActualizar)

        self.proceso_comando = QProcess(self)



    def funcionActualizar(self):
        print ('funActualizarSO')
        self.proceso_comando.start('pkexec', ['dnf update', '-y'])




    def crear_grafica(self):
        self.pluma = pg.mkPen(width=2, color='y')
        self.graphicsView.plotItem.showGrid(True, True, 0.5)
        self.graphicsView.setXRange(0, 59)
        self.graphicsView.setYRange(0, 100)

        self.label.setText("RAM")
        memoria = psutil.virtual_memory()
        self.label_5.setText(str(memoria.total / (1024 * 1024 * 1024))+" GiB")

        self.label_2.setText("Disco:")
        disco = psutil.disk_usage('/').total
        self.label_8.setText(str(disco / (1024 * 1024 * 1024))+" GiB")

        self.label_3.setText("CPU:")
        self.label_6.setText(str(psutil.cpu_count()))

        self.label_4.setText("SWAP:")
        swap = psutil.swap_memory().total
        self.label_7.setText(str(swap/(1024 * 1024 * 1024))+" GiB")



    def inicializar_timer(self):
        tiempo = QTimer(self)
        tiempo.timeout.connect(self.actualizar_grafica)#cuanto termina tiempo, llamo actualizar_grafica
        tiempo.start(1000)


    def actualizar_grafica(self):
        if len(self.grafica_datos_y) == 60:
            self.grafica_datos_y.pop(0)
        self.grafica_datos_y.extend([psutil.virtual_memory().percent])

        if len(self.grafica_datos_x) == 60:
            pass
        else:
            self.grafica_datos_x.extend([self.contador_x])
            self.contador_x += 1

        self.graphicsView.plot(self.grafica_datos_x, self.grafica_datos_y[::-1], pen=self.pluma, clear=True)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationDomain('www.gatituz.me')
    app.setApplicationName('MemoriayC')
    app.setApplicationVersion('1')
    app.setOrganizationName('delissme')
    window = MainWindow()
    window.show()
    app.exec_()
