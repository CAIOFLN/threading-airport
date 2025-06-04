import threading
import time
import queue
from enum import Enum
from typing import List, Dict, Optional
import uuid
from dataclasses import dataclass, asdict
import json

class PlaneAction(Enum):
    TAKEOFF = "decolar"
    LANDING = "pousar"

class PlaneStatus(Enum):
    WAITING = "na fila"
    IN_ACTION = "em ação"
    COMPLETED = "concluído"

@dataclass
class Plane:
    id: str
    name: str
    action: PlaneAction
    duration: float  # tempo em segundos para completar a ação
    status: PlaneStatus
    created_at: float
    started_at: Optional[float] = None
    completed_at: Optional[float] = None

class AirportController:
    def __init__(self, max_runways: int = 1):
        """
        Torre de controle do aeroporto (semáforo)
        max_runways: número máximo de pistas (recursos compartilhados)
        """
        self.runway_semaphore = threading.Semaphore(max_runways)
        self.planes: Dict[str, Plane] = {}
        self.event_log: List[Dict] = []
        self.max_runways = max_runways
        self.active_threads: List[threading.Thread] = []
        self.shutdown_event = threading.Event()
        self.log_lock = threading.Lock()
        
    def log_event(self, message: str, plane_id: str = None):
        """Thread-safe logging de eventos"""
        with self.log_lock:
            event = {
                "timestamp": time.time(),
                "message": message,
                "plane_id": plane_id,
                "time_str": time.strftime("%H:%M:%S")
            }
            self.event_log.append(event)
            print(f"[{event['time_str']}] {message}")
    
    def create_plane(self, name: str, action: PlaneAction, duration: float) -> str:
        """Cria um novo avião (thread)"""
        plane_id = str(uuid.uuid4())[:8]
        plane = Plane(
            id=plane_id,
            name=name,
            action=action,
            duration=duration,
            status=PlaneStatus.WAITING,
            created_at=time.time()
        )
        self.planes[plane_id] = plane
        
        # Criar e iniciar thread
        thread = threading.Thread(target=self._plane_worker, args=(plane_id,))
        thread.daemon = True
        self.active_threads.append(thread)
        thread.start()
        
        action_text = "decolar" if action == PlaneAction.TAKEOFF else "pousar"
        self.log_event(f"✈️  Avião {name} ({plane_id}) criado para {action_text} (duração: {duration}s)", plane_id)
        
        return plane_id
    
    def _plane_worker(self, plane_id: str):
        """Função executada por cada thread (avião)"""
        plane = self.planes[plane_id]
        action_text = "decolagem" if plane.action == PlaneAction.TAKEOFF else "pouso"
        
        try:
            # Avião entra na fila (tenta adquirir o semáforo)
            self.log_event(f"🔄 Avião {plane.name} aguardando permissão para {action_text}", plane_id)
            
            # Tentar adquirir pista (semáforo)
            self.runway_semaphore.acquire()
            
            if self.shutdown_event.is_set():
                return
                
            # Avião conseguiu a pista
            plane.status = PlaneStatus.IN_ACTION
            plane.started_at = time.time()
            
            icon = "🛫" if plane.action == PlaneAction.TAKEOFF else "🛬"
            self.log_event(f"{icon} Avião {plane.name} iniciando {action_text}!", plane_id)
            
            # Simular o tempo da ação
            time.sleep(plane.duration)
            
            if not self.shutdown_event.is_set():
                # Ação concluída
                plane.status = PlaneStatus.COMPLETED
                plane.completed_at = time.time()
                
                success_icon = "✅" if plane.action == PlaneAction.TAKEOFF else "✅"
                self.log_event(f"{success_icon} Avião {plane.name} completou {action_text} com sucesso!", plane_id)
            
        except Exception as e:
            self.log_event(f"❌ Erro com avião {plane.name}: {str(e)}", plane_id)
        finally:
            # Liberar pista (semáforo)
            self.runway_semaphore.release()
            self.log_event(f"🏁 Avião {plane.name} liberou a pista", plane_id)
    
    def get_airport_status(self) -> Dict:
        """Retorna o status atual do aeroporto"""
        waiting_planes = []
        active_planes = []
        completed_planes = []
        
        # Ordenar aviões por ordem de criação para manter fila cronológica
        sorted_planes = sorted(self.planes.values(), key=lambda p: p.created_at)
        
        for plane in sorted_planes:
            plane_info = {
                "id": plane.id,
                "name": plane.name,
                "action": plane.action.value,
                "duration": plane.duration,
                "status": plane.status.value
            }
            
            if plane.status == PlaneStatus.WAITING:
                waiting_planes.append(plane_info)
            elif plane.status == PlaneStatus.IN_ACTION:
                plane_info["elapsed_time"] = time.time() - plane.started_at if plane.started_at else 0
                active_planes.append(plane_info)
            else:
                completed_planes.append(plane_info)
        
        return {
            "total_runways": self.max_runways,
            "available_runways": self.runway_semaphore._value,
            "waiting_planes": waiting_planes,
            "active_planes": active_planes,
            "completed_planes": completed_planes,
            "total_planes": len(self.planes)
        }
    
    def get_recent_events(self, limit: int = 10) -> List[Dict]:
        """Retorna os eventos mais recentes"""
        with self.log_lock:
            return self.event_log[-limit:] if self.event_log else []
    
    def configure_runways(self, new_runway_count: int):
        """Reconfigura o número de pistas do aeroporto"""
        if new_runway_count < 1:
            raise ValueError("Número de pistas deve ser pelo menos 1")
        
        old_count = self.max_runways
        self.max_runways = new_runway_count
        
        # Criar novo semáforo com o número correto de pistas
        self.runway_semaphore = threading.Semaphore(new_runway_count)
        
        self.log_event(f"🔧 Aeroporto reconfigurado: {old_count} → {new_runway_count} pistas")
    
    def reset_airport(self):
        """Reseta o aeroporto, removendo todos os aviões"""
        # Parar todas as threads ativas
        self.shutdown_event.set()
        
        # Aguardar threads terminarem
        for thread in self.active_threads:
            thread.join(timeout=1.0)
        
        # Limpar dados
        self.planes.clear()
        self.active_threads.clear()
        self.event_log.clear()
        
        # Recriar semáforo e reset do evento de shutdown
        self.runway_semaphore = threading.Semaphore(self.max_runways)
        self.shutdown_event.clear()
        
        self.log_event("🔄 Aeroporto resetado - todas as operações foram canceladas")
    
    def shutdown(self):
        """Encerra todas as threads"""
        self.shutdown_event.set()
        self.log_event("🔴 Aeroporto encerrando operações...")
        
        # Aguardar threads terminarem (com timeout)
        for thread in self.active_threads:
            thread.join(timeout=2.0)
        
        self.log_event("🔴 Aeroporto encerrado")

# Singleton para o controlador
airport = AirportController(max_runways=2)  # 2 pistas por padrão
