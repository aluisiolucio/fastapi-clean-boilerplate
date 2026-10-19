# fastapi-clean-boilerplate

Template [Copier](https://copier.readthedocs.io/) para APIs FastAPI em Clean Architecture.
Variações: **sync** e **async**.

## Uso

```bash
uvx copier copy gh:aluisiolucio/fastapi-clean-boilerplate caminho/do/projeto
cd caminho/do/projeto
uv sync
cp .env.example .env   # SECRET_KEY com pelo menos 32 caracteres
uv run poe migrate
uv run poe run
```

Cópia local (desenvolvimento do template):

```bash
uvx copier copy --trust "$PWD" ../minha-api
```

Use o caminho absoluto: o Copier grava a origem em `.copier-answers.yml`, e um
caminho relativo como `.` apontaria para o próprio projeto na hora do `update`.

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

## Changelog

As mudanças do template estão documentadas em [CHANGELOG.md](CHANGELOG.md).

## Validar o template

```bash
uvx copier copy --trust --defaults --force \
  --data project_slug=demo_api --data async_mode=sync "$PWD" /tmp/demo-sync
uvx copier copy --trust --defaults --force \
  --data project_slug=demo_api --data async_mode=async "$PWD" /tmp/demo-async
```

Em cada destino: `uv sync && uv run poe lint && uv run poe typecheck && uv run poe test`.
