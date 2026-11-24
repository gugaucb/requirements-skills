# De/Para de skills

Três visões: (1) skills do repositório de Matt Pocock para este repositório; (2) skills da v1.2 deste repositório para a v2.0; (3) as dores relatadas e onde cada uma foi resolvida.

Legenda de **Situação**: **Novo** (não existia aqui), **Adaptado** (mesmo papel, reescrito para requisitos), **Renomeado**, **Mantido** (função preservada, conteúdo ampliado), **Sem equivalente** (fora do escopo: este repositório não gera código).

## 1. mattpocock/skills para requirements-skills

| Skill de Matt Pocock | Papel original | Skill aqui | Situação | O que mudou |
| --- | --- | --- | --- | --- |
| `ask-matt` | Roteador de fluxos | `ask-req` | Novo | Além do mapa, **lê o estado dos artefatos** (visão, backlog, Stale, CHG) e recomenda o próximo passo |
| `wayfinder` | Mapa de tickets de decisão para esforços grandes e nebulosos | `wayfinder` | Novo | Destino é visão ou spec; tipos de ticket: research, sketch, grilling, ask, task; resolve decisões e registra DEC; entrega para `create-product-vision` ou `spec-req` |
| `grill-me` | Entrevista implacável, sem estado | `grill-me` | Novo | Mesmo nome. Chama `grilling`; em **modo mudança** termina com análise de impacto (só no chat) |
| `grilling` | Primitiva de entrevista (rodadas, fronteira) | `grilling` | Novo | Tags Confirmed/Proposed/Pending, nunca responde pelo PO, **rodada de impacto** ao alterar item existente |
| `grill-with-docs` | Entrevista que grava glossário e ADRs | `grill-with-docs` | Novo | Chama `grilling` + `domain-modeling`; grava `GLOSSARY.md`, `DECISIONS.md` e `05-changes/CHG-NNN.md` |
| `domain-modeling` | Linguagem ubíqua e ADRs | `domain-modeling` | Renomeado (era `model-domain`) | Glossário com `_Avoid_` e status; decisões viram linhas DEC |
| `spec-req` | Conversa vira spec | `spec-req` | Novo | Gera `SPEC-NNN` (problema, resultado, histórias candidatas, regras, fora de escopo) |
| `to-tickets` | Spec vira tickets verticais com bloqueios | `split-backlog` | Adaptado | Fatias verticais, arestas **Blocked by**, quiz com o usuário, publica no tracker só com autorização |
| `implement` | Implementa um ticket por contexto limpo | `refine-request` | Adaptado | Refina **uma história** por contexto limpo, conduzindo as skills de escrita e verificação |
| `implement-spec` | Implementa a spec inteira em paralelo | n/a | Sem equivalente | Refinar histórias em paralelo ficou como evolução futura |
| `triage` | Máquina de estados de issues | `triage` | Adaptado | Categorias `new`/`change`; estados `needs-triage`, `needs-info`, `ready-for-refinement`, `ready-for-po`, `out-of-scope`; mudança dispara `impact-analysis` |
| `setup-matt-pocock-skills` | Configura tracker, labels, docs | `setup-requirements-repo` | Mantido | Também grava vocabulário de processo e regras operacionais (uma vez, em vez de 15 vezes) |
| `handoff` | Documento para outra sessão | `handoff` | Adaptado | Inclui passo do fluxo, IDs ativos, DECs abertas e skills sugeridas |
| `wait-what` | "Não entendi, re-explique" | `wait-what` | Adaptado | Linguagem simples no idioma do usuário, com vocabulário do `GLOSSARY.md` |
| `to-questionnaire` | Questionário para quem tem a resposta | `to-questionnaire` | Adaptado | Cita DEC/CAP/US desbloqueados; respostas viram DEC só se o responsável confirmar |
| `research` | Pesquisa em fontes primárias | `research` | Adaptado | Fontes: legislação, contratos, documentação de sistemas existentes |
| `retro` | Melhora o ambiente do agente | `retro` | Adaptado | Foca vocabulário, perguntas repetidas, retrabalho e checks determinísticos |
| `writing-for-agents` | Guia de escrita de skills | `docs/AUTHORING-SKILLS.md` | Adaptado | Vira documento do repositório, não skill |
| `code-review` | Revisão em dois eixos | `review-readiness` | Adaptado (parcial) | Eixos **Standards** (gates) e **Alignment** (visão e decisões); nunca assina pelo PO |
| `tdd` | Red-green-refactor | `design-test-scenarios` | Adaptado (parcial) | Casos de teste derivados de AC, independentes de implementação |
| `prototype` | Protótipo descartável | ticket `sketch` do `wayfinder` | Adaptado (parcial) | Artefato barato para reagir: exemplos, fluxo Mermaid, mock em texto |
| `pr`, `diagnosing-bugs`, `improve-codebase-architecture`, `codebase-design`, `wizard`, `teach` | Código, PR, arquitetura, aprendizado | n/a | Sem equivalente | Fora do foco de elucidação e documentação de requisitos |

## 2. requirements-skills v1.2 para v2.0

| v1.2 | v2.0 | Situação | Observação |
| --- | --- | --- | --- |
| (nenhuma) | `ask-req` | Novo | Roteador |
| (nenhuma) | `wayfinder` | Novo | Esforços grandes e nebulosos |
| (nenhuma) | `grill-me`, `grilling`, `grill-with-docs` | Novo | Antes dependia da skill de Matt; agora o repositório é autossuficiente |
| (nenhuma) | `impact-analysis` | Novo | Análise de impacto de mudanças; gera `CHG-NNN` e marca itens `Stale` |
| (nenhuma) | `spec-req` | Novo | Ponte entre entrevista e histórias |
| (nenhuma) | `triage`, `handoff`, `wait-what`, `to-questionnaire`, `research`, `retro` | Novo | Ver tabela 1 |
| `setup-requirements-repo` | `setup-requirements-repo` | Mantido | Absorve `initialize-requirements`; seeds de configuração dentro da skill |
| `initialize-requirements` | `setup-requirements-repo` | Mesclado | Arquivos de produto são criados sob demanda pela primeira skill que precisa deles |
| `create-product-vision` | `create-product-vision` | Mantido | Usa `grilling` para lacunas; revisão usa `impact-analysis` |
| `review-product-vision` | `review-product-vision` | Mantido | Passa a sugerir próximo passo |
| `refine-request` | `refine-request` | Mantido | Agora por história, em contexto limpo; modo mudança |
| `interview-product-owner` | `grilling` | Mesclado | Rodadas por fronteira com resposta recomendada |
| `model-domain` | `domain-modeling` | Renomeado | |
| `split-backlog` | `split-backlog` | Mantido | Fatias verticais, bloqueios, quiz; passa a ser acionada pelo usuário |
| `write-user-story` | `write-user-story` | Mantido | Modo revisão chama `impact-analysis`; template dentro da skill |
| `specify-requirements` | `specify-requirements` | Mantido | Procedimento detalhado |
| `define-acceptance-criteria` | `define-acceptance-criteria` | Mantido | Locale do Gherkin |
| `design-test-scenarios` | `design-test-scenarios` | Mantido | |
| `diagram-requirements` | `diagram-requirements` | Mantido | |
| `audit-traceability` | `audit-traceability` | Mantido | Novo `scripts/check-ids.py` (checagem determinística) e detecção de `Stale` |
| `review-readiness` | `review-readiness` | Mantido | Gates G1 a G9, incluindo frescor (G7) |

Removidos: adaptadores duplicados `.claude/skills/*` (substituídos por `scripts/install.sh`), o bloco "Shared operating rules" repetido em 15 skills (agora uma vez em `docs/agents/requirements-workflow.md`) e a pasta `templates/` (cada template mora na skill dona).

## 3. Dores relatadas e solução

| Dor | Solução |
| --- | --- |
| 1. Falta algo como `/ask-matt` | `ask-req`: roteador que lê o estado dos artefatos |
| 2. Falta algo como `/wayfinder` | `wayfinder`: mapa de tickets de decisão, com névoa e destino |
| 3. As skills não se conhecem | Toda skill termina em `## Next steps` com `➡️ Next step`; `ask-req` lista todas; o validador impede referência para skill inexistente e chamada de skill manual por outra skill |
| 4. Falta fluxo bem definido | Fluxo principal, on-ramps e fluxo de mudança em `docs/FLOW.md` e no README; máquina de estados da história; regras de fronteira de fase |
| 5. Alterar HU não gera análise de impacto | `impact-analysis` + **modo mudança** do `grilling` (rodada final de impacto, também em `/grill-me`); `write-user-story`, `specify-requirements`, `define-acceptance-criteria` e `design-test-scenarios` chamam a análise antes de editar; `CHG-NNN` e status `Stale` bloqueiam a prontidão |

## Aviso sobre colisão de nomes

Os nomes `grill-me`, `grilling`, `grill-with-docs`, `wayfinder`, `triage`, `spec-req`, `handoff`, `wait-what`, `to-questionnaire`, `research`, `retro` e `domain-modeling` coincidem de propósito com os de Matt Pocock. Se os dois repositórios estiverem instalados no mesmo agente, mantenha **uma** cópia de cada nome (aqui as versões são supersets para requisitos). Para convivência, use a invocação com namespace do seu agente, ou instale só um conjunto por projeto.

## 4. Integração com o Graphify (v2.1)

| Aspecto | Decisão |
| --- | --- |
| Nova skill | `graph-sync` (model-invoked, opcional, ativada no `/setup-requirements-repo`) |
| Grafo de requisitos | `req-graph.py`: determinístico, sem LLM, sem instalar nada; IDs próprios como nós (sem deriva de IDs) |
| Regra de direção | Toda aresta aponta para aquilo de que a origem depende. O impacto flui contra a seta, o que o `graphify affected` já faz |
| Camadas | Requisitos (local), Código (`graphify update`, local) e Conhecimento (`graphify extract`, LLM, só para material não estruturado) |
| Junção | `graphify merge-graphs`; as camadas ficam independentes e com cache próprio |
| Não fazer | Injetar nós no `graph.json` do Graphify (o `update` incremental os descarta) |
| Privacidade | Artefatos estruturados ficam fora do passe LLM (`.graphifyignore`); `GRAPHIFY_BACKEND=none` mantém tudo local |
| Skills que usam o grafo | `impact-analysis`, `refine-request`, `ask-req`, `audit-traceability`, `triage`, `retro` |
| Screens e Fields | Tópico opcional `## Screens` (decidido por história conforme a política `ask`, `always` ou `never`), IDs `FLD-` e `SCR-`, relação `uses` no grafo |
| Versionamento | Seção G do `setup-requirements-repo`: git local ou remoto, layout, ramificação e revisão, convenção de commit, o que versionar, e nenhuma ação git sem pedido |
| Consultas | `req-graph.py query`, `path` e `explain` cobrem o que antes só o `graphify query/path/explain` fazia sobre o grafo de requisitos. O Graphify fica restrito às camadas de código e de documentos; busca semântica (sinônimos) continua sendo dele |
| Visualização | `req-graph.py build --view` gera `graph/req-graph.html`: arquivo único, offline, sem Graphify. Layout em camadas, clique mostra impactados (laranja) e dependências (azul), status na borda, busca e filtros. O HTML do Graphify (`graphify export html`) continua disponível como visão separada do grafo mesclado |
| Sem o grafo | Todas as skills continuam funcionando (fallback para `check-ids.py` e leitura dos arquivos) |

## 5. Evolução v3.0: fases, contrato entre skills e pastas

| Aspecto | Decisão |
| --- | --- |
| Fluxo em 5 fases | 1 Canvas e visão, 2 WBS e backlog, 3 Spec, 4 Aplicação, 5 Revisão. A saída de cada fase é a entrada da seguinte; cada skill de fase tem seção `## Contract` com Reads, Writes e Gate (o validador confere) |
| `project-canvas` (nova) | Guia o patrocinador pelos 13 blocos do Project Model Canvas e aplica os protocolos de integração: tríade justificativa, objetivo e benefício; produto e requisitos; produto e entregas (regra dos 100%); premissas e riscos; restrições contra linha do tempo e custos; stakeholders; equipe; teste de rastreabilidade reversa. `canvas-check.py` verifica as regras mecânicas (C1 a C10, R); as de julgamento (J1 a J6) são perguntas ao patrocinador |
| Visão a partir do canvas | `create-product-vision` deriva GOAL dos objetivos e CAP das entregas e itens do produto, com coluna **Origin** (IDs do canvas); equipe, prazo e custo ficam só no canvas |
| EAP no backlog | `split-backlog` gera CAP > EPIC > HU, com checklist de operações por história. Status continua sendo o ciclo de vida; **Progress** é derivado do checklist (`req-graph.py backlog`) |
| `spec-req` (ex `to-spec`) | Três entradas: história do backlog, conversa (por exemplo a partir do `/ask-req`) ou ata de reunião (itens extraídos ficam Proposed). Escreve Estratégia, prévia de impacto e **Plano de mudanças** (`PLN-NNN`: alvo, tipo, mudança, motivo, dependências, status) |
| `apply-spec` (nova) | Só roda sobre spec aprovada. Um CHG para a spec inteira, uma ou mais linhas prontas por execução, na ordem de dependência (`req-graph.py plan`), retomável. Linhas de visão e canvas esperam o usuário, pois essas skills são acionadas por ele |
| `review-spec` (nova) | Fase 5: fechamento do plano, conformidade linha a linha, nada fora do plano, nada `Stale`, gates de qualidade. Não assina pelo PO |
| `refine-story` (nova, interna) | Pipeline de refinamento extraído do `refine-request`; usado por `refine-request` (uma HU) e `apply-spec` (lote). Marca o checklist de operações |
| `req-graph` (nova) | Acionador em linguagem natural do `req-graph.py` (reconstruir, abrir visualizador, dependentes, busca, caminho, backlog, plano) |
| Grafo | Novos tipos do canvas, `PLN`, relações `traces_to` e `plans`, comandos `backlog` e `plan`; o visualizador mostra os novos tipos |
| Pastas | `00-canvas`, `01-vision`, `02-backlog`, `03-specs`, `04-stories`, `05-changes`, `inputs/`, `shared/`, `wayfinder/`, `diagrams/`, `graph/`; migração com `migrate-layout.py` |
| Renomeado | `to-spec` para `spec-req` |

## 6. Hardening v3.1: o que foi feito, adaptado e não feito

| Pedido | Resultado |
| --- | --- |
| Parsing tolerante (espaços, quebras, `\|`, `<br>`, linha sem pipe, linha continuada) | Feito, em `reqmd.py` (módulo único usado por `req-graph.py`, `check-ids.py` e `canvas-check.py`) |
| IDs em caixa alta, UTF-8 com `errors="replace"`, `[PARSE-WARNING]` no stderr | Feito. `--strict` transforma qualquer aviso em saída 3 |
| IDs `RN-xxx` e `EP-xxx` | **Não adotados**: o repositório usa `FR/NFR` (regras funcionais e não funcionais), `DEC` (decisões) e `EPIC`. Se o seu time quiser `RN` ou `EP`, é uma decisão de vocabulário: avise e eu adiciono como prefixo ou alias |
| DAG com ordenação topológica e ciclos | Feito com DFS de 3 cores sobre as relações de dependência e `superseded_by`. Registros de mudança (`impacts`, `changed_by`) ficam **fora** de propósito: uma mudança e a história que ela impacta sempre apontam uma para a outra, o que geraria falso ciclo em toda mudança |
| Top 5 artefatos críticos | Feito (`validate` e `critical --top N`): ordena pelo total de dependentes em cascata, depois pelos diretos |
| Unificar `check-ids.py` e `req-graph.py` | Feito: `check-ids.py` virou um atalho para `req-graph.py validate` (uma só implementação) |
| Códigos de saída 0/1/2/3 | Feito. Uso incorreto passa a 64 e alvo desconhecido a 66, fora do contrato de CI |
| Visualizador: sanitização | Feito: `<`, `>` e `&` viram `\uXXXX`, o payload é ASCII e os testes provam o ciclo ida e volta |
| `--bundle-assets` / fallback local para Vis.js ou Cytoscape | **Não necessário**: o visualizador já é 100% offline e não usa nenhuma biblioteca externa nem CDN (o teste garante que a única URL é o namespace do SVG). Adicionar uma biblioteca só para empacotá-la aumentaria o tamanho e a superfície sem ganho |
| Manifesto neutro por skill | Feito: `agents/agent.yaml`, gerado do `SKILL.md`, com bloco no formato de ferramenta MCP (nome, descrição, `inputSchema`). Não testei em um host MCP real |
| Pré-condições em cada `SKILL.md` | Feito, com o título `Preflight (Pré-condições / Insumos Obrigatórios)` e nível 2. Em vez de acionar o `wayfinder`, a skill para e **indica a skill que produz o insumo**, usando o `wayfinder` quando várias faltam, porque o `wayfinder` é acionado pelo usuário e uma skill do modelo não pode chamá-lo |
| `setup` cria `GLOSSARY.md` e `DECISIONS.md` | Feito (esqueletos vazios), para que o Preflight de `spec-req` possa passar sem quebrar o princípio de criar o resto sob demanda |
| Evidência dos scripts nas skills de validação | Feito em `project-canvas`, `audit-traceability`, `review-readiness` e `review-spec`; sem terminal o veredito é `Unverified` |
| Fundir `grill-me` e `grilling` | **Parcial**: ficam duas skills porque uma é acionada pelo usuário e a outra pelo modelo, e a invocação é definida por skill. `grilling` ganhou os modos `quick` (uma rodada, até 5 perguntas) e `exhaustive`, e `/grill-me quick` os aciona |
| Fundir `spec-req` e `specify-requirements` | **Não feito**: são fases e artefatos diferentes (plano de mudanças entre artefatos versus linhas FR e NFR de uma história). Acrescentei a nota "não confundir" nas duas. Se o nome confunde, a alternativa é renomear `specify-requirements` para `write-requirements` |
| Tabelas de exemplo dentro do `SKILL.md` | Feito em `write-user-story`, `split-backlog`, `impact-analysis` e `domain-modeling`; os arquivos de formato continuam para as regras completas |
| Rotas de correção e `BLOCKED` | Feito: seção "Return routes" no `docs/FLOW.md`, coluna "Return to" em `QUALITY-GATES.md` e veredito `PASS`, `NEEDS CHANGES` ou `BLOCKED` no `review-readiness` |
| `status` e `version` no cabeçalho YAML | Feito para specs e histórias. É o ciclo de vida grosso e convive com a linha `**Status:**` detalhada, com tabela de correspondência e aviso quando divergem |
