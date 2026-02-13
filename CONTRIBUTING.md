# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al monitor de alertas TMP Murcia! Este documento te guiará sobre cómo puedes ayudar a mejorar el proyecto.

## 🎯 Formas de Contribuir

### 🐛 Reportar Bugs

Si encuentras un error:

1. Revisa los [Issues existentes](../../issues) para ver si ya fue reportado
2. Si no existe, [crea un nuevo Issue](../../issues/new)
3. Incluye:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Comportamiento esperado vs. actual
   - Logs del error (si aplica)
   - Capturas de pantalla (si ayuda)

### 💡 Sugerir Mejoras

¿Tienes una idea para mejorar el proyecto?

1. [Crea un Issue](../../issues/new) con la etiqueta "enhancement"
2. Describe:
   - Qué problema resuelve tu idea
   - Cómo debería funcionar
   - Casos de uso

### 🔧 Contribuir con Código

#### Pre-requisitos

- Python 3.11 o superior
- Git
- Cuenta de GitHub

#### Proceso

1. **Fork** el repositorio
2. **Clona** tu fork:
   ```bash
   git clone https://github.com/TU_USUARIO/tmp-murcia-alertas.git
   cd tmp-murcia-alertas
   ```

3. **Crea una rama** para tu cambio:
   ```bash
   git checkout -b feature/mi-mejora
   ```

4. **Instala dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Haz tus cambios** y pruébalos localmente:
   ```bash
   python test_local.py
   ```

6. **Commit** tus cambios:
   ```bash
   git add .
   git commit -m "Descripción clara del cambio"
   ```

7. **Push** a tu fork:
   ```bash
   git push origin feature/mi-mejora
   ```

8. **Crea un Pull Request** desde GitHub

#### Estilo de Código

- Sigue PEP 8 para Python
- Usa nombres descriptivos para variables y funciones
- Añade comentarios para lógica compleja
- Mantén funciones pequeñas y enfocadas

#### Commits

Usa prefijos claros en tus commits:
- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formato, estilo (sin cambios de código)
- `refactor:` Refactorización de código
- `perf:` Mejoras de rendimiento
- `test:` Añadir o corregir tests

## 🧪 Testing

Antes de enviar un PR:

1. Ejecuta el test local:
   ```bash
   python test_local.py
   ```

2. Verifica que no hay errores
3. Prueba con diferentes escenarios si es posible

## 📋 Ideas para Contribuir

### Fáciles (buenas para empezar)
- [ ] Mejorar mensajes de error
- [ ] Mejorar documentación
- [ ] Añadir ejemplos de uso

### Intermedias
- [ ] Notificaciones por email
- [ ] Filtrado por palabras clave
- [ ] Tests automatizados

### Avanzadas
- [ ] Dashboard web para ver historial
- [ ] Integración con Google Calendar

## ❓ ¿Dudas?

Si tienes preguntas sobre cómo contribuir:

1. Revisa este documento
2. Lee el [README.md](README.md)
3. Busca en [Issues cerrados](../../issues?q=is%3Aissue+is%3Aclosed)
4. [Crea un Issue](../../issues/new) con tu pregunta

## 📜 Código de Conducta

- Sé respetuoso y constructivo
- Acepta críticas constructivas
- Enfócate en lo que es mejor para la comunidad
- Muestra empatía hacia otros miembros

## 🙏 Agradecimientos

¡Gracias por hacer que este proyecto sea mejor para todos! Cada contribución, por pequeña que sea, es valiosa.

---

**¿Primera contribución a open source?** ¡Genial! Todos empezamos alguna vez. No dudes en pedir ayuda si la necesitas.
