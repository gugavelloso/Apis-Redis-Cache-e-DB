"""
app.py

Micro-serviço Flask que consome API1 (/temperature/:cityId) e API2 (/temperatures) para calcular e
retornar previsão de temperatura para a semana.
"""
import os
from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta
import redis
import logging

# Configuração de logging
logging.basicConfig(filename='logs/app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)

# Carregar variáveis de ambiente
API1_BASE = os.getenv('API1_URL', 'http://localhost:3000')
API2_BASE = os.getenv('API2_URL', 'http://localhost:4000')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Setup Redis cache
cache = redis.from_url(REDIS_URL)

@app.route('/weekly-forecast/<int:city_id>', methods=['GET'])
def weekly_forecast(city_id):
    """
    Gera a previsão semanal para a cidade especificada.

    :param city_id: ID da cidade
    :return: JSON com lista de dias e previsão calculada
    """
    cache_key = f"weekly_forecast:{city_id}"
    cached = cache.get(cache_key)
    if cached:
        logging.info(f"Cache hit for city {city_id}")
        return jsonify(eval(cached))

    try:
        # Buscar histórico completo de temperaturas da cidade
        historico_resp = requests.get(f"{API1_BASE}/city/{city_id}")
        if historico_resp.status_code != 200:
            return jsonify({'error': 'Não foi possível obter histórico'}), 404
        historico_json = historico_resp.json()

        # Buscar todas leituras
        tabela_resp = requests.get(f"{API2_BASE}/weather")
        tabela_resp.raise_for_status()
        dados = tabela_resp.json()

        # Filtrar por city_id e ordenar por forecastDate
        registros = sorted(
            [r for r in dados if r['cityId'] == city_id],
            key=lambda x: x['forecastDate']
        )

        # Últimos 7 registros (supondo um por dia)
        ultimos_sete = registros[-7:]

        # Gerar previsão semanal
        base_date = datetime.utcnow()
        weekly = []
        for i, rec in enumerate(ultimos_sete):
            date = (base_date + timedelta(days=i)).strftime('%Y-%m-%d')
            temp_media = rec['temperature']
            previsao = temp_media + 0.5 * i
            weekly.append({'date': date, 'forecast_temperature': round(previsao, 1)})

        response = {
            'cityId': city_id,
            'cityName': historico_json.get('name'),
            'weeklyForecast': weekly
        }

        # Armazenar no cache por 60s
        cache.set(cache_key, str(response), ex=60)
        logging.info(f"Cache set for city {city_id} with key {cache_key}")

        return jsonify(response)

    except Exception as e:
        logging.error(f"Erro em weekly_forecast: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
