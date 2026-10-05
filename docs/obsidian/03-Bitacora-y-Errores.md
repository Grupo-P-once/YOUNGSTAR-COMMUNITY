---
title: Bitácora y errores
tags: [youngstar, bitacora, bugs]
---

# Bitácora

## 2026-10-05
- Recibido `EMILIANO_PEREZANDI_original.txt` y petición de buscar el audio en *Descargas*.
- Convertida transcripción, leída completa, investigación web, notas creadas en `docs/obsidian/`.

## Errores / incidencias

### 1. Audio no accesible
- **Qué pasó:** se pidió buscar el audio en Descargas.
- **Por qué:** la sesión corre en un contenedor cloud; no existe `~/Downloads` ni el archivo (`find / -iname "*PEREZANDI*"` solo halló el `.txt`).
- **Resolución:** se usó la transcripción `.txt`. Si hay que revisar el audio, súbelo como adjunto.

### 2. Lectura del .txt falló/ilegible
- **Qué pasó:** `Read` rechazó el archivo (>25k tokens) y `head` mostró caracteres separados por espacios.
- **Por qué:** archivo en **UTF‑16 LE**, ~88 KB.
- **Resolución:** `iconv -f UTF-16 -t UTF-8`, quitar líneas vacías (queda ~45 KB) y leer por tramos.

### 3. Transcripción con errores de reconocimiento
- Nombres mal transcritos: "Strike"→Stripe, "Air Dable/arte"→Airtable, "Training Pink/Pix"→TrainingPeaks, "WHOOP"→"uhop/Wood", "jonster"→¿Youngstar?, "Sancho"→¿Sancho/plataforma previa?, "Neurónomi".
- **Resolución:** se normalizaron por contexto; marcar como supuestos.

### 4. Repositorio vacío
- `git log` → sin commits. Las notas son lo primero en el repo.

### 5. Foros / redes
- Las búsquedas no devolvieron hilos de Reddit/foros útiles; no se inventó contenido.

### 6. No se pudo abrir el PR
- **Qué pasó:** `create_pull_request` con base `main` falló: `PullRequest.base (invalid)`.
- **Por qué:** el repositorio remoto solo tiene la rama `claude/blissful-lovelace-7nnuyz`; no existe `main` (repo recién creado, sin commits previos), así que no hay rama base.
- **Resolución:** pendiente. Opciones: que el dueño cree `main` (o fije una rama por defecto) y luego se abre el PR. No se creó `main` sin autorización.

### 7. No se pudo descargar el audio desde aconvert.com
- **Qué pasó:** `curl` al enlace `s21.aconvert.com/...m4a` falló con `CONNECT tunnel failed, response 403`.
- **Por qué:** la política de red del entorno cloud solo permite ciertos dominios; `s21.aconvert.com` no está en la lista permitida (no es un problema del enlace).
- **Resolución:** no se eludió el proxy. Opciones: añadir `aconvert.com` en *Allowed domains* del entorno, o seguir con la transcripción. Además no hay `whisper` instalado (solo `ffmpeg`), así que habría que instalar un transcriptor.

## 2026-10-05 (tarde)
- El usuario aclaró que es un **tercero** que atendió la llamada y debe ofrecer servicios. Se redactó [[04-Propuesta-de-Servicios]] (borrador, sin precios).
- **Corrección de criterio:** antes recomendé auditar "sin que quien vende el mantenimiento la haga"; en la propuesta se resolvió haciendo la auditoría un entregable independiente y pagado por separado.
- El usuario confirmó que va **como agencia de mantenimiento** de un proyecto ya existente. [[04-Propuesta-de-Servicios]] reescrita (v2): auditoría de entrada, planes mensuales Básico/Estándar/Plus, mejoras por proyecto y transición con el proveedor anterior.
- **Riesgo anotado:** no se puede prometer mantenimiento de un stack que aún no se ha visto; por eso el contrato arranca tras la Fase 0.
- Generado PDF sin precios: `docs/propuesta/Propuesta-Mantenimiento-Youngstar.pdf` (script `docs/propuesta/build.py`, ReportLab). Tono para cliente: sin críticas al proveedor anterior ni notas internas.
- **Incidencia:** `reportlab` no estaba instalado (`ModuleNotFoundError`); se resolvió con `pip install reportlab`. Primera versión salió en 3 páginas con la última casi vacía; se compactó márgenes y tipografía a 2 páginas.
- **Pendiente:** completar `[Nombre de la agencia]`, `[fecha]` y datos de contacto editando `build.py` y regenerando.

## 2026-10-05 (noche) — PDF v2 con diseño de referencia
- El usuario pidió replicar el diseño del PDF de ejemplo (portada con rombos, círculos numerados, tarjetas, columnas antes/después, línea de tiempo, banner verde) e incluir **problema → solución → beneficio**. Se reescribió `docs/propuesta/build.py` (ReportLab, plataforma propia; no se copió el logo ni el contenido del ejemplo). Resultado: 8 páginas, sin precios.
- **Error 1: texto de portada con letras muy separadas y cortado.** *Por qué:* `setCharSpace` en un `textobject` persiste en el flujo del PDF y se aplicó también al título y subtítulo dibujados después. *Solución:* reponer `setCharSpace(0)` tras cada `textOut`.
- **Error 2: "El reto" quedaba partido entre páginas 2 y 3.** *Por qué:* la cabecera y sus tarjetas no cabían juntas. *Solución:* salto de página antes de esa sección.
- **Error 3: página casi vacía al final (desbordaba un párrafo).** *Por qué:* la sección "Qué es de quién" se partía entre páginas. *Solución:* moverla completa a la página final y reorganizar secciones.
- **Error 4: cuadrícula de indicadores partida entre 2 páginas.** *Solución:* pasar de 2×2 a una fila de 4 tarjetas.
- **Error 5: cifras largas partidas en 2 líneas** ("~2 de 100", "100 % vs 55 %"). *Solución:* reducir tamaño y acortar a "100 vs 55" con la unidad en la leyenda.
- **Decisión de contenido:** las cifras (6 años, 127 atletas, ~2 de 100, 100 vs 55) se presentan como "mencionadas por el equipo", y los beneficios son cualitativos o medibles, sin prometer porcentajes inventados.
- Nota: las fuentes son las estándar del PDF (Helvetica/Courier); el ejemplo usa otras, así que la tipografía no es idéntica.
- Se pusieron los datos de **OTLI** en el PDF (nombre, León Guanajuato, correo, WhatsApp, sitio), tomados del PDF de ejemplo que envió el usuario. Ya no quedan marcadores `[ ]`.
- **Error:** mi primer script de reemplazo usó `re.sub` con `\u...` en el texto de reemplazo → `re.error: bad escape \u`. No cambió el archivo y el PDF se regeneró igual que antes (lo detecté porque seguían los corchetes). *Solución:* reemplazos con `str.replace` y comprobación con `assert`.
- **Efecto secundario:** la línea extra del lema hizo que la línea de contacto pasara a una página 9 casi vacía. *Solución:* reducir espaciados en la última página; vuelve a 8 páginas.
- No se incluyó el logo de OTLI (solo texto); está disponible en el PDF de ejemplo si se quiere extraer.
