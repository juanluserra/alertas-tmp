#!/usr/bin/env python3
"""
Script de prueba local para el monitor de TMP Murcia
Ejecuta el scraper sin enviar notificaciones de Telegram para probar que funciona
"""

import os
import sys

# Desactivar notificaciones de Telegram para pruebas
os.environ.pop('TELEGRAM_BOT_TOKEN', None)
os.environ.pop('TELEGRAM_CHAT_ID', None)

# Importar y ejecutar el scraper
import scraper

if __name__ == "__main__":
    print("🧪 Modo de prueba local (sin notificaciones Telegram)\n")
    scraper.main()
    print("\n✅ Prueba completada. Revisa los resultados arriba.")
    print("📝 Nota: En producción, las notificaciones se enviarán por Telegram")
