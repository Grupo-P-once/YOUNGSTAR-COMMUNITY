---
title: Resumen del proyecto Youngstar Community
tags: [youngstar, proyecto, ia, entrenamiento, trainingpeaks, airtable]
fuente: transcripción de reunión EMILIANO PEREZANDI (audio + txt)
fecha: 2026-10-05
---

# Youngstar Community — visión general

> [!info] Fuente
> Transcripción completa de la reunión entre **Emiliano (fundador de la comunidad deportiva)** y **Neurónomi/Neuronomy** (agencia de agentes IA, 2 egresados de Inteligencia de Negocios). Hablante 1 = Emiliano, Hablantes 2 y 3 = Neurónomi.
> El audio original no está en el contenedor cloud; se trabajó con el `.txt` (UTF‑16, convertido a UTF‑8).

## 1. Qué es el negocio
- Comunidad deportiva de resistencia (running, triatlón, natación, ciclismo), **6 años**, de las más grandes de México/LatAm.
- **127 atletas activos**, cobro con **pagos domiciliados**.
- Equipo: Emiliano, su hermano, **Dr. Dapo (director deportivo/médico)** y Eduardo. Quieren **delegar la operación** y que el sistema sea ~100 % autónomo, dirigido por el doctor.
- Planes por tipo: running (el que mejor funciona), triatlón (el más flojo), natación.

## 2. Arquitectura actual (según el audio)
```
Formulario inicial del atleta ──► Airtable (BD central + dashboard financiero)
Sancho (plataforma anterior) ──► migrado a Airtable
Stripe ──► cobros domiciliados + agente de soporte de pagos (mensaje autónomo)
Airtable ──► Dashboard propio (127 atletas, planes activos / por revisar / por generar)
Dashboard IA ──► genera planes de 4 semanas (2 visibles, 2 ocultas)
              ──► TrainingPeaks (API cerrada; conexión indirecta)
              ──► métricas WHOOP (strain, sueño, FC, HRV, recovery)
```
- Desarrollado por un proveedor en **Monterrey**; Emiliano es **dueño** del servidor/dominio/código por contrato.
- Producto "semi‑terminado": falta el producto final y la parte de ventas.

## 3. Problemas detectados
| # | Problema | Causa probable |
|---|----------|----------------|
| 1 | Métricas de adherencia incorrectas (dashboard dice 100 %, TrainingPeaks 55 %) | Datos cruzados/desactualizados entre canales; API de TrainingPeaks cerrada |
| 2 | Datos duplicados / repetidos en tablas | Cadena larga de sincronización (Formulario → Airtable → IA → TrainingPeaks), sin clave única ni idempotencia |
| 3 | Competencias canceladas siguen alimentando el plan (ciclos de volumen para carreras que ya no harán) | Airtable solo se alimenta del formulario inicial; no hay confirmación periódica |
| 4 | Plan de **triatlón** mal construido: no programa **bricks** (bici→correr) ni técnica de natación | El generador no tiene reglas de dominio por deporte |
| 5 | Indicadores en inglés / gráficas crudas (ej. 76 ppm vs 142) | Falta traducción y capa de interpretación para el atleta |
| 6 | IA y doctor pueden dar indicaciones contradictorias | No existe expediente médico central que ambos lean |
| 7 | El bot de Instagram "se nota que es un chatbot" → leads mueren | Falta tono humano/memoria por usuario |
| 8 | Embudo: de 100 leads solo ~2 cierran; las ventas reales las hace Emiliano "por fuera" | No hay segmentación ni agentes de venta/seguimiento |
| 9 | Proveedor quiere subir fuerte la mensualidad de mantenimiento (antes era mínima) | Dependencia total del desarrollador original |
| 10 | Flujo con "muchos canales" donde "todo se descompone" | Sin observabilidad de webhooks/APIs |

## 4. Qué quieren lograr
1. Terminar el producto final y que sea **estable** y barato de mantener.
2. **Seguimiento autónomo por WhatsApp** a atletas: detectar molestias/enfermedad, ajustar el plan, escalar al doctor cuando proceda.
3. **Recordatorios de competencias** (1 mes antes: ¿sigues inscrito?) y reajuste automático del plan.
4. **Panel del doctor** con expedientes de atletas, para que la IA use la misma información.
5. **Sales funnel automatizado**: agentes de venta y administración; scoring de leads (alto/medio/bajo), campañas de recuperación.
6. Migrar la administración a otro equipo sin costos excesivos.

## 5. Lo que ofreció Neurónomi
- Agentes con **memoria por usuario**, autoaprendizaje nocturno, escalamiento a humano por intención (facturación, soporte, venta empresarial), CRM en vivo conectado a Meta (IG/WhatsApp) por webhooks, orquestación en **n8n**.
- Primero **auditar**: mapear APIs, webhooks, canales y dónde se pierde o distorsiona la información; luego reunión con los programadores.
- Precios mencionados (agencia): ~$13,099 MXN mensual en un caso; costos aparte de API, plantillas, servidor y tokens. Emiliano pidió **propuesta formal**.
- Pidió **discreción** (NDA informal).

## 6. Investigación externa (panorama)
Ver [[01-Investigacion-Externa]].

## 7. Siguientes pasos sugeridos
Ver [[02-Plan-de-Accion]].
