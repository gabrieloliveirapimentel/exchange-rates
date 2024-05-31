import requests
import openpyxl
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Atribuir os valores das variáveis do arquivo .env
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

# Função para buscar a taxa de câmbio usando a API da Wise
def fetch_exchange_rate():
    url = API_URL
    headers = {
        "Authorization": API_KEY
    }
    params = {
        "source": "EUR",
        "target": "BRL"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        # Verifica se a resposta é uma lista e extrai o primeiro item
        if isinstance(data, list) and data:
            data = data[0]
        # Verifica se a resposta contém o campo 'rate' e 'time'
        rate = data.get("rate") if isinstance(data, dict) else None
        time = data.get("time") if isinstance(data, dict) else None
        if rate and time:
            return time, rate
    return None

def update_excel(time, rate):
    try:
        workbook = openpyxl.load_workbook('exchange_rates.xlsx')
    except FileNotFoundError:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Rates'
        sheet.append(['Date', 'EUR', 'BRL'])
    else:
        sheet = workbook['Rates']

    existing_dates = set(cell.value for cell in sheet['A'] if cell.value != 'Date')

    if time not in existing_dates:
        sheet.append([time, 1, rate])

    workbook.save('exchange_rates.xlsx')

# Função para verificar a taxa de câmbio e enviar mensagem do WhatsApp se necessário
def check_exchange_rate():
    time, rate = fetch_exchange_rate()
    if rate and time:
        print(f"Atualizado com a nova taxa de câmbio: 1 EUR = {rate} BRL.")
        update_excel(time, rate)

# Loop principal
if __name__ == "__main__":
    check_exchange_rate()