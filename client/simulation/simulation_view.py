"""Vue graphique 2D et moteur visuel simplifié du carrefour."""
from __future__ import annotations

import random
from PySide6.QtCore import QTimer, Qt, QRectF, QPointF, Signal
from PySide6.QtGui import QColor, QPen, QPainter, QFont
from PySide6.QtWidgets import QWidget


class SimulationView(QWidget):
    """Dessine un carrefour et anime des véhicules pour une démonstration locale.

    Ce modèle n'est pas un simulateur certifié du code de la route et ne commande
    aucun équipement réel. Les trajectoires restent volontairement simplifiées.
    """
    priority_finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(390)
        self.timer = QTimer(self)
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.tick)
        self.running = False
        self.paused = False
        self.emergency = False
        self.emergency_ticks = 0
        self.tick_count = 0
        self.t_junction = False
        self.traffic_level = 1
        self.rule = 0
        self.direction = 0
        self.vehicle_count = 10
        self.vehicles = []
        self.start_simulation()

    def configure(self, t_junction: bool, traffic_level: int, rule: int, direction: int, vehicle_count: int):
        """Applique les paramètres de scénario choisis dans l'interface."""
        changed = (self.t_junction != t_junction or self.vehicle_count != vehicle_count)
        self.t_junction = t_junction
        self.traffic_level = traffic_level
        self.rule = rule
        self.direction = direction
        self.vehicle_count = vehicle_count
        if changed and self.running:
            self._create_vehicles()
        self.update()

    def _create_vehicles(self):
        self.vehicles = []
        lane_count = 3 if self.t_junction else 4
        palette = ["#60a5fa", "#a78bfa", "#fbbf24", "#34d399", "#f472b6", "#cbd5e1"]
        for i in range(self.vehicle_count):
            self.vehicles.append({
                "lane": i % lane_count,
                "progress": random.uniform(-0.25, 0.85),
                "speed": random.uniform(0.0015, 0.003),
                "color": QColor(palette[i % len(palette)]),
            })

    def start_simulation(self):
        """Réinitialise et démarre le mouvement des véhicules."""
        self._create_vehicles()
        self.emergency = False
        self.emergency_ticks = 0
        self.tick_count = 0
        self.running = True
        self.paused = False
        self.timer.start()
        self.update()

    def request_priority(self):
        """Active temporairement la priorité visuelle pour l'approche choisie."""
        self.emergency = True
        self.emergency_ticks = 180
        self.update()

    def pause_simulation(self):
        """Met l'animation en pause."""
        self.paused = True
        self.timer.stop()
        self.update()

    def resume_simulation(self):
        """Reprend l'animation."""
        self.paused = False
        self.running = True
        self.timer.start()
        self.update()

    def tick(self):
        if not self.running or self.paused:
            return
        self.tick_count += 1
        for car in self.vehicles:
            factor = 0.35 if self.traffic_level == 2 else 0.7 if self.traffic_level == 1 else 1.0
            car["progress"] += car["speed"] * factor
            if car["progress"] > 1.15:
                car["progress"] = -0.15
        if self.emergency:
            self.emergency_ticks -= 1
            if self.emergency_ticks <= 0:
                self.emergency = False
                self.priority_finished.emit()
        self.update()

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor("#f8fafc"))
        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2
        road_w = min(w, h) * 0.38
        road = QColor("#303b4d")
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(road)
        p.drawRect(QRectF(cx - road_w / 2, 0, road_w, h))
        p.drawRect(QRectF(0, cy - road_w / 2, w, road_w))
        if self.t_junction:
            p.fillRect(QRectF(cx - road_w / 2, 0, road_w, cy - road_w / 2), QColor("#f8fafc"))

        # Marquages au sol.
        p.setPen(QPen(QColor("#cbd5e1"), 2, Qt.PenStyle.DashLine))
        p.drawLine(QPointF(cx, cy + road_w / 2), QPointF(cx, h))
        p.drawLine(QPointF(0, cy), QPointF(w, cy))
        if not self.t_junction:
            p.drawLine(QPointF(cx, 0), QPointF(cx, cy - road_w / 2))

        # Passages piétons stylisés aux entrées.
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#e2e8f0"))
        for i in range(6):
            offset = -road_w * .32 + i * road_w * .13
            p.drawRect(QRectF(cx + offset, cy - road_w / 2 - 12, 5, 9))
            p.drawRect(QRectF(cx + offset, cy + road_w / 2 + 3, 5, 9))
            p.drawRect(QRectF(cx - road_w / 2 - 12, cy + offset, 9, 5))
            p.drawRect(QRectF(cx + road_w / 2 + 3, cy + offset, 9, 5))

        # Feux : cycle simplifié, avec priorité temporaire sur l'approche sélectionnée.
        lights = [(cx - road_w * .34, cy - road_w * .62),
                  (cx + road_w * .62, cy - road_w * .34),
                  (cx + road_w * .34, cy + road_w * .62),
                  (cx - road_w * .62, cy + road_w * .34)]
        for lane, (lx, ly) in enumerate(lights):
            if self.t_junction and lane == 0:
                continue
            is_green = (self.emergency and lane == self.direction) or (
                not self.emergency and (self.tick_count // 85) % 2 == lane % 2)
            p.setBrush(QColor("#22c55e" if is_green else "#ef4444"))
            p.setPen(QPen(QColor("#ffffff"), 2))
            p.drawEllipse(QPointF(lx, ly), 9, 9)

        # Véhicules ordinaires (trajectoires schématiques).
        for car in self.vehicles:
            prog, lane = car["progress"], car["lane"]
            if lane == 0:
                x, y = cx - road_w * .18, h * (1 - prog)
            elif lane == 1:
                x, y = w * prog, cy - road_w * .18
            elif lane == 2:
                x, y = cx + road_w * .18, h * prog
            else:
                x, y = w * (1 - prog), cy + road_w * .18
            p.setPen(QPen(QColor("#0f172a"), 1))
            p.setBrush(car["color"])
            p.drawRoundedRect(QRectF(x - 7, y - 12, 14, 24), 4, 4)

        if self.emergency:
            coords = [(cx - road_w * .18, cy - road_w * .38),
                      (cx + road_w * .38, cy - road_w * .18),
                      (cx + road_w * .18, cy + road_w * .38),
                      (cx - road_w * .38, cy + road_w * .18)]
            ex, ey = coords[self.direction]
            p.setPen(QPen(QColor("#ffffff"), 2))
            p.setBrush(QColor("#f97316"))
            p.drawRoundedRect(QRectF(ex - 10, ey - 15, 20, 30), 4, 4)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor("#fee2e2"))
            p.drawRoundedRect(QRectF(12, 12, 205, 30), 9, 9)
            p.setPen(QColor("#b91c1c"))
            p.setFont(QFont("Arial", 9, QFont.Weight.Bold))
            p.drawText(QRectF(20, 12, 190, 30), Qt.AlignmentFlag.AlignVCenter, "PRIORITÉ D'URGENCE ACTIVE")

        if self.paused:
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(15, 23, 42, 165))
            p.drawRoundedRect(QRectF(cx - 80, cy - 24, 160, 48), 12, 12)
            p.setPen(QColor("#ffffff"))
            p.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            p.drawText(QRectF(cx - 80, cy - 24, 160, 48), Qt.AlignmentFlag.AlignCenter, "EN PAUSE")
        p.end()
