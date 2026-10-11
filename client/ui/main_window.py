"""Fenêtre principale et contrôles de la simulation locale."""
from __future__ import annotations

from PySide6.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QVBoxLayout, QWidget, QGroupBox, QFormLayout, QSpinBox)
from client.simulation.simulation_view import SimulationView


class MainWindow(QMainWindow):
    """Présente les paramètres du scénario et la vue du carrefour."""
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Carrefour connecté — SAÉ 3.02")
        self.resize(1050, 760)
        central = QWidget()
        layout = QVBoxLayout(central)
        intro = QLabel("SIMULATION DE CARREFOUR CONNECTÉ\nGestion expérimentale de la priorité d'un véhicule d'urgence")
        intro.setStyleSheet("font-size: 20px; font-weight: 700; padding: 12px;")
        layout.addWidget(intro)
        controls = QGroupBox("Configuration du scénario")
        form = QFormLayout(controls)
        self.junction = QComboBox(); self.junction.addItems(["Carrefour à 4 branches", "Carrefour en T"])
        self.traffic = QComboBox(); self.traffic.addItems(["Fluide", "Modéré", "Embouteillage"])
        self.rule = QComboBox(); self.rule.addItems(["Feux tricolores", "STOP", "Priorité à droite"])
        self.emergency_direction = QComboBox(); self.emergency_direction.addItems(["Nord", "Est", "Sud", "Ouest"])
        self.vehicle_count = QSpinBox(); self.vehicle_count.setRange(2, 30); self.vehicle_count.setValue(10)
        form.addRow("Géométrie", self.junction); form.addRow("Densité du trafic", self.traffic)
        form.addRow("Régulation", self.rule); form.addRow("Arrivée du véhicule d'urgence", self.emergency_direction)
        form.addRow("Véhicules ordinaires", self.vehicle_count)
        layout.addWidget(controls)
        self.view = SimulationView()
        layout.addWidget(self.view, 1)
        actions = QHBoxLayout()
        self.start_button = QPushButton("Démarrer / réinitialiser")
        self.priority_button = QPushButton("Demander la priorité d'urgence")
        self.status = QLabel("Simulation arrêtée")
        actions.addWidget(self.start_button); actions.addWidget(self.priority_button); actions.addWidget(self.status, 1)
        layout.addLayout(actions)
        self.start_button.clicked.connect(self.start_simulation)
        self.priority_button.clicked.connect(self.request_priority)
        self.junction.currentIndexChanged.connect(self.refresh_config)
        self.traffic.currentIndexChanged.connect(self.refresh_config)
        self.rule.currentIndexChanged.connect(self.refresh_config)
        self.emergency_direction.currentIndexChanged.connect(self.refresh_config)
        self.vehicle_count.valueChanged.connect(self.refresh_config)
        self.setCentralWidget(central)
        self.refresh_config()

    def refresh_config(self, *_args) -> None:
        """Transmet les paramètres courants au moteur d'affichage."""
        self.view.configure(self.junction.currentIndex() == 1, self.traffic.currentIndex(),
                            self.rule.currentIndex(), self.emergency_direction.currentIndex(),
                            self.vehicle_count.value())

    def start_simulation(self) -> None:
        """Lance ou réinitialise le scénario local."""
        self.refresh_config(); self.view.start_simulation(); self.status.setText("Simulation en cours")

    def request_priority(self) -> None:
        """Déclenche la séquence temporaire de priorité dans la démo."""
        if not self.view.running:
            self.start_simulation()
        self.view.request_priority(); self.status.setText("Priorité d'urgence demandée — scénario simulé")
