import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QGroupBox, 
                             QVBoxLayout, QHBoxLayout, QSlider, QLabel)
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath

class Grzalka:
    def __init__(self, x, y, width=100, height=15):
        self.x = x; self.y = y; self.width = width; self.height = height
        self.moc = 0 

    def ustaw_moc(self, wartosc):
        self.moc = wartosc

    def draw(self, painter):
        if self.moc > 0: kolor = QColor(255, 50, 50) 
        else: kolor = Qt.white            
        
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(kolor)
        painter.drawRect(int(self.x), int(self.y), int(self.width), int(self.height))
        
        painter.setPen(Qt.black)
        font = painter.font(); font.setPointSize(8); painter.setFont(font)
        painter.drawText(int(self.x), int(self.y), int(self.width), int(self.height), 
                         Qt.AlignCenter, f"GRZAŁKA {self.moc}%")

class Chlodnica:
    def __init__(self, x, y, width=40, height=100):
        self.x = x; self.y = y; self.width = width; self.height = height
        self.moc = 0

    def ustaw_moc(self, wartosc):
        self.moc = wartosc

    def draw(self, painter):
        if self.moc > 0: kolor = QColor(0, 0, 139)       
        else: kolor = QColor(160, 160, 160)   
        
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(kolor)
        painter.drawRect(int(self.x), int(self.y), int(self.width), int(self.height))
        
        painter.setPen(QColor(255, 255, 255, 100))
        for i in range(1, 10):
            y_line = self.y + (self.height / 10) * i
            painter.drawLine(int(self.x), int(y_line), int(self.x + self.width), int(y_line))

        painter.setPen(Qt.white)
        painter.drawText(int(self.x), int(self.y), int(self.width), int(self.height), 
                         Qt.AlignCenter, f"{self.moc}%")

class Wskaznik:
    def __init__(self, x, y, zbiornik, label):
        self.x = x
        self.y = y
        self.zbiornik = zbiornik
        self.label = label
        self.radius = 25

    def draw(self, painter):
        jest_pelny = self.zbiornik.czy_pelny()
        
        if jest_pelny:
            fill_color = QColor(0, 255, 0)
            border_color = QColor(0, 100, 0)
        else:
            fill_color = QColor(80, 80, 80)
            border_color = QColor(50, 50, 50)

        painter.setPen(QPen(border_color, 3))
        painter.setBrush(fill_color)
        painter.drawEllipse(int(self.x), int(self.y), int(self.radius*2), int(self.radius*2))

        painter.setPen(Qt.white)
        font = painter.font(); font.setPointSize(10); font.setBold(True)
        painter.setFont(font)
        painter.drawText(int(self.x - 25), int(self.y - 25), int(self.radius*2 + 50), 20, 
                         Qt.AlignCenter, self.label)
        
        if jest_pelny:
            font.setPointSize(7); painter.setFont(font); painter.setPen(Qt.black)
            painter.drawText(int(self.x), int(self.y), int(self.radius*2), int(self.radius*2), 
                             Qt.AlignCenter, "FULL")

class Rura:
    def __init__(self, punkty, grubosc=12, kolor_rury=Qt.gray, kolor_medium=QColor(0, 180, 255)):
        self.punkty = [QPointF(float(p[0]), float(p[1])) for p in punkty]
        self.grubosc = grubosc
        self.kolor_rury = kolor_rury
        self.kolor_medium = kolor_medium
        self.czy_plynie = False

    def ustaw_przeplyw(self, plynie):
        self.czy_plynie = plynie

    def draw(self, painter):
        if len(self.punkty) < 2: return
        path = QPainterPath()
        path.moveTo(self.punkty[0])
        for p in self.punkty[1:]: path.lineTo(p)

        painter.setPen(QPen(self.kolor_rury, self.grubosc, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

        if self.czy_plynie:
            painter.setPen(QPen(self.kolor_medium, self.grubosc - 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawPath(path)

class Zbiornik:
    def __init__(self, x, y, width=100, height=140, nazwa="", typ="ciecz"):
        self.x = x; self.y = y
        self.width = width; self.height = height
        self.nazwa = nazwa
        self.typ = typ
        self.pojemnosc = 100.0
        self.aktualna_ilosc = 0.0
        self.poziom = 0.0

    def dodaj_ciecz(self, ilosc):
        wolne = self.pojemnosc - self.aktualna_ilosc
        dodano = min(ilosc, wolne)
        self.aktualna_ilosc += dodano
        self.aktualizuj_poziom()
        return dodano

    def usun_ciecz(self, ilosc):
        usunieto = min(ilosc, self.aktualna_ilosc)
        self.aktualna_ilosc -= usunieto
        self.aktualizuj_poziom()
        return usunieto

    def aktualizuj_poziom(self):
        self.poziom = self.aktualna_ilosc / self.pojemnosc

    def czy_pusty(self): return self.aktualna_ilosc <= 0.1
    def czy_pelny(self): return self.aktualna_ilosc >= self.pojemnosc - 0.1

    def punkt_gora_srodek(self): return (self.x + self.width/2, self.y)
    def punkt_dol_srodek(self): return (self.x + self.width/2, self.y + self.height)
    def punkt_lewa_gora(self): return (self.x, self.y + 20)
    def punkt_prawa_gora(self): return (self.x + self.width, self.y + 20)
    def punkt_lewa_dol(self): return (self.x, self.y + self.height - 20)
    def punkt_dol_prawa(self): return (self.x + self.width - 30, self.y + self.height)
    def punkt_dol_lewa(self): return (self.x + 30, self.y + self.height)

    def draw(self, painter):
        if self.poziom > 0:
            h_fill = self.height * self.poziom
            if self.typ == "ciecz":
                y_start = self.y + self.height - h_fill
                painter.setBrush(QColor(0, 120, 255, 200))
                painter.setPen(Qt.NoPen)
                painter.drawRect(int(self.x + 3), int(y_start), int(self.width - 6), int(h_fill - 2))
            elif self.typ == "para":
                y_start = self.y + 2
                painter.setBrush(QColor(200, 200, 200, 220))
                painter.setPen(Qt.NoPen)
                painter.drawRect(int(self.x + 3), int(y_start), int(self.width - 6), int(h_fill - 2))

        pen = QPen(Qt.white, 4); pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen); painter.setBrush(Qt.NoBrush)
        painter.drawRect(int(self.x), int(self.y), int(self.width), int(self.height))
        painter.setPen(Qt.white)
        painter.drawText(int(self.x), int(self.y - 10), self.nazwa)


class SymulacjaKaskady(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Symulacja: Panel Wskaźników")
        self.setFixedSize(1300, 650) 
        self.setStyleSheet("background-color: #222;")

        self.z1 = Zbiornik(150, 50, nazwa="Z1 (Źródło)", typ="ciecz")
        self.z2 = Zbiornik(400, 200, nazwa="Z2 (Bojler)", typ="ciecz")
        self.z3 = Zbiornik(700, 50, nazwa="Z3 (Para)", typ="para")
        self.z4 = Zbiornik(700, 350, nazwa="Z4 (Zlew)", typ="ciecz")
        self.zbiorniki = [self.z1, self.z2, self.z3, self.z4]

        self.wskazniki = []
        labels = ["Z1", "Z2", "Z3", "Z4"]
        base_y = 80
        step_y = 120
        for i, z in enumerate(self.zbiorniki):
            w = Wskaznik(1220, base_y + i * step_y, z, labels[i])
            self.wskazniki.append(w)

        self.grzalka = Grzalka(400, 345, width=100, height=20)
        self.chlodnica = Chlodnica(805, 70, width=40, height=100)

        self.wlot_otwarty = False
        self.wylot_otwarty = False

        p0_s = (-50, 70) 
        p0_e = self.z1.punkt_lewa_gora()
        self.rura_wlot = Rura([p0_s, p0_e])

        p1_s = self.z1.punkt_dol_srodek(); p1_e = self.z2.punkt_lewa_gora()
        self.rura1 = Rura([p1_s, (p1_s[0], p1_e[1]), p1_e])

        p2_s = self.z2.punkt_prawa_gora()
        p2_e = self.z3.punkt_lewa_dol()
        p2_m1 = (p2_s[0] + 50, p2_s[1])
        p2_m2 = (p2_m1[0], p2_e[1])
        self.rura2 = Rura([p2_s, p2_m1, p2_m2, p2_e], kolor_medium=QColor(200, 200, 200))

        p3_s = self.z3.punkt_dol_prawa()
        p3_e = self.z4.punkt_gora_srodek()
        self.rura3 = Rura([p3_s, (p3_s[0], p3_s[1] + 20), (p3_e[0], p3_s[1] + 20), p3_e])

        p4_s = self.z4.punkt_dol_prawa() 
        p4_out = (1180, p4_s[1]) 
        self.rura_wylot = Rura([p4_s, p4_out])

        self.rury = [self.rura_wlot, self.rura1, self.rura2, self.rura3, self.rura_wylot]

        self.timer = QTimer(); self.timer.timeout.connect(self.logika_przeplywu)
        self.setup_ui()
        self.running = False
        self.base_speed = 0.5

    def setup_ui(self):
        self.panel = QGroupBox("Centrum Sterowania", self)
        self.panel.setGeometry(150, 520, 750, 120) 
        self.panel.setStyleSheet("QGroupBox { color: white; font-weight: bold; border: 1px solid gray; } QLabel { color: #AAA; }")

        layout = QHBoxLayout()

        self.btn_start = QPushButton("START /\nSTOP")
        self.btn_start.setFixedSize(80, 80)
        self.btn_start.setStyleSheet("background-color: #444; color: white; font-weight: bold;")
        self.btn_start.clicked.connect(self.przelacz_sym)
        layout.addWidget(self.btn_start)

        layout.addSpacing(20)

        layout_valves = QVBoxLayout()
        self.btn_wlot = QPushButton("<<< WLOT DO Z1")
        self.btn_wlot.setCheckable(True)
        self.btn_wlot.setMinimumHeight(35)
        self.btn_wlot.setStyleSheet("QPushButton { background-color: #262; color: white; font-weight: bold; } QPushButton:checked { background-color: #4A4; }")
        self.btn_wlot.clicked.connect(self.toggle_wlot)
        layout_valves.addWidget(self.btn_wlot)

        self.btn_wylot = QPushButton("WYLOT Z Z4 >>>")
        self.btn_wylot.setCheckable(True)
        self.btn_wylot.setMinimumHeight(35)
        self.btn_wylot.setStyleSheet("QPushButton { background-color: #622; color: white; font-weight: bold; } QPushButton:checked { background-color: #A44; }")
        self.btn_wylot.clicked.connect(self.toggle_wylot)
        layout_valves.addWidget(self.btn_wylot)
        layout.addLayout(layout_valves)

        layout.addSpacing(40)

        layout_temp = QVBoxLayout()
        layout_g = QHBoxLayout()
        layout_g.addWidget(QLabel("Grzałka (Z2):"))
        self.slider_grzalka = QSlider(Qt.Horizontal)
        self.slider_grzalka.setRange(0, 100); self.slider_grzalka.setValue(0)
        self.slider_grzalka.valueChanged.connect(self.update_grzalka)
        layout_g.addWidget(self.slider_grzalka)
        layout_temp.addLayout(layout_g)

        layout_c = QHBoxLayout()
        layout_c.addWidget(QLabel("Chłodnica (Z3):"))
        self.slider_chlodnica = QSlider(Qt.Horizontal)
        self.slider_chlodnica.setRange(0, 100); self.slider_chlodnica.setValue(0)
        self.slider_chlodnica.valueChanged.connect(self.update_chlodnica)
        layout_c.addWidget(self.slider_chlodnica)
        layout_temp.addLayout(layout_c)

        layout.addLayout(layout_temp)
        self.panel.setLayout(layout)

    def update_grzalka(self, val):
        self.grzalka.ustaw_moc(val); self.update()

    def update_chlodnica(self, val):
        self.chlodnica.ustaw_moc(val); self.update()

    def toggle_wlot(self):
        self.wlot_otwarty = self.btn_wlot.isChecked(); self.update()

    def toggle_wylot(self):
        self.wylot_otwarty = self.btn_wylot.isChecked(); self.update()

    def przelacz_sym(self):
        if self.running: self.timer.stop()
        else: self.timer.start(30)
        self.running = not self.running

    def logika_przeplywu(self):
        speed_woda = self.base_speed * 0.75

        p0 = False
        if self.wlot_otwarty and not self.z1.czy_pelny():
            self.z1.dodaj_ciecz(speed_woda) 
            p0 = True
        self.rura_wlot.ustaw_przeplyw(p0)

        p1 = False
        if not self.z1.czy_pusty() and not self.z2.czy_pelny():
            self.z2.dodaj_ciecz(self.z1.usun_ciecz(speed_woda))
            p1 = True
        self.rura1.ustaw_przeplyw(p1)

        p2 = False
        moc_g = self.grzalka.moc / 100.0
        if moc_g > 0 and self.z2.aktualna_ilosc > 0.1 and not self.z3.czy_pelny():
            speed_para = self.base_speed * 1.5 * moc_g
            self.z3.dodaj_ciecz(self.z2.usun_ciecz(speed_para))
            p2 = True
        self.rura2.ustaw_przeplyw(p2)

        p3 = False
        moc_c = self.chlodnica.moc / 100.0
        if moc_c > 0 and not self.z3.czy_pusty() and not self.z4.czy_pelny():
            speed_skropliny = self.base_speed * 1.5 * moc_c
            self.z4.dodaj_ciecz(self.z3.usun_ciecz(speed_skropliny))
            p3 = True
        self.rura3.ustaw_przeplyw(p3)

        p4 = False
        if self.wylot_otwarty and not self.z4.czy_pusty():
            self.z4.usun_ciecz(speed_woda)
            p4 = True
        self.rura_wylot.ustaw_przeplyw(p4)

        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(40, 40, 40))
        p.drawRect(1180, 0, 120, 650)
        
        p.setPen(QPen(Qt.gray, 2))
        p.drawLine(1180, 0, 1180, 650)
        
        for r in self.rury: r.draw(p)
        for z in self.zbiorniki: z.draw(p)
        self.grzalka.draw(p)
        self.chlodnica.draw(p)
        
        for w in self.wskazniki: w.draw(p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = SymulacjaKaskady()
    okno.show()
    sys.exit(app.exec_())