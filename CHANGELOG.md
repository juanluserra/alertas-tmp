# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

## [2.0.0] - 2026-02-13

### 🎉 Nueva Funcionalidad Principal: Sistema de Suscripciones

#### ✨ Añadido
- **Sistema de suscripciones personalizado por usuario**
  - Cada usuario puede elegir las líneas que quiere monitorear
  - No hay límite de líneas por usuario
  - Bot interactivo de Telegram con comandos
  
- **Comandos del bot:**
  - `/start` - Iniciar bot y ver bienvenida
  - `/suscribir [línea]` - Suscribirse a una línea
  - `/desuscribir [línea]` - Desuscribirse de una línea
  - `/mis_lineas` - Ver suscripciones actuales
  - `/alertas_generales [on/off]` - Configurar alertas sin línea
  - `/ayuda` - Ver ayuda completa
  - `/stats` - Ver estadísticas del sistema (admin)

- **Alertas generales configurables**
  - Por defecto, todos reciben alertas sin número de línea específico
  - Se puede desactivar con `/alertas_generales off`

- **Sistema multi-usuario**
  - Múltiples personas pueden usar el mismo bot
  - Cada uno configura sus preferencias independientemente
  - Las notificaciones se envían solo a usuarios suscritos a cada línea

- **Nuevos archivos:**
  - `bot.py` - Bot de Telegram para gestionar comandos
  - `subscriptions.py` - Módulo de gestión de suscripciones
  - `subscriptions.json` - Base de datos de suscripciones de usuarios
  - `migrate_v1_to_v2.py` - Script de migración de v1 a v2
  - `CHANGELOG.md` - Este archivo

#### 🔄 Cambiado
- **Ya no se necesita TELEGRAM_CHAT_ID**
  - Los usuarios se registran usando el bot
  - Solo se necesita TELEGRAM_BOT_TOKEN

- **Workflow de GitHub Actions actualizado**
  - Ahora ejecuta primero el bot (procesar comandos)
  - Luego ejecuta el scraper (enviar alertas)
  - Guarda 3 archivos: `alerts_history.json`, `subscriptions.json`, `.telegram_offset`

- **scraper.py completamente refactorizado**
  - Usa el sistema de suscripciones en lugar de líneas hardcodeadas
  - Envía notificaciones a usuarios específicos según suscripciones
  - Soporta alertas con y sin número de línea

- **Documentación actualizada**
  - `README.md` con nuevo sistema de comandos
  - `GUIA_RAPIDA.txt` con instrucciones actualizadas
  - Nuevos ejemplos de notificaciones

#### 🗑️ Eliminado
- Variable `LINES_TO_MONITOR` del código
- Necesidad de editar código para cambiar líneas monitoreadas
- Dependencia de TELEGRAM_CHAT_ID

### 🐛 Correcciones
- Mejorada la detección de líneas en títulos de alertas
- Mejor manejo de errores en envío de notificaciones

### 📝 Notas de Migración

Si ya usabas la v1.0:

1. **Actualiza tu repositorio** con los nuevos archivos
2. **Ya no necesitas TELEGRAM_CHAT_ID** (pero si lo dejas configurado, seguirá funcionando temporalmente con el script de migración)
3. **Inicia conversación con tu bot** en Telegram
4. **Suscríbete a tus líneas** con `/suscribir [línea]`

Opcionalmente, puedes ejecutar `migrate_v1_to_v2.py` para migrar automáticamente tu configuración anterior.

---

## [1.0.0] - 2026-02-13

### Primera versión

#### ✨ Añadido
- Monitor automático de alertas de TMP Murcia
- Ejecución cada 15 minutos con GitHub Actions
- Notificaciones por Telegram
- Monitoreo de líneas 11 y 44 (hardcodeado)
- Sistema de historial para evitar duplicados
- Documentación completa en README.md
- Guía rápida de configuración
- Templates de issues para GitHub
- Licencia MIT

#### 📦 Archivos incluidos
- `scraper.py` - Script principal de monitoreo
- `.github/workflows/monitor.yml` - Workflow de GitHub Actions
- `requirements.txt` - Dependencias
- `alerts_history.json` - Historial de alertas
- `README.md` - Documentación
- `GUIA_RAPIDA.txt` - Guía rápida
- `CONTRIBUTING.md` - Guía de contribución
- `LICENSE` - Licencia MIT
