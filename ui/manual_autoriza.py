from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
    QMessageBox, QProgressBar, QDateEdit
)
from PyQt5.QtCore import QThread, pyqtSignal, QDate
from datetime import datetime
from autorizacao.autorizacao import (
    executa, insert_sqlite, exportar_para_csv,
    resetar_tabela_transacoes
)
from utils.caminhos import caminhos
from utils.logs_escrita import log_info


# Worker em thread para rodar a execução sem travar a UI
class ExecucaoWorker(QThread):
    progress_changed = pyqtSignal(int)
    finished_ok = pyqtSignal()
    finished_error = pyqtSignal(str)

    def __init__(self, data_inicio, data_fim, pasta_saida):
        super().__init__()
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.pasta_saida = pasta_saida

    def run(self):
        try:
            caminho = caminhos()

            # 🚀 Modo manual (usa parâmetros do usuário)
            inicio = datetime.strptime(
                f"{self.data_inicio.strftime('%d/%m/%Y')} 00:00:01",
                '%d/%m/%Y %H:%M:%S'
            )
            fim = datetime.strptime(
                f"{self.data_fim.strftime('%d/%m/%Y')} 23:59:59",
                '%d/%m/%Y %H:%M:%S'
            )

            nm_arquivo = f'{self.data_inicio.strftime("%d_%m_%Y")}_MANUAL'

            # 1) Executa Autorização
            self.progress_changed.emit(40)
            resetar_tabela_transacoes()
            lista_autorizacao = executa(inicio, fim)

            # 2) Insere no banco
            self.progress_changed.emit(70)
            insert_sqlite(lista_autorizacao)

            # 3) Exporta para CSV
            self.progress_changed.emit(95)
            exportar_para_csv(nm_arquivo, self.pasta_saida)

            if caminho['RP_ESC_LOG'] == 'Sim':
                log_info("Execução manual da Autorização concluída!")

            self.progress_changed.emit(100)
            self.finished_ok.emit()

        except Exception as e:
            caminho = caminhos()
            if caminho['RP_ESC_LOG'] == 'Sim':
                log_info(f"Erro durante execução manual da Autorização: {e}")
            self.finished_error.emit(str(e))


class AUTManualwidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # 👈 manter referência para voltar à tela inicial  # noqa # type: ignore

        self.pasta_saida = None
        self.data_inicio = None
        self.data_fim = None

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Dados para execução da Autorização"))

        # Pasta saída
        self.lbl_aut = QLabel("📂 Pasta Saída: [não selecionado]")
        btn_aut = QPushButton("Selecionar Pasta de saída")
        btn_aut.clicked.connect(self.select_saida)
        layout.addWidget(self.lbl_aut)
        layout.addWidget(btn_aut)

        # Data início
        self.lbl_data_ini = QLabel("🗓️ Data Início:")
        self.date_edit_ini = QDateEdit()
        self.date_edit_ini.setCalendarPopup(True)
        self.date_edit_ini.setDate(QDate.currentDate())
        layout.addWidget(self.lbl_data_ini)
        layout.addWidget(self.date_edit_ini)

        # Data fim
        self.lbl_data_fim = QLabel("🗓️ Data Fim:")
        self.date_edit_fim = QDateEdit()
        self.date_edit_fim.setCalendarPopup(True)
        self.date_edit_fim.setDate(QDate.currentDate())
        layout.addWidget(self.lbl_data_fim)
        layout.addWidget(self.date_edit_fim)

        # Barra de progresso
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Botão executar
        btn_exec = QPushButton("▶️ Executar Autorização")
        btn_exec.clicked.connect(self.run_execucao)
        layout.addWidget(btn_exec)

        # Botão voltar
        btn_voltar = QPushButton("⬅️ Voltar")
        btn_voltar.clicked.connect(self.voltar_tela_inicial)
        layout.addWidget(btn_voltar)

        self.setLayout(layout)

    def select_saida(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Selecione a pasta de Autorização"
        )
        if folder:
            self.pasta_saida = folder
            self.lbl_aut.setText(f"📂 Pasta Saída: {folder}")

    def run_execucao(self):
        self.data_inicio = self.date_edit_ini.date().toPyDate()
        self.data_fim = self.date_edit_fim.date().toPyDate()

        if not all([self.pasta_saida, self.data_inicio, self.data_fim]):
            QMessageBox.warning(
                self, "Atenção", "Por favor, preencha todos os campos!"
            )
            return

        self.worker = ExecucaoWorker(
            self.data_inicio, self.data_fim, self.pasta_saida
        )
        self.worker.progress_changed.connect(self.progress_bar.setValue)

        # ✅ Popup de sucesso
        self.worker.finished_ok.connect(self.show_success_message)

        # ❌ Popup de erro
        self.worker.finished_error.connect(
            lambda e: QMessageBox.critical(self, "Erro", f"Erro durante a execução: {e}")  # noqa # type: ignore
        )

        self.worker.start()

    def show_success_message(self):
        QMessageBox.information(self, "Sucesso", "Autorização executada com sucesso!")  # noqa # type: ignore
        self.progress_bar.setValue(0)  # reset barra de progresso

    def voltar_tela_inicial(self):
        if self.parent:
            self.parent.show_menu_inicial()  # noqa # type: ignore
