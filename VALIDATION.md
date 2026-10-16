# Physical validation — 2026-10-16

Hardware: ideaspark ESP-WROOM-32 display board, ESP32-D0WD, 4 MiB flash, 170×320 ST7789 panel.

## Result

| Check | Observed result |
|---|---|
| Firmware identity | `MSA-WiFi-Sentinel-0.1` |
| Passive flag | `true` |
| Wi-Fi association | `false` |
| Injection enabled | `false` |
| Channel hopping | channels 1–13 observed |
| AP cache | 9 APs during the test window |
| Parser health | 0 malformed, 0 dropped after 1,800+ frames |
| Pause | frame count stayed at 622 for 2 seconds |
| Resume | count advanced from 622 to 648 in 3 seconds |
| Display | all five real framebuffers captured |
| Heap | about 87 KiB free during monitoring |

No deauthentication or disassociation frame happened to be observed in this short local test. The alert counter therefore remained at zero; no traffic was generated to force it.

Identifiers in public screenshots are deliberately redacted. The private validation captures are excluded by `.gitignore`.
