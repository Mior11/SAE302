"""Vue graphique 2D et simulation pédagogique locale du carrefour."""
from __future__ import annotations
import math
import random
from PySide6.QtCore import QTimer, Qt, QRectF, QPointF
from PySide6.QtGui import QColor, QBrush, QPen, QPainter
from PySide6.QtWidgets import QWidget


class SimulationView(QWidget):
    """Dessine un carrefour et anime des véhicules sur quatre approches.

    Ce modèle est visuel et simplifié : il ne constitue pas un simulateur
    certifié du code de la route ni un système de commande de feux réels.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(350)
        self.timer = QTimer(self); self.timer.setInterval(40); self.timer.timeout.connect(self.tick)
        self.running = False; self.emergency = False; self.emergency_ticks = 0; self.tick_count = 0
        self.t_junction = False; self.traffic_level = 1; self.rule = 0; self.direction = 0; self.vehicle_count = 10
        self.vehicles = []
        self.start_simulation()

    def configure(self, t_junction: bool, traffic_level: int, rule: int, direction: int, vehicle_count: int):
        self.t_junction = t_junction; self.traffic_level = traffic_level; self.rule = rule
        self.direction = direction; self.vehicle_count = vehicle_count
        self.update()

    def start_simulation(self):
        """Crée un nouveau jeu de véhicules et démarre l'horloge."""
        random.seed()
        self.vehicles = []
        for i in range(self.vehicle_count):
            lane = i % (3 if self.t_junction else 4)
            self.vehicles.append({"lane": lane, "progress": random.uniform(-0.2, 0.8), "speed": random.uniform(0.0015, 0.003), "color": QColor.fromHsv(random.randint(0, 359), 150, 220)})
        self.emergency = False; self.emergency_ticks = 0; self.tick_count = 0; self.running = True
        self.timer.start(); self.update()

    def request_priority(self):
        """Active une fenêtre de priorité temporaire, puis restaure les feux."""
        self.emergency = True; self.emergency_ticks = 180; self.update()

    def tick(self):
        if not self.running: return
        self.tick_count += 1
        for car in self.vehicles:
            # En cas d'embouteillage, la progression est volontairement ralentie.
            speed = car["speed"] * (0.35 if self.traffic_level == 2 else 0.7 if self.traffic_level == 1 else 1.0)
            car["progress"] += speed
            if car["progress"] > 1.15: car["progress"] = -0.15
        if self.emergency:
            self.emergency_ticks -= 1
            if self.emergency_ticks <= 0: self.emergency = False
        self.update()

    def paintEvent(self, _event):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor("#e7eee9"))
        w, h = self.width(), self.height(); cx, cy = w / 2, h / 2
        road_w = min(w, h) * 0.32
        p.setPen(Qt.PenStyle.NoPen); p.setBrush(QColor("#4b5563"))
        p.drawRect(QRectF(cx-road_w/2, 0, road_w, h))
        p.drawRect(QRectF(0, cy-road_w/2, w, road_w))
        if self.t_junction:
            # Branche nord absente pour illustrer la géométrie en T.
            p.fillRect(QRectF(cx-road_w/2, 0, road_w, cy-road_w/2), QColor("#e7eee9"))
        p.setPen(QPen(QColor("#f8fafc"), 2, Qt.PenStyle.DashLine))
        p.drawLine(QPointF(cx, 0 if not self.t_junction else cy), QPointF(cx, h))
        p.drawLine(QPointF(0, cy), QPointF(w, cy))
        p.setPen(Qt.PenStyle.NoPen)
        # Feux schématiques aux quatre approches. En urgence, l'approche cible passe au vert.
        for lane, (lx, ly) in enumerate([(cx, cy-road_w/2-18),(cx+road_w/2+18,cy),(cx,cy+road_w/2+18),(cx-road_w/2-18,cy)]):
            if self.t_junction and lane == 0: continue
            color = QColor("#22c55e") if self.emergency and lane == self.direction else QColor("#ef4444")
            if not self.emergency and (self.tick_count // 70) % 2 == lane % 2: color = QColor("#22c55e")
            p.setBrush(color); p.drawEllipse(QPointF(lx, ly), 7, 7)
        # Véhicules ordinaires : trajet visuel simplifié autour du centre.
        for car in self.vehicles:
            prog = car["progress"]; lane = car["lane"]
            if lane == 0: x, y = cx-road_w*.18, h*(1-prog)
            elif lane == 1: x, y = w*prog, cy-road_w*.18
            elif lane == 2: x, y = cx+road_w*.18, h*prog
            else: x, y = w*(1-prog), cy+road_w*.18
            p.setBrush(car["color"]); p.setPen(QPen(QColor("#111827"), 1)); p.drawRoundedRect(QRectF(x-7,y-12,14,24),3,3)
        if self.emergency:
            lane = self.direction
            coords = [(cx, cy-road_w*.18),(cx+road_w*.18,cy),(cx,cy+road_w*.18),(cx-road_w*.18,cy)]
            ex, ey = coords[lane]
            p.setBrush(QColor("#f97316")); p.setPen(QPen(QColor("white"),2)); p.drawRoundedRect(QRectF(ex-9,ey-15,18,30),4,4)
            p.setPen(QColor("#111827")); p.drawText(12, 24, "PRIORITÉ D'URGENCE ACTIVE")
        p.end()
