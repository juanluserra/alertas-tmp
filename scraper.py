#!/usr/bin/env python3
"""
TMP Murcia Bus Alerts Monitor
Monitorea la página de últimas noticias de TMP Murcia y envía alertas personalizadas por usuario
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import sys
from datetime import datetime
import re
from subscriptions import SubscriptionManager

# Configuración
TMP_URL = "https://tmpmurcia.es/ultima.asp"
ALERTS_FILE = "alerts_history.json"

def load_previous_alerts():
    """Carga las alertas previas del archivo JSON"""
    if os.path.exists(ALERTS_FILE):
        try:
            with open(ALERTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Error al leer el archivo de alertas, creando uno nuevo")
            return {"alerts": []}
    return {"alerts": []}

def save_alerts(alerts_data):
    """Guarda las alertas en el archivo JSON"""
    with open(ALERTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(alerts_data, f, ensure_ascii=False, indent=2)

def extract_line_number(text):
    """Extrae el número de línea del texto"""
    match = re.search(r'Línea\s+(\d+)', text, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def scrape_tmp_alerts():
    """Extrae las alertas de la página de TMP"""
    try:
        print(f"🔍 Consultando {TMP_URL}...")
        response = requests.get(TMP_URL, timeout=30)
        response.encoding = 'latin-1'  # La página usa codificación latin-1
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar todos los enlaces con alertas
        alerts = []
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            if 'Cuerpo.asp?codigo=' in href:
                title = link.get_text(strip=True)
                code = href.split('codigo=')[1] if 'codigo=' in href else None
                
                if code and title:
                    line_number = extract_line_number(title)
                    alerts.append({
                        'code': code,
                        'title': title,
                        'line': line_number,
                        'url': f"https://tmpmurcia.es/{href}"
                    })
        
        print(f"✅ Encontradas {len(alerts)} alertas totales")
        return alerts
        
    except Exception as e:
        print(f"❌ Error al consultar la página: {e}")
        return []

def get_monitored_alerts(alerts, subscription_manager):
    """
    Retorna todas las alertas que al menos un usuario quiere recibir
    Esto incluye alertas de líneas específicas y alertas generales
    """
    monitored_lines = subscription_manager.get_all_monitored_lines()
    
    # Separar alertas en dos categorías
    line_alerts = []
    general_alerts = []
    
    for alert in alerts:
        if alert['line']:
            # Alerta con línea específica
            if alert['line'] in monitored_lines:
                line_alerts.append(alert)
        else:
            # Alerta general (sin línea específica)
            general_alerts.append(alert)
    
    # Mantener el orden original (tal como aparece en la web)
    all_monitored = []
    for alert in alerts:
        if alert['line'] and alert['line'] in monitored_lines:
            all_monitored.append(alert)
        elif not alert['line']:
            all_monitored.append(alert)
    
    print(f"📊 Alertas monitoreadas:")
    print(f"   • Con línea específica: {len(line_alerts)}")
    print(f"   • Generales (sin línea): {len(general_alerts)}")
    print(f"   • Total: {len(all_monitored)}")
    
    return all_monitored

def find_new_alerts(current_alerts, previous_data):
    """Compara alertas actuales con las previas para encontrar nuevas"""
    previous_codes = {alert['code'] for alert in previous_data.get('alerts', [])}
    new_alerts = [alert for alert in current_alerts if alert['code'] not in previous_codes]
    
    print(f"🆕 Nuevas alertas encontradas: {len(new_alerts)}")
    return new_alerts

def send_telegram_notifications(alert, subscription_manager):
    """Envía notificaciones a todos los usuarios suscritos a la alerta"""
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("⚠️ No se configuró TELEGRAM_BOT_TOKEN")
        return 0
    
    # Obtener usuarios que deben recibir esta alerta
    recipients = subscription_manager.get_users_for_alert(alert['line'])
    
    if not recipients:
        print(f"   ℹ️ No hay usuarios suscritos a {'línea ' + alert['line'] if alert['line'] else 'alertas generales'}")
        return 0
    
    # Preparar mensaje
    line_text = f"Línea {alert['line']}" if alert['line'] else "⚠️ Alerta General"
    message = f"""🚌 *Nueva Alerta TMP Murcia*

📍 *{line_text}*
📝 {alert['title']}

🔗 [Ver detalles]({alert['url']})

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}
"""
    
    # Enviar a cada usuario suscrito
    sent_count = 0
    for chat_id in recipients:
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True
            }
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                sent_count += 1
            else:
                print(f"   ⚠️ Error al enviar a {chat_id}: {response.status_code}")
        
        except Exception as e:
            print(f"   ⚠️ Error al enviar a {chat_id}: {e}")
    
    print(f"   ✅ Notificación enviada a {sent_count}/{len(recipients)} usuario(s)")
    return sent_count

def main():
    """Función principal"""
    print("=" * 60)
    print("🚍 TMP Murcia - Monitor de Alertas")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    # Cargar gestor de suscripciones
    subscription_manager = SubscriptionManager()
    stats = subscription_manager.get_stats()
    
    print(f"👥 Usuarios activos: {stats['total_users']}")
    print(f"🚌 Líneas monitoreadas: {', '.join(sorted(stats['monitored_lines'])) if stats['monitored_lines'] else 'Ninguna'}")
    print(f"📢 Usuarios con alertas generales: {stats['general_alerts_users']}")
    
    # Verificar si hay usuarios
    if stats['total_users'] == 0:
        print("\n⚠️ No hay usuarios suscritos todavía")
        print("💡 Los usuarios deben usar el bot de Telegram para suscribirse")
        return
    
    # Cargar alertas previas
    previous_data = load_previous_alerts()
    print(f"📂 Alertas previas en historial: {len(previous_data.get('alerts', []))}")
    
    # Obtener alertas actuales
    all_alerts = scrape_tmp_alerts()
    if not all_alerts:
        print("⚠️ No se pudieron obtener alertas, saliendo...")
        sys.exit(1)
    
    # Filtrar solo las alertas monitoreadas (por al menos un usuario)
    monitored_alerts = get_monitored_alerts(all_alerts, subscription_manager)
    
    # Encontrar alertas nuevas
    new_alerts = find_new_alerts(monitored_alerts, previous_data)
    
    # Enviar notificaciones para alertas nuevas
    if new_alerts:
        print(f"\n🔔 Enviando notificaciones para {len(new_alerts)} alerta(s) nueva(s)...")
        total_sent = 0
        for alert in reversed(new_alerts):
            line_desc = f"Línea {alert['line']}" if alert['line'] else "General"
            print(f"\n📨 {line_desc}: {alert['title'][:50]}...")
            sent = send_telegram_notifications(alert, subscription_manager)
            total_sent += sent
                
        print(f"\n✅ Total de notificaciones enviadas: {total_sent}")
    else:
        print("\n✨ No hay alertas nuevas")
    
    # Guardar el estado actualizado
    updated_data = {
        'last_check': datetime.now().isoformat(),
        'alerts': monitored_alerts
    }
    save_alerts(updated_data)
    print(f"\n💾 Estado guardado: {len(monitored_alerts)} alertas en historial")
    
    print("=" * 60)
    print("✅ Ejecución completada")
    print("=" * 60)

if __name__ == "__main__":
    main()
