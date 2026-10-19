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

O `copier update` só funciona em projetos versionados com Git. Se você alterou o
template localmente, faça commit antes de gerar o projeto de teste: com a árvore
suja, o Copier grava em `.copier-answers.yml` um commit temporário do estado
alterado. Esse commit não existe no repositório e o update falha com
`Unknown revision`. As respostas ficam em `.copier-answers.yml` e são
reutilizadas no update.

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
com `name` (obrigatório, `str`, até 255) e `description` (opcional, `text`, até
5000). Para outro recurso:

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

- `name`: identificador em `snake_case`, com até 32 caracteres
- `type`: `str`, `text`, `int`, `float`, `bool`, `datetime` ou `uuid`
- `required`: `true` ou `false`
- `max_length`: opcional, inteiro positivo, apenas para `str`/`text`

O valor de `resource_fields` é YAML; o JSON do exemplo é um YAML válido. Os
nomes `resource_name` e o módulo derivado têm limite de 16 caracteres cada;
`resource_plural` tem limite de 40. Nomes reservados, campos duplicados, tipos
inválidos, `max_length` em campo não textual e aliases Pydantic colidentes são
rejeitados antes de qualquer arquivo ser gerado.

O `PATCH` é parcial: campo omitido não é alterado, campo opcional aceita `null` e
campo obrigatório com `null` retorna 422. Relações/FKs, `unique`, índices, enums,
JSON, defaults por campo e regras de negócio ficam fora do escopo desta versão.

Use `--data include_crud=false` para gerar apenas auth, health e a infraestrutura
compartilhada. Nesse caso não são criados entidade, use cases, rotas, tabela ou
testes do CRUD. A resposta fica em `.copier-answers.yml` e é reutilizada pelo
`copier update`.

## O que o projeto gerado inclui

- Camadas `domain` → `application` → `adapters` → `infrastructure`
- Contratos com `typing.Protocol` em `domain/interfaces/`
- CRUD configurável (default: `Item` em `/api/v1/items`) + JWT com refresh opaco,
  rotação e detecção de reuso
- Dockerfile e `docker-compose.yml` opcionais (`include_docker`)
- Testes unitários e de integração; o CRUD gerado cobre PATCH parcial, `null`
  opcional, `null` obrigatório e campo omitido
- Ruff, ty, pytest, testcontainers, Poe the Poet (sem Makefile)
- CI GitHub Actions

## Changelog

As mudanças do template estão documentadas em [CHANGELOG.md](CHANGELOG.md).

## Validar o template

Matriz mínima: sync e async com os defaults, uma variante customizada e uma sem
CRUD. Gere os destinos fora do repositório:

```bash
uvx copier copy --trust --defaults --force \
  --data project_slug=demo_api --data async_mode=sync "$PWD" /tmp/opencode/demo-sync
uvx copier copy --trust --defaults --force \
  --data project_slug=demo_api --data async_mode=async "$PWD" /tmp/opencode/demo-async

# sem CRUD (repita com async_mode=async)
uvx copier copy --trust --defaults --force \
  --data project_slug=demo_api --data async_mode=sync \
  --data include_crud=false "$PWD" /tmp/opencode/demo-no-crud
```

Em cada destino: `uv sync && uv run poe lint && uv run poe typecheck && uv run poe test`.
Docker precisa estar disponível para os testes de integração. Para validar
campos/tipos diferentes, passe `resource_name`, `resource_plural` e
`resource_fields` como no exemplo acima. Vale cobrir também `include_docker=false`,
todos os campos opcionais, primeiro campo `bool`/`datetime` e nomes no limite de
tamanho.
