---
title: Propuesta de servicios para Youngstar Community
tags: [youngstar, propuesta, ventas]
estado: borrador
fecha: 2026-10-05
---

# Propuesta de servicios — Youngstar Community

> [!note] Borrador
> Basada en la llamada con Emiliano (ver [[00-Resumen-Proyecto-Youngstar]]). **Los precios van en blanco a propósito**: hay que cotizarlos con horas reales y costos de API/servidor/tokens. Ajustar nombres y alcance antes de enviar.

## 1. Lo que escuchamos
Producto ya construido por un proveedor en Monterrey, con tres dolores:
1. **Datos poco confiables** (adherencia, duplicados, competencias canceladas que siguen en el plan).
2. **Dependencia y costo de mantenimiento** del desarrollador original.
3. **Ventas y seguimiento** que dependen de Emiliano (≈2 de cada 100 leads cierran).

Objetivo declarado: que la operación sea autónoma, dirigida por el doctor, **sin gastar más de lo necesario**.

## 2. Propuesta por fases (cada fase se aprueba por separado)

### Fase 0 — Auditoría y mapa de datos *(entregable independiente)*
- Inventario de Airtable, formularios, Stripe, webhooks, APIs, cron, servidor y accesos.
- Diagrama extremo a extremo y **lista priorizada de dónde se pierde o duplica información**.
- Revisión de **propiedad** de código, dominio, servidor y llaves.
- Opciones para TrainingPeaks (API de socio / carga por archivo / plataforma abierta) con pros, contras y costo.
- **Entrega:** informe + diagrama + plan con costo por fase. Si deciden no continuar con nosotros, el informe es suyo.
- Precio: $______ · Plazo: 1‑2 semanas.

### Fase 1 — Estabilizar datos
- ID único por atleta, escrituras idempotentes, bitácora de cada sincronización y alertas cuando algo falla.
- Definir y corregir la fórmula de **adherencia**.
- Confirmación mensual de competencias por WhatsApp (plantilla) que actualiza el plan.
- Precio: $______ · Plazo: 2‑4 semanas.

### Fase 2 — Calidad del entrenamiento y panel del doctor
- Reglas fijas por deporte (bricks, técnica de natación, descargas) fuera del LLM.
- Panel del doctor: expedientes, aprobación de planes antes de publicarse, alertas por síntomas.
- Indicadores en español con interpretación.
- Precio: $______ · Plazo: 4‑6 semanas.

### Fase 3 — Agente de seguimiento y ventas
- Agente WhatsApp con alcance acotado (cumple la política de Meta), memoria por atleta y escalamiento al doctor.
- Calificación de leads (alto/medio/bajo) y campañas de recuperación.
- Métrica objetivo: pasar de ~2 % a la meta que acordemos tras medir el embudo.
- Precio: $______ · Plazo: 4‑6 semanas.

### Mantenimiento mensual (opcional)
- Monitoreo, correcciones, soporte y mejoras. **Costos de API, servidor, plantillas y tokens a costo, transparentes.**
- Precio: $______ / mes.

## 3. Cómo reducimos su riesgo
- **Se paga por fase**, sin compromiso de continuar.
- **Todo queda a su nombre**: código, cuentas, llaves y documentación.
- El doctor aprueba lo que afecta la salud; la IA propone, no decide sola.
- Informes con evidencia, no solo demos.

## 4. Lo que necesitamos de ustedes
- Accesos de solo lectura a Airtable, Stripe, TrainingPeaks y servidor.
- Reunión técnica con los desarrolladores de Monterrey.
- Confirmar contrato y propiedad del código.
- Persona de contacto y disponibilidad del doctor para validar reglas.

## 5. Riesgos que declaramos de entrada
| Riesgo | Mitigación |
|---|---|
| API de TrainingPeaks cerrada | Fase 0 define ruta alterna; no se promete integración directa |
| El desarrollador original no coopera | Auditar con accesos propios; documentar antes de tocar |
| Resultados de salud de la IA | Reglas fijas + aprobación del doctor + escalamiento obligatorio |
| Meta cambia políticas de WhatsApp | Agente con alcance acotado y plantillas aprobadas |
| Costos de tokens crecen | Tope mensual y reporte de consumo |

## 6. Preguntas por resolver antes de enviar
- ¿Cuál es tu rol/empresa en la oferta (agencia, freelance, socio de Neurónomi)? Cambia el tono y el alcance.
- ¿Qué precios y horas puedes comprometer?
- ¿Quieres incluir mantenimiento desde el inicio o solo después de la Fase 1?
- ¿Se firma NDA? Emiliano pidió discreción.
