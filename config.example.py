# Configuración del Monitor TMP Murcia
# Este archivo muestra las opciones de configuración disponibles
# Para usarlo, edita los valores en scraper.py directamente

# URL de la página de TMP Murcia
TMP_URL = "https://tmpmurcia.es/ultima.asp"

# Líneas de autobús a monitorear
# Puedes añadir o quitar números según tus necesidades
LINES_TO_MONITOR = [
    "11",  # Murcia - Alcantarilla
    "44",  # Murcia - UCAM
    # "36",  # Descomentar para añadir línea 36
    # "39",  # Descomentar para añadir línea 39
]

# Archivo donde se guarda el historial de alertas
ALERTS_FILE = "alerts_history.json"

# Formato del mensaje de Telegram
# Variables disponibles: {line}, {title}, {url}, {date}
MESSAGE_TEMPLATE = """🚌 *Nueva Alerta TMP Murcia*

📍 *Línea {line}*
📝 {title}

🔗 [Ver detalles]({url})

⏰ {date}
"""

# Palabras clave para filtrar alertas (opcional)
# Si está vacío, se envían todas las alertas de las líneas monitoreadas
# Si tiene valores, solo se envían alertas que contengan estas palabras
KEYWORDS_FILTER = [
    # "obras",
    # "corte",
    # "desvío",
]

# Configuración de reintentos en caso de error
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5
