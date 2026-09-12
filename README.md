# fastapi-clean-boilerplate

Template [Copier](https://copier.readthedocs.io/) para APIs FastAPI em Clean Architecture.
Variações: **sync** e **async**.

## Uso

```bash
uvx copier copy gh:aluisiolucio/fastapi-clean-boilerplate caminho/do/projeto
cd caminho/do/projeto
uv sync
cp .env.example .env
uv run poe migrate
uv run poe run
```

Cópia local (desenvolvimento do template):

```bash
uvx copier copy --trust . ../minha-api
```

Atualizar um projeto já gerado:

```bash
cd minha-api
uvx copier update
```

## Perguntas do Copier

| Campo | Efeito |
|---|---|
| `project_name` / `project_slug` | Nome de exibição e pacote Python |
| `async_mode` | `sync` ou `async` (endpoints, SQLAlchemy, testes) |
| `author_name` / `author_email` | `pyproject.toml` e `LICENSE` |
| `license` | MIT (default) ou Apache-2.0 |
| `include_docker` | `Dockerfile` + `docker-compose.yml` |

## O que o projeto gerado inclui

- Camadas `domain` → `application` → `adapters` → `infrastructure`
- Contratos com `typing.Protocol` em `domain/interfaces/`
- CRUD `Item` + JWT com refresh opaco, rotação e detecção de reuso
- Ruff, ty, pytest, testcontainers, Poe the Poet (sem Makefile)
- CI GitHub Actions

## Validar o template

```bash
uvx copier copy --trust --defaults --force \
  --data project_slug=demo_api --data async_mode=sync . /tmp/demo-sync
uvx copier copy --trust --defaults --force \
  --data project_slug=demo_api --data async_mode=async . /tmp/demo-async
```

Em cada destino: `uv sync && uv run poe lint && uv run poe typecheck && uv run poe test`.
