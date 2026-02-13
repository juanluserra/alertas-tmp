#!/usr/bin/env python3
"""
Bot de Telegram para gestionar suscripciones a alertas de TMP Murcia
Versión mejorada con mejor logging y manejo de errores
"""

import requests
import os
import sys
from datetime import datetime
from subscriptions import SubscriptionManager

class TelegramBot:
    def __init__(self):
        self.token = os.environ.get('TELEGRAM_BOT_TOKEN')
        if not self.token:
            print("❌ Error: TELEGRAM_BOT_TOKEN no configurado")
            sys.exit(1)
        
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.subscription_manager = SubscriptionManager()
        self.offset = self.load_offset()
        print(f"📝 Offset inicial: {self.offset}")
    
    def load_offset(self) -> int:
        """Carga el último offset procesado"""
        try:
            with open('.telegram_offset', 'r') as f:
                offset = int(f.read().strip())
                print(f"📂 Offset cargado desde archivo: {offset}")
                return offset
        except FileNotFoundError:
            print("ℹ️ No existe archivo de offset, comenzando desde 0")
            return 0
        except Exception as e:
            print(f"⚠️ Error al cargar offset: {e}, comenzando desde 0")
            return 0
    
    def save_offset(self, offset: int):
        """Guarda el offset para la próxima ejecución"""
        try:
            with open('.telegram_offset', 'w') as f:
                f.write(str(offset))
            print(f"💾 Offset guardado: {offset}")
        except Exception as e:
            print(f"⚠️ Error al guardar offset: {e}")
    
    def get_updates(self) -> list:
        """Obtiene actualizaciones pendientes de Telegram"""
        try:
            url = f"{self.base_url}/getUpdates"
            params = {
                'offset': self.offset,
                'timeout': 0  # Sin timeout para GitHub Actions
            }
            print(f"🔍 Consultando actualizaciones desde offset {self.offset}...")
            
            response = requests.get(url, params=params, timeout=15)
            
            print(f"📡 Respuesta de Telegram: Status {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    updates = data.get('result', [])
                    print(f"✅ Se obtuvieron {len(updates)} actualizaciones")
                    return updates
                else:
                    print(f"❌ Error en respuesta: {data}")
                    return []
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                print(f"Respuesta: {response.text[:200]}")
                return []
                
        except Exception as e:
            print(f"❌ Excepción al obtener actualizaciones: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def send_message(self, chat_id: str, text: str, parse_mode: str = 'Markdown'):
        """Envía un mensaje a un chat"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode
            }
            
            print(f"📤 Enviando mensaje a {chat_id}...")
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Mensaje enviado exitosamente a {chat_id}")
                return True
            else:
                print(f"❌ Error al enviar mensaje: {response.status_code}")
                print(f"Respuesta: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ Excepción al enviar mensaje: {e}")
            return False
    
    def handle_start(self, chat_id: str, username: str):
        """Maneja el comando /start"""
        message = f"""🚌 *¡Bienvenido al Monitor de Alertas TMP Murcia!*

Hola {username}! 👋

Este bot te enviará notificaciones automáticas cuando haya alertas de las líneas de autobús que elijas.

📋 *Comandos disponibles:*

/suscribir [línea] - Suscribirte a una línea
   Ejemplo: `/suscribir 11`

/desuscribir [línea] - Desuscribirte de una línea
   Ejemplo: `/desuscribir 44`

/mis_lineas - Ver tus suscripciones actuales

/alertas_generales [on/off] - Activar/desactivar alertas sin línea específica
   Ejemplo: `/alertas_generales off`

/ayuda - Ver esta ayuda de nuevo

💡 *Nota:* Por defecto recibirás alertas generales (sin línea específica). Puedes desactivarlas con `/alertas_generales off`

¿Listo para empezar? Usa `/suscribir [número]` para empezar a recibir alertas de tu línea favorita 🎯
"""
        self.send_message(chat_id, message)
    
    def handle_subscribe(self, chat_id: str, line: str):
        """Maneja el comando /suscribir"""
        if not line:
            self.send_message(chat_id, "❌ Uso: /suscribir [número de línea]\nEjemplo: `/suscribir 11`")
            return
        
        success = self.subscription_manager.subscribe_line(chat_id, line)
        if success:
            self.send_message(chat_id, f"✅ ¡Suscrito a la línea {line}!\n\nAhora recibirás alertas cuando haya novedades en esta línea.")
        else:
            self.send_message(chat_id, f"ℹ️ Ya estabas suscrito a la línea {line}")
    
    def handle_unsubscribe(self, chat_id: str, line: str):
        """Maneja el comando /desuscribir"""
        if not line:
            self.send_message(chat_id, "❌ Uso: /desuscribir [número de línea]\nEjemplo: `/desuscribir 11`")
            return
        
        success = self.subscription_manager.unsubscribe_line(chat_id, line)
        if success:
            self.send_message(chat_id, f"✅ Desuscrito de la línea {line}\n\nYa no recibirás alertas de esta línea.")
        else:
            self.send_message(chat_id, f"ℹ️ No estabas suscrito a la línea {line}")
    
    def handle_my_lines(self, chat_id: str):
        """Maneja el comando /mis_lineas"""
        lines = self.subscription_manager.get_subscribed_lines(chat_id)
        receive_general = self.subscription_manager.get_receive_general(chat_id)
        
        if not lines and not receive_general:
            message = "ℹ️ No estás suscrito a ninguna línea y no recibes alertas generales.\n\n"
            message += "Usa `/suscribir [línea]` para empezar a recibir alertas."
        else:
            message = "📊 *Tus suscripciones actuales:*\n\n"
            
            if lines:
                message += "🚌 *Líneas:*\n"
                for line in sorted(lines):
                    message += f"   • Línea {line}\n"
            else:
                message += "🚌 *Líneas:* Ninguna\n"
            
            message += f"\n📢 *Alertas generales:* {'✅ Activadas' if receive_general else '❌ Desactivadas'}\n"
            message += "\n💡 Usa `/suscribir [línea]` para añadir más líneas"
            if receive_general:
                message += "\n💡 Usa `/alertas_generales off` para desactivar alertas generales"
        
        self.send_message(chat_id, message)
    
    def handle_general_alerts(self, chat_id: str, setting: str):
        """Maneja el comando /alertas_generales"""
        if not setting or setting.lower() not in ['on', 'off']:
            self.send_message(chat_id, "❌ Uso: /alertas_generales [on/off]\nEjemplo: `/alertas_generales off`")
            return
        
        receive = setting.lower() == 'on'
        self.subscription_manager.set_receive_general(chat_id, receive)
        
        if receive:
            self.send_message(chat_id, "✅ Alertas generales activadas\n\nRecibirás notificaciones de alertas que no tengan número de línea específico.")
        else:
            self.send_message(chat_id, "✅ Alertas generales desactivadas\n\nYa no recibirás alertas sin línea específica.")
    
    def handle_help(self, chat_id: str):
        """Maneja el comando /ayuda"""
        message = """📚 *Ayuda - Monitor TMP Murcia*

🔧 *Comandos disponibles:*

• `/suscribir [línea]` - Suscribirte a una línea
• `/desuscribir [línea]` - Desuscribirte de una línea
• `/mis_lineas` - Ver tus suscripciones
• `/alertas_generales [on/off]` - Alertas sin línea específica
• `/ayuda` - Ver esta ayuda

📖 *Ejemplos de uso:*

`/suscribir 11` - Recibir alertas de la línea 11
`/suscribir 44` - Recibir alertas de la línea 44
`/desuscribir 36` - Dejar de recibir alertas de la 36
`/alertas_generales off` - No recibir alertas generales

ℹ️ *Sobre alertas generales:*
Algunas alertas no especifican número de línea (ej: avisos generales, cambios de servicio global). Por defecto las recibirás, pero puedes desactivarlas.

🤖 *Sobre el bot:*
El bot revisa la página de TMP cada 15 minutos y te avisa automáticamente de novedades en tus líneas suscritas.

¿Problemas? Reporta en: github.com/[tu-repo]/issues
"""
        self.send_message(chat_id, message)
    
    def handle_stats(self, chat_id: str):
        """Maneja el comando /stats (solo para administradores)"""
        stats = self.subscription_manager.get_stats()
        
        message = "📊 *Estadísticas del Sistema*\n\n"
        message += f"👥 Total de usuarios: {stats['total_users']}\n"
        message += f"🚌 Líneas monitoreadas: {len(stats['monitored_lines'])}\n"
        message += f"📢 Usuarios con alertas generales: {stats['general_alerts_users']}\n\n"
        
        if stats['line_counts']:
            message += "*Suscripciones por línea:*\n"
            for line in sorted(stats['line_counts'].keys()):
                count = stats['line_counts'][line]
                message += f"   • Línea {line}: {count} usuario{'s' if count != 1 else ''}\n"
        
        self.send_message(chat_id, message)
    
    def process_message(self, message: dict):
        """Procesa un mensaje recibido"""
        try:
            chat_id = str(message['chat']['id'])
            username = message['chat'].get('first_name', 'Usuario')
            text = message.get('text', '')
            
            # Ignorar mensajes vacíos
            if not text:
                print(f"⚠️ Mensaje vacío de {username} ({chat_id})")
                return
            
            # Parsear comando y argumentos
            parts = text.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ''
            
            print(f"📨 Procesando mensaje de {username} ({chat_id}): {text}")
            
            # Procesar comandos
            if command == '/start':
                self.handle_start(chat_id, username)
            elif command == '/suscribir':
                self.handle_subscribe(chat_id, args)
            elif command == '/desuscribir':
                self.handle_unsubscribe(chat_id, args)
            elif command == '/mis_lineas' or command == '/mislineas':
                self.handle_my_lines(chat_id)
            elif command == '/alertas_generales' or command == '/alertasgenerales':
                self.handle_general_alerts(chat_id, args)
            elif command == '/ayuda' or command == '/help':
                self.handle_help(chat_id)
            elif command == '/stats':
                self.handle_stats(chat_id)
            else:
                print(f"⚠️ Comando no reconocido: {command}")
                self.send_message(chat_id, f"❓ Comando no reconocido: {command}\n\nUsa /ayuda para ver los comandos disponibles.")
        
        except Exception as e:
            print(f"❌ Error procesando mensaje: {e}")
            import traceback
            traceback.print_exc()
    
    def process_updates(self):
        """Procesa todas las actualizaciones pendientes"""
        updates = self.get_updates()
        
        if not updates:
            print("✨ No hay mensajes nuevos en cola")
            return
        
        print(f"📬 Hay {len(updates)} mensaje(s) en cola para procesar")
        
        for i, update in enumerate(updates):
            try:
                update_id = update.get('update_id', 'unknown')
                print(f"\n--- Procesando update {i+1}/{len(updates)} (ID: {update_id}) ---")
                
                # Actualizar offset
                self.offset = int(update_id) + 1
                
                # Procesar mensaje
                if 'message' in update:
                    self.process_message(update['message'])
                else:
                    print(f"⚠️ Update {update_id} no contiene mensaje")
            
            except Exception as e:
                print(f"❌ Error procesando update {update.get('update_id')}: {e}")
                import traceback
                traceback.print_exc()
        
        # Guardar offset
        self.save_offset(self.offset)
        print(f"\n✅ Todos los mensajes procesados correctamente")

def main():
    """Función principal"""
    print("=" * 60)
    print("🤖 Bot de Telegram - TMP Murcia (versión mejorada)")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    try:
        bot = TelegramBot()
        bot.process_updates()
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("=" * 60)
    print("✅ Procesamiento completado exitosamente")
    print("=" * 60)

if __name__ == "__main__":
    main()
