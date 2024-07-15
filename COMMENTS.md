# Comments
Meus comentários a respeito do desenvolvimento projeto.

### Algoritmo de Busca por Texto
Buscar texto em um grande volume de dados pode ser bastante custoso se utilizado algoritmos com alta complexidade. Para tal, penso em utilizar o ElasticSearch que é um motor de busca bastante eficiente e open-source, e implementa o famoso *reverse indexing* que otimiza a busca por texto. 

Segundo minhas pesquisas, a complexidade da busca deve ser `O(1)` no caso médio, mas alguns usuários relataram o contrário — dadas algumas circunstâncias — e eu ainda não encontrei na documentação oficial a sua complexidade. Pelo menos, a sua complexidade certamente é `O(log(n))`, o que já é melhor do que utilizar um algoritmo de busca por padrão, no qual o menor custo é `O(n)`.

### Persistência dos Dados
Como a única informação que eu pretendo persistir e recuperar é um único texto por linha, não faz sentido ao meu ver, para este projeto, a utilização de um banco de dados. Sendo assim, irei apenas criar um arquivo JSON para seeding, e uma rota na API para adicionar novos textos.

É possível popular a aplicação através do pacote `seeder` no back-end.

### Back-end (API)
Para o back-end, eu resolvi utilizar FastAPI. Nenhum motivo especial. Apenas por ser uma ótima ferramenta para desenvolvimento de servidores API, por eu ter uma certa familiaridade com ele e ser mais simples e comum para o propósito.

Bem no início do projeto, eu havia implementado uma "mini" arquitetura MVC para a API — utilizando Pydantic para tratar as entradas das rotas — porém modifiquei a estrutura do projeto após eu aprender sobre o GraphQL. Inclusive, devo dizer que ficou até mais enxuto o código.

Para me comunicar com o motor de busca, estou utilizando a biblioteca [`elasticsearch`](https://elasticsearch-py.readthedocs.io/), e para o GraphQL estou usando a biblioteca [`strawberry`](https://strawberry.rocks/), para tornar mais fácil o desenvolvimento do back-end em Python pois, além do mesmo já implementar um servidor GraphQL, ele ainda conta com suporte para o FastAPI.

Além disso, durante o desenvolvimento, eu criava uma instância do Elasticsearch fora do servidor, para ser utilizado nas rotas do GraphQL. Depois, eu descobri sobre o `context_getter` do `strawberry`, e passei a utilizar o Elasticsearch como uma dependência, tal como é feito com instâncias de banco de dados. Isso facilitou inclusive o desenvolvimento dos testes, para mockar o Elasticsearch na API.

Também estou utilizando o pacote [`fastapi-cache2`](https://pypi.org/project/fastapi-cache2/) para cachear os resultados da API, a fim de otimizar as requisições.

Implementei também uma rota para obter todos os documentos do motor de busca — para realizar testes e saber se o motor de busca e a inserção está funcionando certinho. Pensando em evitar abusos, caso o motor de busca venha a guardar um grande volume de termos, implementei uma paginação para barrar a sobrecarga do servidor e da rede.

Desde o início do projeto, eu já estava em mente de utilizar o Elasticsearch de forma assíncrona, para não atrasar as requests de outros usuários. Então pesquisei sobre e descobri que havia o `AsyncElasticsearch` que, segundo a documentação, era a mesma coisa que usar a classe `Elasticsearch`, porém usando o `await` nos métodos. Então, para agilizar logo as tarefas, tendo em vista que é um projeto pequeno, desenvolvi tudo com a classe `Elasticsearch` — com as rotas do GraphQL assíncronas — para depois passar as suas chamadas para *async*. Neste momento, pensei ser uma boa estratégia, porque o Elasticsearch já estava me dando alguns problemas de configuração, e começar a fazer as coisas com o seu *client* assíncrono me parecia ser um impecilho em potencial para dar continuidade com as outras tarefas. No final das contas, consegui passar o seu *client* de síncrono para assíncrono sem qualquer dificuldade, como eu planejava. Mas agora que eu estou fazendo uma reflexão de tudo o que eu fiz, considero que essa decisão talvez tenha sido errada, uma vez que, tratando o assincronismo do Elasticsearch como um requisito, talvez fosse melhor tratar os seus problemas durante o desenvolvimento do que depois de ter tudo pronto. Todavia, se fosse em um de maior escala, certamente eu escolheria por desenvolver tudo desde o início com o seu *client* assíncrono.

### Front-end
Para o front-end, tal como é pedido nos requisitos do projeto, utilizei React.js.

Para fins de simplificade e também devido à minha falta de habilidade em design, optei por utilizar os componentes do [Material UI](https://mui.com/) para criar a página do front. A caixa de pesquisa foi feita utilizando o `Autocomplete`, que além de ter um visual bastante agradável, traz consigo vários recursos.

Separei os elementos visuais no pacote `components` e as funcionalidades no pacote `services`.

Devido à minha falta de experiência em desenvolvimento front-end, a minha maior dificuldade no projeto foi a tarefa de manter apenas 10 sugestões visíveis na caixa de sugestões, e ainda fazendo isso de forma responsiva. Foi onde eu mais demorei.

### Testes
Implementei no back-end testes — utilizando unittest — para verificar o funcionamento do Elasticsearch e das rotas do GraphQL.

Pesquisei por um mock do Elasticsearch, porém o melhor pacote que eu encontrei foi o [`ElasticMock`](https://pypi.org/project/ElasticMock/), que apresentava erros devido à incompatibilidade da minha versão do Elasticsearch. Além disso, olhando as suas issues, fiquei um pouco com um pé atrás pois seria uma depêndencia no projeto sem muito suporte, e eu não teria tanto controle quanto ao seu funcionamento. Então, para o teste do motor de busca, decidi criar um *index* de teste somente para testes, que é sempre resetado no início e no final do teste.

Para o teste das rotas do GraphQL, eu entendo que é uma boa prática um teste não depender do outro. Sendo assim, criei um mock da minha classe `SearchEngine` — está no módulo `mocked.py` — para ser utilizado nas rotas do servidor. Realizei essa alteração no `app.dependency_overrides`. Também estou utilizando o `TestClient` do FastAPI para testar as rotas sem precisar inicializar o servidor de fato.

### Formatação de Código
Estou utilizando o [`Flake8`](https://flake8.pycqa.org/) para verificar a estilização do back-end e o [`Black`](https://pypi.org/project/black/) para formatar. O `black` em alguns poucos momentos é meio chatinho e acaba formatando alguns trechos de uma maneira que não me agrada muito — como colocar toda estrutura de um dicionário em uma única linha, quando eu queria a estrutura indentada para melhor visibilidade — mas no geral é um ótimo formatador de código.

Para o front-end, estou utilizando o [`ESLint`](https://eslint.org/) e o [`Prettier`](https://prettier.io/). Coloquei as suas chamadas no `package.json` do projeto.

### Integração Contínua
Eu criei um *workflow* do GitHub Actions para o projeto, para realizar todos os testes existentes. Eu entendo que é sempre bom automatizar isso também, pois em algum momento, o desenvolvedor pode dar *push* das alterações sem fazer os testes locais antes, e alguma coisa acabar quebrando o sistema — como aconteceu comigo algumas vezes durante o desenvolvimento do projeto.

Fiz um *workflow* para o back-end e um para o front-end.

### Variáveis de Ambiente
Tanto no back-end como no front-end, existe um módulo de configuração dentro de `src` para carregar as variáveis de ambiente — ou definir seus valores padrão caso não exista. A configuração padrão desses módulos já é suficiente para rodar o projeto localmente.

### Docker
Todo o projeto, como foi pedido nos requisitos, é capaz de rodar no Docker, com apenas um único comando `docker-compose up`. O projeto inteiro é dividido em três serviços: `elasticsearch`, `backend` e `frontend`. O `frontend` e o `elasticsearch` podem ser executados separadamente dos demais, enquanto o `backend` depende do `elasticsearch` estar em execução e pronto para ser utilizado.

No comando do serviço `backend`, implementei um script para liberar a inicialização do servidor somente quando o motor de busca estiver pronto. Além disso, é possível também popular o motor de busca no *compose*, apenas definindo antes a variável de ambiente `seed=true` no seu sistema.

### Documentação
Tanto o diretório do back-end quando o diretório do front-end possuem uma documentação própria para eles, no arquivo `README.md`. Lá, é possível encontrar mais informações sobre eles. O `README.md` da raíz do repositório é destinado apenas à uma execução local simples e segura do projeto.

### Ideias para o Projeto
Irei dedicar essa seção para falar de coisas que eu faria, ou gostaria de implementar, se eu tivesse mais tempo ou caso fosse um requisito do projeto;

- Para a rota de inserção de um novo termo, eu faria um sistema de autenticação, para que essa rota fosse utilizada apenas pelos administradores;

- Assumindo que esse projeto fosse utilizado em larga escala, eu configuraria o Elasticsearch para rodar em vários clusters e com réplicas, a fim de manter o servidor funcionando normalmente em caso de um cluster cair por sobrecarga, erro ou desastres naturais.

- Ainda assumindo que esse projeto fosse utilizado em larga escala, acho que seria legal utilizar um *middleware* Anti-DDoS para evitar ataques de negação de serviço. Mas isso tem que ser feito com muito cuidado, já que o objetivo é a recuperação dos termos na maior velocidade possível;

- Implementar testes automatizados de UI;

- Caso esse projeto fosse deployado para uma cloud, eu implementaria um CD no workflow do GitHub Actions;

- Utilizar alguma ferramenta para passar as variáveis de ambiente de um arquivo para o *docker-compose*.
