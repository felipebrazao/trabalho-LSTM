"""Executa o notebook inteiro e salva as saídas, inclusive se houver erro."""
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def main():
    pasta = Path(__file__).resolve().parent
    caminho = pasta / "LSTM.ipynb"
    notebook = nbformat.read(caminho, as_version=4)
    notebook.metadata.kernelspec = {
        "display_name": "Python (LSTM - projeto)",
        "language": "python",
        "name": "lstm-projeto",
    }
    cliente = NotebookClient(
        notebook,
        timeout=1800,
        kernel_name="lstm-projeto",
        resources={"metadata": {"path": str(pasta)}},
    )

    def informar(cell, cell_index, **kwargs):
        if cell.cell_type == "code":
            print(f"Executando célula {cell_index + 1}...", flush=True)

    cliente.on_cell_start = informar
    try:
        cliente.execute()
    finally:
        nbformat.write(notebook, caminho)
    print("Notebook executado e salvo com todas as saídas.", flush=True)


if __name__ == "__main__":
    main()
