# Comments
Comentários a respeito do desenvolvimento projeto.

## Brainstorm:

### Busca de Texto
Buscar texto em um grande volume de dados pode ser bastante custoso se utilizado algoritmos com alta complexidade. Para tal, penso
em utilizar o ElasticSearch que é um motor de busca open-source.

### API
Para o back-end, eu penso em utilizar FastAPI. Nenhum motivo especial. Apenas por ser uma ótima ferramenta para desenvolvimento de
servidores API, por eu ter uma certa familiaridade com ele e ser mais simples e comum para o propósito.

Para utilizar o GraphQL, farei uso da biblioteca Strawberry.

### Persistência dos Dados
Como a única informação que eu pretendo persistir e recuperar é um único texto por linha, não faz sentido ao meu ver, para este projeto,
a utilização de um banco de dados. Sendo assim, irei apenas criar um arquivo para seeding, e uma rota na API para adicionar novos textos.

### Front-end
Para o front-end, tal como é pedido nos requisitos do projeto, utilizarei React.js. 

### Testes
Pretendo, se houver tempo, criar alguns testes unitários com Pytest ou Unittest para a API.

### Lint Code
Pretendo utilizar o `flake8` e `black` para o back e o `eslint` na aplicação React, se houver um tempinho.