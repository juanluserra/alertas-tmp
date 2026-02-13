# 🚍 TMP Murcia - Monitor de Alertas

Monitor automático de alertas de autobuses TMP Murcia con **sistema de suscripciones personalizado**. Cada usuario elige qué líneas quiere monitorear y recibe notificaciones instantáneas en Telegram.

## ✨ Características

- 🔄 **Monitoreo automático cada 15 minutos** usando GitHub Actions
- 📱 **Notificaciones push instantáneas** vía Telegram
- 👤 **Sistema de suscripciones personalizadas** - cada usuario elige sus líneas
- 🎯 **Alertas generales** - recibe avisos sin línea específica (configurable)
- 💾 **Sin duplicados** - solo te avisa de alertas nuevas
- 👥 **Multi-usuario** - cada persona configura sus preferencias
- ☁️ **100% en la nube** - no necesitas tener nada encendido
- 🆓 **Totalmente gratuito**

## 🚀 Configuración Rápida (10 minutos)

### Paso 1: Fork del Repositorio

1. Haz clic en el botón **Fork** arriba a la derecha
2. Esto creará una copia del proyecto en tu cuenta de GitHub

### Paso 2: Crear Bot de Telegram

1. Abre Telegram y busca: **@BotFather**
2. Envía el comando: `/newbot`
3. Elige un nombre para tu bot (ej: "TMP Murcia Alertas")
4. Elige un username (ej: "tmp_murcia_bot")
5. **Guarda el token** que te da (algo como: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Paso 3: Configurar Secret en GitHub

1. Ve a tu fork del repositorio en GitHub
2. Click en **Settings** (⚙️ Configuración)
3. En el menú izquierdo: **Secrets and variables** → **Actions**
4. Click en **New repository secret**
5. Añade este secret:

   **Secret:**
   - Name: `TELEGRAM_BOT_TOKEN`
   - Value: El token que te dio BotFather (ej: `123456789:ABCdefGHI...`)

⚠️ **Nota:** Ya NO necesitas el TELEGRAM_CHAT_ID porque ahora cada usuario se suscribe individualmente con el bot.

### Paso 4: Activar GitHub Actions

1. Ve a la pestaña **Actions** en tu repositorio
2. Si aparece un mensaje para habilitar workflows, haz click en **"I understand my workflows, go ahead and enable them"**
3. El monitor empezará a funcionar automáticamente cada 15 minutos

4. **IMPORTANTE:** Configura permisos de escritura:
   - Settings → Actions → General
   - En "Workflow permissions" selecciona **"Read and write permissions"**
   - Guarda cambios

### Paso 5: Suscribirte a tus líneas favoritas 🎯

1. **Busca tu bot** en Telegram (el que creaste con @BotFather)
2. **Inicia conversación** con él: `/start`
3. **Suscríbete a las líneas que quieras:**
   ```
   /suscribir 11
   /suscribir 44
   /suscribir 36
   ```
4. **Verifica tus suscripciones:** `/mis_lineas`

¡Y listo! Ahora recibirás alertas personalizadas de solo las líneas que elegiste.

### Paso 6: Probar (Opcional)

Para probar que funciona sin esperar:

1. Ve a **Actions** → **Monitor TMP Murcia**
2. Click en **Run workflow** → **Run workflow**
3. Espera 30 segundos y revisa los logs
4. Si hay alertas nuevas de tus líneas suscritas, ¡te llegará un mensaje de Telegram! 🎉

## 🤖 Comandos del Bot

Una vez que has iniciado conversación con tu bot, puedes usar estos comandos:

### Gestión de Suscripciones

- **`/suscribir [línea]`** - Suscribirte a una línea específica
  ```
  /suscribir 11
  /suscribir 44
  /suscribir 36
  ```

- **`/desuscribir [línea]`** - Desuscribirte de una línea
  ```
  /desuscribir 11
  ```

- **`/mis_lineas`** - Ver tus líneas suscritas actualmente

### Alertas Generales

- **`/alertas_generales on`** - Activar alertas sin línea específica (por defecto: ON)
- **`/alertas_generales off`** - Desactivar alertas generales

💡 **Sobre las alertas generales:** Algunas notificaciones de TMP no especifican número de línea (ej: avisos importantes, cambios globales). Por defecto las recibirás automáticamente, pero puedes desactivarlas si solo quieres alertas de líneas específicas.

### Otros Comandos

- **`/ayuda`** - Ver ayuda y lista de comandos
- **`/start`** - Reiniciar bot y ver mensaje de bienvenida

## 📊 Cómo Funciona

```
┌──────────────────────────────────────────────┐
│   GitHub Actions (cada 15 minutos)          │
│   ┌──────────────────────────────────────┐  │
│   │ 1. Procesar comandos del bot         │  │
│   │ 2. Actualizar suscripciones          │  │
│   │ 3. Consultar tmpmurcia.es            │  │
│   │ 4. Extraer alertas de líneas activas │  │
│   │ 5. Comparar con historial            │  │
│   │ 6. Enviar a usuarios suscritos       │  │
│   │ 7. Guardar historial y estado        │  │
│   └──────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
                    ↓
    ┌───────────────────────────────────┐
    │         Telegram Bot              │
    │  📱 Notificaciones personalizadas │
    │  👤 Usuario A: L11, L44           │
    │  👤 Usuario B: L36                │
    │  👤 Usuario C: L11, L39, General  │
    └───────────────────────────────────┘
          └───────────────┘
```

## 🔧 Personalización

### Cambiar la frecuencia de verificación

Edita `.github/workflows/monitor.yml`:

```yaml
on:
  schedule:
    - cron: '*/15 * * * *'  # Cada 15 minutos
    # Ejemplos:
    # '*/5 * * * *'   → Cada 5 minutos
    # '*/30 * * * *'  → Cada 30 minutos
    # '0 * * * *'     → Cada hora
```

⚠️ **Nota:** GitHub Actions tiene un límite de 2000 minutos/mes en cuentas gratuitas, pero con ejecuciones cada 15 minutos solo usas ~200 minutos/mes.

## 📱 Formato de las Notificaciones

### Alertas de Línea Específica
Recibirás mensajes como este cuando haya alertas en tus líneas suscritas:

```
🚌 Nueva Alerta TMP Murcia

📍 Línea 44
📝 Línea 44. Corte al tráfico en Alcantarilla por Carnaval 13 y 15 febrero

🔗 Ver detalles

⏰ 13/02/2026 09:30
```

### Alertas Generales
Si tienes activadas las alertas generales, también recibirás:

```
🚌 Nueva Alerta TMP Murcia

📍 ⚠️ Alerta General
📝 Nuevo descuento Bonos Tricolor a partir de 1 julio 2025

🔗 Ver detalles

⏰ 13/02/2026 09:30
```

## 🐛 Solución de Problemas

### No recibo notificaciones

1. **Verifica que estás suscrito:**
   - Envía `/mis_lineas` al bot para ver tus suscripciones
   - Si no aparece nada, suscríbete con `/suscribir [línea]`

2. **Verifica el bot:**
   - Envía `/start` a tu bot en Telegram
   - Debe responderte con el mensaje de bienvenida

3. **Verifica los secrets:**
   - Ve a Settings → Secrets and variables → Actions
   - Confirma que `TELEGRAM_BOT_TOKEN` está configurado

3. **Revisa los logs:**
   - Ve a Actions → último workflow ejecutado
   - Click en "check-alerts" para ver los logs
   - Busca errores en rojo

### El workflow no se ejecuta

1. **Verifica que Actions está habilitado:**
   - Settings → Actions → General
   - Debe estar en "Allow all actions and reusable workflows"

2. **Haz un push manualmente:**
   - Edita cualquier archivo (ej: añade un espacio en README.md)
   - Haz commit y push
   - Esto forzará una ejecución

### GitHub Actions dice que tengo permisos insuficientes

1. Ve a Settings → Actions → General
2. En "Workflow permissions" selecciona "Read and write permissions"
3. Guarda los cambios

## 📈 Estadísticas

Puedes ver el historial de ejecuciones en:
- **Actions** → **Monitor TMP Murcia** → ver todas las ejecuciones

El archivo `alerts_history.json` mantiene un registro de las alertas conocidas.

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar el monitor:

1. Fork del proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -am 'Añadir mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## 💡 Ideas para Futuras Mejoras

- [ ] Notificaciones por email como alternativa a Telegram
- [ ] Filtrado por palabras clave (obras, horarios, etc.)
- [ ] Interfaz web para ver historial de alertas
- [ ] Integración con Google Calendar para alertas de horarios
- [ ] Soporte para otras ciudades/empresas de autobuses
- [ ] Sistema de prioridad de alertas (urgente, normal, info)

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## ⚠️ Disclaimer

Este es un proyecto personal no oficial. No está afiliado con TMP Murcia ni con la empresa operadora. Los datos se obtienen de la página pública de TMP Murcia.

---

**¿Problemas? ¿Sugerencias?** Abre un [Issue](../../issues) en GitHub

**¿Te ha sido útil?** Dale una ⭐ al repositorio
