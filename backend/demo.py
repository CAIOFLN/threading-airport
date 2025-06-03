#!/usr/bin/env python3
"""
Teste simples do backend - Demonstração de threads e semáforos
Execute este arquivo para ver o sistema funcionando no terminal
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from airport_controller import AirportController, PlaneAction
import time

def demo_airport():
    """Demonstração simples do aeroporto"""
    print("🏢" + "="*60)
    print("   SIMULADOR DE AEROPORTO - THREADS E SEMÁFOROS")
    print("="*62)
    print()
    print("📚 CONCEITOS DEMONSTRADOS:")
    print("   • Threads = Aviões (executam tarefas concorrentemente)")
    print("   • Semáforos = Torre de Controle (limitam acesso às pistas)")
    print("   • Recursos Compartilhados = Pistas do aeroporto")
    print()
    
    # Criar aeroporto com 2 pistas
    airport = AirportController(max_runways=2)
    print(f"🛩️  Aeroporto criado com {airport.max_runways} pistas")
    print()
    
    # Criar alguns aviões para demonstração
    planes_data = [
        ("Boeing-747", PlaneAction.TAKEOFF, 3),
        ("Airbus-A320", PlaneAction.LANDING, 4),
        ("Cessna-172", PlaneAction.TAKEOFF, 2),
        ("Embraer-190", PlaneAction.LANDING, 3),
        ("Boeing-737", PlaneAction.TAKEOFF, 5),
    ]
    
    print("✈️  Criando aviões (threads)...")
    for name, action, duration in planes_data:
        airport.create_plane(name, action, duration)
        time.sleep(0.5)  # Pequeno delay para ver a sequência
    
    print()
    print("⏳ Aguardando operações do aeroporto...")
    print("   (Pressione Ctrl+C para encerrar)")
    print()
    
    try:
        # Monitorar o aeroporto por 20 segundos
        start_time = time.time()
        while time.time() - start_time < 20:
            status = airport.get_airport_status()
            
            print(f"\r🛬 Pistas: {status['available_runways']}/{status['total_runways']} | "
                  f"Aguardando: {len(status['waiting_planes'])} | "
                  f"Ativo: {len(status['active_planes'])} | "
                  f"Concluído: {len(status['completed_planes'])}", end="")
            
            time.sleep(1)
            
        print("\n")
        print("📊 RELATÓRIO FINAL:")
        final_status = airport.get_airport_status()
        print(f"   Total de aviões: {final_status['total_planes']}")
        print(f"   Concluídos: {len(final_status['completed_planes'])}")
        print(f"   Ainda aguardando: {len(final_status['waiting_planes'])}")
        
    except KeyboardInterrupt:
        print("\n\n🔴 Encerrando aeroporto...")
    
    finally:
        airport.shutdown()
        print("✅ Demonstração concluída!")
        print()
        print("🚀 Para usar a interface gráfica completa:")
        print("   1. Execute: ./start_backend.sh")
        print("   2. Em outro terminal: ./start_frontend.sh")

if __name__ == "__main__":
    demo_airport()
