import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton
)
from PyQt5.QtGui import QIcon
from ui.manual_trn import TRNManualWidget
from ui.manual_autoriza import AUTManualwidget
from ui.manual_caminhos import AmbienteWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Titanic")
        self.setGeometry(200, 200, 500, 400)

        self.layout = QVBoxLayout()  # type: ignore
        self.setLayout(self.layout)  # type: ignore

        # 🔹 Cabeçalho fixo
        header_layout = QHBoxLayout()
        app_label = QLabel("Titanic - Execuções Manuais")
        app_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(app_label)

        header_layout.addStretch()

        gear_button = QPushButton()
        gear_button.setIcon(QIcon("assets/gear.png"))  # ícone customizado
        gear_button.setFixedSize(30, 30)
        gear_button.clicked.connect(self.show_ambiente)
        header_layout.addWidget(gear_button)

        self.layout.addLayout(header_layout)  # type: ignore

        # 🔹 Área de conteúdo que muda
        self.content_layout = QVBoxLayout()
        self.layout.addLayout(self.content_layout)  # type: ignore

        self.show_menu_inicial()

    def clear_layout(self):
        """Remove widgets do content_layout apenas"""
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)  # type: ignore

    def show_menu_inicial(self):
        self.clear_layout()

        subtitle = QLabel("Selecione a rotina para execução manual")
        subtitle.setStyleSheet("margin-top: 10px; font-size: 14px;")
        self.content_layout.addWidget(subtitle)

        trn_button = QPushButton("TRN Domingo")
        trn_button.clicked.connect(self.run_trn)
        self.content_layout.addWidget(trn_button)

        aut_button = QPushButton("Autorização")
        aut_button.clicked.connect(self.run_aut)
        self.content_layout.addWidget(aut_button)

        exit_button = QPushButton("Encerrar")
        exit_button.clicked.connect(QApplication.quit)
        self.content_layout.addWidget(exit_button)

    def run_trn(self):
        self.clear_layout()
        self.trn_widget = TRNManualWidget(self)
        self.content_layout.addWidget(self.trn_widget)

    def run_aut(self):
        self.clear_layout()
        self.aut_widget = AUTManualwidget(self)
        self.content_layout.addWidget(self.aut_widget)

    def show_ambiente(self):
        self.clear_layout()
        self.ambiente_widget = AmbienteWidget(self)
        self.content_layout.addWidget(self.ambiente_widget)


def iniciar_interface_manual():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
