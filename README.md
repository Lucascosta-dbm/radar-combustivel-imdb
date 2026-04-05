# Radar Combustível — IMDB Project

Projeto desenvolvido para o **Trabalho Final — MBA Engenharia de Dados (SENAC)**.

O sistema simula um **pipeline moderno de dados orientado a eventos**, utilizando MongoDB, Redis e Streamlit para análise em tempo quase real de preços de combustíveis.

---

## Objetivo

Construir uma arquitetura de dados capaz de:

* ingerir eventos de preços de combustíveis;
* processar dados via pipeline Python;
* disponibilizar consultas rápidas usando Redis (Serving Layer);
* visualizar insights em tempo real através de dashboard interativo.

---

## Arquitetura da Solução

```
MongoDB (Eventos)
        ↓
Python Loader (IMDB Pipeline)
        ↓
Redis (Serving Layer)
        ↓
Streamlit Dashboard
```

---

## Tecnologias Utilizadas

* Python 3.10+
* MongoDB
* Redis
* Docker
* Streamlit
* Pandas

---

## Estruturas Redis Utilizadas

| Estrutura  | Uso                           |
| ---------- | ----------------------------- |
| Sorted Set | Ranking de menores preços     |
| Sorted Set | Combustíveis mais buscados    |
| Sorted Set | Variação percentual de preços |
| GEO        | Localização de postos         |

Motivo: consultas extremamente rápidas (O(log N)) ideais para dashboards.

---

## Como Executar o Projeto

### Clonar repositório

```bash
git clone https://github.com/Lucascosta-dbm/radar-combustivel-imdb.git
cd radar-combustivel-imdb
```

---

### Criar ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate
```

---

### Instalar dependências

```bash
pip install -r requirements.txt
```

---

### Subir bancos com Docker

```bash
docker-compose up -d
```

---

### Carregar dados no Redis

```bash
python -m src.imdb.imdb_loader
```

---

### Executar Dashboard

```bash
streamlit run dashboard.py
```

Acesse:

```
http://localhost:8501
```

---

## Funcionalidades

* KPIs em tempo real
* Ranking de postos mais baratos
* Combustíveis em alta
* Variação de preços
* Mapa geográfico de postos

---

## Estrutura do Projeto

```
src/
 ├── config/
 ├── imdb/
app/
dashboard.py
```

---

## Evidências Visuais

Imagens do funcionamento encontram-se em:

```
/docs/prints
```

---

## Integrantes

(Adicionar nomes do grupo)

---

## Licença

Projeto acadêmico — uso educacional.
