# ✈️ Simulador de Aeroporto - Threads e Semáforos

Um jogo educativo interativo que explica conceitos de **threads** e **semáforos** usando a metáfora visual de um aeroporto. Desenvolvido para ensinar programação concorrente de forma prática e divertida!

## 🎯 Conceitos Demonstrados

- **✈️ Threads (Aviões)**: Cada avião é uma thread independente executando uma tarefa
- **🏗️ Semáforos (Torre de Controle)**: Controlam acesso às pistas (recursos limitados)
- **🛫 Recursos Compartilhados (Pistas)**: Múltiplas threads competindo por recursos
- **⏳ Sincronização**: Coordenação entre threads sem race conditions
- **📋 Fila Cronológica**: Primeiro a chegar, primeiro a ser atendido (FIFO)

## 🚀 Como Executar

### Execução Rápida 🎮
```bash
chmod +x start_game.sh
./start_game.sh
```
Depois abra: `frontend/web_interface.html` no navegador!

### Execução Manual 🔧
```bash
cd backend
python3 api_server.py
```
Em seguida, abra `frontend/web_interface.html` no navegador.

## 🏗️ Arquitetura do Projeto

```
TrabSO/
├── backend/                    # Lógica do servidor
│   ├── airport_controller.py   # ⚙️ Core: Threads + Semáforos
│   ├── api_server.py          # 🌐 API REST (Flask)
│   ├── demo.py               # 🖥️ Demonstração terminal
│   └── requirements.txt      # 📦 Dependências Python
├── frontend/                 # Interface do usuário
│   └── web_interface.html    # 🎨 Interface web completa
├── start_game.sh            # 🚀 Script de execução
├── COMO_JOGAR.txt          # 📖 Manual detalhado
└── README.md               # 📄 Este arquivo
```

## 🎮 Funcionalidades Principais

### 🖥️ Interface Visual Avançada
- **📊 Painel em Tempo Real**: Status dinâmico do aeroporto
- **🛫 Pistas Animadas**: Visualização das operações em progresso
- **📋 Filas Separadas**: Pouso e decolagem com ordem cronológica
- **🏆 Próximo Avião**: Destaque visual do próximo na fila global
- **📈 Estatísticas**: Contadores de aviões e pistas em tempo real

### ✈️ Sistema de Aviões Inteligente
- **🎲 Nomes Reais**: 40+ nomes de aviões comerciais brasileiros e internacionais
- **⚡ Criação Rápida**: Botões para gerar aviões instantaneamente
- **🎯 Distribuição Inteligente**: Balanceamento automático entre múltiplas pistas
- **🔄 Animações Realistas**: Movimento linear sincronizado com duração

### ⚙️ Configurações Flexíveis
- **🛫 Pistas**: 1-5 pistas configuráveis (controle do semáforo)
- **⏱️ Duração**: 1-30 segundos por operação
- **🔄 Reset Completo**: Limpar todas as operações
- **📊 Monitoramento**: Log detalhado de todas as ações

## 🎮 Como Usar

### 🏢 Área do Aeroporto (Esquerda)
- **🛫 Pistas Visuais**: Veja aviões em ação em tempo real
- **📊 Estatísticas Dinâmicas**: Total, aguardando, ativos, pistas livres
- **🛬 Fila de Pouso**: Aviões aguardando para pousar (ordem cronológica)
- **🛫 Fila de Decolagem**: Aviões aguardando para decolar (ordem cronológica)
- **👑 Próximo Avião**: Destaque verde para o próximo da fila global

### 🎮 Painel de Controle (Direita)
- **⚙️ Configurar Aeroporto**: 1-5 pistas (valor do semáforo)
- **✈️ Criar Avião Manual**: Nome personalizado, ação e duração
- **🎲 Gerador de Nomes**: Botão para nomes de aviões reais
- **⚡ Criação Rápida**: Botões para pouso (5s) e decolagem (3s)
- **🔄 Reset**: Cancela todas as operações

## 🔬 Explicação Técnica dos Conceitos

### 🧵 Threads (Aviões)
Cada avião representa uma **thread independente** que:

1. **Criação**: Nasce quando você clica "Criar Avião"
2. **Espera**: Tenta adquirir o semáforo (pista livre)
3. **Execução**: Realiza sua operação (pouso/decolagem)
4. **Liberação**: Libera o recurso para outros
5. **Finalização**: Thread termina automaticamente

```python
def _plane_worker(self, plane_id):
    # Thread do avião executando independentemente
    self.runway_semaphore.acquire()  # 🔒 Bloqueia se necessário
    # ... executa operação ...
    self.runway_semaphore.release()  # 🔓 Libera para outros
```

### 🚦 Semáforos (Torre de Controle)
A **torre de controle** implementa um semáforo que:

- **🔢 Contador**: Define quantas pistas existem (1-5)
- **🚫 Bloqueio**: Para threads quando recursos esgotam
- **✅ Liberação**: Permite threads quando recursos ficam livres
- **⚖️ Equidade**: FIFO - primeiro a chegar, primeiro atendido

```python
# Semáforo com N pistas
self.runway_semaphore = threading.Semaphore(max_runways)
```

### 🔄 Sincronização e Ordem Cronológica
- **📋 Fila Global**: Mantém ordem de chegada independente da ação
- **🎯 Próximo Real**: Apenas UM avião marcado como "PRÓXIMO"
- **⚡ Sem Race Conditions**: Semáforo previne conflitos
- **🔒 Thread-Safe**: Operações atômicas garantidas

## 📝 Exemplos de Uso Educacional

### 🎯 Cenário 1: Entendendo Bloqueio de Threads
1. Configure **1 pista** no aeroporto
2. Crie **3 aviões** rapidamente
3. Observe: Apenas 1 ativo, 2 aguardando (threads bloqueadas)

### 🎯 Cenário 2: Teste de Concorrência
1. Configure **3 pistas**
2. Crie **5 aviões** com durações longas (10s)
3. Veja 3 threads executando simultaneamente

### 🎯 Cenário 3: Ordem Cronológica
1. Configure **1 pista**
2. Crie: Pouso → Pouso → Decolagem → Pouso
3. Observe que apenas o PRIMEIRO tem marcação "PRÓXIMO"

## 🛠️ Tecnologias Utilizadas

### Backend (Python)
- **🐍 Threading**: Módulo nativo para threads
- **🔒 Semaphore**: Sincronização de threads
- **🌐 Flask**: API REST para comunicação
- **📦 JSON**: Serialização de dados

### Frontend (Web)
- **🎨 HTML5/CSS3**: Interface moderna e responsiva
- **⚡ JavaScript**: Comunicação assíncrona com backend
- **🔄 Fetch API**: Requisições HTTP
- **🎭 Animações CSS**: Movimento dos aviões

## 🎓 Objetivos Educacionais Alcançados

### ✅ Conceitos Fundamentais
- **Threads**: Execução concorrente visualizada
- **Semáforos**: Controle de recursos limitados
- **Sincronização**: Coordenação sem conflitos
- **Race Conditions**: Como evitar com semáforos

### ✅ Habilidades Práticas
- **Debugging Concorrente**: Ver threads em ação
- **Performance**: Balanceamento de carga entre pistas
- **Arquitetura**: Separação backend/frontend
- **APIs REST**: Comunicação entre sistemas

## 🏆 Características Avançadas

### 🎨 Interface Intuitiva
- Design responsivo e moderno
- Cores e animações educativas
- Status em tempo real
- Feedback visual imediato

### ⚡ Performance Otimizada
- Distribuição inteligente entre pistas
- Animações sincronizadas com threads
- Atualização eficiente da interface
- Gerenciamento automático de recursos

### 🔧 Código Limpo
- Arquitetura modular
- Documentação completa
- Tratamento robusto de erros
- Padrões de código Python

---

## 🚀 Para Professores

Este simulador é ideal para:
- **Aulas de Sistemas Operacionais**
- **Programação Concorrente**
- **Disciplinas de Python**
- **Conceitos de Sincronização**

Os alunos podem **experimentar**, **observar** e **compreender** como threads e semáforos funcionam na prática, tornando conceitos abstratos em experiências visuais e interativas!

---

**Desenvolvido para tornar o aprendizado de programação concorrente divertido e visual! ✈️🎓**
