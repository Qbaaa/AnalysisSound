import time
from scipy.io import wavfile
from scipy import fftpack
from scipy.signal import get_window, signaltools
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
    overlap = 0.4
    nperseg = 512
    window = 'hamming'
    pause = False
    regionPause = False
    deletePlotFragment = True

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
        self.comboBoxDlugoscZakladki.addItem("30%")
        self.comboBoxDlugoscZakladki.addItem("40%")
        self.comboBoxDlugoscZakladki.addItem("50%")
        self.comboBoxDlugoscZakladki.addItem("60%")
        self.comboBoxDlugoscZakladki.addItem("70%")
        self.comboBoxDlugoscZakladki.addItem("80%")
        self.comboBoxDlugoscZakladki.addItem("90%")
        self.comboBoxDlugoscZakladki.setCurrentIndex(3)
        self.comboBoxDlugoscZakladki.currentIndexChanged.connect(self.updateSpectrum)


        self.groupBoxOkno = QGroupBox(self.centralwidget)
        self.groupBoxOkno.setEnabled(True)
        self.groupBoxOkno.setGeometry(QRect(530, 20, 131, 111))
        self.groupBoxOkno.setTitle("Okna:")
        self.comboBoxOkno = QComboBox(self.groupBoxOkno)
        self.comboBoxOkno.setEnabled(True)
        self.comboBoxOkno.setGeometry(QRect(10, 30, 81, 25))
        self.comboBoxOkno.addItem("HAMMING")
        self.comboBoxOkno.addItem("BLACKMAN")
        self.comboBoxOkno.addItem("HANN")
        self.comboBoxOkno.addItem("BARTLETT")
        self.comboBoxOkno.addItem("TRIANG")
        self.comboBoxOkno.currentIndexChanged.connect(self.updateSpectrum)


        self.groupBoxDlugoscProbki = QGroupBox(self.centralwidget)
        self.groupBoxDlugoscProbki.setGeometry(QRect(370, 20, 131, 111))
        self.groupBoxDlugoscProbki.setTitle("Dlugość próbki:")
        self.comboBoxDlugoscProbki = QComboBox(self.groupBoxDlugoscProbki)
        self.comboBoxDlugoscProbki.setGeometry(QRect(10, 30, 70, 25))
        self.comboBoxDlugoscProbki.addItem("16")
        self.comboBoxDlugoscProbki.addItem("32")
        self.comboBoxDlugoscProbki.addItem("64")
        self.comboBoxDlugoscProbki.addItem("128")
        self.comboBoxDlugoscProbki.addItem("256")
        self.comboBoxDlugoscProbki.addItem("512")
        self.comboBoxDlugoscProbki.addItem("1024")
        self.comboBoxDlugoscProbki.addItem("2048")
        self.comboBoxDlugoscProbki.addItem("4096")
        self.comboBoxDlugoscProbki.setCurrentIndex(5)
        self.comboBoxDlugoscProbki.currentIndexChanged.connect(self.updateSpectrum)
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
            self.nameFileWave = ""
            self.nameFileWave = wave[0]
            self.fileReadSound()

    def filePlay(self):

        print("Play")
        try:
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

        except:
            QMessageBox.information(None,'Informacja','Program nie moze otworzyc dzwieku, ale przeanalizował sygnal.',QMessageBox.Ok)

    def filePause(self):

        print("Pause")
        try:
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
        except:
            pass

    def fileStop(self):
        print("Stop")
        try:
            if self.nameFileWave == "":
                QMessageBox.information(None,'Informacja','Nie został wczytany żaden dźwięk.',QMessageBox.Ok)
            else:
                pygame.mixer.music.stop()
                self.pause = False
                self.regionPause = False
        except:
            pass

    def fileReadSound(self):

        try:
            self.pause = False
            self.regionPause = False

            rate, data = wavfile.read(self.nameFileWave)

            if len(data.shape) == 2:
                data = data[:,1]

            wavfile.write('fragment.wav', rate, data)
            self.tempRegionRate = rate
            self.tempRegionData = data
            times = np.arange(len(data)) / float(rate)
            self.x = times
            self.y = data
            self.tempx = times
            self.tempy = data
            self.makePlot()

        except ValueError:
            self.nameFileWave = ''
            QMessageBox.information(None,'Błąd','Nie można wczytać tego pliku,\n Proszę wybrać inny.',QMessageBox.Ok)

    def makePlot(self):

        if self.deletePlotFragment:
            self.plotFragment.close()

        self.plotCalosc.plot(x = self.x, y = self.y, clear=True)
        #self.plotCalosc = pg.PlotWidget(x = self.x, y = self.y)
        tempMinX = min(self.x)
        tempMaxX = max(self.x)
        tempMinY = min(self.y)
        tempMaxY = max(self.y)

        tempDistanceX = 0.02
        if tempMaxX <= 10.0:
            pass
        else:
            if tempMaxX <= 100.0:
                tempDistanceX = 0.2
            else:
                tempDistanceX = 2.0


        if tempMinY > 0:
            tempDistanceMinY = tempMinY - tempMinY/2
        else:
            if tempMinY < 0:
                tempDistanceMinY = tempMinY + tempMinY/2
            else:
                tempDistanceMinY =- 10

        if tempMaxY < 0:
            tempDistanceMaxY = tempMaxX - tempMaxX/2
        else:
            if tempMaxY > 0:
                tempDistanceMaxY = tempMaxY + tempMaxY/2
            else:
                tempDistanceMaxY =+ 10

        self.plotCalosc.setRange(xRange=[tempMinX - tempDistanceX,tempMaxX + tempDistanceX], yRange=[tempDistanceMinY, tempDistanceMaxY])
        self.plotCalosc.setLimits(xMin= tempMinX-tempDistanceX ,xMax= tempMaxX+tempDistanceX, yMin= tempDistanceMinY, yMax= tempDistanceMaxY)

        if(max(self.x) < 90.0):
            self.region = pg.LinearRegionItem([0, self.x[-1]], bounds=[0, self.x[-1]])
            self.region.setZValue(100)
            self.plotCalosc.addItem(self.region)

            self.region.sigRegionChanged.connect(self.updateRegion)

            self.plotFragment = pg.PlotWidget(x = self.tempx, y = self.tempy)
            self.plotFragment.setRange(xRange=[tempMinX - tempDistanceX,tempMaxX + tempDistanceX], yRange=[tempMinY + tempMinY/2,tempMaxY + tempMaxY/2])
            self.plotFragment.setLimits(xMin= tempMinX-tempDistanceX ,xMax= tempMaxX+tempDistanceX, yMin= tempMinY + tempMinY/2, yMax= tempMaxY + tempMaxY/2)
            self.plotFragment.setTitle("POWIEKSZONY FRAGMENT FALI SYGNAŁU")
            self.plotFragment.setLabel('bottom', "Czas", units='s')
            self.plotFragment.setLabel('left', "Amplituda", units='')
            self.verticalLayout.addWidget(self.plotFragment)
            self.deletePlotFragment = True
        else:
            self.deletePlotFragment = False

        self.makeSpectrum()

    def updateRegion(self):

        temp = (self.x > self.region.getRegion()[0]-0.000000001) & (self.x < self.region.getRegion()[1]+0.000000001)

        self.tempx = self.x[temp]
        self.tempy = self.y[temp]
        self.tempRegionData = self.tempy
        self.updatePlot()

    def updatePlot(self):

        self.regionPause = False
        tempMinX = min(self.tempx)
        tempMaxX = max(self.tempx)
        tempMinY = min(self.tempy)
        tempMaxY = max(self.tempy)

        if tempMinY > 0:
            tempDistanceMinY = tempMinY - tempMinY/2
        else:
            if tempMinY < 0:
                tempDistanceMinY = tempMinY + tempMinY/2
            else:
               tempDistanceMinY =- 10

        if tempMaxY < 0:
            tempDistanceMaxY = tempMaxX - tempMaxX/2
        else:
            if tempMaxY > 0:
                tempDistanceMaxY = tempMaxY + tempMaxY/2
            else:
                tempDistanceMaxY =+ 10

        self.plotFragment.setRange(xRange=[tempMinX,tempMaxX ], yRange=[tempDistanceMinY, tempDistanceMaxY])
        self.plotFragment.setLimits(xMin= tempMinX ,xMax= tempMaxX, yMin= tempDistanceMinY, yMax= tempDistanceMaxY)
        self.plotFragment.plot(x = self.tempx , y = self.tempy, clear=True)
        self.updateSpectrum()

    def makeSpectrum(self):

        if self.nameFileWave == "":
            overlap = self.dlugoscZakladki(self.comboBoxDlugoscZakladki.currentText())
            window = self.comboBoxOkno.currentText().lower()
            nperseg = int(self.comboBoxDlugoscProbki.currentText())
        else:

            overlap = self.dlugoscZakladki(self.comboBoxDlugoscZakladki.currentText())
            window = self.comboBoxOkno.currentText().lower()
            nperseg = int(self.comboBoxDlugoscProbki.currentText())

            tempwindow = get_window(window, nperseg)
            tempoverlap = nperseg * overlap
            tempoverlap = int(round(tempoverlap))

            try:
                f, t, S = self.stft(self.tempy, self.tempRegionRate, tempwindow, nperseg, tempoverlap, window)
                S = 20*np.log10(S)
                self.plotSonogram.close()
                self.plotSonogram = pg.PlotWidget()
                self.plotSonogram.setTitle("SPEKTOGRAM")
                self.plotSonogram.setLabel('bottom', "Czas", units='s')
                self.plotSonogram.setLabel('left', "Czestotliwosc", units='Hz')

                pg.setConfigOptions(imageAxisOrder='row-major')
                self.img = pg.ImageItem()
                self.plotSonogram.addItem(self.img)
                hist = pg.HistogramLUTItem()
                hist.setImageItem(self.img)
                hist.setLevels(np.min(S), np.max(S))
                hist.gradient.restoreState(
                    {'mode' : 'rgb',
                    'ticks':  [(0.0, (0,255,255,255)),
                                (0.25, (0, 0, 255, 255)),
                                (0.5, (0,0,0,255)),
                                (0.75, (255, 0, 0, 255)),
                                (1.0, (255, 255, 0, 255))
                                ]
                    }
                    )
                self.img.setImage(S)
                self.img.scale(t[-1]/np.size(S, axis=1), f[-1]/np.size(S, axis=0))
                self.plotSonogram.setLimits(xMin=0, xMax=t[-1], yMin=0, yMax=f[-1])
                self.verticalLayout.addWidget(self.plotSonogram)

            except:
                pass

    def updateSpectrum(self):

            overlap = self.dlugoscZakladki(self.comboBoxDlugoscZakladki.currentText())
            window = self.comboBoxOkno.currentText().lower()
            nperseg = int(self.comboBoxDlugoscProbki.currentText())

            tempwindow = get_window(window, nperseg)
            tempoverlap = nperseg * overlap
            tempoverlap = int(round(tempoverlap))

            try:
                f, t, S = self.stft(self.tempy, self.tempRegionRate, tempwindow, nperseg, tempoverlap, window)

                S = 20*np.log10(S)

                pg.setConfigOptions(imageAxisOrder='row-major')
                self.img = pg.ImageItem()
                self.plotSonogram.plot(clear=True)
                self.plotSonogram.addItem(self.img)
                hist = pg.HistogramLUTItem()
                hist.setImageItem(self.img)
                hist.setLevels(np.min(S), np.max(S))
                hist.gradient.restoreState(
                    {'mode' : 'rgb',
                    'ticks':  [(0.0, (0,255,255,255)),
                                (1.0, (255, 255, 0, 255)),
                                (0.5, (0,0,0,255)),
                                (0.25, (0, 0, 255, 255)),
                                (0.75, (255, 0, 0, 255))
                            ]
                    }
                )
                self.img.setImage(S)
                self.img.scale(t[-1]/np.size(S, axis=1), f[-1]/np.size(S, axis=0))
                self.plotSonogram.setLimits(xMin=0, xMax=t[-1], yMin=0, yMax=f[-1])

            except:
                pass

    def stft(self,x, fs, window, nperseg, noverlap, nameWindow):

        x = np.asarray(x)
        outdtype = np.result_type(x, np.complex64)

        if x.size == 0:
            return np.empty(x.shape), np.empty(x.shape), np.empty(x.shape)

        if nperseg > x.shape[-1]:
            nperseg = x.shape[-1]
            win = get_window(nameWindow, nperseg)
        else:
            win = window

        if np.result_type(win,np.complex64) != outdtype:
            win = win.astype(outdtype)

        scale = 1.0 / win.sum()**2
        scale = np.sqrt(scale)

        if np.iscomplexobj(x):
            freqs = fftpack.fftfreq(nperseg, 1/fs)
        else:
            freqs = np.fft.rfftfreq(nperseg, 1/fs)

        result = self.fft(x, win, nperseg, noverlap)
        result *= scale
        time = np.arange(nperseg/2, x.shape[-1] - nperseg/2 + 1, nperseg - noverlap)/float(fs)
        result = result.astype(outdtype)
        result = np.rollaxis(result, -1, -2)
        result = np.abs(result)
        tempResult = result[result!=0]
        result[result==0] = np.min(tempResult)

        return freqs, time, result

    def fft(self,x, win, nperseg, noverlap):

        if nperseg == 1 and noverlap == 0:
            result = x[..., np.newaxis]
        else:
            step = nperseg - noverlap
            shape = x.shape[:-1]+((x.shape[-1]-noverlap)//step, nperseg)
            strides = x.strides[:-1]+(step*x.strides[-1], x.strides[-1])
            result = np.lib.stride_tricks.as_strided(x, shape=shape, strides=strides)

        result = signaltools.detrend(result, type='constant', axis=-1)
        result = win * result

        if np.iscomplexobj(x):
            func = fftpack.fft
        else:
            result = result.real
            func = np.fft.rfft

        result = func(result, n=nperseg)

        return result

    def dlugoscZakladki(self,temp):

        if(temp == '10%'):
            overlap = 0.1
        else:
            if(temp == '20%'):
                overlap = 0.2
            else:
                if(temp == '30%'):
                    overlap = 0.3
                else:
                    if(temp == '40%'):
                        overlap = 0.4
                    else:
                        if(temp == '50%'):
                            overlap = 0.5
                        else:
                            if(temp == '60%'):
                                overlap = 0.6
                            else:
                                if(temp == '70%'):
                                    overlap = 0.7
                                else:
                                    if(temp == '80%'):
                                        overlap = 0.8
                                    else:
                                         overlap = 0.9

        return overlap

if __name__ == "__main__":

        pygame.init()
        app = QApplication(sys.argv)
        window = QMainWindow()
        gui = Ui_MainWindow()
        gui.setupUi(window)
        window.show()
        sys.exit(app.exec_())
