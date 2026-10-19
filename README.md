# fastapi-clean-boilerplate

Template [Copier](https://copier.readthedocs.io/) para APIs FastAPI em Clean Architecture.
Variações: **sync** e **async**, com CRUD inicial configurável em tempo de cópia.

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
| `include_crud` | Gera o CRUD inicial (default `true`) |
| `resource_name` | Entidade em PascalCase (default `Item`) |
| `resource_plural` | Rota e tabela em snake_case (default `items`) |
| `resource_fields` | Lista YAML com os campos do recurso |

`resource_module` é derivado automaticamente de `resource_name` e não é perguntado.

## CRUD configurável

Sem argumentos extras, o template reproduz o CRUD de `Item` em `/api/v1/items`
com `name` (obrigatório) e `description` (opcional). Para outro recurso:

```bash
uvx copier copy --trust \
  --data resource_name=Product \
  --data resource_plural=products \
  --data 'resource_fields=[
    {"name": "sku", "type": "str", "required": true, "max_length": 32},
    {"name": "title", "type": "str", "required": true, "max_length": 120},
    {"name": "price", "type": "float", "required": true},
    {"name": "active", "type": "bool", "required": true},
    {"name": "notes", "type": "text", "required": false}
  ]' \
  gh:aluisiolucio/fastapi-clean-boilerplate caminho/do/projeto
```

Cada campo aceita:

- `name`: identificador em `snake_case`
- `type`: `str`, `text`, `int`, `float`, `bool`, `datetime` ou `uuid`
- `required`: `true` ou `false`
- `max_length`: opcional, apenas para `str`/`text`

O `PATCH` é parcial: campo omitido não é alterado, campo opcional aceita `null` e
campo obrigatório com `null` retorna 422. Relações/FKs, `unique`, índices, enums,
JSON, defaults por campo e regras de negócio ficam fora do escopo desta versão.

Use `--data include_crud=false` para gerar apenas auth, health e a infraestrutura
compartilhada. Nesse caso não são criados entidade, use cases, rotas, tabela ou
testes do CRUD.

## O que o projeto gerado inclui

- Camadas `domain` → `application` → `adapters` → `infrastructure`
- Contratos com `typing.Protocol` em `domain/interfaces/`
- CRUD configurável (default: `Item` em `/api/v1/items`) + JWT com refresh opaco,
  rotação e detecção de reuso
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

Para validar a variante sem CRUD, acrescente `--data include_crud=false`. Para
validar campos/tipos diferentes, passe `resource_name`, `resource_plural` e
`resource_fields` como no exemplo acima.
