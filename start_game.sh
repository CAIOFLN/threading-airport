#!/bin/bash

echo "🏢 =========================================="
echo "   SIMULADOR DE AEROPORTO - THREADS E SEMÁFOROS"
echo "   =========================================="
echo ""
echo "📚 COMO FUNCIONA:"
echo "   • Torre de Controle = Semáforo (controla acesso)"
echo "   • Aviões = Threads (executam em paralelo)"  
echo "   • Pistas = Recursos compartilhados limitados"
echo ""

# Verificar se Python está disponível
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado! Por favor, instale o Python3."
    exit 1
fi

# Verificar se as dependências estão instaladas
echo "🔍 Verificando dependências..."
python3 -c "import flask, flask_cors, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Instalando dependências necessárias..."
    pip3 install flask flask-cors requests
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao instalar dependências. Tente:"
        echo "   sudo apt update && sudo apt install python3-pip"
        echo "   pip3 install flask flask-cors requests"
        exit 1
    fi
fi

echo "✅ Dependências verificadas!"
echo ""

# Ir para o diretório backend
cd "$(dirname "$0")/backend"

echo "🚀 Iniciando servidor backend..."
echo "📡 API disponível em: http://localhost:5001"
echo "🌐 Interface web disponível em: ../frontend/web_interface.html"
echo ""
echo "⚠️  INSTRUÇÕES:"
echo "   1. Mantenha este terminal aberto (servidor backend)"
echo "   2. Abra o arquivo web_interface.html no navegador"
echo "   3. Divirta-se criando aviões e vendo threads/semáforos!"
echo ""
echo "📱 Para parar o servidor: Ctrl+C"
echo "================================================"
echo ""

# Iniciar servidor
python3 api_server.py
