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
  e `max_length` (só str/text). Limites: `resource_name`/módulo até 16 caracteres,
  plural até 40 e campo até 32. Validadores também rejeitam nomes reservados,
  duplicados, `max_length` inválido e aliases Pydantic colidentes. Fora do escopo:
  relações, unique, enums, JSON, defaults por campo e owner.
- Defaults do CRUD: `Item` em `/api/v1/items`, com `name` obrigatório (`str`, 255) e
  `description` opcional (`text`, 5000).
- Geração Jinja deve sair formatada. Prefira listas de linhas pré-computadas +
  `join('\n')` para loops; `-%}` remove a indentação do corpo do loop. Imports
  longos são quebrados condicionalmente conforme o limite de 88 colunas.
- `PATCH` usa `model_dump(exclude_unset=True)`: omitido não altera, opcional aceita
  `null`, obrigatório com `null` retorna 422.
- Docs gerados (README, AGENTS.md) em português; identificadores de código em inglês.
- JWT funcional: access curto + refresh persistido. Não simplificar para só access.
- Erros de domínio que precisam persistir alterações herdam de `CommitRequiredError`;
  a dependência de sessão faz commit antes de propagar (reuso de refresh revoga a família).

## Pegadinhas do template

- `resource_module` é derivado por regex e marcado com `when: false`; ele não aparece
  no `.copier-answers.yml`. Ao renomear `resource_name`, os caminhos renderizados
  mudam, então mantenha o `_exclude` consistente.
- As macros são importadas como `{% import "template/_macros.jinja" as m %}` porque
  o loader do Copier enxerga a raiz do clone, não `template/`. O diretório `_macros`
  é excluído da cópia; não o remova do `_exclude`.
- Arquivos condicionais usam sufixo `.jinja`, mas o `_exclude` referencia o caminho
  renderizado (por exemplo, `src/{{ project_slug }}/.../{{ resource_module }}.py`).
- Para testar `copier update`, use o caminho absoluto do template (`"$PWD"`) e faça
  commit das alterações locais antes de gerar. Com a árvore suja, o Copier grava um
  commit temporário no `.copier-answers.yml`; esse commit não existe no repositório
  e o update falha com `Unknown revision`.
- Gere sempre em `/tmp/opencode` ou outro diretório externo e rode `uv sync`,
  `uv run poe lint`, `uv run poe typecheck` e `uv run poe test` no destino. Valide
  também a saída sem CRUD, sem Docker, com todos os campos opcionais, primeiro
  campo `bool`/`datetime` e nomes nos limites de tamanho.

## Como validar

Docker precisa estar disponível para os testes de integração. Rode a matriz mínima:

```bash
uvx copier copy --trust --defaults --force \
  --data project_slug=demo_api --data async_mode=sync "$PWD" /tmp/opencode/demo-sync
uvx copier copy --trust --defaults --force \
  --data project_slug=demo_api --data async_mode=async "$PWD" /tmp/opencode/demo-async
uvx copier copy --trust --defaults --force \
  --data project_slug=demo_api --data async_mode=sync \
  --data include_crud=false "$PWD" /tmp/opencode/demo-no-crud
```

Em cada destino:

```bash
uv sync
uv run poe lint
uv run poe typecheck
uv run poe test
```

Depois, gere uma variante customizada (como no README) e outra com
`--data include_docker=false`. Para testar `copier update`, use o caminho absoluto
do template e um projeto de destino versionado com Git; um `_src_path` relativo
como `.` aponta para o projeto gerado e quebra o update.
