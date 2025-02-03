import requests
from dotenv import load_dotenv
from tkinter import filedialog, messagebox
import os
import logging
import base64

# Configurar logs
logging.basicConfig(level=logging.INFO)

# Carregar variáveis de ambiente
load_dotenv()
AUTH_KEY = os.getenv("AUTH_KEY")


def obter_token():
    """
    Obtém o token de acesso do serviço Serpro.
    """
    url = "https://gateway.apiserpro.serpro.gov.br/token"
    headers = {
        "Authorization": f"Basic {AUTH_KEY}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao obter token: {e}")
        return None


def consultar_cnd(token, tipo_contribuinte, contribuinte, codigo_identificacao, gerar_certidao):
    """
    Consulta a CND e, opcionalmente, gera a certidão em PDF.
    """
    url = "https://gateway.apiserpro.serpro.gov.br/consulta-cnd/v1/certidao"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "TipoContribuinte": tipo_contribuinte,
        "ContribuinteConsulta": contribuinte,
        "CodigoIdentificacao": codigo_identificacao,
        "GerarCertidaoPdf": gerar_certidao
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro na consulta de CND: {e}")
        return None


def exportar_pdf_base64(nome_arquivo, base64_content):
    """
    Decodifica o conteúdo Base64 e salva como um arquivo PDF.
    """
    try:
        # Verificar se o conteúdo Base64 foi recebido corretamente
        print("Conteúdo Base64 recebido:", base64_content[:50], "...")  # Mostra os primeiros 50 caracteres do Base64
        
        # Decodifica o conteúdo Base64
        try:
            pdf_data = base64.b64decode(base64_content)
            print("Base64 decodificado com sucesso.")  # Log de sucesso na decodificação
        except Exception as e:
            print("Erro na decodificação do Base64:", e)
            messagebox.showerror("Erro", f"Erro na decodificação do conteúdo Base64: {e}")
            return

        # Abrir a caixa de diálogo para salvar o arquivo
        print("Abrindo caixa de diálogo para salvar o arquivo...")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Salvar Certidão em PDF",
            initialfile=f"{nome_arquivo}.pdf"
        )

        # Verificar se o caminho do arquivo foi escolhido
        if not file_path:
            print("Salvamento cancelado pelo usuário.")  # Log para cancelamento
            logging.info("Salvamento cancelado pelo usuário.")
            return

        print(f"Caminho do arquivo escolhido: {file_path}")  # Log do caminho escolhido

        # Salva o PDF no local escolhido
        try:
            with open(file_path, "wb") as pdf_file:
                pdf_file.write(pdf_data)
            logging.info(f"Certidão salva em {file_path}.")
            print(f"Certidão salva com sucesso em: {file_path}")  # Log de sucesso no salvamento
            messagebox.showinfo("Sucesso", f"Certidão salva com sucesso em:\n{file_path}")
        except Exception as e:
            print(f"Erro ao salvar o PDF: {e}")  # Log de erro no salvamento
            logging.error(f"Erro ao salvar o PDF: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar o PDF: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")  # Log de erro geral
        logging.error(f"Erro inesperado: {e}")
        messagebox.showerror("Erro", f"Erro inesperado: {e}")
