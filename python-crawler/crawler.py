import requests
import json
import time
from datetime import datetime

# Configurações
API_URL = "https://buildmatch-homolog.up.railway.app/api/products" # URL do seu Backend

# Simulação de Web Scraping (Para integração real, usaríamos Selenium ou BeautifulSoup)
def fetch_prices():
    print(f"[{datetime.now()}] Iniciando captura de preços nos fornecedores...")
    
    # Exemplo de dados que seriam capturados dos sites
    market_data = [
        {"name": "Porcelanato Retificado 60x60", "category": "Acabamentos", "supplier": "Leroy Merlin", "price": 92.50, "unit": "m2"},
        {"name": "Porcelanato Retificado 60x60", "category": "Acabamentos", "supplier": "Obramax", "price": 86.90, "unit": "m2"},
        {"name": "Cimento CP II 50kg", "category": "Materiais Brutos", "supplier": "Obramax", "price": 34.50, "unit": "saco"},
        {"name": "Cimento CP II 50kg", "category": "Materiais Brutos", "supplier": "Telhanorte", "price": 36.20, "unit": "saco"},
        {"name": "Tinta Acrílica Branca 18L", "category": "Acabamentos", "supplier": "C&C", "price": 289.00, "unit": "lata"},
        {"name": "Luminária Pendente Industrial", "category": "Estética", "supplier": "Tok&Stok", "price": 245.00, "unit": "unid"}
    ]
    return market_data

def update_hub():
    products = fetch_prices()
    success_count = 0
    
    for prod in products:
        try:
            # Envia para a API Java para salvar/atualizar no Postgres
            response = requests.post(API_URL, json=prod)
            if response.status_code in [200, 201]:
                success_count += 1
                print(f"Sucesso: {prod['name']} em {prod['supplier']} atualizado.")
        except Exception as e:
            print(f"Erro ao atualizar {prod['name']}: {e}")
            
    print(f"[{datetime.now()}] Sincronização finalizada. {success_count} itens atualizados.")

if __name__ == "__main__":
    # Para rodar diariamente no Railway, podemos usar um loop ou um agendador (Cron)
    update_hub()
