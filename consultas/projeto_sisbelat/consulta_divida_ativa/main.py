from tkinter import Tk, Frame, Label, Entry, Button, Text, WORD, messagebox
from utils import obter_token, consultar_api, exportar_para_pdf, exportar_para_xls, organizar_resultados


def realizar_consulta():
    cnpj = cnpj_entry.get().strip()
    if not cnpj:
        messagebox.showwarning("Entrada inválida", "Por favor, insira um número de CNPJ.")
        return

    resultado_text.delete("1.0", "end")
    token = obter_token()
    if token:
        dados = consultar_api(token, cnpj)
        if dados:
            resultado_formatado = organizar_resultados(cnpj, dados)
            resultado_text.insert("1.0", resultado_formatado)

            # Ativar botões de exportação
            pdf_button.config(state="normal", command=lambda: exportar_para_pdf(cnpj, dados))
            xls_button.config(state="normal", command=lambda: exportar_para_xls(cnpj, dados))
            
        else:
            resultado_text.insert("1.0", "Nenhum dado encontrado para o CNPJ informado.")
    else:
        resultado_text.insert("1.0", "Erro ao obter o token de acesso.")

# Interface gráfica
root = Tk()
root.title("Consulta de Dívida ativa")

frame = Frame(root)
frame.pack(padx=10, pady=10)

Label(frame, text="CNPJ:").grid(row=0, column=0, sticky="e")
cnpj_entry = Entry(frame, width=30)
cnpj_entry.grid(row=0, column=1, padx=5)

consultar_button = Button(frame, text="Consultar", command=realizar_consulta)
consultar_button.grid(row=0, column=2, padx=5)

resultado_text = Text(root, wrap=WORD, height=20, width=80)
resultado_text.pack(padx=10, pady=10)

pdf_button = Button(root, text="Exportar para PDF", state="disabled")
pdf_button.pack(side="left", padx=10, pady=5)

xls_button = Button(root, text="Exportar para XLS", state="disabled")
xls_button.pack(side="left", padx=10, pady=5)

root.mainloop()