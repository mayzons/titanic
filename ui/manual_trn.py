from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
    QMessageBox, QProgressBar, QDateEdit
)
from PyQt5.QtCore import QThread, pyqtSignal, QDate
from datetime import datetime
from trn_domingo.trn_domingo import (executa, opc_dados,
                                     gera_expurgo, insert_sqlite)
from utils.caminhos import caminhos
from utils.logs_escrita import log_info


# Worker em thread para rodar a execução sem travar a UI
class ExecucaoWorker(QThread):
    progress_changed = pyqtSignal(int)
    finished_ok = pyqtSignal()
    finished_error = pyqtSignal(str)

    def __init__(self, caminho_trn, caminho_opc, arquivo_abono, data_expurgo):
        super().__init__()
        self.caminho_trn = caminho_trn
        self.caminho_opc = caminho_opc
        self.arquivo_abono = arquivo_abono
        self.data_expurgo = data_expurgo

    def run(self):
        try:
            caminho = caminhos()
            nome_log = datetime.strftime(datetime.now(), '%d_%m_%Y')

            # 1) Executa TRN
            self.progress_changed.emit(10)
            lista_trn = executa(self.caminho_trn, nome_log)

            # 2) Executa OPC
            self.progress_changed.emit(40)
            lista_opc = opc_dados(self.caminho_opc, self.caminho_trn, nome_log)

            # 3) Gera expurgo
            self.progress_changed.emit(70)
            gera_expurgo(lista_opc, lista_trn,
                         self.arquivo_abono, self.data_expurgo)

            # 4) Insere no banco
            hora_atual_str = datetime.now().strftime("%H:%M:%S")
            insert_sqlite([(
                'trn domingo', datetime.now().date(), hora_atual_str, 'manual')
                ])

            if caminho['RP_ESC_LOG'] == 'Sim':
                log_info("Execução manual do TRN Domingo concluída!")

            self.progress_changed.emit(100)
            self.finished_ok.emit()

        except Exception as e:
            caminho = caminhos()
            if caminho['RP_ESC_LOG'] == 'Sim':
                log_info(f"Erro durante execução manual do TRN: {e}")
            self.finished_error.emit(str(e))


class TRNManualWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.caminho_trn = None
        self.caminho_opc = None
        self.arquivo_abono = None
        self.data_expurgo = None

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Parâmetros da Execução TRN Domingo"))

        # TRN
        self.lbl_trn = QLabel("📂 Pasta TRN: [não selecionado]")
        btn_trn = QPushButton("Selecionar pasta TRN")
        btn_trn.clicked.connect(self.select_trn)
        layout.addWidget(self.lbl_trn)
        layout.addWidget(btn_trn)

        # OPC
        self.lbl_opc = QLabel("📂 Pasta OPC: [não selecionado]")
        btn_opc = QPushButton("Selecionar pasta OPC")
        btn_opc.clicked.connect(self.select_opc)
        layout.addWidget(self.lbl_opc)
        layout.addWidget(btn_opc)

        # Abono
        self.lbl_abono = QLabel("📂 Arquivo Abono: [não selecionado]")
        btn_abono = QPushButton("Selecionar arquivo de Abono")
        btn_abono.clicked.connect(self.select_abono)
        layout.addWidget(self.lbl_abono)
        layout.addWidget(btn_abono)

        # Data com calendário
        self.lbl_data = QLabel("🗓️ Data de Expurgo:")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.lbl_data)
        layout.addWidget(self.date_edit)

        # Barra de progresso
        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        # Executar
        btn_exec = QPushButton("▶️ Executar TRN Domingo")
        btn_exec.clicked.connect(self.run_trn)
        layout.addWidget(btn_exec)

        self.setLayout(layout)

    def select_trn(self):
        folder = QFileDialog.getExistingDirectory(self,
                                                  "Selecione a pasta para TRN")
        if folder:
            self.caminho_trn = folder
            self.lbl_trn.setText(f"📂 Pasta TRN: {folder}")

    def select_opc(self):
        folder = QFileDialog.getExistingDirectory(self,
                                                  "Selecione a pasta do OPC")
        if folder:
            self.caminho_opc = folder
            self.lbl_opc.setText(f"📂 Pasta OPC: {folder}")

    def select_abono(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Selecione o arquivo de Abono")
        if folder:
            self.arquivo_abono = folder
            self.lbl_abono.setText(f"📂 Arquivo Abono: {folder}")

    def run_trn(self):
        self.data_expurgo = self.date_edit.date().toString("dd/MM/yyyy")

        if not all([self.caminho_trn, self.caminho_opc,
                    self.arquivo_abono, self.data_expurgo]):
            QMessageBox.warning(
                self, "Atenção",
                "Preencha todos os parâmetros antes de executar.")
            return

        self.worker = ExecucaoWorker(
            self.caminho_trn, self.caminho_opc,
            self.arquivo_abono, self.data_expurgo)
        self.worker.progress_changed.connect(self.progress.setValue)
        self.worker.finished_ok.connect(lambda: QMessageBox.information(self, "Sucesso", "Execução concluída!"))  # noqa # type: ignore
        self.worker.finished_error.connect(lambda e: QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {e}"))  # noqa # type: ignore
        self.worker.start()
