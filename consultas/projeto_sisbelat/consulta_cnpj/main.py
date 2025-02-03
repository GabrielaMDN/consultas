import tkinter as tk
from tkinter import messagebox, filedialog
from utils import obter_token, consultar_api, exportar_para_pdf, exportar_para_xls, traduzir_dados

# Função para realizar a consulta
def realizar_consulta():
    cnpj = cnpj_entry.get().strip()
    if not cnpj:
        messagebox.showwarning("Entrada inválida", "Por favor, insira um número de CNPJ.")
        return

    resultado_text.delete("1.0", tk.END)
    token = obter_token()
    if token:
        dados = consultar_api(token, cnpj)
        if dados:
            # Traduzir os dados antes de exibir
            dados = traduzir_dados(dados)
            resultado_text.insert(tk.END, f"Resultado para o CNPJ {cnpj}:\n")
            for chave, valor in dados.items():
                resultado_text.insert(tk.END, f"{chave}: {valor}\n")

            # Ativar botões de exportação com dados traduzidos
            pdf_button.config(
                state=tk.NORMAL,
                command=lambda: salvar_arquivo("PDF", cnpj, dados)
            )
            xls_button.config(
                state=tk.NORMAL,
                command=lambda: salvar_arquivo("XLS", cnpj, dados)
            )
        else:
            resultado_text.insert(tk.END, "Nenhum dado encontrado para o CNPJ informado.")
    else:
        resultado_text.insert(tk.END, "Erro ao obter o token de acesso.")


# Função para salvar o arquivo
def salvar_arquivo(formato, cnpj, dados):
    ext = ".pdf" if formato == "PDF" else ".xlsx"
    file_path = filedialog.asksaveasfilename(defaultextension=ext, filetypes=[(f"{formato} files", f"*{ext}")])
    if not file_path:
        return

    if formato == "PDF":
        exportar_para_pdf(cnpj, dados, file_path)
    elif formato == "XLS":
        exportar_para_xls(cnpj, dados, file_path)

    messagebox.showinfo("Sucesso", f"Arquivo {formato} salvo com sucesso!")


# Interface gráfica
root = tk.Tk()
root.title("Consulta de CNPJ")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="CNPJ:").grid(row=0, column=0, sticky="e")
cnpj_entry = tk.Entry(frame, width=30)
cnpj_entry.grid(row=0, column=1, padx=5)

consultar_button = tk.Button(frame, text="Consultar", command=realizar_consulta)
consultar_button.grid(row=0, column=2, padx=5)

resultado_text = tk.Text(root, wrap=tk.WORD, height=20, width=80)
resultado_text.pack(padx=10, pady=10)

pdf_button = tk.Button(root, text="Exportar para PDF", state=tk.DISABLED)
pdf_button.pack(side=tk.LEFT, padx=10, pady=5)

xls_button = tk.Button(root, text="Exportar para XLS", state=tk.DISABLED)
xls_button.pack(side=tk.RIGHT, padx=10, pady=5)

root.mainloop()
