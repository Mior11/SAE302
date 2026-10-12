"""Fenêtre principale de l'application Carrefour connecté."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QFrame, QFormLayout, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSpinBox, QVBoxLayout, QWidget,
)
from client.simulation.simulation_view import SimulationView


class MainWindow(QMainWindow):
    """Interface de pilotage d'une simulation pédagogique de carrefour."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Carrefour connecté | SAÉ 3.02")
        self.resize(1240, 820)
        self.setMinimumSize(980, 680)
        self.setStyleSheet("""
            QMainWindow, QWidget#root { background: #f3f6fa; color: #172033; }
            QLabel { color: #172033; }
            QLabel#eyebrow { color: #2563eb; font-size: 11px; font-weight: 800; letter-spacing: 1px; }
            QLabel#pageTitle { font-size: 25px; font-weight: 800; }
            QLabel#muted { color: #64748b; font-size: 12px; }
            QFrame#panel, QFrame#metric { background: white; border: 1px solid #e2e8f0; border-radius: 14px; }
            QLabel#sectionTitle { font-size: 15px; font-weight: 750; }
            QLabel#metricValue { font-size: 22px; font-weight: 800; }
            QLabel#metricLabel { color: #64748b; font-size: 11px; }
            QComboBox, QSpinBox { background: #f8fafc; border: 1px solid #dbe3ee; border-radius: 7px; padding: 8px; min-height: 20px; }
            QPushButton { border-radius: 8px; padding: 11px 14px; font-weight: 700; }
            QPushButton#primary { background: #2563eb; color: white; border: 0; }
            QPushButton#primary:hover { background: #1d4ed8; }
            QPushButton#emergency { background: #dc2626; color: white; border: 0; }
            QPushButton#emergency:hover { background: #b91c1c; }
            QPushButton#secondary { background: white; color: #334155; border: 1px solid #cbd5e1; }
        """)

        root = QWidget()
        root.setObjectName("root")
        page = QVBoxLayout(root)
        page.setContentsMargins(24, 20, 24, 22)
        page.setSpacing(16)

        header = QHBoxLayout()
        brand = QVBoxLayout()
        eyebrow = QLabel("SAÉ 3.02  /  GROUPE A113")
        eyebrow.setObjectName("eyebrow")
        title = QLabel("Carrefour connecté")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Simulation de trafic et gestion de la priorité des véhicules d'urgence")
        subtitle.setObjectName("muted")
        brand.addWidget(eyebrow)
        brand.addWidget(title)
        brand.addWidget(subtitle)
        header.addLayout(brand)
        header.addStretch()
        self.connection_badge = QLabel("●  MODE LOCAL")
        self.connection_badge.setStyleSheet("background:#dbeafe;color:#1d4ed8;border-radius:10px;padding:9px 12px;font-size:11px;font-weight:800;")
        header.addWidget(self.connection_badge, 0, Qt.AlignmentFlag.AlignTop)
        page.addLayout(header)

        metrics = QHBoxLayout()
        metrics.setSpacing(12)
        self.metric_state = self._metric("ÉTAT DU SYSTÈME", "Prêt", "Simulation locale")
        self.metric_traffic = self._metric("DENSITÉ DU TRAFIC", "Modéré", "Véhicules ordinaires")
        self.metric_priority = self._metric("PRIORITÉ URGENCE", "Inactive", "Feux en mode normal")
        metrics.addWidget(self.metric_state)
        metrics.addWidget(self.metric_traffic)
        metrics.addWidget(self.metric_priority)
        page.addLayout(metrics)

        content = QHBoxLayout()
        content.setSpacing(16)
        sidebar = QFrame()
        sidebar.setObjectName("panel")
        sidebar.setFixedWidth(290)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(18, 18, 18, 18)
        side.setSpacing(14)
        section = QLabel("Configuration")
        section.setObjectName("sectionTitle")
        hint = QLabel("Personnalisez le scénario avant de lancer la simulation.")
        hint.setObjectName("muted")
        hint.setWordWrap(True)
        side.addWidget(section)
        side.addWidget(hint)

        form = QFormLayout()
        form.setVerticalSpacing(12)
        self.junction = QComboBox()
        self.junction.addItems(["Carrefour à 4 branches", "Carrefour en T"])
        self.traffic = QComboBox()
        self.traffic.addItems(["Fluide", "Modéré", "Embouteillage"])
        self.rule = QComboBox()
        self.rule.addItems(["Feux tricolores", "STOP", "Priorité à droite"])
        self.emergency_direction = QComboBox()
        self.emergency_direction.addItems(["Nord", "Est", "Sud", "Ouest"])
        self.vehicle_count = QSpinBox()
        self.vehicle_count.setRange(2, 30)
        self.vehicle_count.setValue(10)
        form.addRow("Type de carrefour", self.junction)
        form.addRow("Densité du trafic", self.traffic)
        form.addRow("Règle de circulation", self.rule)
        form.addRow("Arrivée urgence", self.emergency_direction)
        form.addRow("Véhicules ordinaires", self.vehicle_count)
        side.addLayout(form)
        side.addStretch()
        self.start_button = QPushButton("▶   Démarrer / réinitialiser")
        self.start_button.setObjectName("primary")
        self.priority_button = QPushButton("⚠   Demander la priorité")
        self.priority_button.setObjectName("emergency")
        self.stop_button = QPushButton("Ⅱ   Mettre en pause")
        self.stop_button.setObjectName("secondary")
        side.addWidget(self.start_button)
        side.addWidget(self.priority_button)
        side.addWidget(self.stop_button)
        content.addWidget(sidebar)

        right = QVBoxLayout()
        right.setSpacing(12)
        map_panel = QFrame()
        map_panel.setObjectName("panel")
        map_layout = QVBoxLayout(map_panel)
        map_layout.setContentsMargins(16, 14, 16, 14)
        map_header = QHBoxLayout()
        map_title_box = QVBoxLayout()
        map_title = QLabel("Vue du carrefour")
        map_title.setObjectName("sectionTitle")
        map_subtitle = QLabel("Vue en temps réel du scénario simulé")
        map_subtitle.setObjectName("muted")
        map_title_box.addWidget(map_title)
        map_title_box.addWidget(map_subtitle)
        map_header.addLayout(map_title_box)
        map_header.addStretch()
        self.live_label = QLabel("●  EN ATTENTE")
        self.live_label.setStyleSheet("color:#64748b;font-size:10px;font-weight:800;")
        map_header.addWidget(self.live_label, 0, Qt.AlignmentFlag.AlignVCenter)
        map_layout.addLayout(map_header)
        self.view = SimulationView()
        self.view.setMinimumHeight(390)
        map_layout.addWidget(self.view, 1)
        legend = QHBoxLayout()
        for color, text in [("#3b82f6", "Véhicule ordinaire"), ("#ef4444", "Feu rouge"), ("#22c55e", "Feu vert"), ("#f97316", "Véhicule d'urgence")]:
            item = QLabel(f"●  {text}")
            item.setStyleSheet(f"color:{color};font-size:11px;font-weight:650;")
            legend.addWidget(item)
        legend.addStretch()
        map_layout.addLayout(legend)
        right.addWidget(map_panel, 1)

        status_panel = QFrame()
        status_panel.setObjectName("panel")
        status_layout = QHBoxLayout(status_panel)
        status_layout.setContentsMargins(14, 10, 14, 10)
        status_icon = QLabel("●")
        status_icon.setStyleSheet("color:#16a34a;font-size:12px;")
        self.status = QLabel("Prêt à démarrer. Configurez le scénario puis lancez la simulation.")
        self.status.setObjectName("muted")
        status_layout.addWidget(status_icon)
        status_layout.addWidget(self.status, 1)
        right.addWidget(status_panel)
        content.addLayout(right, 1)
        page.addLayout(content, 1)
        self.setCentralWidget(root)

        self.start_button.clicked.connect(self.start_simulation)
        self.priority_button.clicked.connect(self.request_priority)
        self.stop_button.clicked.connect(self.toggle_pause)
        self.junction.currentIndexChanged.connect(self.refresh_config)
        self.traffic.currentIndexChanged.connect(self.refresh_config)
        self.rule.currentIndexChanged.connect(self.refresh_config)
        self.emergency_direction.currentIndexChanged.connect(self.refresh_config)
        self.vehicle_count.valueChanged.connect(self.refresh_config)
        self.refresh_config()

    def _metric(self, label: str, value: str, detail: str) -> QFrame:
        """Crée une petite carte d'indicateur."""
        card = QFrame()
        card.setObjectName("metric")
        box = QVBoxLayout(card)
        box.setContentsMargins(15, 12, 15, 12)
        box.setSpacing(4)
        name = QLabel(label)
        name.setObjectName("metricLabel")
        val = QLabel(value)
        val.setObjectName("metricValue")
        sub = QLabel(detail)
        sub.setObjectName("muted")
        box.addWidget(name)
        box.addWidget(val)
        box.addWidget(sub)
        card.value_label = val
        card.detail_label = sub
        return card

    def refresh_config(self, *_args) -> None:
        """Transmet les paramètres sélectionnés au moteur graphique."""
        self.view.configure(self.junction.currentIndex() == 1, self.traffic.currentIndex(),
                            self.rule.currentIndex(), self.emergency_direction.currentIndex(),
                            self.vehicle_count.value())
        self.metric_traffic.value_label.setText(self.traffic.currentText())
        self.metric_traffic.detail_label.setText(f"{self.vehicle_count.value()} véhicules configurés")

    def start_simulation(self) -> None:
        """Démarre ou réinitialise le scénario local."""
        self.refresh_config()
        self.view.start_simulation()
        self.status.setText("Simulation en cours — les véhicules circulent dans le carrefour.")
        self.live_label.setText("●  EN DIRECT")
        self.live_label.setStyleSheet("color:#16a34a;font-size:10px;font-weight:800;")
        self.metric_state.value_label.setText("En cours")

    def request_priority(self) -> None:
        """Active la séquence visuelle de priorité d'urgence."""
        if not self.view.running:
            self.start_simulation()
        self.view.request_priority()
        self.status.setText("Demande reçue : priorité temporaire activée pour le véhicule d'urgence.")
        self.metric_priority.value_label.setText("Active")
        self.metric_priority.detail_label.setText("Retour automatique au cycle normal")
        self.metric_priority.value_label.setStyleSheet("color:#dc2626;")
        self.view.priority_finished.connect(self.restore_priority_status, Qt.ConnectionType.UniqueConnection)

    def restore_priority_status(self) -> None:
        """Met à jour les indicateurs après la fin de la priorité."""
        self.metric_priority.value_label.setText("Inactive")
        self.metric_priority.detail_label.setText("Feux en mode normal")
        self.metric_priority.value_label.setStyleSheet("")
        self.status.setText("Priorité terminée. Le cycle normal des feux est rétabli.")

    def toggle_pause(self) -> None:
        """Met la simulation en pause ou la reprend."""
        if self.view.running:
            self.view.pause_simulation()
            self.status.setText("Simulation en pause.")
            self.live_label.setText("Ⅱ  EN PAUSE")
            self.metric_state.value_label.setText("En pause")
        else:
            self.view.resume_simulation()
            self.status.setText("Simulation reprise.")
            self.live_label.setText("●  EN DIRECT")
            self.metric_state.value_label.setText("En cours")
