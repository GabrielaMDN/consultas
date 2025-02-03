import tkinter as tk
from tkinter import BooleanVar, IntVar, messagebox
from utils import consultar_cnd, obter_token, exportar_pdf_base64
import logging
import base64


def atualizar_dica_identificacao(*args):
    """
    Atualiza a dica do Código de Identificação com base no Tipo de Contribuinte.
    """
    try:
        tipo = tipo_contribuinte_var.get()
        if tipo == 1:  # CNPJ
            dica_identificacao_label.config(text="Código para CNPJ: 9001")
        elif tipo == 2:  # CPF
            dica_identificacao_label.config(text="Código para CPF: 9002")
        else:
            dica_identificacao_label.config(text="Tipo inválido")
    except tk.TclError:
        dica_identificacao_label.config(text="Tipo inválido")

def realizar_consulta():
    """
    Realiza a consulta de CND com base nos inputs do usuário.
    """
    tipo_contribuinte = tipo_contribuinte_var.get()
    contribuinte = contribuinte_entry.get().strip()
    codigo_identificacao = codigo_identificacao_entry.get().strip()
    gerar_certidao = gerar_certidao_var.get()

    if not contribuinte or not codigo_identificacao:
        messagebox.showwarning("Entrada inválida", "Preencha todos os campos obrigatórios.")
        return

    token = obter_token()
    if token:
        resultado = consultar_cnd(
            token,
            tipo_contribuinte,
            contribuinte,
            codigo_identificacao,
            gerar_certidao
        )

        if resultado:
            resultado_text.delete("1.0", tk.END)
            resultado_text.insert(tk.END, resultado)

            if gerar_certidao:
                # Verificar se a API retornou o conteúdo em Base64
                base64_content = resultado.get("Certidao", {}).get("DocumentoPdf")  # Caminho correto para o campo
            if base64_content:
                print("Base64 encontrado na resposta. Exportando PDF...")
                exportar_pdf_base64("certidao_cnd", base64_content)
            else:
                print("O campo 'DocumentoPdf' não foi encontrado na resposta da API.")

            
            # Log da resposta completa para depuração
            logging.debug(f"Resposta da API: {resultado}")


# Interface gráfica
root = tk.Tk()
root.title("Consulta de CND")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Campo Tipo de Contribuinte
tk.Label(frame, text="Tipo de Contribuinte (1=CNPJ, 2=CPF):").grid(row=0, column=0, sticky="e")
tipo_contribuinte_var = IntVar(value=1)
tipo_contribuinte_entry = tk.Entry(frame, textvariable=tipo_contribuinte_var, width=10)
tipo_contribuinte_entry.grid(row=0, column=1, padx=5)

# Monitorar mudanças no Tipo de Contribuinte
tipo_contribuinte_var.trace("w", atualizar_dica_identificacao)

# Campo Contribuinte
tk.Label(frame, text="Contribuinte (CNPJ ou CPF) *sem pontos ou traços:").grid(row=1, column=0, sticky="e")
contribuinte_entry = tk.Entry(frame, width=30)
contribuinte_entry.grid(row=1, column=1, padx=5)

# Campo Código de Identificação
tk.Label(frame, text="Código de Identificação:").grid(row=2, column=0, sticky="e")
codigo_identificacao_entry = tk.Entry(frame, width=30)
codigo_identificacao_entry.grid(row=2, column=1, padx=5)

# Dica do Código de Identificação
dica_identificacao_label = tk.Label(frame, text="Código para CNPJ: 9001", fg="gray")
dica_identificacao_label.grid(row=2, column=2, sticky="w")

# Opção de Gerar Certidão
gerar_certidao_var = BooleanVar(value=False)
tk.Checkbutton(frame, text="Gerar Certidão em PDF", variable=gerar_certidao_var).grid(row=3, columnspan=2, sticky="w")

# Botão de Consultar
consultar_button = tk.Button(frame, text="Consultar", command=realizar_consulta)
consultar_button.grid(row=4, column=0, columnspan=2, pady=10)

# Resultado
resultado_text = tk.Text(root, wrap=tk.WORD, height=20, width=80)
resultado_text.pack(padx=10, pady=10)

root.mainloop()
