from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QComboBox, QScrollArea
)
from utils.caminhos import caminhos, salvar_caminho
from utils.database import carregar_caminhos_salvos  # função que retorna lista de ambientes do banco   # noqa # type: ignore


class AmbienteWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent  # type: ignore
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Título
        title = QLabel("Configuração de Caminhos")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title)

        # 🔹 Combo box de ambientes
        combo_layout = QHBoxLayout()
        combo_label = QLabel("Selecione o ambiente:")
        combo_layout.addWidget(combo_label)

        self.combo_ambiente = QComboBox()
        ambientes = carregar_caminhos_salvos()  # espera retornar lista de ambientes ["Dev", "Prod", ...]   # noqa # type: ignore
        self.combo_ambiente.addItems(ambientes)
        self.combo_ambiente.currentTextChanged.connect(
            self.carregar_campos_ambiente)
        combo_layout.addWidget(self.combo_ambiente)
        main_layout.addLayout(combo_layout)

        # 🔹 Scroll area para campos
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        main_layout.addWidget(self.scroll)

        # Container interno do scroll
        self.scroll_container = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_container)
        self.scroll.setWidget(self.scroll_container)

        self.campos = {}

        # 🔹 Botões
        btn_layout = QHBoxLayout()
        salvar_button = QPushButton("💾 Salvar")
        salvar_button.clicked.connect(self.salvar)
        btn_layout.addWidget(salvar_button)

        voltar_button = QPushButton("⬅️ Voltar")
        voltar_button.clicked.connect(self.voltar)
        btn_layout.addWidget(voltar_button)

        main_layout.addLayout(btn_layout)

        # Carrega inicialmente o primeiro ambiente
        if ambientes:
            self.carregar_campos_ambiente(ambientes[0])

    def carregar_campos_ambiente(self, ambiente):
        """Carrega os caminhos do ambiente selecionado"""
        # Limpa campos antigos
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)   # noqa # type: ignore
        self.campos = {}

        # Busca caminhos no banco
        cfg = caminhos(ambiente)
        if not cfg:
            QMessageBox.warning(
                self,
                "Aviso",
                f"Nenhum caminho encontrado para o ambiente {ambiente}")
            return

        # Cria campos editáveis para cada chave
        for chave, valor in cfg.items():
            label = QLabel(chave.upper())
            campo = QLineEdit(str(valor))
            self.scroll_layout.addWidget(label)
            self.scroll_layout.addWidget(campo)
            self.campos[chave] = campo

    def salvar(self):
        """Salva alterações no banco"""
        ambiente = self.combo_ambiente.currentText()
        dados = {chave: campo.text() for chave, campo in self.campos.items()}

        try:
            salvar_caminho(ambiente, dados)
            QMessageBox.information(
                self, "Sucesso",
                f"Configurações do ambiente {ambiente} salvas com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar: {e}")

    def voltar(self):
        if self.parent:
            self.parent.show_menu_inicial()   # noqa # type: ignore
