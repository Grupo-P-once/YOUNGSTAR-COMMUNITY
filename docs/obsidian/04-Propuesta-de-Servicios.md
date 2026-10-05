---
title: Propuesta de mantenimiento para Youngstar Community
tags: [youngstar, propuesta, mantenimiento, agencia]
estado: borrador v2
fecha: 2026-10-05
---

# Propuesta — Mantenimiento y operación de la plataforma Youngstar

> [!note] Borrador v2
> Cambio respecto a v1: la agencia entra como **equipo de mantenimiento** de un producto ya construido (no como desarrolladora desde cero). **Precios en blanco**: cotizar con horas reales y costos de API/servidor/tokens. Contexto en [[00-Resumen-Proyecto-Youngstar]].

## 1. Situación
- Producto ya desarrollado por un proveedor externo; Emiliano es dueño por contrato.
- El proveedor quiere subir mucho la mensualidad de mantenimiento; ellos quieren **migrar la administración** sin pagar de más.
- Síntomas a atender: datos inconsistentes (adherencia, duplicados), competencias canceladas que siguen en el plan, plan de triatlón incompleto, integración limitada con TrainingPeaks, seguimiento y ventas manuales.

## 2. Qué hacemos como agencia
**Tomamos la operación técnica del sistema actual**, lo estabilizamos y lo mejoramos poco a poco, con costos claros.

### Fase 0 — Onboarding y auditoría (pago único)
- Inventario de Airtable, formularios, Stripe, webhooks, APIs, cron, servidor y accesos.
- Mapa de datos: dónde se pierde o duplica información.
- Verificar **propiedad** de código, dominio, servidor y llaves; respaldos.
- **Transición ordenada** con el proveedor anterior (reunión técnica, entrega de documentación y accesos). No se cambia nada en producción hasta tener respaldo y plan.
- Opciones para TrainingPeaks con pros/contras/costo.
- **Entregable:** informe + diagrama + backlog priorizado. Es de ellos aunque no continúen.
- Precio: $______ · Plazo: 1‑2 semanas.

### Mantenimiento mensual (servicio principal)
Elegir plan:

| | Básico | Estándar | Plus |
|---|---|---|---|
| Monitoreo de flujos, pagos y sincronizaciones | ✔ | ✔ | ✔ |
| Alertas cuando algo falla | ✔ | ✔ | ✔ |
| Corrección de errores (bugs) | ✔ | ✔ | ✔ |
| Respuesta a incidentes | ___ h hábiles | ___ h | ___ h (incluye fines de semana) |
| Horas de mejoras incluidas al mes | — | ___ h | ___ h |
| Reporte mensual (incidentes, consumo, adherencia) | ✔ | ✔ | ✔ |
| Revisión de calidad de planes con el doctor | — | trimestral | mensual |
| Precio mensual | $____ | $____ | $____ |

**Costos variables a costo y a la vista** (sin margen oculto): tokens/IA, servidor, APIs, plantillas de WhatsApp. Con tope mensual acordado y aviso al 80 %.

### Mejoras por proyecto (se cotizan aparte, se aprueban una por una)
1. **Estabilizar datos:** ID único por atleta, escrituras idempotentes, fórmula de adherencia corregida.
2. **Competencias:** confirmación mensual por WhatsApp que actualiza el plan.
3. **Calidad de entrenamiento:** reglas fijas por deporte (bricks, técnica de natación, descargas) y panel del doctor con aprobación antes de publicar.
4. **Seguimiento y ventas:** agente de WhatsApp acotado, calificación de leads y campañas de recuperación.

## 3. Qué incluye y qué no
**Incluye:** monitoreo, correcciones, soporte técnico, respaldos, actualizaciones de dependencias, reportes.
**No incluye (se cotiza aparte):** funciones nuevas grandes, rediseños, migración de plataforma, soporte a deportistas finales, decisiones médicas.

## 4. Cómo reducimos su riesgo
- **Sin letra chica:** contrato mensual con salida a 30 días y entrega completa de documentación y accesos al terminar.
- **Todo a nombre de ellos:** cuentas, llaves y repositorio.
- **Cambios seguros:** respaldo antes de tocar producción, entorno de pruebas y registro de cambios.
- **Salud primero:** la IA propone, el doctor aprueba; escalamiento obligatorio ante síntomas.
- **Transparencia de costos:** consumo de IA y servidor reportado cada mes.

## 5. Lo que necesitamos de ellos
- Accesos de lectura (luego de administración) a Airtable, Stripe, TrainingPeaks, servidor y repositorio.
- Presentación con los desarrolladores de Monterrey y autorización escrita para recibir la documentación.
- Confirmación de la propiedad contractual del código y del servidor.
- Un contacto operativo y la disponibilidad del doctor para validar reglas.
- NDA firmado por ambas partes (Emiliano pidió discreción).

## 6. Riesgos declarados
| Riesgo | Mitigación |
|---|---|
| Código o documentación incompleta del proveedor anterior | Fase 0 lo cuantifica; el mantenimiento arranca solo tras la auditoría |
| El proveedor no coopera en la transición | Contrato de propiedad primero; auditar con accesos propios |
| API de TrainingPeaks cerrada | Se propone ruta alterna; no se promete integración directa |
| Cambios de política de WhatsApp | Agente acotado, plantillas aprobadas |
| Crecimiento del gasto en tokens | Tope mensual, alertas y reporte |

## 7. Pendiente antes de enviar
- [ ] Completar precios y horas por plan.
- [ ] Definir tiempos de respuesta (SLA) realistas con tu equipo.
- [ ] Redactar NDA y contrato de servicio.
- [ ] Verificar que no hay conflicto de intereses con los desarrolladores actuales.
- [ ] Revisar con el equipo si podrían asumir el stack real (se sabrá tras la Fase 0).
