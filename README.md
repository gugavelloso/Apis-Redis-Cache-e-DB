# Apis-Redis-Cache-e-DB
Sistema de previsão do tempo com histórico e análise
## API 3: Python Weather Analysis Service

## 🎯 Visão Geral
Micro-serviço responsável por gerar uma **previsão semanal** de temperatura para cidades brasileiras, consumindo dados de duas APIs JavaScript:
- **API 1** (`/temperature/:cityId`, `/forecast/:cityId`): gera dados de previsão individual e persiste no banco MySQL.
- **API 2** (`/temperatures`): expõe histórico de leituras gravadas.

## 🛠️ Tecnologias Utilizadas
- **Linguagem**: Python 3.10+
- **Framework Web**: Flask
- **Cliente HTTP**: requests
- **Banco de Dados (integração externa)**: MySQL via APIs JavaScript
- **Cache**: Redis (intercepta e armazena respostas das chamadas HTTP)
- **Controle de versão**: Git + GitHub

## 🏗️ Arquitetura e Padrões
1. **Três micro-serviços**: dois em JavaScript (API 1 e API 2) e este em Python.
2. **Programação**: orientada a objetos em Flask (uso de blueprints e classes caso o projeto escale) e estruturada para funções de consumo e lógica de negócio.
3. **Comunicação entre linguagens**:
   - Chamadas HTTP RESTful protegidas por cache Redis para reduzir latência e evitar sobrecarga nas APIs JavaScript.
   - Variáveis de ambiente definem URLs e credenciais de cache.
4. **Boas práticas de API**:
   - **RESTful**: uso de verbos GET e URIs semânticas.
   - **Tratamento de erros**: respostas com códigos HTTP adequados (200, 404, 500) e mensagens padronizadas.
   - **Cache-Control**: cabeçalhos expiram em 60 segundos.
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
