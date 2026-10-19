# AGENTS.md

## O que é este repositório

Template **Copier** (`copier.yml`, `_subdirectory: template`). Não é um pacote Python
na raiz. O projeto gerado vive em `template/` e usa `{{ project_slug }}`.

## Stack do projeto gerado

- Python `>=3.13` (pin 3.14), **uv**, build `uv_build`
- FastAPI, pydantic-settings, SQLAlchemy 2, Alembic, `psycopg[binary]`
- Ruff (inclui regra `I`), ty `~=0.0.80`, pytest, poethepoet
- JWT (PyJWT) + refresh opaco persistido (hash SHA-256, rotação, reuse detection)
- CRUD inicial configurável em tempo de cópia (`include_crud`, `resource_name`,
  `resource_plural`, `resource_fields`); default `Item` / `items`
- Testes de integração: `testcontainers[postgres]` com `driver="psycopg"` (nunca o
  default `psycopg2`)

## Convenções que um agente erra se não ler

- Sem Makefile. Tarefas: `uv run poe …` (`lint`, `format`, `typecheck`, `test`,
  `test-unit`, `test-integration`, `run`, `migrate`, `revision`).
- Clean Architecture clássica, não Hexagonal: `domain` → `application` → `adapters`
  → `infrastructure`. Contratos são `typing.Protocol` em `domain/interfaces/`, não ABC
  e não "ports".
- Variações do template: `async_mode` (`sync` | `async`), `include_docker` e
  `include_crud`. Mesma URL `postgresql+psycopg://`; no modo async muda
  `create_engine` vs `create_async_engine`.
- Proibido: isort, psycopg2, asyncpg, pre-commit, mkdocs, Makefile.
- Arquivos que dependem de `async_mode`, `project_slug`, `include_crud` ou nomes de
  recurso usam sufixo `.jinja` quando o conteúdo é condicional.
- Docker é condicional (`include_docker`). Nomes
  `{% if include_docker %}Dockerfile{% endif %}.jinja`.
- CRUD: `resource_name` define classes; `resource_plural` define rota/tabela;
  `resource_module` é derivado e define arquivos/variáveis/atributos. Tipos v1:
  `str`, `text`, `int`, `float`, `bool`, `datetime`, `uuid`; opcionais `required`
  e `max_length` (só str/text). Fora do escopo: relações, unique, enums, JSON,
  defaults por campo e owner.
- Geração Jinja deve sair formatada. Prefira listas de linhas pré-computadas +
  `join('\n')` para loops; `-%}` remove a indentação do corpo do loop. Imports
  longos são quebrados condicionalmente conforme o limite de 88 colunas.
- `PATCH` usa `model_dump(exclude_unset=True)`: omitido não altera, opcional aceita
  `null`, obrigatório com `null` retorna 422.
- Docs gerados (README, AGENTS.md) em português; identificadores de código em inglês.
- JWT funcional: access curto + refresh persistido. Não simplificar para só access.
- Erros de domínio que precisam persistir alterações herdam de `CommitRequiredError`;
  a dependência de sessão faz commit antes de propagar (reuso de refresh revoga a família).

## Como validar

Gerar as duas variantes com Copier e rodar Poe no destino (Docker para integração):

```bash
uvx copier copy --trust --defaults --force \
  --data project_slug=demo_api --data async_mode=sync "$PWD" /tmp/demo-sync
```

`uv sync && uv run poe lint && uv run poe typecheck && uv run poe test`

Para testar `copier update`, use o caminho absoluto do template (`"$PWD"`).
O Copier grava a origem em `.copier-answers.yml`; um `_src_path` relativo
como `.` aponta para o projeto gerado e quebra o update.
