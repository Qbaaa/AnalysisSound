from scipy.io import wavfile
import sys
import pygame
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QMenuBar, QMenu, QAction, QWidget, \
    QGroupBox, QPushButton, QRadioButton, QComboBox, QVBoxLayout
import pyqtgraph as pg
import numpy as np
import os

class Ui_MainWindow(object):
    nameFileWave = ''
    overlap = 0.1
    nperseg = 32
    window = 'hamming'
    pause = False
    regionPause = False

    def __del__(self):

        if os.path.isfile('fragment.wav') :
            os.remove('fragment.wav')
        else :
            pass

    def setupUi(self, MainWindow):

        MainWindow.setGeometry(450,50,1000,785)
        MainWindow.setWindowTitle("CFS")

        self.mainMenu = QMenuBar(MainWindow)
        self.mainMenu.setGeometry(QRect(0, 0, 1000, 21))
        self.fileMenu = QMenu('&Dzwiek', self.mainMenu)
        MainWindow.setMenuBar(self.mainMenu)
        self.actionOpenFile = QAction('&Wczytaj',MainWindow)
        self.actionOpenFile.setShortcut('Ctrl+W')
        self.actionOpenFile.setStatusTip('Wczytaj dzwięk')
        self.actionOpenFile.triggered.connect(self.fileName)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actionOpenFile)
        self.mainMenu.addAction(self.fileMenu.menuAction())


        self.centralwidget = QWidget(MainWindow)
        self.groupBoxOdtwarzacz = QGroupBox(self.centralwidget)
        self.groupBoxOdtwarzacz.setTitle("Odtwarzacz:")
        self.groupBoxOdtwarzacz.setGeometry(QRect(10, 20, 171, 111))
        self.pushButtonPlay = QPushButton(self.groupBoxOdtwarzacz)
        self.pushButtonPlay.setGeometry(QRect(20, 80, 31, 23))
        self.pushButtonPlay.setText("Play")
        self.pushButtonPlay.clicked.connect(self.filePlay)
        self.pushButtonStop = QPushButton(self.groupBoxOdtwarzacz)
        self.pushButtonStop.setGeometry(QRect(110, 80, 31, 23))
        self.pushButtonStop.setText("Stop")
        self.pushButtonStop.clicked.connect(self.fileStop)
        self.pushButtonPause = QPushButton(self.groupBoxOdtwarzacz)
        self.pushButtonPause.setGeometry(QRect(60, 80, 41, 23))
        self.pushButtonPause.setText("Pause")
        self.pushButtonPause.clicked.connect(self.filePause)
        self.radioButtonCalosc = QRadioButton(self.groupBoxOdtwarzacz)
        self.radioButtonCalosc.setGeometry(QRect(10, 20, 91, 20))
        self.radioButtonCalosc.setText("całe nagranie")
        self.radioButtonCalosc.setChecked(True)
        self.radioButtonFragment = QRadioButton(self.groupBoxOdtwarzacz)
        self.radioButtonFragment.setGeometry(QRect(10, 40, 161, 17))
        self.radioButtonFragment.setText("wybrany przedział nagrania")

        self.groupBoxDlugoscZakladki = QGroupBox(self.centralwidget)
        self.groupBoxDlugoscZakladki.setEnabled(True)
        self.groupBoxDlugoscZakladki.setGeometry(QRect(210, 20, 131, 111))
        self.groupBoxDlugoscZakladki.setTitle("Długość zakładki:")
        self.comboBoxDlugoscZakladki = QComboBox(self.groupBoxDlugoscZakladki)
        self.comboBoxDlugoscZakladki.setGeometry(QRect(10, 30, 70, 25))
        self.comboBoxDlugoscZakladki.addItem("10%")
        self.comboBoxDlugoscZakladki.addItem("20%")
        self.comboBoxDlugoscZakladki.addItem("40%")
        self.comboBoxDlugoscZakladki.addItem("50%")
        self.comboBoxDlugoscZakladki.setCurrentIndex(3)

        self.groupBoxOkno = QGroupBox(self.centralwidget)
        self.groupBoxOkno.setEnabled(True)
        self.groupBoxOkno.setGeometry(QRect(530, 20, 131, 111))
        self.groupBoxOkno.setTitle("Okna:")
        self.comboBoxOkno = QComboBox(self.groupBoxOkno)
        self.comboBoxOkno.setEnabled(True)
        self.comboBoxOkno.setGeometry(QRect(10, 30, 81, 25))
        self.comboBoxOkno.addItem("HAMMING")
        self.comboBoxOkno.addItem("BLACKMAN")


        self.groupBoxDlugoscProbki = QGroupBox(self.centralwidget)
        self.groupBoxDlugoscProbki.setGeometry(QRect(370, 20, 131, 111))
        self.groupBoxDlugoscProbki.setTitle("Dlugość próbki:")
        self.comboBoxDlugoscProbki = QComboBox(self.groupBoxDlugoscProbki)
        self.comboBoxDlugoscProbki.setGeometry(QRect(10, 30, 70, 25))
        self.comboBoxDlugoscProbki.addItem("32")
        self.comboBoxDlugoscProbki.addItem("256")
        self.comboBoxDlugoscProbki.addItem("512")
        self.comboBoxDlugoscProbki.addItem("1024")
        self.comboBoxDlugoscProbki.setCurrentIndex(2)

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(12,130,10,10)
        self.plotCalosc = pg.PlotWidget()
        self.plotCalosc.setTitle("FALA SYGNAŁU")
        self.plotCalosc.setLabel('bottom', "Czas", units='s')
        self.plotCalosc.setLabel('left', "Amplituda", units='')
        self.verticalLayout.addWidget(self.plotCalosc)

        self.plotFragment = pg.PlotWidget()
        self.plotFragment.setTitle("POWIEKSZONY FRAGMENT FALI SYGNAŁU")
        self.plotFragment.setLabel('bottom', "Czas", units='s')
        self.plotFragment.setLabel('left', "Amplituda", units='')
        self.verticalLayout.addWidget(self.plotFragment)

        self.plotSonogram = pg.PlotWidget()
        self.plotSonogram.setTitle("SPEKTOGRAM")
        self.plotSonogram.setLabel('bottom', "Czas", units='s')
        self.plotSonogram.setLabel('left', "Czestotliwosc", units='')
        self.verticalLayout.addWidget(self.plotSonogram)

        MainWindow.setCentralWidget(self.centralwidget)

    def fileName(self):
        wave = QFileDialog.getOpenFileName(caption='Wczytaj dzwiek',directory='F:/UKSW/V sem/Moje/CPS/Spektogram/', filter = "Music(*.wav)", options=QFileDialog.DontUseNativeDialog)

        if wave == ('', ''):
            QMessageBox.information(None,'Informacja',"Nie wczytales dzwieku.",QMessageBox.Ok)
        else:
            self.nameFileWave = wave[0]
            self.fileReadSound()

    def filePlay(self):

        print("Play")
        if self.nameFileWave == "":
            QMessageBox.information(None,'Informacja','Nie został wczytany żaden dźwięk.',QMessageBox.Ok)
        else:
            if self.radioButtonCalosc.isChecked() == True:

                if self.pause == False:
                    pygame.mixer.music.load(self.nameFileWave)
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.unpause()
                    self.pause = False

            else:
                print("Test")

                if self.regionPause == False:

                    try:
                        pygame.mixer.music.load(self.nameFileWave)
                        wavfile.write('fragment.wav', self.tempRegionRate, self.tempRegionData)

                    except:
                        pass

                    pygame.mixer.music.load('fragment.wav')
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.unpause()
                    self.regionPause = False

    def filePause(self):

        print("pause")
        if self.nameFileWave == "":
            QMessageBox.information(None,'Informacja','Nie został wczytany żaden dźwięk.',QMessageBox.Ok)
        else:
            pygame.mixer.music.pause()

            if pygame.mixer.music.get_busy() == 0:
                self.pause = False
                self.regionPause = False
            else:
                self.pause = True
                self.regionPause = True

            print('Pause')

    def fileStop(self):
        print("Stop")
        if self.nameFileWave == "":
            QMessageBox.information(None,'Informacja','Nie został wczytany żaden dźwięk.',QMessageBox.Ok)
        else:
            pygame.mixer.music.stop()
            self.pause = False
            self.regionPause = False

    def fileReadSound(self):

        try:
            self.pause = False
            self.regionPause = False

            rate, data = wavfile.read(self.nameFileWave)

            if len(data.shape) == 2:
                data = data[:,1]
            else:
                pass

            wavfile.write('fragment.wav', rate, data)
            self.tempRegionRate = rate
            self.tempRegionData = data
            times = np.arange(len(data)) / float(rate)
            self.x = times
            self.y = data
            self.makePlot()

        except ValueError:
            self.nameFileWave = ''
            QMessageBox.information(None,'Błąd','Nie można wczytać tego pliku,\n Proszę wybrać inny.',QMessageBox.Ok)

    def makePlot(self):

        self.plotCalosc.close()
        self.plotFragment.close()
        self.plotSonogram.close()

        self.plotCalosc = pg.PlotWidget(x = self.x, y = self.y)
        self.plotCalosc.setTitle("FALA SYGNAŁU")
        self.plotCalosc.setLabel('bottom', "Czas", units='s')
        self.plotCalosc.setLabel('left', "Amplituda", units='')
        #self.plotCalosc.setLimits(xMin= -1, xMax=max(self.times) + 1)#, yMin=min(y), yMax=max(y))
        #self.plotCalosc.setRange(xRange=[-1,max(self.times)+1])
        #self.plotCalosc.setRange(yRange=[min(y),max(y)])

        self.region = pg.LinearRegionItem([0, self.x[-1]], bounds=[0, self.x[-1]])
        self.region.setZValue(100)
        self.plotCalosc.addItem(self.region)
        self.verticalLayout.addWidget(self.plotCalosc)

        self.region.sigRegionChanged.connect(self.updateRegion)

        self.plotFragment = pg.PlotWidget(x = self.x, y = self.y)
        self.plotFragment.setTitle("POWIEKSZONY FRAGMENT FALI SYGNAŁU")
        self.plotFragment.setLabel('bottom', "Czas", units='s')
        self.plotFragment.setLabel('left', "Amplituda", units='')
        self.verticalLayout.addWidget(self.plotFragment)

        self.plotSonogram = pg.PlotWidget()
        self.plotSonogram.setTitle("SPEKTOGRAM")
        self.plotSonogram.setLabel('bottom', "Czas", units='s')
        self.plotSonogram.setLabel('left', "Czestotliwosc", units='')
        self.verticalLayout.addWidget(self.plotSonogram)

    def updateRegion(self):

        temp = (self.x > self.region.getRegion()[0]-0.000000001) & (self.x < self.region.getRegion()[1]+0.000000001)

        self.tempx = self.x[temp]
        self.tempy = self.y[temp]
        self.tempRegionData = self.tempy

        self.updatePlot()

    def updatePlot(self):

        self.regionPause = False
        self.plotFragment.plot(x = self.tempx , y = self.tempy, clear=True)
        self.plotSonogram.plot()

if __name__ == "__main__":

    pygame.init()
    app = QApplication(sys.argv)
    window = QMainWindow()
    gui = Ui_MainWindow()
    gui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
