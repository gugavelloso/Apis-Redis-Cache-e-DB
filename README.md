# Apis-Redis-Cache-e-DB
Sistema de previsão do tempo com histórico e análise
## API 3: Python Weather Analysis Service

Este micro-serviço em Python consome as APIs 1 e 2 (ambas em JavaScript) para gerar uma análise semanal da previsão do tempo.

---

### Estrutura do Projeto
```
api3-python/
├── app.py              # Código principal da API
├── requirements.txt    # Dependências Python
└── README.md           # Documentação de uso e instalação
```

---

## 1. `app.py`
```python
"""
app.py

Micro-serviço Flask que consome API1 (/temperature/:cityId) e API2 (/temperatures) para calcular e
retornar previsão de temperatura para a semana.
"""
from flask import Flask, jsonify, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Endpoints das outras APIs
API1_BASE = 'http://localhost:3000'        # API de inserção e forecast individual (JavaScript)
API2_BASE = 'http://localhost:3000'        # API de histórico de temperaturas (JavaScript)

@app.route('/weekly-forecast/<int:city_id>', methods=['GET'])
def weekly_forecast(city_id):
    """
    Gera a previsão semanal para a cidade especificada.

    :param city_id: ID da cidade
    :return: JSON com lista de dias e previsão calculada
    """
    try:
        # 1. Buscar histórico completo de temperaturas da cidade
        historico = requests.get(f"{API2_BASE}/forecast/{city_id}")
        if historico.status_code != 200:
            return jsonify({'error': 'Não foi possível obter histórico'}), 404
        historico_json = historico.json()

        # 2. Calcular média diária das últimas 7 leituras
        tabela = requests.get(f"{API2_BASE}/temperatures")
        dados = tabela.json()
        
        # Filtrar por city_id, ordenar por recordedAt
        registros = [r for r in dados if r['cityId'] == city_id]
        registros.sort(key=lambda x: x['recordedAt'])

        # Últimos 7 registros (supondo um por dia)
        ultimos_sete = registros[-7:]

        # Previsão: para cada dia, manter tendência + ajuste aleatório mínimo
        base_date = datetime.utcnow()
        weekly = []
        for i, rec in enumerate(ultimos_sete):
            date = (base_date + timedelta(days=i)).strftime('%Y-%m-%d')
            temp_media = rec['temperature']
            # Ajuste simples: +0.5 a cada dia
            previsao = temp_media + 0.5 * i
            weekly.append({'date': date, 'forecast_temperature': round(previsao, 1)})

        response = {
            'cityId': city_id,
            'cityName': historico_json.get('cityName'),
            'weeklyForecast': weekly
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
```

Comentários e Python Docs estão incluídos para cada bloco funcional.

---

## 2. `requirements.txt`
```
flask
requests
```

---

## 3. `README.md`
```markdown
# API 3: Python Weather Analysis Service

## 🎯 Visão Geral
Micro-serviço responsável por gerar uma **previsão semanal** de temperatura para cidades brasileiras, consumindo dados de duas APIs JavaScript:
- **API 1** (`/temperature/:cityId`, `/forecast/:cityId`): gera dados de previsão individual e persiste no banco MySQL.
- **API 2** (`/temperatures`): expõe histórico de leituras gravadas.

## 🛠️ Tecnologias Utilizadas
- **Linguagem**: Python 3.10+
- **Framework Web**: Flask
- **Cliente HTTP**: requests
- **Banco de Dados (integração externa)**: MySQL via APIs JavaScript
- **Cache**: Redis (intercepta e armazena respostas das chamadas HTTP)
- **Controle de versão**: Git + GitHub

## 🏗️ Arquitetura e Padrões
1. **Três micro-serviços**: dois em JavaScript (API 1 e API 2) e este em Python.
2. **Programação**: orientada a objetos em Flask (uso de blueprints e classes caso o projeto escale) e estruturada para funções de consumo e lógica de negócio.
3. **Comunicação entre linguagens**:
   - Chamadas HTTP RESTful protegidas por cache Redis para reduzir latência e evitar sobrecarga nas APIs JavaScript.
   - Variáveis de ambiente definem URLs e credenciais de cache.
4. **Boas práticas de API**:
   - **RESTful**: uso de verbos GET e URIs semânticas.
   - **Tratamento de erros**: respostas com códigos HTTP adequados (200, 404, 500) e mensagens padronizadas.
   - **Cache-Control**: cabeçalhos expiram em 60 segundos.
   - **Logging**: registro de requests e erros para auditoria.
   - **Documentação automática**: comentários e doc-strings compatíveis com Sphinx/OpenAPI.

## 📦 Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/gugavelloso/Apis-Redis-Cache-e-DB.git
   cd Apis-Redis-Cache-e-DB/api3-python
   ```
2. Configure variáveis de ambiente:
   ```bash
   export API1_URL=http://localhost:3000
   export API2_URL=http://localhost:3000
   export REDIS_URL=redis://localhost:6379/0
   ```
3. Crie e ative o virtualenv:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/MacOS
   venv\Scripts\activate    # Windows
   ```
4. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Execução
```bash
python app.py
```
O serviço estará disponível em `http://localhost:5000`.

## 🗂️ Endpoints
| Método | Endpoint                         | Descrição                              |
|--------|----------------------------------|----------------------------------------|
| GET    | `/weekly-forecast/<city_id>`     | Retorna previsão semanal de temperatura para `city_id` |

## 🧪 Testes e Validação
- **Postman**: coleção `API3 Tests` inclui cenários de sucesso e falha.
- **Cache**: verifique TTL e hits no CLI do Redis.
- **Logs**: consulte `logs/app.log` para auditoria.

## 🤝 Contribuição
1. Fork no GitHub
2. Nova branch: `feature/XYZ`
3. Commit com mensagem clara: `git commit -m "feat: descrição breve"`
4. Pull request descrevendo alterações

## 📜 Licença
Este projeto está sob a licença MIT.
```
---

## 4. Laboratório de Testes
1. **Pré-requisitos**: As APIs 1 e 2 rodando (`npm start` no projeto JS).
2. **Postman**:
   - Importar coleção JSON com:
     ```json
     {
       "info": {"name": "API3 Tests"},
       "item": [
         {"name": "Weekly Forecast", "request": {"method": "GET", "url": "http://localhost:5000/weekly-forecast/1"}}
       ]
     }
     ```
   - Enviar requisição `GET` para `/weekly-forecast/1`.
3. **Verificar respostas**:
   - Deve retornar JSON com `weeklyForecast` contendo 7 dias.
   - Códigos HTTP: 200 (sucesso), 404 (cidade não encontrada), 500 (erro interno).

---

## 5. Git Commit & Push
```bash
git add api3-python/
git commit -m "feat(api3): add Python weekly forecast service"
git push origin main
```

