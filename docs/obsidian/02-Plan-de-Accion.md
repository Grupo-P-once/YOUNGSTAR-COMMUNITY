---
title: Plan de acción propuesto
tags: [youngstar, plan]
fecha: 2026-10-05
---

# Plan de acción (borrador)

## Fase 0 — Auditoría (1‑2 semanas)
- [ ] Inventario de flujos: formularios, Airtable (bases/tablas/campos), webhooks, APIs, cron, servidor, credenciales.
- [ ] Diagrama de datos extremo a extremo y puntos de pérdida/duplicado.
- [ ] Confirmar contractualmente la **propiedad** de código, dominio, servidor y llaves.
- [ ] Reunión técnica con los desarrolladores de Monterrey.

## Fase 1 — Estabilizar datos
- [ ] ID único por atleta (email/teléfono normalizado) e **idempotencia** en cada escritura.
- [ ] Fuente única de verdad (Airtable o Postgres/Supabase) y logs de cada sincronización.
- [ ] Corregir métrica de **adherencia** (definir fórmula y fuente).
- [ ] Confirmación mensual de competencias por WhatsApp (plantilla) → actualiza plan.

## Fase 2 — Calidad del entrenamiento
- [ ] Reglas por deporte (bricks, técnica de natación, descargas) fuera del LLM.
- [ ] Validación del doctor antes de publicar; panel del doctor con expedientes.
- [ ] Indicadores en español con interpretación.
- [ ] Decidir vía TrainingPeaks: solicitar API de socio vs. exportación de archivos vs. migrar a plataforma abierta.

## Fase 3 — Agente de seguimiento y ventas
- [ ] Agente WhatsApp con alcance acotado (cumple política Meta), memoria por atleta, escalamiento a doctor.
- [ ] Scoring de leads alto/medio/bajo, campañas de recuperación.

## Fase 4 — Costos / propuesta
- [ ] Comparar: mantener proveedor vs. Neurónomi vs. equipo propio. Costos: servidor, tokens, APIs, plantillas WhatsApp.

## Preguntas abiertas
1. ¿Cómo se llama exactamente la comunidad? (la transcripción dice "jonster", probablemente "Youngstar").
2. ¿Qué hay realmente en este repositorio? Está **vacío** (sin commits).
3. ¿Quieres que construya algo concreto aquí (dashboard, panel del doctor, flujo n8n, propuesta formal)?
