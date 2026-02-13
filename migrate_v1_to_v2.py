#!/usr/bin/env python3
"""
Script de migración de v1 a v2
Convierte la configuración antigua (TELEGRAM_CHAT_ID) al nuevo sistema de suscripciones
"""

import os
import sys
from subscriptions import SubscriptionManager

def migrate_to_subscriptions():
    """Migra la configuración antigua al nuevo sistema de suscripciones"""
    
    print("=" * 60)
    print("🔄 Migración de v1 a v2")
    print("=" * 60)
    
    # Verificar si existe TELEGRAM_CHAT_ID en las variables de entorno
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not chat_id:
        print("\n❌ No se encontró TELEGRAM_CHAT_ID")
        print("ℹ️ Si ya usabas la v2, no necesitas migrar")
        print("ℹ️ Si es tu primera instalación, simplemente usa /start en tu bot")
        return
    
    print(f"\n✅ Encontrado TELEGRAM_CHAT_ID: {chat_id}")
    print("\n🔧 Creando suscripción automática...")
    
    # Cargar gestor de suscripciones
    sub_manager = SubscriptionManager()
    
    # Suscribir al usuario a las líneas por defecto (11 y 44)
    default_lines = ["11", "44"]
    
    for line in default_lines:
        sub_manager.subscribe_line(chat_id, line)
        print(f"   ✅ Suscrito a línea {line}")
    
    # Activar alertas generales por defecto
    sub_manager.set_receive_general(chat_id, True)
    print(f"   ✅ Alertas generales activadas")
    
    print("\n" + "=" * 60)
    print("✅ Migración completada con éxito!")
    print("=" * 60)
    print("\n📝 Resumen:")
    print(f"   • Usuario: {chat_id}")
    print(f"   • Líneas: {', '.join(default_lines)}")
    print(f"   • Alertas generales: Activadas")
    print("\n💡 Ahora puedes:")
    print("   • Usar /mis_lineas para ver tus suscripciones")
    print("   • Usar /suscribir [línea] para añadir más líneas")
    print("   • Usar /desuscribir [línea] para quitar líneas")
    print("\n⚠️ Nota: Puedes eliminar el secret TELEGRAM_CHAT_ID de GitHub")
    print("   ya que ahora no se necesita (el bot gestiona los usuarios)")

if __name__ == "__main__":
    try:
        migrate_to_subscriptions()
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        sys.exit(1)
