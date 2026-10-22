# MSA-WiFi-Sentinel · Estado técnico

**Revisión:** 2026-10-22 · **Categoría:** firmware/hardware experimental

- Estado: Observador pasivo Wi-Fi 2,4 GHz en ESP32 con pruebas físicas descritas.
- Licencia principal: archivo LICENSE, más avisos de dependencias en licenses/ cuando procede.
- Workflow existente: [.github/workflows/ci.yml](../.github/workflows/ci.yml). Su mera presencia no acredita validación de hardware nuevo.
- Capturas disponibles: [`docs/screenshots/contact-sheet.png`](../docs/screenshots/contact-sheet.png), [`docs/screenshots/alerts.png`](../docs/screenshots/alerts.png), [`docs/screenshots/evidence.png`](../docs/screenshots/evidence.png). Procedencia: framebuffer indicada por README.

## Riesgos / límites

Muestreo limitado por salto de canal; una alerta observada no acredita un ataque.

No probar sobre redes o dispositivos de terceros sin autorización. Registrar modelo de hardware, compilador, librerías, firmware exacto y logs anonimizados en cada validación. Ninguna alerta o lectura aislada demuestra intrusión ni ubicación física.
