import sys
from core.tarefas import executar_automacao
from ui.gui import iniciar_interface_manual


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "auto":
        executar_automacao()
    else:
        iniciar_interface_manual()


if __name__ == "__main__":
    main()
