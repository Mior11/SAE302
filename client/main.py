"""Point d'entrée de l'interface graphique."""
from __future__ import annotations

import sys
from PySide6.QtWidgets import QApplication
from client.ui.main_window import MainWindow


def main() -> int:
    """Initialise Qt et affiche la fenêtre principale."""
    app = QApplication(sys.argv)
    app.setApplicationName("Carrefour connecté — SAÉ 3.02")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
