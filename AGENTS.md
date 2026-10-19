# AGENTS.md

## O que é este repositório

Template **Copier** (`copier.yml`, `_subdirectory: template`). Não é um pacote Python
na raiz. O projeto gerado vive em `template/` e usa `{{ project_slug }}`.

## Stack do projeto gerado

- Python `>=3.13` (pin 3.14), **uv**, build `uv_build`
- FastAPI, pydantic-settings, SQLAlchemy 2, Alembic, `psycopg[binary]`
- Ruff (inclui regra `I`), ty `~=0.0.80`, pytest, poethepoet
- JWT (PyJWT) + refresh opaco persistido (hash SHA-256, rotação, reuse detection)
- Testes de integração: `testcontainers[postgres]` com `driver="psycopg"` (nunca o
  default `psycopg2`)

## Convenções que um agente erra se não ler

- Sem Makefile. Tarefas: `uv run poe …` (`lint`, `format`, `typecheck`, `test`,
  `test-unit`, `test-integration`, `run`, `migrate`, `revision`).
- Clean Architecture clássica, não Hexagonal: `domain` → `application` → `adapters`
  → `infrastructure`. Contratos são `typing.Protocol` em `domain/interfaces/`, não ABC
  e não "ports".
- Única variação do template: `async_mode` `sync` | `async`. Mesma URL
  `postgresql+psycopg://`; muda `create_engine` vs `create_async_engine`.
- Proibido: isort, psycopg2, asyncpg, pre-commit, mkdocs, Makefile.
- Arquivos que dependem de `async_mode` ou `project_slug` usam sufixo `.jinja`.
- Docker é condicional (`include_docker`). Nomes
  `{% if include_docker %}Dockerfile{% endif %}.jinja`.
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
