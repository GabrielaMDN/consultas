import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
from PIL import Image, ImageTk
import webbrowser
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
load_dotenv()
USUARIO_VALIDO = os.getenv("USUARIO")
SENHA_VALIDA = os.getenv("SENHA")

# Janela de login para autenticação
class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Autenticação")
        self.geometry("300x150")
        self.parent = parent

        # Criação dos widgets de usuário e senha
        tk.Label(self, text="Usuário:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Senha:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_senha = tk.Entry(self, show="*")
        self.entry_senha.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self, text="Entrar", command=self.verificar_login).grid(row=2, column=0, columnspan=2, pady=10)

        # Impede que a janela seja fechada sem autenticação
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        # Verifica se o usuário e a senha conferem com os valores do .env
        if usuario == USUARIO_VALIDO and senha == SENHA_VALIDA:
            self.parent.authenticated = True  # Usuário autenticado com sucesso
            self.destroy()  # Fecha a janela de login
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    def on_close(self):
        # Impede que o usuário feche a janela sem se autenticar
        messagebox.showwarning("Atenção", "Você precisa se autenticar para continuar!")

# Interface principal do sistema
class InterfaceCentral(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sisbelat")
        self.geometry("600x350")
        self.authenticated = False  # Flag que indica se o usuário já se autenticou

        self.menu_lateral()
        self.cabecalho()
        self.area_principal()

    def abrir_site_1(self):
        webbrowser.open("https://api.infosimples.com/login")

    def abrir_site_2(self):
        webbrowser.open("https://empresas.serasaexperian.com.br/meus-produtos/login")

    def abrir_site_3(self):
        webbrowser.open("https://listacnae.com.br/app/login")

    def menu_lateral(self):
        menu_frame = tk.Frame(self, bg="lightgray", width=200)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        botoes = [
            ("Consulta CNPJ", self.abrir_consulta_cnpj),
            ("Consulta CND", self.abrir_consulta_cnd),
            ("Dívida Ativa", self.abrir_consulta_divida_ativa),
            ("Consulta SCR", self.abrir_consulta_scr),
            ("Infosimples", self.abrir_site_1),
            ("Serasa", self.abrir_site_2),
            ("Lista CNAE", self.abrir_site_3),
        ]

        for nome, func in botoes:
            btn = tk.Button(menu_frame, text=nome, command=func, bg="white", width=20, pady=5)
            btn.pack(pady=5)

    def cabecalho(self):
        cabecalho_frame = tk.Frame(self, background="#00C7AA", height=50)
        cabecalho_frame.pack(side=tk.TOP, fill=tk.X)
        cabecalho_label = tk.Label(cabecalho_frame, text="Sistema de Consultas", font=("Arial", 20), bg="#00C7AA")
        cabecalho_label.pack(pady=10)

    def area_principal(self):
        self.centro_frame = tk.Frame(self, bg="white")
        self.centro_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.exibir_logo()

    def exibir_logo(self):
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        try:
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((400, 200), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(self.centro_frame, image=logo_photo, bg="white")
            logo_label.image = logo_photo  # Mantém referência para evitar garbage collection
            logo_label.pack(expand=True)
        except Exception as e:
            print(f"Erro ao carregar o logo: {e}")

    def abrir_consulta_cnpj(self):
        self.executar_consulta("consulta_cnpj")

    def abrir_consulta_cnd(self):
        self.executar_consulta("consulta_cnd")

    def abrir_consulta_divida_ativa(self):
        self.executar_consulta("consulta_divida_ativa")

    def abrir_consulta_scr(self):
        self.executar_consulta("consulta_scr")

    def executar_consulta(self, consulta_nome):
        """
        Executa a consulta desejada.
        Caso o usuário ainda não esteja autenticado, abre a janela de login.
        """
        if not self.authenticated:
            login_window = LoginWindow(self)
            self.wait_window(login_window)  # Aguarda o fechamento da janela de login
            if not self.authenticated:
                return  # Se não autenticado, interrompe a execução

        # Caminho para o script da consulta
        caminho_consulta = os.path.join(os.path.dirname(__file__), f"../{consulta_nome}/main.py")
        try:
            subprocess.Popen([sys.executable, caminho_consulta])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir a consulta {consulta_nome}:\n{e}")

# Inicialização da interface principal
if __name__ == "__main__":
    app = InterfaceCentral()
    app.mainloop()
