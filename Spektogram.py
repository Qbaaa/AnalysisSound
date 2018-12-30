import sys

import pygame
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QMenuBar, QMenu, QAction, QWidget, \
    QGroupBox, QPushButton, QRadioButton, QComboBox, QVBoxLayout
import pyqtgraph as pg

class Ui_MainWindow(object):
    nameFileWave = ''
    overlap = 0.1
    nperseg = 32
    window = 'hamming'
    pause = False


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
        self.centralwidget.setEnabled(True)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setTitle("Otdwarzacz:")
        self.groupBox.setGeometry(QRect(10, 20, 171, 111))
        self.pushButtonPlay = QPushButton(self.groupBox)
        self.pushButtonPlay.setGeometry(QRect(20, 80, 31, 23))
        self.pushButtonPlay.setText("Play")
        self.pushButtonPlay.clicked.connect(self.filePlay)
        self.pushButtonStop = QPushButton(self.groupBox)
        self.pushButtonStop.setGeometry(QRect(110, 80, 31, 23))
        self.pushButtonStop.setText("Stop")
        self.pushButtonStop.clicked.connect(self.fileStop)
        self.pushButtonPause = QPushButton(self.groupBox)
        self.pushButtonPause.setGeometry(QRect(60, 80, 41, 23))
        self.pushButtonPause.setText("Pause")
        self.pushButtonPause.clicked.connect(self.filePause)
        self.radioButtonCalosc = QRadioButton(self.groupBox)
        self.radioButtonCalosc.setGeometry(QRect(10, 20, 91, 20))
        self.radioButtonCalosc.setText("całe nagranie")
        self.radioButtonCalosc.setChecked(True)
        self.radioButtonFragment = QRadioButton(self.groupBox)
        self.radioButtonFragment.setGeometry(QRect(10, 40, 161, 17))
        self.radioButtonFragment.setText("wybrany przedział nagrania")



        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setEnabled(True)
        self.groupBox_2.setGeometry(QRect(210, 20, 131, 111))
        self.groupBox_2.setTitle("Długość zakładki:")
        self.comboBox = QComboBox(self.groupBox_2)
        self.comboBox.setGeometry(QRect(10, 30, 70, 25))
        self.comboBox.addItem("10%")
        self.comboBox.addItem("20%")
        self.comboBox.addItem("40%")
        self.comboBox.addItem("50%")

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setEnabled(True)
        self.groupBox_3.setGeometry(QRect(530, 20, 131, 111))
        self.groupBox_3.setTitle("Okna:")
        self.comboBox_3 = QComboBox(self.groupBox_3)
        self.comboBox_3.setEnabled(True)
        self.comboBox_3.setGeometry(QRect(10, 30, 81, 25))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("HAMMING")
        self.comboBox_3.addItem("BLACKMAN")


        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QRect(370, 20, 131, 111))
        self.groupBox_4.setTitle("Dlugość próbki:")
        self.comboBox_2 = QComboBox(self.groupBox_4)
        self.comboBox_2.setGeometry(QRect(10, 30, 70, 25))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("32")
        self.comboBox_2.addItem("256")
        self.comboBox_2.addItem("512")
        self.comboBox_2.addItem("1024")


        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.widget = QWidget(self.centralwidget)
        self.widget.setGeometry(QRect(10, 140, 975, 161))
        self.widget.setObjectName("widget")

        self.verticalLayoutWidget = QWidget(self.widget)
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 971, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        plotCalosc = pg.PlotWidget()
        plotCalosc.setTitle("FALA SYGNAŁU")
        plotCalosc.setLabel('bottom', "Czas", units='s')
        plotCalosc.setLabel('left', "Amplituda", units='')
        plotCalosc.setRange(xRange=[0,600])
        plotCalosc.setRange(yRange=[-600,600])
        plotCalosc.setLimits(xMin= -10)
        self.verticalLayout.addWidget(plotCalosc)


        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setGeometry(QRect(10, 310, 975, 171))
        self.widget_2.setObjectName("widget_2")
        self.verticalLayoutWidget_2 = QWidget(self.widget_2)
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 0, 971, 171))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        plotFragment = pg.PlotWidget()
        plotFragment.setTitle("POWIEKSZONY FRAGMENT FALI SYGNAŁU")
        plotFragment.setLabel('bottom', "Czas", units='s')
        plotFragment.setLabel('left', "Amplituda", units='')
        plotFragment.setRange(xRange=[0,600])
        plotFragment.setRange(yRange=[-600,600])
        plotFragment.setLimits(xMin= -10)
        self.verticalLayout_2.addWidget(plotFragment)

        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setGeometry(QRect(10, 490, 975, 261))
        self.widget_3.setObjectName("widget_3")
        self.verticalLayoutWidget_3 = QWidget(self.widget_3)
        self.verticalLayoutWidget_3.setGeometry(QRect(0, 0, 971, 251))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        MainWindow.setCentralWidget(self.centralwidget)

        plotSonogram = pg.PlotWidget()
        plotSonogram.setTitle("SPEKTOGRAM")
        plotSonogram.setLabel('bottom', "Czas", units='s')
        plotSonogram.setLabel('left', "Czestotliwosc", units='')
        plotSonogram.setRange(xRange=[0,600])
        plotSonogram.setRange(yRange=[-600,600])
        plotSonogram.setLimits(xMin= -10)
        self.verticalLayout_3.addWidget(plotSonogram)

        #QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def fileName(self):
        wave = QFileDialog.getOpenFileName(caption='Wczytaj dzwiek',directory='F:/UKSW/V sem/Moje/CPS/Spektogram/', filter = "Music(*.wav)", options=QFileDialog.DontUseNativeDialog)

        if wave == ('', ''):
            print(wave)
            QMessageBox.information(None,'Informacja',"Nie wczytales dzwieku.",QMessageBox.Ok)

        else:
            self.nameFileWave = wave[0]
            print(self.nameFileWave)


    def filePlay(self):

        if self.nameFileWave == "":
            QMessageBox.information(None,'Informacja','Nie został wczytany żaden dźwięk.',QMessageBox.Ok)
        else:
            if self.radioButtonCalosc.isChecked() == True:
                print("Calosc")

                if self.pause == False:
                    pygame.mixer.music.load(self.nameFileWave)
                    pygame.mixer.music.play()
                    print("NIE uruchomiona  pauza")

                else:
                    pygame.mixer.music.unpause()
                    self.pause = False

            else:
                print("Fragment")

    def filePause(self):
        if self.nameFileWave == "":
            QMessageBox.information(None,'Informacja','Nie został wczytany żaden dźwięk.',QMessageBox.Ok)
        else:
            pygame.mixer.music.pause()
            self.pause = True
            print('Pause')

    def fileStop(self):
        if self.nameFileWave == "":
            QMessageBox.information(None,'Informacja','Nie został wczytany żaden dźwięk.',QMessageBox.Ok)
        else:
            pygame.mixer.music.stop()
            self.pause = False
            print("Stop")

if __name__ == "__main__":
    def run():

        pygame.init()
        app = QApplication(sys.argv)
        window=QMainWindow()

        gui = Ui_MainWindow()
        gui.setupUi(window)
        window.show()
        sys.exit(app.exec_())

run()