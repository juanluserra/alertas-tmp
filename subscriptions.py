#!/usr/bin/env python3
"""
Sistema de gestión de suscripciones de usuarios
"""

import json
import os
from typing import Dict, List, Set, Optional

SUBSCRIPTIONS_FILE = "subscriptions.json"

class SubscriptionManager:
    def __init__(self):
        self.data = self.load_subscriptions()
    
    def load_subscriptions(self) -> dict:
        """Carga las suscripciones desde el archivo JSON"""
        if os.path.exists(SUBSCRIPTIONS_FILE):
            try:
                with open(SUBSCRIPTIONS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️ Error al leer suscripciones, creando nuevo archivo")
                return {"users": {}}
        return {"users": {}}
    
    def save_subscriptions(self):
        """Guarda las suscripciones en el archivo JSON"""
        with open(SUBSCRIPTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_user_data(self, chat_id: str) -> dict:
        """Obtiene los datos de un usuario, creándolos si no existen"""
        chat_id = str(chat_id)
        if chat_id not in self.data["users"]:
            self.data["users"][chat_id] = {
                "lines": [],
                "receive_general": True  # Por defecto recibe alertas generales
            }
        return self.data["users"][chat_id]
    
    def subscribe_line(self, chat_id: str, line: str) -> bool:
        """Suscribe a un usuario a una línea"""
        user = self.get_user_data(chat_id)
        if line not in user["lines"]:
            user["lines"].append(line)
            self.save_subscriptions()
            return True
        return False
    
    def unsubscribe_line(self, chat_id: str, line: str) -> bool:
        """Desuscribe a un usuario de una línea"""
        user = self.get_user_data(chat_id)
        if line in user["lines"]:
            user["lines"].remove(line)
            self.save_subscriptions()
            return True
        return False
    
    def get_subscribed_lines(self, chat_id: str) -> List[str]:
        """Obtiene las líneas a las que está suscrito un usuario"""
        user = self.get_user_data(chat_id)
        return user["lines"]
    
    def set_receive_general(self, chat_id: str, receive: bool):
        """Configura si el usuario recibe alertas generales"""
        user = self.get_user_data(chat_id)
        user["receive_general"] = receive
        self.save_subscriptions()
    
    def get_receive_general(self, chat_id: str) -> bool:
        """Verifica si el usuario recibe alertas generales"""
        user = self.get_user_data(chat_id)
        return user.get("receive_general", True)
    
    def get_users_for_alert(self, line: Optional[str]) -> List[str]:
        """
        Obtiene la lista de chat_ids que deben recibir una alerta
        
        Args:
            line: Número de línea (ej: "11") o None para alertas generales
        
        Returns:
            Lista de chat_ids que deben recibir la notificación
        """
        recipients = []
        
        for chat_id, user_data in self.data["users"].items():
            # Si la alerta tiene línea específica
            if line:
                if line in user_data.get("lines", []):
                    recipients.append(chat_id)
            # Si es una alerta general (sin línea)
            else:
                if user_data.get("receive_general", True):
                    recipients.append(chat_id)
        
        return recipients
    
    def get_all_monitored_lines(self) -> Set[str]:
        """Obtiene todas las líneas que están siendo monitoreadas por al menos un usuario"""
        lines = set()
        for user_data in self.data["users"].values():
            lines.update(user_data.get("lines", []))
        return lines
    
    def get_stats(self) -> dict:
        """Obtiene estadísticas del sistema de suscripciones"""
        total_users = len(self.data["users"])
        all_lines = self.get_all_monitored_lines()
        
        line_counts = {}
        for line in all_lines:
            count = sum(1 for user in self.data["users"].values() 
                       if line in user.get("lines", []))
            line_counts[line] = count
        
        general_users = sum(1 for user in self.data["users"].values() 
                           if user.get("receive_general", True))
        
        return {
            "total_users": total_users,
            "monitored_lines": sorted(all_lines),
            "line_counts": line_counts,
            "general_alerts_users": general_users
        }
