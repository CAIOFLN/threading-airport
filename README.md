# 🏢 Simulador de Aeroporto - Threads e Semáforos

Um jogo educativo que explica conceitos de threads e semáforos usando a metáfora de um aeroporto.

## 📖 Conceitos Demonstrados

- **🏗️ Threads (Aviões)**: Cada avião é uma thread independente que executa uma tarefa (pousar ou decolar)
- **🚦 Semáforos (Torre de Controle)**: Controlam o acesso às pistas (recursos compartilhados limitados)
- **🛬 Recursos Compartilhados (Pistas)**: Apenas um número limitado de aviões pode usar as pistas simultaneamente
- **⏳ Sincronização**: Os aviões devem aguardar sua vez para usar as pistas

## 🚀 COMO JOGAR

### Execução Simples 🎮
```bash
./start_game.sh
```
Depois abra o arquivo `frontend/web_interface.html` no navegador!

### Execução Manual 🔧
```bash
cd backend && python3 api_server.py
```
Depois abra `frontend/web_interface.html` no navegador.

## 🏗️ Arquitetura

```
TrabSO/
├── backend/
│   ├── airport_controller.py    # Lógica de threads e semáforos
│   ├── api_server.py           # API REST
│   └── demo.py                 # Demonstração no terminal
├── frontend/
│   └── web_interface.html      # Interface web
├── start_game.sh              # Script para iniciar
├── COMO_JOGAR.txt            # Guia completo
└── README.md                 # Este arquivo
```

## 🎮 Como Usar

### 🏢 Status do Aeroporto (Lado Esquerdo)
- **Pistas Disponíveis**: Mostra quantas pistas estão livres
- **Aviões Aguardando**: Lista os aviões na fila (threads bloqueadas pelo semáforo)
- **Aviões em Ação**: Mostra os aviões usando as pistas atualmente
- **Log de Eventos**: Histórico detalhado de todas as ações

### 🎮 Painel de Controle (Lado Direito)
- **Configurar Aeroporto**: Define o número de pistas (valor do semáforo)
- **Criar Avião**: Cria uma nova thread com:
  - Nome personalizado
  - Ação (pousar ou decolar)
  - Duração da operação
- **Criação Rápida**: Botões para criar aviões rapidamente
- **Reiniciar**: Limpa todo o aeroporto

## 🧠 Explicação dos Conceitos

### Threads (Aviões)
Cada avião é uma thread independente que:
1. É criada quando você clica "Criar Avião"
2. Executa sua função (`_plane_worker`) de forma concorrente
3. Tenta adquirir uma pista (semáforo)
4. Executa sua ação (pouso/decolagem)
5. Libera a pista para outros aviões

### Semáforos (Torre de Controle)
A torre de controle usa um semáforo para:
1. Controlar quantos aviões podem usar pistas simultaneamente
2. Bloquear aviões quando todas as pistas estão ocupadas
3. Liberar aviões quando uma pista fica disponível
4. Evitar condições de corrida (race conditions)

### Sincronização
- Aviões aguardam automaticamente quando não há pistas disponíveis
- O semáforo garante que apenas N aviões (N = número de pistas) estejam ativos
- Threads são sincronizadas sem necessidade de polling ou busy waiting

## 🔧 Configurações

- **Pistas**: 1 a 5 (valor do semáforo)
- **Duração das Operações**: 1 a 30 segundos
- **Tipos de Operação**: Pouso ou Decolagem
- **Nomes**: Personalizáveis ou gerados automaticamente

## 📊 Monitoramento

O sistema fornece:
- Status em tempo real de todas as threads
- Log detalhado de eventos com timestamps
- Visualização clara da fila de espera
- Indicadores visuais do estado do sistema

## 🎯 Objetivos Educacionais

1. **Entender Threads**: Ver como múltiplas tarefas executam simultaneamente
2. **Compreender Semáforos**: Observar como recursos limitados são controlados
3. **Visualizar Sincronização**: Acompanhar aviões aguardando e sendo liberados
4. **Experimentar**: Testar diferentes configurações e cenários

Este simulador torna conceitos abstratos de programação concorrente tangíveis e visuais!
