# Spec Kit Docker Template

[![Spec Kit](https://img.shields.io/badge/Spec%20Kit-1.x-blue?style=flat-square)](https://github.com/github/spec-kit)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat-square&logo=docker)](https://docker.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python)](https://python.org)
[![GitHub](https://img.shields.io/badge/GitHub-Template-181717?style=flat-square&logo=github)](https://github.com/wagner-sousa/spec-kit-docker)

> Template Docker para [Spec Kit](https://github.com/github/spec-kit) — desenvolvimento orientado por especificações (SDD) com tudo configurado e pronto para usar.

## 🎯 Sobre

Este repositório é um template Docker com [Spec Kit](https://github.com/github/spec-kit) e todas as extensões oficiais configuradas. Use como base para projetos que seguem Spec-Driven Development com qualquer AI Coding Agent.

## 🛠 Tecnologias

- **Docker** — ambiente isolado e reproduzível
- **Spec Kit 1.x** — core do SDD
- **8 extensões** — Git, Verify-Tasks, Sync, Bugfix, Refine, Doctor, Agent-Context, [Lifecycle](https://github.com/wagner-sousa/spec-kit-lifecycle), [Switch](https://github.com/wagner-sousa/spec-kit-switch)

## 📦 Pré-requisitos

- Docker e Docker Compose instalados
- Git
- AI Coding Agent com suporte a Spec Kit (qualquer integração suportada)

## 🚀 Instalação

### Clone o Repositório

```bash
git clone https://github.com/wagner-sousa/spec-kit-docker.git meu-projeto
cd meu-projeto
```

### Personalize

Renomeie o README e o arquivo `.specify/memory/constitution.md` para seu projeto.

### Build da Imagem

```bash
docker compose -f docker-compose.specify.yml build
```

### Inicialize o Spec Kit

```bash
./specify init --here --force --integration <seu-agente> --ignore-agent-tools
```

### Instale as Extensões do Template

As extensões não são versionadas (thin template). O manifest declarativo
`.specify/extensions-manifest.json` lista as extensões:

```bash
chmod +x install-extensions.sh
./install-extensions.sh
./specify extension update
```

> 8 extensões instalam via manifest. `review` e `verify` foram removidos — falham na validação da CLI 1.x (scripts com underscore no upstream).
> da CLI 1.x (`detect-changed-files.sh` e `load-config.sh` com underscore
> no upstream).

Para atualizar depois:

```bash
./specify extension update
```

### Inicie o Fluxo SDD

```bash
./specify constitution
./specify specify "Descrição da feature"
```

## 🔐 Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| `SPECIFY_INIT_DIR` | Diretório do projeto contendo `.specify/` (útil para monorepos) |
| `SPECIFY_FEATURE_DIRECTORY` | Sobrescreve a feature ativa (prioridade sobre `feature.json`) |
| `SPECIFY_FEATURE` | Nome da feature para repositórios sem Git |

## 📁 Estrutura do Projeto

```
spec-kit-docker/
├── .specify/                       # Core do Spec Kit (gerado via init)
│   ├── extensions/                 # Gerado via install-extensions.sh (não versionado)
│   ├── extensions-manifest.json    # Manifest declarativo das extensões
│   ├── extensions.yml              # Hooks das extensões
│   └── memory/                     # Constitution e contexto
├── specs/                 # Especificações das features
│   └── NNN-feature-name/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── docker-compose.specify.yml
├── install-extensions.sh  # Instala extensões do manifest
├── specify                # Entrypoint CLI
└── README.md
```

## 🏗️ Arquitetura e Fluxo de Trabalho

### Ciclo Principal SDD

```mermaid
graph LR
    A[constitution] -->|Define princípios| B[specify]
    B -->|Define requisitos| C[plan]
    C -->|Plano técnico| D[tasks]
    D -->|Gera tarefas| E[implement]
    E -->|Implementa| F{Verify-Tasks & Sync}
    F -->|Aprovado| G[PR / Deploy]
    F -->|Reprovado| E
```

### Fluxo com Hooks (before → comando → after)

Cada comando core é envolvido por hooks que executam antes e depois automaticamente:

```mermaid
graph LR
    subgraph "Foundation"
        A[before_constitution] --> B[constitution] --> C[after_constitution]
    end
    subgraph "Specification"
        D[before_specify] --> E[specify] --> F[after_specify]
    end
    subgraph "Planning"
        G[before_plan] --> H[plan] --> I[after_plan]
    end
    subgraph "Execution"
        J[before_tasks] --> K[tasks] --> L[after_tasks]
        M[before_implement] --> N[implement] --> O[after_implement]
    end
    C --> D
    F --> G
    I --> J
    L --> M
```

Os hooks `before_*` preparam o ambiente (git branches, contexto). Os hooks `after_*` executam verificações (verify-tasks, sync, commit, etc.).

### Extensões Instaladas

**Grupo A — Core + Quality:**

```mermaid
graph LR
    subgraph "Core"
        A[Agent-Context] -->|Atualiza contexto| L[Coding Agent]
        B[Git] -->|Gerencia branches| M[Git Repository]
    end
    subgraph "Quality"
        E[Verify-Tasks] -->|Detecta phantom tasks| P[Task Completion]
    end
```

**Grupo B — Workflow + Governance + Diagnostics:**

```mermaid
graph LR
    subgraph "Workflow"
        F[Sync] -->|Detecta drift| Q[Spec Drift]
        G[Bugfix] -->|Workflow de correção| R[Bugfixes]
        H[Refine] -->|Refina especificações| S[Specification]
        K[Switch] -->|Navega entre specs| M
    end
    subgraph "Governance"
        J[Lifecycle] -->|Bloqueia/libera comandos| L
    end
    subgraph "Diagnostics"
        I[Doctor] -->|Diagnóstico do projeto| T[Project Health]
    end
```

📖 As extensões são instaladas via `install-extensions.sh` e documentadas nos próprios repositórios: [Agent-Context](https://github.com/github/spec-kit) · [Doctor](https://github.com/KhawarHabibKhan/spec-kit-doctor) · [Verify-Tasks](https://github.com/datastone-inc/spec-kit-verify-tasks) · [Lifecycle](https://github.com/wagner-sousa/spec-kit-lifecycle) · [Switch](https://github.com/wagner-sousa/spec-kit-switch)

### Extensão Git — Branch Management & Auto-Commit

```mermaid
graph LR
    A[before_constitution] -->|git initialize| B[Repo iniciado]
    C[before_specify] -->|git feature| D[Branch criada]
    E[before_clarify] -->|git commit| F[Commit automático]
    G[before_plan] -->|git commit| F
    H[before_tasks] -->|git commit| F
    I[before_implement] -->|git commit| F
    J[after_constitution] -->|git commit| F
    K[after_specify] -->|git commit| F
    L[after_plan] -->|git commit| F
    M[after_tasks] -->|git commit| F
    N[after_implement] -->|git commit| F
```

📖 [README da extensão](.specify/extensions/git/README.md)

### Extensão Sync — Detecção de Drift

Disparado em `after_implement`:

```mermaid
graph LR
    A[after_implement] --> B[sync.analyze]
    B --> C{Drift detectado?}
    C -->|Não| D[Tudo ok]
    C -->|Sim| E[sync.propose]
    E --> F{Aprovar resolução?}
    F -->|Sim| G[sync.apply]
    F -->|Não| H[Revisar manualmente]
    G --> I[Specs atualizados]
```

📖 [README da extensão](.specify/extensions/sync/README.md)

### Extensão Bugfix — Workflow de Correção

```mermaid
graph LR
    A[Identificar bug] --> B[bugfix.report]
    B --> C[Rastreia artefatos spec]
    C --> D[bugfix.patch]
    D --> E[Atualiza spec / plan / tasks]
    E --> F[after_implement]
    F --> G[bugfix.verify]
    G --> H{Consistente?}
    H -->|Sim| I[Bugfix completo]
    H -->|Não| J[Corrigir artefatos]
    J --> D
```

📖 [README da extensão](.specify/extensions/bugfix/README.md)

### Extensão Refine — Refinamento de Especificações

```mermaid
graph LR
    A[Nova requisição] --> B[refine.update]
    B --> C[Atualiza spec.md]
    C --> D[refine.propagate]
    D --> E[Atualiza plan.md]
    D --> F[Atualiza tasks.md]
    G[after_specify] --> H[refine.status]
    H --> I{Spec desatualizada?}
    I -->|Sim| J[refine.diff]
    I -->|Não| K[Tudo sincronizado]
```

### Extensão Lifecycle — Gerenciamento de Fases

```mermaid
graph LR
    A[Fase active] --> B[Todos os comandos disponíveis]
    B --> C{Spec finalizada?}
    C -->|Não| B
    C -->|Sim| D[lifecycle.lock]
    D --> E[Fase locked]
    E --> F[Core SDD bloqueado]
    E --> H[bugfix.* liberado]
    E --> I[write-agents → AGENTS.md]
    F --> J{Precisa alterar?}
    J -->|Mudança controlada| G
    J -->|Bug| H
    J -->|Mudança estrutural| K[lifecycle.unlock]
    K --> L[write-agents remove regras]
    L --> B
    M[switch.set] --> N[auto-unlock spec anterior]
    N --> L
```

Controla o ciclo de vida da especificação. Quando ativa (`locked`), bloqueia comandos de escrita direta (`specify`, `clarify`, `plan`, `tasks`, `checklist`, `analyze`) e permite apenas caminhos controlados (`bugfix.*`).

O estado fica **por spec** em `specs/NNN-feature/.lifecycle.json`. O comando `unlock --spec-dir <path>` é a interface genérica usada por outros plugins (ex: `switch.set` faz auto-unlock da spec anterior). Regras de bloqueio são sincronizadas com `AGENTS.md` via `lifecycle.write-agents` após cada lock/unlock.

📖 [README da extensão](.specify/extensions/lifecycle/README.md)

### Extensão Switch — Navegação entre Specs

```mermaid
graph LR
    A[Spec 010] --> B{trocar para spec 013?}
    B -->|sim| C[git status]
    C --> D{Limpo?}
    D -->|não| E[commit ou stash]
    E --> C
    D -->|sim| F[auto-unlock spec anterior]
    F --> G[git checkout 013-feature]
    G --> H[feature.json atualizado automaticamente]
    H --> I[Pronto para trabalhar]
```

Navega entre especificações sem conflitos de `feature.json`. O `switch.set` faz `git checkout` primeiro — a branch alvo já contém o `feature.json` correto. Durante a troca, faz auto-unlock da spec anterior via `lifecycle.unlock --spec-dir`.

📖 [README da extensão](.specify/extensions/switch/README.md)

### Comandos

#### Comandos Core — Ciclo SDD

| Comando | Descrição | Quando usar |
|---------|-----------|-------------|
| `./specify constitution` | Define princípios e constraints do projeto | Antes de qualquer especificação |
| `./specify specify "..."` | Define requisitos de uma feature | Após constitution, antes de plan |
| `./specify plan` | Cria plano técnico detalhado | Após specify, antes de tasks |
| `./specify tasks` | Gera breakdown de tarefas | Após plan, antes de implement |
| `./specify implement` | Executa implementação orientada por specs | Após tasks |
| `./specify clarify` | Esclarece requisitos ambíguos | Durante specify ou implement |
| `./specify analyze` | Analisa o projeto e sugere direções | A qualquer momento |
| `./specify checklist` | Gera checklist de verificação | Antes de PR/deploy |
| `./specify converge` | Converge artefatos spec desatualizados | Quando houver drift |
| `./specify taskstoissues` | Converte tasks em issues do GitHub | Após tasks, para acompanhamento |

#### Comandos das Extensões

| Extensão | Comando | Descrição | Disparo automático |
|----------|---------|-----------|--------------------|
| **Git** | `speckit.git.initialize` | Inicializa repositório git | `before_constitution` |
| | `speckit.git.feature` | Cria branch para feature | `before_specify` |
| | `speckit.git.commit` | Auto-commit do progresso | `before_*` e `after_*` |
| | `speckit.git.validate` | Valida estado da branch | Manual |
| | `speckit.git.remote` | Detecta remote configurado | Manual |
| **Agent-Context** | `speckit.agent-context.update` | Atualiza contexto do agente | `after_*` |
| **Verify-Tasks** | `speckit.verify-tasks.run` | Detecta phantom tasks (tasks implementadas sem especificação) | `after_implement` |
| **Sync** | `speckit.sync.analyze` | Detecta drift entre spec e código | `after_implement` |
| | `speckit.sync.propose` | Propõe resoluções para drift | Manual |
| | `speckit.sync.apply` | Aplica resoluções aprovadas | Manual |
| | `speckit.sync.conflicts` | Detecta conflitos entre artefatos | Manual |
| | `speckit.sync.backfill` | Gera spec a partir de código existente | Manual |
| **Bugfix** | `speckit.bugfix.report` | Reporta bug e rastreia artefatos | Após identificar bug |
| | `speckit.bugfix.patch` | Aplica patch e atualiza specs | Manual |
| | `speckit.bugfix.verify` | Verifica consistência pós-patch | `after_implement` |
| **Refine** | `speckit.refine.update` | Atualiza spec.md com nova requisição | Após nova solicitação |
| | `speckit.refine.propagate` | Propaga mudanças para plan/tasks | Manual |
| | `speckit.refine.diff` | Mostra diferenças entre artefatos | Manual |
| | `speckit.refine.status` | Verifica se specs estão sincronizadas | `after_specify`, `after_plan` |
| **Doctor** | `speckit.doctor.check` | Diagnóstico completo do projeto | Manual |
| **Lifecycle** | `speckit.lifecycle.check` | Guard hook — bloqueia comandos se spec locked | `before_specify`, `before_clarify`, `before_plan`, `before_tasks`, `before_checklist`, `before_analyze`, `before_sync_apply`, `before_sync_backfill` |
| | `speckit.lifecycle.lock` | Bloqueia comandos de escrita da spec ativa | Manual |
| | `speckit.lifecycle.unlock` | Reabilita todos os comandos (ou `--spec-dir <path>`) | Manual |
| | `speckit.lifecycle.status` | Mostra fase atual e disponibilidade de comandos | Manual |
| | `speckit.lifecycle.write-agents` | Sincroniza regras de bloqueio com AGENTS.md | `after_lifecycle_lock/unlock` |
| **Switch** | `speckit.switch.list` | Lista todas as specs disponíveis | Manual |
| | `speckit.switch.set NNN` | Troca para outra spec (git checkout + auto-unlock lifecycle) | Manual |

## 🧪 Testes

- **`speckit.doctor.check`** — diagnóstico completo (extensões, hooks, sincronia)
- **`speckit.verify-tasks.run`** — detecta phantom tasks

## 🔄 Atualizando seu Projeto

Este repositório é um template. Para receber atualizações de novas versões:

1. Copie o workflow de atualização para o seu projeto:
   ```bash
   cp .github/workflow-templates/update-from-template.yml .github/workflows/update-from-template.yml
   ```
2. Se você fez fork, edite `TEMPLATE_REPO` no workflow para apontar para o seu fork
3. O workflow roda automaticamente toda segunda-feira e verifica novas releases
4. Se houver atualização, um PR é aberto automaticamente com as mudanças

### O que é atualizado

| Atualizado | Preservado |
|------------|------------|
| `Dockerfile` | `README.md` |
| `docker-compose.specify.yml` | `specs/` |
| `specify` (entrypoint) | `.specify/memory/constitution.md` |
| `install-extensions.sh` | `.env*` |
| `.specify/extensions-manifest.json` | Demais arquivos do projeto |
| `.specify/extensions.yml` | |

### Atualização manual

```bash
git remote add template https://github.com/wagner-sousa/spec-kit-docker.git
git fetch template tag vX.Y.Z
git checkout FETCH_HEAD -- Dockerfile docker-compose.specify.yml specify install-extensions.sh .specify/extensions-manifest.json .specify/extensions.yml ':!.specify/memory/'
echo "vX.Y.Z" > .template-version
git add . && git commit -m "chore: update template to vX.Y.Z"
```

## 📄 Licença

MIT. Veja [LICENSE](LICENSE).

## 📬 Contato

**Wagner Sousa** — [GitHub](https://github.com/wagner-sousa)
