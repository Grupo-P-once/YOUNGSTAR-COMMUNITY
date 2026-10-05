---
title: Investigación externa
tags: [youngstar, investigacion]
fecha: 2026-10-05
---

# Investigación externa (búsqueda web)

> [!warning] Limitación
> Las búsquedas devolvieron sobre todo blogs/documentación; **no se encontraron hilos de Reddit o foros** relevantes ni redes sociales de la comunidad. No se afirma nada que no esté en las fuentes.

## TrainingPeaks y su API
- API **solo para socios aprobados**, no para uso personal; respuesta en 7‑10 días y, según su página, **no aceptaba nuevos socios** por mantenimiento. → Explica por qué el proveedor no puede conectar directo ("ellos están cerrados").
  - [Update on TrainingPeaks Partner API](https://www.trainingpeaks.com/blog/an-update-on-trainingpeaks-partner-api/) · [Solicitar acceso](https://api.trainingpeaks.com/request-access)
- TrainingPeaks no está disponible como integración estándar en Zapier/Make.
- WHOOP → TrainingPeaks es **unidireccional** (sueño, HRV, FC reposo, recovery).
  - [WHOOP: integración TrainingPeaks](https://support.whoop.com/s/article/TrainingPeaks-Integration?language=en_US)
- Existen productos de entrenador IA que ya sincronizan planes con TrainingPeaks (AI Endurance, athletedata, TrainBetter.Coach) → prueba de que el flujo es viable, y a la vez competencia.
  - [AI Endurance](https://aiendurance.com/blog/get-your-best-trainingpeaks-plan) · [athletedata](https://www.athletedata.health/integrations/trainingpeaks) · [TrainBetter.Coach](https://trainbetter.coach/)
- Importar planes a TrainingPeaks vía CSV/archivos es una vía alternativa a la API: [guía](https://trainingdojo.app/blog/import-training-plan-to-trainingpeaks)
- Alternativas con ecosistema más abierto: Intervals.icu, Final Surge, The Next Race: [comparativa](https://athlin.app/en/blog/trainingpeaks-alternatives)

## IA para planes de triatlón (riesgos)
- Los LLM genéricos fallan en reglas de dominio: apilar días duros entre deportes, no ver técnica, no detectar señales de lesión; riesgo de alucinación en salud.
  - [Why AI Training Plans Fail Runners and Triathletes](https://thirdcoasttraining.com/why-ai-training-plans-fails-runners-and-triathletes/) · [GPTCoach (ACM)](https://dl.acm.org/doi/10.1145/3706598.3713819) · [LLM como coach, media maratón](https://arxiv.org/html/2509.26593v1)
- Implicación: poner **reglas determinísticas** (bricks, descargas, límites de carga) y **revisión del doctor** antes de publicar.

## WhatsApp / agentes IA
- Meta prohíbe en la API de WhatsApp Business los **chatbots de propósito general** desde 15‑ene‑2026; los bots **estructurados** (soporte, citas, notificaciones, ventas) siguen permitidos. Un agente de atletas con alcance acotado cumple.
  - [respond.io](https://respond.io/blog/whatsapp-general-purpose-chatbots-ban) · [TechCrunch](https://techcrunch.com/2025/12/04/eu-investigating-meta-over-policy-change-that-bans-rival-ai-chatbots-from-whatsapp/)
- Fuera de la ventana de 24 h solo se pueden enviar **plantillas aprobadas** (relevante para el recordatorio mensual de competencias).
- Click‑to‑WhatsApp ads + seguimiento automatizado es la práctica común para leads fitness: [Wati](https://www.wati.io/en/blog/whatsapp-api-for-fitness-centers/)

## Airtable / n8n / Stripe
- El trigger de Airtable en n8n es por **polling** (minutos); tiempo real requiere webhooks/scripts. Esto puede explicar datos desfasados.
  - [n8n + Airtable](https://www.eesel.ai/blog/airtable-integrations-with-n8n)
- Existen plantillas para detección de duplicados de clientes Stripe↔Airtable: [n8n](https://n8n.io/integrations/airtable/and/stripe/)
- Stripe en México soporta tarjeta, OXXO y SPEI; domiciliación SPEI tiene soporte limitado: [Stripe OXXO](https://stripe.com/payment-method/oxxo) · [pasarelas para gimnasios](https://connectgyms.com/blog/pasarela-pagos-gimnasio-mexico-spei-oxxo)
