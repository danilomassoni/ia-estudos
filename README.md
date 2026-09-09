# IA de Estudos

Aplicativo em Python para apoiar o estudo pessoal com uma assistente de IA local, usando Ollama. O projeto permite registrar sessões de estudo, conversar com a IA, gerar relatórios semanais, acompanhar memória de aprendizado e identificar padrões e prioridades de estudo.

## Visão geral

Este projeto foi pensado para funcionar como um assistente pessoal de estudos. Ele combina:

- registro de estudos manuais;
- conversação em linguagem natural com um modelo local;
- análise semanal de desempenho e progresso;
- memória persistente do que o estudante aprendeu;
- exportação/armazenamento em arquivos JSON para histórico.

A aplicação usa o arquivo principal `main.py` como interface de interação via terminal e persiste dados em `data/` em formato JSON.

---

## Funcionalidades

### 1. Registro de estudo
O usuário pode registrar:

- assunto geral;
- tópico específico;
- resumo do conteúdo estudado;
- duração em minutos;
- nível de compreensão (1 a 5);
- dificuldades;
- aprendizados;
- próximo passo.

Esses dados são guardados em `data/estudos.json`.

### 2. Conversa com IA
A aplicação conversa com um modelo local de IA via Ollama. O histórico da conversa é salvo em `data/conversas.json` e enviado ao modelo para manter contexto da sessão.

### 3. Relatório semanal
A partir dos estudos registrados, o sistema:

- calcula estatísticas;
- reúne assuntos e tópicos estudados;
- analisa dificuldades e interpretações;
- sugere recomendações e prioridades.

Os relatórios ficam em `data/relatorios.json`.

### 4. Memória de aprendizado
A memória do sistema guarda observações relevantes, como:

- pontos fortes;
- dificuldades recorrentes;
- lacunas de conhecimento;
- padrões de aprendizagem;
- assuntos para revisar;
- evolução de conhecimento;
- observações importantes.

Essas informações são atualizadas após o relatório semanal.

### 5. Interface no terminal
A aplicação funciona em linha de comando, com comandos especiais:

- `/estudar` — registrar estudo manualmente;
- `/relatorio` — gerar relatório semanal;
- `/memoria` — visualizar memória consolidada;
- `/ajuda` — mostrar comandos;
- `/sair` — encerrar a aplicação.

---

## Tecnologias utilizadas

- Python 3
- Ollama
- Modelo: `llama3.2:latest`
- JSON para persistência de dados
- Estrutura modular por serviços e repositórios

---

## Estrutura do projeto

```text
ia-estudos/
├── main.py
├── config.py
├── requirements.py
├── tasks.txt
├── ai/
│   ├── __init__.py
│   ├── analyzers.py
│   ├── ollama_client.py
│   └── prompt.py
├── data/
│   ├── conversas.json
│   ├── estudos.json
│   ├── memoria.json
│   ├── perfil.json
│   └── relatorios.json
├── prompts/
│   ├── consolidar_memoria.txt
│   ├── mentor.txt
│   ├── resumo_semanal.txt
│   └── sistema.txt
├── repositories/
│   ├── __init__.py
│   ├── conversa_repository.py
│   ├── estudos_repository.py
│   ├── memoria_repository.py
│   └── relatorio_repository.py
├── services/
│   ├── __init__.py
│   ├── conversa_service.py
│   ├── estudo_service.py
│   ├── memoria_service.py
│   └── relatorio_service.py
└── README.md
```

### Descrição das pastas

- `ai/`: integração com a IA e lógica de prompt.
- `services/`: regras de negócio e orquestração de estudo, conversa, memória e relatórios.
- `repositories/`: camada de persistência e leitura dos dados em JSON.
- `data/`: armazenamento dos dados do projeto.
- `prompts/`: arquivos de prompt para análise e memória.

---

## Configuração

### 1. Requisitos

- Python 3.9 ou superior
- Ollama instalado e em execução
- Modelo local baixado:

```bash
ollama pull llama3.2:latest
```

### 2. Instalação das dependências

No momento, o projeto depende principalmente da biblioteca `ollama` para Python. Instale-a com:

```bash
pip install ollama
```

Se você quiser, pode também criar um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install ollama
```

### 3. Configuração do modelo

O arquivo `config.py` define as principais configurações:

```python
NOME_MODELO = "llama3.2:latest"
DIRETORIO_DATA = "data"
```

Você pode alterar o modelo para outro disponível no Ollama, caso deseje.

---

## Como usar

### Executar o projeto

```bash
python main.py
```

### Comandos disponíveis

Depois de iniciar o programa, você verá o menu com os comandos:

```text
/estudar
/relatorio
/memoria
/ajuda
/sair
```

### Fluxo típico de uso

1. Registrar estudo com `/estudar`.
2. Conversar livremente com a IA.
3. Gerar um relatório semanal com `/relatorio`.
4. Consultar memória com `/memoria`.
5. Acompanhar padrões de aprendizado e próximos passos.

---

## Arquivos de dados

A pasta `data/` contém os arquivos de persistência:

- `estudos.json` — histórico de sessões de estudo;
- `conversas.json` — histórico das conversas com a IA;
- `memoria.json` — memória consolidada do estudante;
- `relatorios.json` — relatórios semanais gerados;
- `perfil.json` — perfil do usuário (ainda pode ser expandido).

---

## Fluxo do sistema

### Registro de estudo

O processo começa em `main.py` quando o usuário chama `/estudar`. A função `registrar_estudo_manual()` coleta as informações do estudo e envia para `services.estudo_service.registrar_estudo()`.

### Conversa

Quando o usuário envia uma mensagem normal, `main.py` chama `services.conversa_service.conversar()`, que:

1. carrega o histórico;
2. monta a mensagem para a IA;
3. envia para o Ollama;
4. salva a resposta no histórico.

### Relatório semanal

A função `gerar_relatorio_semana()` chama `services.relatorio_service.gerar_relatorio()`, que:

1. busca todos os estudos do período;
2. gera um resumo estatístico;
3. monta um prompt para análise;
4. usa a IA para separar fatos, interpretações e recomendações;
5. salva o relatório.

### Atualização da memória

Após gerar o relatório, o sistema chama `services.memoria_service.atualizar_memoria()`, que compara os novos dados com a memória atual e atualiza as observações relevantes.

---

## Observações importantes

- O projeto foi criado para uso local e simples em terminal.
- Os dados são guardados em arquivos JSON, não em banco de dados.
- A IA depende do Ollama e do modelo escolhido no arquivo `config.py`.
- A estrutura sugere evolução para arquitetura mais robusta no futuro, como SQLite, dashboard e RAG.

---

## Roadmap / próximos passos

O arquivo `tasks.txt` indica que o projeto tem ideias futuras, como:

- arquitetura;
- modelagem dos dados;
- estrutura das pastas;
- repository JSON;
- serviço de estudos;
- interface de anotação;
- serviço de conversação;
- integração com Llama 3.2;
- memória de curto/longo prazo;
- análise semanal;
- automação de domingo;
- dashboard;
- SQLite;
- RAG / vector database.

Esses itens mostram que o projeto está em evolução e pode ser expandido para uma aplicação mais completa.

---

## Dicas de uso

- Use assuntos e tópicos consistentes para facilitar a análise semanal.
- Registre dificuldades e aprendizados sempre que possível, pois isso melhora a qualidade do relatório e da memória.
- Mantenha o Ollama instalado e o modelo disponível localmente.
- Se o comportamento da IA parecer genérico, ajuste prompts e qualidade dos dados de estudo.

---

## Licença

Este projeto ainda não possui uma licença formal definida no repositório. Se você pretende compartilhar ou publicar o projeto, vale definir uma licença como MIT, Apache 2.0 ou GPL.

---

## Autor

Projeto desenvolvido para uso pessoal de estudo com IA local.

Se quiser, posso também criar uma versão mais profissional do README com:

- badges;
- seção de screenshots;
- instruções para Windows/Linux/macOS;
- tabela de comandos;
- roadmap em formato de produto;
- documentação de arquitetura mais detalhada.
