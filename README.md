# README — Trabajo Fin de Grado

## Sistema modular para la indexación de un conjunto de documentos locales: Aplicaci on de algoritmos de recuperación de información y análisis documental

### Clara Sola Ruiz  
**Grado en Ingeniería Informática — Universidad de Granada**

---

## Descripción

La búsqueda de documentos específicos dentro de grandes volúmenes de información puede convertirse en una tarea compleja si no se dispone de herramientas adecuadas para facilitar su indexación, recuperación y clasificación.

Este proyecto ofrece una solución a este desafío mediante el diseño de una arquitectura modular capaz de gestionar colecciones documentales locales utilizando técnicas de recuperación de información. La arquitectura propuesta abarca todas las fases necesarias: desde la extracción y transformación del contenido textual, hasta su representación estructurada mediante diversos modelos de indexación.

Además, el sistema incorpora mecanismos de almacenamiento flexible, permitiendo consultar y conservar las representaciones generadas de forma eficiente y adaptada a distintas necesidades. Para comprobar la eficacia de la solución desarrollada, se ha definido un caso de estudio práctico que demuestra cómo esta arquitectura mejora tanto el acceso a la información como la organización de los documentos procesados.

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu_usuario/tu_tfg.git
   cd tu_tfg
   ```

2. **Crear un entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar MongoDB (si se usa almacenamiento en base de datos):**
   - Asegúrate de que el servidor de MongoDB esté activo y accesible.
   - Configura las variables de conexión en `config.py` o en variables de entorno.

---

## 🗂️ Cómo usar

1. **Registrar una colección de documentos:**
   - Coloca tus archivos en la carpeta de colección.
   - Ejecuta el módulo de registro para indexar los documentos.

2. **Configurar y ejecutar un pipeline:**
   - Define el pipeline en la interfaz o en un archivo de configuración.
   - Ejecuta `main.py` para aplicar extracción, preprocesamiento y representación.

3. **Realizar búsquedas:**
   - Usa la interfaz para introducir consultas.
   - El sistema aplica el mismo pipeline para representar la consulta y devuelve documentos relevantes.

4. **Consultar y descargar representaciones:**
   - Desde la interfaz, es posible consultar representaciones guardadas en MongoDB o localmente.
   - Opcionalmente, se pueden descargar en formato JSON.

---

## 📑 Documentación

El proyecto incluye:
- **Manual de instalación:** Ver `apendices/manual_instalacion.tex`
- **Manual de usuario:** Ver `apendices/manual_usuario.tex`
- **Informe completo:** Documento principal del TFG (capítulos de introducción, estado del arte, diseño, implementación, ejemplo de uso y conclusiones).

---

## 👩‍💻 Autor

**Clara Sola Ruiz**  
Universidad de Granada

---

## 📚 Licencia

Este proyecto se presenta como parte de los requisitos para la obtención del título de Grado en Ingeniería Informática de la Universidad de Granada. Su uso académico y su distribución están permitidos con fines educativos y de investigación.

---

## ✅ Referencias

Las referencias bibliográficas completas se encuentran en el documento principal (`bibliografia/bibliografia.bib`).

---

## 🔗 Contacto

Para más información o sugerencias, contactar a través del correo institucional.

---

## 💡 Notas finales

Este README resume el propósito, la instalación y el uso del sistema. Para detalles técnicos, ejemplos y casos de uso, se recomienda consultar el informe completo y los manuales anexos.
