# Changelog

Todas as mudanças relevantes deste template são documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o versionamento segue [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Adicionado

- Geração de `.copier-answers.yml` pelo template, permitindo `copier update`
  nos projetos criados.
- Validação de `SECRET_KEY` com no mínimo 32 caracteres.
- `CommitRequiredError` para erros de domínio que precisam persistir alterações
  antes de propagar, com teste de regressão do reuso de refresh token.
- Licença Apache-2.0 completa, selecionável via `license`, declarada no
  `pyproject.toml` e incluída na imagem Docker.
- CRUD inicial configurável em tempo de cópia: `include_crud`, `resource_name`,
  `resource_plural` e `resource_fields`, com validação de nomes, tipos,
  `required` booleano, `max_length` positivo (apenas strings), campos
  reservados/duplicados e limites de tamanho.
- Rejeição na cópia de nomes de campos que geram o mesmo alias de validação
  Pydantic, evitando schemas inválidos.
- Tipos suportados no CRUD v1: `str`, `text`, `int`, `float`, `bool`, `datetime`
  e `uuid`; `required` e `max_length` (apenas strings) por campo.
- `include_crud=false` gera o projeto apenas com auth, health e infraestrutura
  compartilhada, sem entidade, use cases, rota, tabela ou testes de CRUD.
- `PATCH` parcial com `model_dump(exclude_unset=True)`: campo omitido não muda,
  opcional aceita `null` e obrigatório com `null` retorna 422.
- Testes de integração do CRUD gerado cobrindo PATCH parcial: campo omitido
  inalterado, opcional aceitando `null` e obrigatório rejeitando `null`.

### Corrigido

- Reuso de refresh token agora revoga toda a família e persiste a revogação
  mesmo quando a exceção é propagada.
- Logout de refresh token já revogado deixa de ser tratado como reuso.
- Nome de item em branco ou composto apenas por espaços retorna erro de
  validação (422) em vez de erro interno (500).
- Modo assíncrono instala `greenlet` via `sqlalchemy[asyncio]`.
- Substituição de `httpx` por `httpx2`, eliminando o aviso de depreciação do
  Starlette.
- Configuração do Alembic atualizada de `version_path_separator` para
  `path_separator`.
- Import de testcontainers atualizado para `testcontainers.community.postgres`.
- Tarefas `test-unit` e `test-integration` não aplicam mais o limite de
  cobertura; a cobertura mínima de 80% fica restrita a `poe test`.
- Ajustes de whitespace nos templates Jinja para lint e formatação das duas
  variantes.
- Nomes longos de recurso, plural e campos não estouram mais o limite de 88
  colunas: imports e chamadas são quebrados condicionalmente e a saída continua
  formatada pelo Ruff.
- `SECRET_KEY` do `docker-compose.yml` ajustada ao mínimo de 32 caracteres.

### Alterado

- CRUD deixou de ser fixo em `Item`: os arquivos, classes, rotas e tabelas agora são
  gerados a partir de `resource_name`, `resource_plural` e `resource_fields`,
  preservando `Item`/`items` como default.
- Campos opcionais de string passam a gerar `str | None` no domínio e no schema de
  resposta (antes, string opcional era tratada sem `None`).
- O `description` default passou a ser opcional (`text`, `max_length=5000`) no
  domínio, resposta, model e migration; antes era obrigatório no domínio/banco e
  usava `""` como default no schema de criação.
- Documentação de uso, validação e atualização do template revisada, incluindo
  limites de campos, matriz de testes, uso de caminho absoluto em cópias locais e
  a exigência de template limpo/commitado para testar `copier update`.
- Dependências e tarefas Poe alinhadas entre as variantes sync e async.
