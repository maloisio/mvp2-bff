# 🔗 MVP2 — Healthcare BFF

Backend for Frontend (**BFF**) responsável por centralizar a comunicação entre a interface web e os serviços de backend do sistema de gestão de saúde.

O BFF disponibiliza uma **API GraphQL** para o frontend e, internamente, realiza chamadas **REST** para os backends responsáveis por pacientes e consultas.

Este serviço faz parte de uma arquitetura composta por:

* [**Frontend** — interface web (docker-composer)](https://github.com/maloisio/mvp2-healthcare-frontend)
* [**BFF (Backend for Frontend)** — API GraphQL que centraliza as requisições do frontend](https://github.com/maloisio/mvp2-bff)
* [**Patient Backend** — gerenciamento de pacientes](https://github.com/maloisio/mvp2-patient-backend)
* [**Scheduling Backend** — gerenciamento de consultas](https://github.com/maloisio/mvp2-scheduling-backend)



---

# 📌 Responsabilidade

O BFF funciona como uma camada intermediária entre o frontend e os serviços da aplicação.

Sua principal responsabilidade é:

* Expor uma API GraphQL para o frontend
* Receber queries e mutations do frontend
* Consultar o Patient Backend através de REST
* Consultar o Scheduling Backend através de REST
* Combinar dados provenientes de diferentes serviços
* Encaminhar operações de criação, atualização e remoção
* Consumir a API externa ViaCEP para consulta de endereços



# ️ 🚀 Como executar

### As instruções de como executar estão no diretório do projeto [mvp2-healthcare-frontend](https://github.com/maloisio/mvp2-healthcare-frontend)



# 🏗️ Arquitetura

```text
┌─────────────────────┐
│      Frontend       │
│   HTML / CSS / JS   │
└──────────┬──────────┘
           │
           │ GraphQL
           ▼
┌─────────────────────┐ REST  ┌─────────┐    
│         BFF         │◄─────►│  ViaCEP │ 
│ Flask + Ariadne     │       │         │ 
└──────────┬──────────┘       └─────────┘
           │
           ├──────────────────────────┐
           │                          │
           │ REST                     │ REST
           ▼                          ▼
┌─────────────────────┐      ┌─────────────────────┐
│   Patient Backend   │◄────►│ Scheduling Backend  │
│      Flask          │      │       Flask         │
└─────────────────────┘      └─────────────────────┘
           │                          │
           ▼                          ▼
      Banco de dados             Banco de dados
```


---

# 🔄 Como funciona a comunicação

O GraphQL é utilizado **entre o frontend e o BFF**.

Os backends continuam disponibilizando suas próprias APIs REST.

Portanto, o fluxo principal é:

```text
Frontend
   │
   │ GraphQL
   ▼
BFF
   │
   ├── REST ──► Patient Backend
   │
   └── REST ──► Scheduling Backend
```

Essa separação permite que o frontend conheça apenas a API GraphQL do BFF, enquanto os detalhes das APIs REST dos serviços ficam encapsulados no BFF.

---

# 🚀 Por que utilizar um BFF?

O BFF permite adaptar os dados dos serviços às necessidades da interface.

Por exemplo, o Patient Backend possui informações do paciente, enquanto o Scheduling Backend possui as consultas.

O frontend pode solicitar:

```graphql
query {
  patients {
    patient_id
    name
    phone
    profession
    total_appointments
  }
}
```

O BFF consulta os serviços necessários e monta uma resposta única.

```text
             GraphQL
Frontend ───────────────► BFF
                           │
                           ├── GET /patients
                           │
                           └── GET /appointments/batch
                                      │
                                      ▼
                              Dados combinados
```

Dessa forma, o frontend não precisa realizar múltiplas chamadas REST para descobrir informações relacionadas.

---

# 🧩 GraphQL

O BFF utiliza **Ariadne** para implementar GraphQL.

Endpoint:

```text
POST http://localhost:5002/graphql
```

Interface GraphiQL:

```text
http://localhost:5002/graphql
```

---


# 🌐 Comunicação REST interna

O BFF possui services específicos para comunicação com cada backend:

```text
services/
├── patient_service.py
├── scheduling_service.py
└── address_service.py
```

#

O `patient_service.py` é responsável pelas chamadas ao Patient Backend.




O `scheduling_service.py` realiza chamadas ao Scheduling Backend.

O `address_service.py` realiza chamadas para o serviço externo de endereços ViaCEP.




---

# 🏠 ViaCEP

O BFF também possui integração com a API pública do **ViaCEP** para consulta de endereços através do CEP.

Fluxo:

```text
Frontend
   │
   │ GraphQL addressByCep
   ▼
BFF
   │
   │ HTTP
   ▼
ViaCEP
   │
   ▼
Endereço
```

O dado retornado pelo serviço externo é processado pelo BFF e disponibilizado ao frontend através do GraphQL.

O frontend não precisa acessar ou redirecionar o usuário para o ViaCEP.


---

#  🐳 Execução com Docker

A aplicação também possui um `Dockerfile`.

A imagem pode ser construída com:

```bash
docker build -t healthcare-bff .
```

##  Entretanto, no ambiente completo do projeto, o serviço é executado pelo `docker-compose.yml` localizado no repositório principal do frontend.

Caso queira subir individualmente o bff, algumas opções abaixo:



### 🚀 Execução local

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python app.py
```

O BFF estará disponível em:

```text
http://localhost:5002
```

GraphiQL:

```text
http://localhost:5002/graphql
```

---


# 📁 Estrutura

```text
mvp2-bff/
├── graphql_api/
│   ├── schema.py
│   ├── queries.py
│   └── mutations.py
├── services/
│   ├── patient_service.py
│   ├── scheduling_service.py
│   └── address_service.py
├── logger.py
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

### `graphql_api/`

Contém a definição e implementação da API GraphQL.

```text
graphql_api/
├── schema.py
├── queries.py
└── mutations.py
```

### `services/`

Contém a lógica de comunicação com serviços externos ao BFF.

```text
services/
├── patient_service.py
├── scheduling_service.py
└── address_service.py
```
# 🛠️ Tecnologias

* Python 3.12
* Flask
* Ariadne
* GraphQL
* Requests
* Flask-CORS
* Docker
* ViaCEP

---

# 📌 Resumo

O BFF possui três responsabilidades principais:

### 1. Interface GraphQL

```text
Frontend → GraphQL → BFF
```

### 2. Integração com os backends

```text
BFF → REST → Patient Backend
BFF → REST → Scheduling Backend
```

### 3. Composição de dados

O BFF pode consultar diferentes serviços e entregar ao frontend uma resposta única e adequada às necessidades da interface.

Assim, o frontend não precisa conhecer a estrutura interna dos backends nem realizar diretamente chamadas para cada serviço.
