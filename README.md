# IA de Estudos

Aplicativo em Python para apoiar o estudo pessoal com uma assistente de IA local, usando Ollama. O projeto combina organização de estudos, análise de progresso, memória persistente e uma interface gráfica moderna para facilitar o acompanhamento do aprendizado.

## Visão geral

Este projeto foi pensado como um assistente pessoal de estudos. Ele permite:

- registrar sessões de estudo com detalhes por assunto, tópico e tempo;
- conversar com uma IA local em linguagem natural;
- gerar relatórios semanais com análise de desempenho;
- acompanhar memória e padrões de aprendizagem;
- revisar conteúdos através de perguntas automatizadas;
- visualizar tudo em uma interface gráfica com dashboard e navegação lateral.

A base do projeto ainda usa persistência em JSON em `data/`, mas o fluxo principal da experiência agora é a interface gráfica em Python com `customtkinter`.

---

## Nova interface gráfica (GUI)

A aplicação possui uma interface desktop moderna com menu lateral, páginas dedicadas e visualização de dados em tempo real.

### Navegação principal

A tela principal da aplicação inclui:

- botão de menu lateral com acesso às áreas do sistema;
- dashboard inicial com visão geral dos estudos;
- telas separadas para cada funcionalidade;
- layout responsivo com painel central para conteúdo principal;
- tema escuro com visual limpo e focado em produtividade.

### Telas disponíveis

1. Dashboard
   - indicadores de sessões, tempo total e média de compreensão;
   - assuntos mais estudados;
   - pontos que precisam de atenção;
   - próximas prioridades e próximos passos;
   - lista de estudos recentes.

2. Registrar estudo
   - formulário para inserir assunto, tópico, conteúdo, duração e compreensão;
   - campos para dificuldades, aprendizados e próximo passo;
   - gravação dos dados em arquivo JSON para análise posterior.

3. Chat IA
   - conversa em tempo real com a IA local;
   - histórico da sessão em uma área de mensagens;
   - envio por teclado ou botão;
   - contexto da conversa mantido na sessão atual.

4. Relatório semanal
   - geração de análise baseada nos últimos 7 dias;
   - atualização automática da memória após a análise;
   - apresentação do relatório em tela com estrutura textual organizada.

5. Memória
   - visão das categorias de memória do estudante;
   - pontos fortes;
   - dificuldades recorrentes;
   - lacunas de conhecimento;
   - padrões de aprendizagem;
   - assuntos para revisar;
   - evolução dos conhecimentos;
   - observações importantes.

6. Histórico
   - listagem dos estudos registrados;
   - ordenação por data mais recente;
   - visão resumida por sessão com detalhes do estudo.

7. Revisão inteligente
   - seleção de período, assunto e tópico;
   - geração de perguntas por IA com base nos estudos;
   - avaliação da resposta do usuário;
   - progresso da revisão por pergunta;
   - feedback e pontuação da performance.

---

## Funcionalidades do sistema

### 1. Registro de estudo
O usuário pode registrar:

- assunto geral;
- tópico específico;
- resumo do conteúdo estudado;
- duração em minutos;
- nível de compreensão de 1 a 5;
- dificuldades encontradas;
- aprendizados adquiridos;
- próximo passo para continuar evoluindo.

Esses dados são salvos em `data/estudos.json`.

### 2. Chat com IA local
A aplicação conversa com um modelo local de IA via Ollama. O histórico da conversa pode ser mantido por sessão e usado para contextualizar a resposta da IA.

### 3. Dashboard analítico
A dashboard extrai estatísticas dos estudos, como:

- número de sessões;
- tempo total estudado;
- média de compreensão;
- assuntos mais frequentes;
- pontos de atenção;
- próximos passos sugeridos.

### 4. Relatório semanal
A partir dos estudos registrados, o sistema:

- calcula métricas e tendência de aprendizado;
- reune temas e tópicos estudados;
- analiza dificuldades e interpretações;
- sugere recomendações e prioridades de estudo.

Os relatórios ficam em `data/relatorios.json`.

### 5. Memória de aprendizado
A memória do sistema guarda observações relevantes, como:

- pontos fortes;
- dificuldades recorrentes;
- lacunas de conhecimento;
- padrões de aprendizagem;
- preferências observadas;
- assuntos para revisar;
- evolução dos conhecimentos;
- observações importantes.

### 6. Revisão inteligente
A funcionalidade de revisão gera perguntas sobre os tópicos estudados e avalia a resposta do usuário com feedback em linguagem natural. Isso ajuda a consolidar o conteúdo e identificar lacunas de compreensão.

---

## Tecnologias utilizadas

- Python 3
- `customtkinter` para a interface gráfica
- Ollama para execução local de IA
- Modelo recomendado: `llama3.2:latest`
- JSON para persistência de dados
- Arquitetura modular com `interface/`, `services/`, `repositories/` e `ai/`

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
│   ├── prompt.py
│   └── revisao_ai.py
├── data/
│   ├── conversas.json
│   ├── estudos.json
│   ├── memoria.json
│   ├── perfil.json
│   ├── relatorios.json
│   └── revisoes.json
├── interface/
│   ├── __init__.py
│   ├── app.py
│   ├── chat_view.py
│   ├── dashboard_view.py
│   ├── estudo_view.py
│   ├── historico_view.py
│   ├── memoria_view.py
│   ├── relatorio_view.py
│   └── revisao_view.py
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
│   ├── dashboard_service.py
│   ├── estudo_service.py
│   ├── memoria_service.py
│   ├── relatorio_service.py
│   └── revisao_service.py
├── README.md
└── .gitignore
```

### Descrição das pastas

- `ai/`: integração com a IA, prompts e geração de respostas/revisões.
- `interface/`: interface gráfica principal em `customtkinter`.
- `services/`: regras de negócio e orchestramento do fluxo de estudo, memória e relatórios.
- `repositories/`: camada de persistência e leitura dos dados em JSON.
- `data/`: armazenamento dos dados do usuário e do sistema.
- `prompts/`: arquivos de prompt usados para memória, relatório e interação com a IA.

---

## Configuração

### 1. Requisitos

- Python 3.9 ou superior
- Ollama instalado e em execução
- Modelo local disponível:

```bash
ollama pull llama3.2:latest
```

### 2. Instalação das dependências

Instale as bibliotecas necessárias:

```bash
pip install customtkinter ollama
```

Se preferir, crie um ambiente virtual:

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install customtkinter ollama
```

### 3. Configuração do modelo

O arquivo `config.py` define as principais configurações:

```python
NOME_MODELO = "llama3.2:latest"
DIRETORIO_DATA = "data"
```

Você pode trocar o modelo para outro disponível no Ollama se quiser utilizar uma variante diferente.

---

## Como usar

### Executar a interface gráfica

A forma principal de uso do projeto agora é via GUI:

```bash
python interface/app.py
```

Também existe a versão em terminal, ainda útil para testes e uso legado:

```bash
python main.py
```

### Fluxo recomendado de uso

1. Abra a aplicação e navegue pelo menu lateral.
2. Registre seu estudo na tela de "Estudar".
3. Converse com a IA na aba de chat.
4. Analise o desempenho no Dashboard.
5. Gere o relatório semanal.
6. Consulte a memória e acompanhe os pontos de atenção.
7. Faça revisões por assunto e tópico para consolidar o aprendizado.

---

## Arquivos de dados

A pasta `data/` contém os arquivos de persistência:

- `estudos.json` — histórico de sessões de estudo;
- `conversas.json` — histórico das conversas com a IA;
- `memoria.json` — memória consolidada do estudante;
- `relatorios.json` — relatórios semanais gerados;
- `revisoes.json` — revisões e avaliações realizadas;
- `perfil.json` — dados de perfil e configuração do usuário.

---

## Fluxo do sistema

### Registro de estudo

O formulário de estudo coleta as informações da sessão e salva em `services.estudo_service`, que grava os dados no arquivo JSON.

### Conversa

Na tela de chat, a aplicação envia a mensagem para `services.conversa_service.conversar()`, que:

1. carrega o histórico da sessão;
2. monta o prompt para a IA;
3. envia a mensagem ao Ollama;
4. salva a resposta no histórico.

### Dashboard e relatórios

O dashboard e os relatórios usam os estudos salvos para gerar métricas, identificar pontos fracos e sugerir prioridades.

### Memória

Depois de gerar um relatório, o sistema atualiza a memória com informações relevantes para revisão e planejamento futuro.

### Revisão inteligente

Com base nos estudos do período selecionado, o sistema gera perguntas e avalia respostas para reforçar a fixação do conteúdo.

---

## Observações importantes

- O projeto foi evoluído para uma experiência visual e prática com GUI.
- A persistência continua em JSON, sem banco de dados externo.
- A IA depende do Ollama e do modelo definido em `config.py`.
- O projeto é adequado para uso local, pessoal e de acompanhamento de estudo.

---

## Próximos passos possíveis

- melhorar a aparência e usabilidade da interface;
- adicionar exportação de relatórios em PDF ou TXT;
- implementar filtros por períodos e assuntos na dashboard;
- expandir a memória com histórico de evolução por tema;
- adicionar autenticação ou múltiplos perfis de estudo.

Se você quiser, posso também ajustar o README para um formato mais profissional, com badges, screenshots e instruções de instalação mais detalhadas.
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
