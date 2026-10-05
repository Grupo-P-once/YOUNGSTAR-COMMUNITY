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
