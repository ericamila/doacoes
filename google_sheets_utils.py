import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Caminho para o arquivo JSON das credenciais (ajuste conforme a sua estrutura)
CREDENTIALS_FILE = 'alura-dash0002-4b6f6030833c.json'

# ID da sua planilha do Google Sheets
SPREADSHEET_ID = '13WgMVQELQy8JDyFFBU2AWMmzbQla77B1xot7PWZy60A'

def get_google_sheets_service():
    """Autentica e retorna o serviço da Google Sheets API."""
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE)
        service = build('sheets', 'v4', credentials=creds)
        return service
    except Exception as e:
        print(f"Erro ao autenticar com a Google Sheets API: {e}")
        return None

def read_sheet_data(spreadsheet_id, sheet_name):
    """Lê todos os valores de uma aba específica da planilha."""
    service = get_google_sheets_service()
    if not service:
        return None

    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f'{sheet_name}!A:Z'  # Lê todas as colunas (ajuste se necessário)
        ).execute()
        values = result.get('values', [])
        if not values:
            print(f'Nenhum dado encontrado na aba "{sheet_name}".')
            return []
        else:
            headers = values[0]
            data = [dict(zip(headers, row)) for row in values[1:]]
            return data
    except Exception as e:
        print(f'Erro ao ler a aba "{sheet_name}": {e}')
        return None

def load_data_from_sheets():
    """Lê os dados de todas as abas e retorna um dicionário."""
    data = {}
    data['EMPENHOS'] = read_sheet_data(SPREADSHEET_ID, 'EMPENHOS')
    data['LIQUIDACOES'] = read_sheet_data(SPREADSHEET_ID, 'LIQUIDACOES')
    data['PAGAMENTOS'] = read_sheet_data(SPREADSHEET_ID, 'PAGAMENTOS')
    return data

if __name__ == '__main__':
    loaded_data = load_data_from_sheets()
    if loaded_data:
        print(json.dumps(loaded_data, indent=4, ensure_ascii=False))