from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt,QUrl,QTimer
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtWebEngineWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import io
import folium
import datetime
import numpy as np
import sys,shutil,os
import random


sicaklikveri = 0
Basincveri = 0
Yukseklikveri = 0
Voltajveri = 0
gpsenlemveri = 0
gpsboylamveri = 0
hizveri = 0
paketbilgisi = ["[20:54:32] -> Veri paketi alındı.","[20:54:33] -> Veri paketi işlendi.","...","...","[21:01:23] -> Veriler kaydedildi."]
sicaklikbilgi = ["0,1","1,4","2,5","3,20"]


class Window(QWidget):

    def __init__(self):

        app = QApplication(sys.argv)  # !!! 1
        super().__init__()

        self.setGeometry(0,0,1920,1080)
        self.setWindowTitle("Apeiron Space Technologies - Yer İstasyonu - Kocaeli Üniversitesi")
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("background-color:#77AFA2;")

        # rgb(119,175,162)

        tabwidget = QTabWidget()
        tabwidget.setStyleSheet("background-color:#77AFA2;border:None;QTab-color:#000000")

        tabwidget.addTab(Anasekme(),"Genel Panel")
        tabwidget.addTab(Yansekme(),"Sensör Panelleri")

        vbox = QVBoxLayout()
        vbox.addWidget(tabwidget)

        self.setLayout(vbox)

        self.show()



        sys.exit(app.exec())  # !!! 2



class Anasekme(QWidget):
    def __init__(self):
        super().__init__()


        self.qSplitter()


    def qSplitter(self):
        hbox = QHBoxLayout(self)

        left = QFrame(self)
        left.setFrameShape((QFrame.StyledPanel))

        right = QFrame(self)
        right.setFrameShape((QFrame.StyledPanel))

        grid = QGridLayout(left)
        grid.addWidget(self.bilgigrid(),0,0)
        grid.addWidget(self.CanliPanel(),1,0)
        grid.addWidget(self.init_ui(),2,0)
        grid = QGridLayout(right)
        grid.addWidget(self.grafikler(),0,0)


        hbox.addWidget(left)
        hbox.addWidget(right)

        self.setLayout(hbox)


    def createButton(self):

        groupBox = QGroupBox("Buttons")
        button1 = QPushButton("Button1")
        button2 = QPushButton("Button2")
        button3 = QPushButton("Button3")

        vbox = QVBoxLayout()
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        vbox.addWidget(button3)



        groupBox.setLayout(vbox)

        return groupBox
    #-------------------------------------------------------------------------------------------------------------------
    #       GENEL BİLGİ KISMI
    #-------------------------------------------------------------------------------------------------------------------
    def bilgigrid(self):

        groupBox = QGroupBox("Takım ve Konteynır Bilgileri")
        groupBox.setStyleSheet("background-color: #B8E6DB;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: gray;")

        hbox = QHBoxLayout()
        #vbox1 = QVBoxLayout()
        #vbox2 = QVBoxLayout()
        #hbox.addLayout(vbox1)
        #hbox.addLayout(vbox2)

        #vbox1.addWidget(self.logo())
        #vbox2.addWidget(self.Programkapat())
        #vbox2.addWidget(self.KonteyniriAyir())
        hbox.addWidget(self.logo())
        hbox.addWidget(self.ProgramKapat())
        hbox.addWidget(self.KonteyniriAyir())
        hbox.addWidget(self.GenelBilgiTablosu())
        hbox.addWidget(self.Vericiktisialma())
        hbox.addWidget(self.Testler())


        groupBox.setLayout(hbox)

        return groupBox

    def logo(self):

        logolbl = QLabel(self)
        logolbl.setGeometry(50,50,256,256)
        logolbl.setStyleSheet("background-color:#B8E6DB;")
        pixmap = QPixmap('pp.png')
        smaller_pixmap = pixmap.scaled(256,256, Qt.KeepAspectRatio, Qt.FastTransformation)
        logolbl.setPixmap(smaller_pixmap)
        logolbl.show()

    def ProgramKapat(self):
        programkapatbutton = QPushButton("Programı Kapat",self)
        programkapatbutton.setStyleSheet("background-color:#77AFA2;color:#FDFDFD;font-weight:bold")
        programkapatbutton.move(331,50)
        self.programkapat_bilgi = QLabel("Program Çalışıyor", self)
        self.programkapat_bilgi.move(331, 85)
        self.programkapat_bilgi.resize(100, 30)
        self.programkapat_bilgi.setStyleSheet("background-color: lightgreen;"
                                             "font: 11px;"
                                             "border-style: outset;"
                                             "border-width: 1px;"
                                             "border-color: black;")
        programkapatbutton.clicked.connect(self.ProgramKapatFunct)

    def ProgramKapatFunct(self):
        exit()



    def KonteyniriAyir(self):

        konteyniri_ayir = QPushButton("Konteynırı Ayır",self)
        konteyniri_ayir.setStyleSheet("background-color:#77AFA2;color:#FDFDFD;font-weight:bold;")
        konteyniri_ayir.move(441,50)
        self.konteyniri_ayir_bilgi = QLabel(" ", self)
        self.konteyniri_ayir_bilgi.setStyleSheet("background-color:#B8E6DB;")

        self.konteyniri_ayir_bilgi.move(441, 85)
        konteyniri_ayir.clicked.connect(self.KonteyniriAyirFunct)

    def KonteyniriAyirFunct(self):

        #Burada Konteynırın ayrıldığı bilgisi gelecek.
        self.konteyniri_ayir_bilgi.setText("Konyetnır Ayrıldı!")
        self.konteyniri_ayir_bilgi.resize(100,30)
        self.konteyniri_ayir_bilgi.setStyleSheet("background-color: lightcyan;"
                                                 "font: 12px;"
                                                 "border-style: outset;"
                                                 "border-width: 1px;"
                                                 "border-color: black;")

    def Vericiktisialma(self):

        vericiktisial = QPushButton("Verileri Kaydet",self)
        vericiktisial.setStyleSheet("background-color:#77AFA2;color:#FDFDFD;font-weight:bold;")
        vericiktisial.move(551,50)
        vericiktisial.resize(130, 30)
        self.vericiktisial_bilgi = QLabel(" ", self)
        self.vericiktisial_bilgi.setStyleSheet("background-color:#B8E6DB;")

        self.vericiktisial_bilgi.move(551,85)
        vericiktisial.clicked.connect(self.Vericiktisialmafunk)

    def Vericiktisialmafunk(self):
        global paketbilgisi

        veri_dosya = open("veri_kaydı.txt","w")
        for i in paketbilgisi:
            veri_dosya.write(i + "\n")
        veri_dosya.close()

        # Burada Veri Çıktışını kaydetme bilgisi gelecek.
        self.vericiktisial_bilgi.setText("Veri Çıktısı Alındı!")
        self.vericiktisial_bilgi.resize(130, 30)
        self.vericiktisial_bilgi.setStyleSheet("background-color: lightcyan;"
                                                 "font: 12px;"
                                                 "border-style: outset;"
                                                 "border-width: 1px;"
                                                 "border-color: black;")


    def GenelBilgiTablosu(self):

        self.table = QTableWidget(self)
        self.table.setStyleSheet("background-color:#FFFFFF;")

        self.table.setRowCount(3)
        self.table.setColumnCount(2)
        self.table.move(725, 31)
        self.table.resize(202, 285)

        self.table.verticalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.verticalHeader().hide()

        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Parametreler"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Değerler"))

        self.table.setItem(0, 0, QTableWidgetItem("Takım NO:"))
        self.table.setItem(0, 1, QTableWidgetItem(" - "))
        self.table.setItem(1, 0, QTableWidgetItem("Paket NO:"))
        self.table.setItem(1, 1, QTableWidgetItem(" - "))
        self.table.setItem(2, 0, QTableWidgetItem("Video Durumu:"))
        self.table.setItem(2, 1, QTableWidgetItem("BEKLEMEKTE"))

    def Testler(self):

        sistem_test = QPushButton("Sistem Testi", self)
        buzzer_test = QPushButton("Buzzer Testi", self)
        haberlesme_test = QPushButton("Haberleşme Testi", self)
        kalibrasyon = QPushButton("Kalibrasyon", self)

                                          #.move(331, 50)       #.move(441,50)      .move(551,50)
                                                                #.move(441, 85)     .move(551,85)

        sistem_test.move(331, 120)
        sistem_test.setStyleSheet("background-color:#77AFA2;color:#FDFDFD;font-weight:bold;")
        self.sistem_test_bilgi = QLabel("Sistem Testi Başarılı", self)
        self.sistem_test_bilgi.setStyleSheet("background-color:#B8E6DB;")
        self.sistem_test_bilgi.move(331, 155)
        self.sistem_test_bilgi.resize(100, 30)
        self.sistem_test_bilgi.setStyleSheet("background-color: lightcyan;"
                                             "font: 11px;"
                                             "border-style: outset;"
                                             "border-width: 1px;"
                                             "border-color: black;")

        buzzer_test.move(441, 120)
        buzzer_test.setStyleSheet("background-color:#77AFA2;color:#FDFDFD;font-weight:bold;")
        self.buzzer_test_bilgi = QLabel("Buzzer Testi Başarılı ", self)
        self.buzzer_test_bilgi.setStyleSheet("background-color:#B8E6DB;")
        self.buzzer_test_bilgi.move(441, 155)
        self.buzzer_test_bilgi.resize(100, 30)
        self.buzzer_test_bilgi.setStyleSheet("background-color: lightcyan;"
                                             "font: 11px;"
                                             "border-style: outset;"
                                             "border-width: 1px;"
                                             "border-color: black;")

        haberlesme_test.move(551, 120)
        haberlesme_test.resize(130, 30)
        haberlesme_test.setStyleSheet("background-color:#77AFA2;color:#FDFDFD;font-weight:bold;")
        self.haberlesme_test_bilgi = QLabel("Haberleşme Testi Başarılı ", self)
        self.haberlesme_test_bilgi.setStyleSheet("background-color:#B8E6DB;")
        self.haberlesme_test_bilgi.move(551, 155)
        self.haberlesme_test_bilgi.resize(130, 30)
        self.haberlesme_test_bilgi.setStyleSheet("background-color: lightcyan;"
                                             "font: 11px;"
                                             "border-style: outset;"
                                             "border-width: 1px;"
                                             "border-color: black;")

        kalibrasyon.move(331, 190)
        kalibrasyon.setStyleSheet("background-color:#77AFA2;color:#FDFDFD;font-weight:bold;")
        self.kalibrasyon_bilgi = QLabel("Kalibrasyon Başarılı ", self)
        self.kalibrasyon_bilgi.setStyleSheet("background-color:#B8E6DB;")
        self.kalibrasyon_bilgi.move(331, 225)
        self.kalibrasyon_bilgi.resize(100, 30)
        self.kalibrasyon_bilgi.setStyleSheet("background-color: lightcyan;"
                                             "font: 11px;"
                                             "border-style: outset;"
                                             "border-width: 1px;"
                                             "border-color: black;")

    #-------------------------------------------------------------------------------------------------------------------
    #       CANLI PANEL KISMI
    #-------------------------------------------------------------------------------------------------------------------

    def CanliPanel(self):
        groupBox = QGroupBox("Canlı Panel")
        groupBox.setStyleSheet("background-color: #B8E6DB;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: gray;")
        hbox = QHBoxLayout()


        hbox.addWidget(self.CanliPanelSicaklik())
        hbox.addWidget(self.CanliPanelBasinc())
        hbox.addWidget(self.CanliPanelYukseklik())
        hbox.addWidget(self.CanliPanelVoltaj())
        hbox.addWidget(self.CanliPanelGPS())
        hbox.addWidget(self.CanliPanelHiz())
        hbox.addWidget(self.CanliPanelPaket())


        groupBox.setLayout(hbox)
        return groupBox


    def CanliPanelSicaklik(self):

        global sicaklikveri
        SicaklikLabel = QLabel("Sıcaklık Bilgisi (°C)",self)

        SicaklikDegerLabel = QLabel(str(sicaklikveri)+" °C",self)


        SicaklikLabel.move(50,375)
        SicaklikLabel.resize(110,30)
        SicaklikLabel.setStyleSheet("background-color:#B8E6DB; Font: 14px;")

        SicaklikDegerLabel.move(50,405)
        SicaklikDegerLabel.setAlignment(Qt.AlignCenter)
        SicaklikDegerLabel.setStyleSheet("background-color: black;"
                                         "color: white;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: gray;")

    def CanliPanelBasinc(self):

        global Basincveri
        BasincLabel = QLabel("Basınç Bilgisi (Pa)", self)
        BasincDegerLabel = QLabel(str(Basincveri) + " Pa", self)

        BasincLabel.move(200, 375)
        BasincLabel.resize(110, 30)
        BasincLabel.setStyleSheet("background-color:#B8E6DB; Font: 14px;")

        BasincDegerLabel.move(200, 405)
        BasincDegerLabel.setAlignment(Qt.AlignCenter)
        BasincDegerLabel.setStyleSheet("background-color: black;"
                                       "color: white;"
                                       "border-style: outset;"
                                       "border-width: 2px;"
                                       "border-color: gray;")

    def CanliPanelYukseklik(self):

        global Yukseklikveri
        YukseklikLabel = QLabel("Yükseklik Bilgisi (km)", self)
        YukseklikDegerLabel = QLabel(str(Yukseklikveri) + " km", self)

        YukseklikLabel.move(350, 375)
        YukseklikLabel.resize(110, 30)
        YukseklikLabel.setStyleSheet("background-color:#B8E6DB; Font: 14px;")

        YukseklikDegerLabel.move(350, 405)
        YukseklikDegerLabel.setAlignment(Qt.AlignCenter)
        YukseklikDegerLabel.setStyleSheet("background-color: black;"
                                          "color: white;"
                                          "border-style: outset;"
                                          "border-width: 2px;"
                                          "border-color: gray;")

    def CanliPanelVoltaj(self):

        global Voltajveri
        VoltajLabel = QLabel("Voltaj Bilgisi (V)", self)
        VoltajDegerLabel = QLabel(str(Voltajveri) + " V", self)

        VoltajLabel.move(50, 475)
        VoltajLabel.resize(110, 30)
        VoltajLabel.setStyleSheet("background-color:#B8E6DB; Font: 14px;")

        VoltajDegerLabel.move(50, 505)
        VoltajDegerLabel.setAlignment(Qt.AlignCenter)
        VoltajDegerLabel.setStyleSheet("background-color: black;"
                                       "color: white;"
                                       "border-style: outset;"
                                       "border-width: 2px;"
                                       "border-color: gray;")

    def CanliPanelGPS(self):

        global gpsenlemveri, gpsboylamveri

        enlemLabel = QLabel("GPS Bilgisi(Enlem)", self)
        enlemDegerLabel = QLabel(str(gpsenlemveri), self)

        enlemLabel.move(200, 475)
        enlemLabel.resize(110, 30)
        enlemLabel.setStyleSheet("background-color:#B8E6DB; Font: 14px;")

        enlemDegerLabel.move(200, 505)
        enlemDegerLabel.setAlignment(Qt.AlignCenter)
        enlemDegerLabel.setStyleSheet("background-color: black;"
                                       "color: white;"
                                       "border-style: outset;"
                                       "border-width: 2px;"
                                       "border-color: gray;")

        boylamLabel = QLabel("GPS Bilgisi(Boylam)", self)
        boylamDegerLabel = QLabel(str(gpsboylamveri), self)

        boylamLabel.move(350, 475)
        boylamLabel.resize(115, 30)
        boylamLabel.setStyleSheet("background-color:#B8E6DB; Font: 14px;")

        boylamDegerLabel.move(350, 505)
        boylamDegerLabel.setAlignment(Qt.AlignCenter)
        boylamDegerLabel.setStyleSheet("background-color: black;"
                                       "color: white;"
                                       "border-style: outset;"
                                       "border-width: 2px;"
                                       "border-color: gray;")

    def CanliPanelHiz(self):

        global hizveri

        hizLabel = QLabel("Hız Bilgisi (m/s)", self)
        hizDegerLabel = QLabel(str(gpsenlemveri) + " m/s", self)

        hizLabel.move(200, 555)
        hizLabel.resize(110, 30)
        hizLabel.setStyleSheet("background-color:#B8E6DB; Font: 14px;")

        hizDegerLabel.move(200, 585)
        hizDegerLabel.setAlignment(Qt.AlignCenter)
        hizDegerLabel.setStyleSheet("background-color: black;"
                                      "color: white;"
                                      "border-style: outset;"
                                      "border-width: 2px;"
                                      "border-color: gray;")

    def CanliPanelPaket(self):

        global paketbilgisi

        self.paketliste = QListWidget(self)
        self.paketliste.setStyleSheet("background-color:#FFFFFF;")

        self.paketliste.move(500,375)
        self.paketliste.resize(400,200)


        for i in paketbilgisi:
            self.paketliste.addItem(i)

        buton = QPushButton("Seçilen Paket Verilerine Git",self)
        buton.setStyleSheet("background-color:#77AFA2;color:#FDFDFD;font-weight:bold;")
        buton.move(600,585)
        buton.resize(200,30)
        buton.clicked.connect(self.CanliPanelPaketeGit)

    def CanliPanelPaketeGit(self):
        for item in self.paketliste.selectedItems():
            print("Secilen Paket:",item.text(),"     (HENÜZ TAMAMLANMADI!)")            #BU KISIM DEĞİŞECEK
    #-------------------------------------------------------------------------------------------------------------------
    #       VİDEO PANEL KISMI
    #-------------------------------------------------------------------------------------------------------------------

    def init_ui(self):

        groupBox = QGroupBox("Video Panel")
        groupBox.setStyleSheet("background-color: #B8E6DB;"
                               "color: black;"
                               "border-style: outset;"
                               "border-width: 2px;"
                               "border-color: gray;")
        hbox = QHBoxLayout()

        hbox.addWidget(self.mediaplayerobject())
        hbox.addWidget(self.openbuttonmedia())
        hbox.addWidget(self.playingbuttonmedia())
        hbox.addWidget(self.slidermedia())
        hbox.addWidget(self.VideoAktarımButon())

        groupBox.setLayout(hbox)
        return groupBox


    def mediaplayerobject(self):
        #create media player object
        self.mediaplayer = QMediaPlayer(None,QMediaPlayer.VideoSurface)
        # self.mediaplayer.setStyleSheet("background-color:#B8E6DB;")


        #create videowidget object
        videowidget = QVideoWidget(self)
        videowidget.setStyleSheet("background-color:#CCF6EC;")

        videowidget.move(300,675)
        videowidget.resize(240,240)

        self.mediaplayer.setVideoOutput(videowidget)

        # media player signals
        self.mediaplayer.stateChanged.connect(self.mediastate_changed)
        self.mediaplayer.positionChanged.connect(self.position_changed)
        self.mediaplayer.durationChanged.connect(self.duration_changed)

    def openbuttonmedia(self):
        #create open button
        openBtn = QPushButton("Open Video",self)
        openBtn.setStyleSheet("background-color:#77AFA2;color:#FDFDFD;font-weight:bold;")

        self.adressvideolist = QListWidget(self)
        self.adressvideolist.setStyleSheet("background-color:#FFFFFF;")

        self.adressvideolist.move(25, 735)
        self.adressvideolist.resize(250, 75)
        openBtn.clicked.connect(self.open_file)
        openBtn.move(25,675)
        openBtn.resize(75,25)

    def playingbuttonmedia(self):
        #create button for playing
        self.playBtn = QPushButton(self)
        self.playBtn.setStyleSheet("background-color:#77AFA2;color:#FDFDFD;font-weight:bold;")

        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
        self.playBtn.move(100,675)
        self.playBtn.resize(50,25)

    def slidermedia(self):
        #create slider
        self.slider = QSlider(Qt.Horizontal,self)
        self.slider.setStyleSheet("background-color:#B8E6DB;")

        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)
        self.slider.move(25,705)
        self.slider.resize(250,25)

    def VideoAktarımButon(self):

        videoaktar = QPushButton("Videoyu Aktar",self)
        videoaktar.setStyleSheet("background-color:#77AFA2;color:#FDFDFD;font-weight:bold;")

        videoaktar.move(25,835)
        self.videoaktar_bilgi = QLabel(" ", self)
        self.videoaktar_bilgi.setStyleSheet("background-color:#B8E6DB;")
        self.videoaktar_bilgi.move(130,835)
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(25, 875, 250, 25)
        videoaktar.clicked.connect(self.videoaktarfunc)

    def videoaktarfunc(self):

        kaynak = "C:\\Users\\Onur\\Desktop\\Ours d'Or\\ÇALIŞMALAR VE PROJELER\\APEİRON SPACE TECHNOLOGİES\\TURKSAT 2020\\1 Öğrenme Aşaması\\deneme.mp4"
        hedef = "C:\\Users\\Onur\\Desktop\\Ours d'Or\\ÇALIŞMALAR VE PROJELER\\APEİRON SPACE TECHNOLOGİES\\TURKSAT 2020\\2 Deneme"
        if not os.path.exists(hedef):
            os.makedirs(hedef)

        shutil.copy(kaynak,hedef)


        self.pbar.setValue(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.handleTimer)
        self.timer.start(43)


    def handleTimer(self):
        value = self.pbar.value()
        if value < 100:
            value = value + 1
            self.pbar.setValue(value)

        else:
            self.timer.stop()
            # Burada Veri Çıktışını kaydetme bilgisi gelecek.
            self.videoaktar_bilgi.setText("Video Aktarıldı!")
            self.videoaktar_bilgi.resize(100, 30)
            self.videoaktar_bilgi.setStyleSheet("background-color: lightcyan;"
                                                "font: 12px;"
                                                "border-style: outset;"
                                                "border-width: 1px;"
                                                "border-color: black;")


    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self,"Open Video")
        if filename != '':
            self.mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
            self.adressvideolist.addItem(filename)

    def play_video(self):
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            self.mediaplayer.pause()

        else:
            self.mediaplayer.play()

    def mediastate_changed(self, state):
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.slider.setValue(position)


    def duration_changed(self,duration):
        self.slider.setRange(0,duration)


    def set_position(self, position):
        self.mediaplayer.setPosition(position)


    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error:" + self.mediaplayer.errorString())

    #-------------------------------------------------------------------------------------------------------------------
    #       GRAFİK PANEL KISMI
    # -------------------------------------------------------------------------------------------------------------------

    def grafikler(self):

        groupBox = QGroupBox("Grafikler")
        groupBox.setStyleSheet("background-color: #B8E6DB;"
                               "color: black;"
                               "border-style: outset;"
                               "border-width: 2px;"
                               "border-color: gray;")

        self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.static_ax = self.static_canvas.figure.subplots()
        ys = (2 * np.random.random_sample(20) + 5)*10
        xs = np.linspace(0, 40, 20)
        # xs, ys = self.animate()
        self.static_ax.set_ylabel('Sıcaklık (°C)')
        self.static_ax.set_xlabel('')  # X-Legend'i gözükmüyor. Sıkıştı.
        self.static_ax.set_title('Sıcaklık Grafiği')
        self.static_ax.plot(xs, ys)
        # self.static_ax.legend()

        self.static_canvas2 = FigureCanvas(Figure(figsize=(5, 3)))
        self.static_ax2 = self.static_canvas2.figure.subplots()
        t = np.linspace(0, 10, 50)
        ttan = np.linspace(0,10,50)
        tant = np.abs(np.tan(ttan)) + 30
        tant[23] = 45.23534646
        tant[8] = 46.14576432
        tant[32] = 44.08032885
        tant[33] = 42.47042589

        self.static_ax2.set_ylabel('Basınc (Pa)')
        self.static_ax2.set_title('Basınç Grafiği')
        self.static_ax2.plot(t, tant)

        self.static_canvas3 = FigureCanvas(Figure(figsize=(5, 3)))
        self.static_ax3 = self.static_canvas3.figure.subplots()
        t = np.linspace(0, 10, 25)
        ttant = np.linspace(0, 20, 25)
        tant = np.abs(np.tan(ttant)) + 3
        tant[2] = 3.23445623
        tant[13] = 5.12004233
        tant[17] = 4.76453745
        tant[21] = 5.52033456

        # for i in tant :
        #     if tant[i]<0.1:
        #         tant[i] = tant[i-1]


        self.static_ax3.set_ylabel('Voltaj (V)')
        self.static_ax3.set_title('Voltaj Grafiği')
        self.static_ax3.plot(t, tant )

        # self.static_canvas4 = FigureCanvas(Figure(figsize=(5, 3)))
        # self.static_ax4 = self.static_canvas4.figure.subplots()
        # t = np.linspace(0, 10, 501)
        # self.static_ax4.set_title('static_canvas4')
        # self.static_ax4.plot(t, np.tan(t), ".")

        self.dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))  # real-time yapabildim.
        self.dynamic_ax = self.dynamic_canvas.figure.subplots()
        self._timer = self.dynamic_canvas.new_timer(50, [(self.update_canvasanasekme, (), {})])
        self._timer.start()

        # x3d = np.linspace(0, 10, 501)
        # y3d = np.linspace(0, 10, 501)
        # x3d, y3d = np.meshgrid(x3d, y3d)
        # z3d = np.sin(x3d)

        # N = 100
        # X = np.random.uniform(-1, 1, N)
        # Y = np.random.uniform(-1, 1, N)
        # Z = np.random.uniform(-2, 2, N)

        # Cylinder
        x = np.linspace(-1, 1, 1000)
        z = np.linspace(-2, 2, 1000)
        Xc, Zc = np.meshgrid(x, z)
        Yc = np.sqrt(1 - Xc ** 2)

        self.fig = Figure(figsize=(5, 3))
        self.canvas3d = FigureCanvas(self.fig)
        self.canvas3d_axe = self.fig.add_subplot(1, 1, 1, projection='3d')
        self.canvas3d_axe.set_ylabel('Y')
        self.canvas3d_axe.set_xlabel('X')
        self.canvas3d_axe.set_zlabel('Z')
        self.canvas3d_axe.set_title('3D Duruş Grafiği')
        self.canvas3d_axe.plot_surface(Xc, Yc, Zc, color="r")
        self.canvas3d_axe.plot_surface(Xc, -Yc, Zc, color="r")
        self.canvas3d_axe.set_ylim([-2, 2])
        self.canvas3d_axe.set_xlim([-2, 2])



        self.static_canvas4 = FigureCanvas(Figure(figsize=(5, 3)))
        self.static_ax4 = self.static_canvas4.figure.subplots()
        tt = [0, 1, 2, 3, 4, 5, 6]
        self.static_ax4.set_ylabel('Hız (m/s)')
        self.static_ax4.set_title('Hız Grafiği')
        self.static_ax4.plot(tt, np.tan(tt))

        ylimmin = 0
        ylimmax = 10
        xlimmin = 0
        xlimmax = 10
        self.static_canvas5 = FigureCanvas(Figure(figsize=(5, 3)))
        self.static_ax5 = self.static_canvas5.figure.subplots()
        x = [0, 2, 4, 6, 8, 10, 12]
        y = [6, 5, 4, 3, 2, 1, 0]
        self.static_ax5.set_ylabel('Yükseklik (km)')
        self.static_ax5.set_title('Yükseklik Grafiği')
        self.static_ax5.plot(x, y)
        self.static_ax5.set_ylim([ylimmin,ylimmax])
        self.static_ax5.set_xlim([xlimmin,xlimmax])

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox1.addWidget(self.static_canvas)
        hbox1.addWidget(self.dynamic_canvas)
        hbox2.addWidget(self.static_canvas2)
        hbox2.addWidget(self.static_canvas5)
        hbox3.addWidget(self.static_canvas3)
        hbox3.addWidget(self.canvas3d)
        # hbox4.addWidget(self.static_canvas4)
        # hbox4.addWidget(self.dynamic_canvas)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        groupBox.setLayout(vbox)

        return groupBox



    def update_canvasanasekme(self):
        # self.dynamic_ax.clear()
        # t = np.linspace(0, 10, 101)
        #
        # self.dynamic_ax.set_ylim(-1.1, 1.1)
        #
        # self.dynamic_ax.plot(t, np.sin(t + time.time()))
        # self.dynamic_ax.figure.canvas.draw()

        graph_data = open('example.txt', 'r').read()
        lines = graph_data.split('\n')
        xs = []
        ys = []
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(x)
                ys.append(y)
        self.dynamic_ax.clear()
        self.dynamic_ax.set_title('Hız Grafiği')
        self.dynamic_ax.plot(xs, ys)
        self.dynamic_ax.figure.canvas.draw()

    def animate(self):
        graph_data = open('example.txt', 'r').read()
        lines = graph_data.split('\n')
        xs = []
        ys = []
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(x)
                ys.append(y)
        return xs, ys






class Yansekme(QWidget):
    def __init__(self):
        super().__init__()

        self.sekmeler()


    def sekmeler(self):     #Bu kısım yerine class oluşturarak sekmeleri açıyoruz.
        mainlayout = QVBoxLayout()
        self.tab = QTabWidget()
        # self.tab1 = QWidget()
        # self.tab2 = QWidget()
        # self.tab3 = QWidget()

        self.tab.addTab(SicaklikSekme(), "Sıcaklık")
        self.tab.addTab(BasincSekme(), "Basınç")
        self.tab.addTab(YukseklikSekme(), "Yükseklik")
        self.tab.addTab(VoltajSekme(), "Voltaj")
        self.tab.addTab(HızSekme(), "Hız")
        self.tab.addTab(altsekme(), "Third")
        self.tab.addTab(HaritaSekme(), "Harita")


        mainlayout.addWidget(self.tab)

        self.setLayout(mainlayout)

class SicaklikSekme(QWidget):
    def __init__(self):
        super().__init__()

        self.SicaklikGenelBilgi()

    def SicaklikGenelBilgi(self):
        global paketbilgisi
# Liste
        self.sicaklikliste = QListWidget(self)
        self.sicaklikliste.setStyleSheet("background-color:#FFFFFF;")

        self.sicaklikliste.move(20, 20)
        self.sicaklikliste.resize(600, 800)

        for i in paketbilgisi:
            self.sicaklikliste.addItem(i)
# Grafik
        self.sicaklikgrafik = FigureCanvas(Figure(figsize=(10, 20)))  # real-time yapabildim.
        self.sicaklik_ax = self.sicaklikgrafik.figure.subplots()
        self._timer = self.sicaklikgrafik.new_timer(50, [(self.update_canvassicaklik, (), {})])
        self.sicaklikgrafik.mpl_connect("button_press_event", self.on_press)
        self._timer.start()
# Layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.sicaklikliste)
        hbox.addWidget(self.sicaklikgrafik)
        self.setLayout(hbox)


#Grafik verilerini eklediğim yer.

# '''
# Burada yapılması gereken:
# 1) ylim ve xlim leri gelen verilerden çekip en küçükten en büyüğe sıralamasını hallet.
# 2) ylim sıralaması için küçük bir algoritma yaz.
# 3) bu kadar.
# '''
    def update_canvassicaklik(self):

        graph_data = open('example.txt', 'r').read()
        lines = graph_data.split('\n')
        xs = []
        ys = []
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(x)
                ys.append(y)

        ylimmin = 0
        ylimmax = 20
        self.sicaklik_ax.clear()
        self.sicaklik_ax.set_ylim([ylimmin,ylimmax])
        self.sicaklik_ax.set_title('dynamic_canvas')
        self.sicaklik_ax.plot(xs, ys)
        self.sicaklik_ax.figure.canvas.draw()
#Fare tıklamasını algıladığı yer
    def on_press(self, event):

        self.sicaklikliste.addItem(str("["+str(datetime.datetime.now())+"]"+" PaketNo: "+str(int(event.xdata))+" SicaklikDeğeri: "+str(int(event.ydata))))
        # print("X:", int(event.xdata))             #Bu iki satırı silme kalsın.
        # print("Y:", int(event.ydata))

class BasincSekme(QWidget):
    def __init__(self):
        super().__init__()

        self.BasincGenelBilgi()

    def BasincGenelBilgi(self):
        global paketbilgisi
# Liste
        self.basincliste = QListWidget(self)
        self.basincliste.setStyleSheet("background-color:#FFFFFF;")

        self.basincliste.move(20, 20)
        self.basincliste.resize(600, 800)

        for i in paketbilgisi:
            self.basincliste.addItem(i)
# Grafik
        self.basincgrafik = FigureCanvas(Figure(figsize=(10, 20)))  # real-time yapabildim.
        self.basinc_ax = self.basincgrafik.figure.subplots()
        self._timer = self.basincgrafik.new_timer(50, [(self.update_canvas_basinc, (), {})])
        self.basincgrafik.mpl_connect("button_press_event", self.on_press)
        self._timer.start()
# Layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.basincliste)
        hbox.addWidget(self.basincgrafik)
        self.setLayout(hbox)


#Grafik verilerini eklediğim yer.

# '''
# Burada yapılması gereken:
# 1) ylim ve xlim leri gelen verilerden çekip en küçükten en büyüğe sıralamasını hallet.
# 2) ylim sıralaması için küçük bir algoritma yaz.
# 3) bu kadar.
# '''
    def update_canvas_basinc(self):

        graph_data = open('example.txt', 'r').read()
        lines = graph_data.split('\n')
        xs = []
        ys = []
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(x)
                ys.append(y)

        ylimmin = 0
        ylimmax = 20
        self.basinc_ax.clear()
        self.basinc_ax.set_ylim([ylimmin,ylimmax])
        self.basinc_ax.set_title('dynamic_canvas')
        self.basinc_ax.plot(xs, ys)
        self.basinc_ax.figure.canvas.draw()
#Fare tıklamasını algıladığı yer
    def on_press(self, event):

        self.basincliste.addItem(str("["+str(datetime.datetime.now())+"]"+" PaketNo: "+str(int(event.xdata))+" SicaklikDeğeri: "+str(int(event.ydata))))
        # print("X:", int(event.xdata))             #Bu iki satırı silme kalsın.
        # print("Y:", int(event.ydata))

class HızSekme(QWidget):
    def __init__(self):
        super().__init__()

        self.HızGenelBilgi()

    def HızGenelBilgi(self):
        global paketbilgisi
# Liste
        self.hızliste = QListWidget(self)
        self.hızliste.setStyleSheet("background-color:#FFFFFF;")

        self.hızliste.move(20, 20)
        self.hızliste.resize(600, 800)

        for i in paketbilgisi:
            self.hızliste.addItem(i)
# Grafik
        self.hizgrafik = FigureCanvas(Figure(figsize=(10, 20)))  # real-time yapabildim.
        self.hiz_ax = self.hizgrafik.figure.subplots()
        self._timer = self.hizgrafik.new_timer(50, [(self.update_canvas_basinc, (), {})])
        self.hizgrafik.mpl_connect("button_press_event", self.on_press)
        self._timer.start()
# Layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.hızliste)
        hbox.addWidget(self.hizgrafik)
        self.setLayout(hbox)


#Grafik verilerini eklediğim yer.

# '''
# Burada yapılması gereken:
# 1) ylim ve xlim leri gelen verilerden çekip en küçükten en büyüğe sıralamasını hallet.
# 2) ylim sıralaması için küçük bir algoritma yaz.
# 3) bu kadar.
# '''
    def update_canvas_basinc(self):

        graph_data = open('example.txt', 'r').read()
        lines = graph_data.split('\n')
        xs = []
        ys = []
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(x)
                ys.append(y)

        ylimmin = 0
        ylimmax = 20
        self.hiz_ax.clear()
        self.hiz_ax.set_ylim([ylimmin,ylimmax])
        self.hiz_ax.set_title('dynamic_canvas')
        self.hiz_ax.plot(xs, ys)
        self.hiz_ax.figure.canvas.draw()
#Fare tıklamasını algıladığı yer
    def on_press(self, event):

        self.hızliste.addItem(str("["+str(datetime.datetime.now())+"]"+" PaketNo: "+str(int(event.xdata))+" SicaklikDeğeri: "+str(int(event.ydata))))
        # print("X:", int(event.xdata))             #Bu iki satırı silme kalsın.
        # print("Y:", int(event.ydata))


class VoltajSekme(QWidget):
    def __init__(self):
        super().__init__()

        self.VoltajGenelBilgi()

    def VoltajGenelBilgi(self):
        global paketbilgisi
# Liste
        self.voltajliste = QListWidget(self)
        self.voltajliste.setStyleSheet("background-color:#FFFFFF;")

        self.voltajliste.move(20, 20)
        self.voltajliste.resize(600, 800)

        for i in paketbilgisi:
            self.voltajliste.addItem(i)
# Grafik
        self.voltajgrafik = FigureCanvas(Figure(figsize=(10, 20)))  # real-time yapabildim.
        self.voltaj_ax = self.voltajgrafik.figure.subplots()
        self._timer = self.voltajgrafik.new_timer(50, [(self.update_canvas_basinc, (), {})])
        self.voltajgrafik.mpl_connect("button_press_event", self.on_press)
        self._timer.start()
# Layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.voltajliste)
        hbox.addWidget(self.voltajgrafik)
        self.setLayout(hbox)


#Grafik verilerini eklediğim yer.

# '''
# Burada yapılması gereken:
# 1) ylim ve xlim leri gelen verilerden çekip en küçükten en büyüğe sıralamasını hallet.
# 2) ylim sıralaması için küçük bir algoritma yaz.
# 3) bu kadar.
# '''
    def update_canvas_basinc(self):

        graph_data = open('example.txt', 'r').read()
        lines = graph_data.split('\n')
        xs = []
        ys = []
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(x)
                ys.append(y)

        ylimmin = 0
        ylimmax = 20
        self.voltaj_ax.clear()
        self.voltaj_ax.set_ylim([ylimmin,ylimmax])
        self.voltaj_ax.set_title('dynamic_canvas')
        self.voltaj_ax.plot(xs, ys)
        self.voltaj_ax.figure.canvas.draw()
#Fare tıklamasını algıladığı yer
    def on_press(self, event):

        self.voltajliste.addItem(str("["+str(datetime.datetime.now())+"]"+" PaketNo: "+str(int(event.xdata))+" SicaklikDeğeri: "+str(int(event.ydata))))
        # print("X:", int(event.xdata))             #Bu iki satırı silme kalsın.
        # print("Y:", int(event.ydata))



class YukseklikSekme(QWidget):
    def __init__(self):
        super().__init__()

        self.YukseklikGenelBilgi()

    def YukseklikGenelBilgi(self):
        global paketbilgisi
# Liste
        self.yukseklikliste = QListWidget(self)
        self.yukseklikliste.setStyleSheet("background-color:#FFFFFF;")

        self.yukseklikliste.move(20, 20)
        self.yukseklikliste.resize(600, 800)

        for i in paketbilgisi:
            self.yukseklikliste.addItem(i)
# Grafik
        self.yukseklikgrafik = FigureCanvas(Figure(figsize=(10, 20)))  # real-time yapabildim.
        self.yukseklik_ax = self.yukseklikgrafik.figure.subplots()
        self._timer = self.yukseklikgrafik.new_timer(50, [(self.update_canvas_yukseklik, (), {})])
        self.yukseklikgrafik.mpl_connect("button_press_event", self.on_press)
        self._timer.start()
# Layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.yukseklikliste)
        hbox.addWidget(self.yukseklikgrafik)
        self.setLayout(hbox)


#Grafik verilerini eklediğim yer.

# '''
# Burada yapılması gereken:
# 1) ylim ve xlim leri gelen verilerden çekip en küçükten en büyüğe sıralamasını hallet.
# 2) ylim sıralaması için küçük bir algoritma yaz.
# 3) bu kadar.
# '''
    def update_canvas_yukseklik(self):

        graph_data = open('example.txt', 'r').read()
        lines = graph_data.split('\n')
        xs = []
        ys = []
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(x)
                ys.append(y)

        ylimmin = 0
        ylimmax = 20
        self.yukseklik_ax.clear()
        self.yukseklik_ax.set_ylim([ylimmin,ylimmax])
        self.yukseklik_ax.set_title('dynamic_canvas')
        self.yukseklik_ax.plot(xs, ys)
        self.yukseklik_ax.figure.canvas.draw()
#Fare tıklamasını algıladığı yer
    def on_press(self, event):

        self.yukseklikliste.addItem(str("["+str(datetime.datetime.now())+"]"+" PaketNo: "+str(int(event.xdata))+" SicaklikDeğeri: "+str(int(event.ydata))))
        # print("X:", int(event.xdata))             #Bu iki satırı silme kalsın.
        # print("Y:", int(event.ydata))


class HaritaSekme(QWidget):
    def __init__(self):
        super().__init__()

        # self.haritaveri()

    def haritaveri(self):


        self.view = QtWebEngineWidgets.QWebEngineView()
        # self.view.setContentsMargins(600, 100, 50, 50)

        self.haritalist = QListWidget(self)
        self.haritalist.setStyleSheet("background-color:#FFFFFF;")

        # self.haritalist.move(20, 20)
        # self.haritalist.resize(600, 800)

        for i in paketbilgisi:
            self.haritalist.addItem(i)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.haritalist)
        hbox.addWidget(self.view)
        hbox.addStretch()
        self.setLayout(hbox)

        lon = 40.768840
        iloc = 29.918349
        name = str(lon) + " / " + str(iloc)

        m = folium.Map(
            location=[40.768840, 29.918349], tiles="OpenStreetMap", zoom_start=10,zoom_control=False, min_zoom=10,max_zoom=10)
        folium.Marker([lon, iloc], popup=name).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)
        self.view.setHtml(data.getvalue().decode())


class altsekme(QWidget):
    def __init__(self):
        super().__init__()
        buton = QPushButton("Butonum ben",self)






window = Window()
