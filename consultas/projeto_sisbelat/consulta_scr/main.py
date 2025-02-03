import tkinter as tk
from tkinter import messagebox, filedialog
from utils import obter_token, consulta_completa, exportar_para_excel
import os

def iniciar_consulta():
    email = entry_email.get()
    password = entry_password.get()
    cpf_cnpj = entry_cpf_cnpj.get()
    data_base = entry_data_base.get()
    authorized = 'S' if authorized_var.get() else 'N'

    try:
        token = obter_token(email, password)
        dados = consulta_completa(token, cpf_cnpj, data_base, authorized)
        links_dados = {k: v for k, v in dados['retorno_completa'].items() if v}

        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Salvar Dados SCR"
        )
        if save_path:
            exportar_para_excel(links_dados, save_path)
            messagebox.showinfo("Sucesso", f"Dados salvos em {save_path}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Configurar a interface do Tkinter
root = tk.Tk()
root.title("Consulta SCR")
root.geometry("500x300")  # Define o tamanho padrão da janela (largura x altura)
root.resizable(False, False)  # Torna a janela não redimensionável


tk.Label(root, text="Email:").pack()
entry_email = tk.Entry(root, width=70)
entry_email.pack()

tk.Label(root, text="Senha:").pack()
entry_password = tk.Entry(root, show="*", width=70)
entry_password.pack()

tk.Label(root, text="CPF/CNPJ:").pack()
entry_cpf_cnpj = tk.Entry(root, width=70)
entry_cpf_cnpj.pack()

tk.Label(root, text="Data Base (AAAA-MM):").pack()
entry_data_base = tk.Entry(root, width=70)
entry_data_base.pack()

authorized_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Authorized (S)", variable=authorized_var).pack()

tk.Button(root, text="Consultar e Exportar", command=iniciar_consulta).pack(pady=10)

root.mainloop()
