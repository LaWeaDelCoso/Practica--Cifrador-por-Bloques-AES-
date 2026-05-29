import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication

from controllers import AESController
from views import MainView, STYLESHEET


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("AES App")
    app.setOrganizationName("Práctica Criptografía")

    # Apply global stylesheet
    app.setStyleSheet(STYLESHEET)

    # Instantiate MVC components
    controller = AESController()
    window = MainView(controller)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()