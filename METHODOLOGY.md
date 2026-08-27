# Methodology

## What is the HIV Care Cascade?

A framework tracking people living with HIV through sequential stages of care:
**Tested → Diagnosed Positive → Linked to Treatment → Retained in Treatment → Virally Suppressed**

Each stage naturally loses people relative to the one before it — the gaps between stages are where public health intervention is most needed. This mirrors UNAIDS' internationally recognized 95-95-95 framework.

## Indicator Mapping

| PEPFAR Indicator | Cascade Stage | Definition |
|---|---|---|
| HTS_TST | 1. Tested | People who received HIV testing services and results |
| HTS_TST_POS | 2. Diagnosed Positive | Of those tested, how many tested positive |
| TX_NEW | 3. Linked to Treatment | People newly started on antiretroviral therapy (ART) |
| TX_CURR | 4. Retained (snapshot) | People currently receiving ART as of the most recent period |
| TX_PVLS (N/D) | 5. Virally Suppressed | Numerator (suppressed) ÷ Denominator (tested) × 100 |

Supplementary, non-cascade indicators also present in the dataset: `HTS_SELF` (self-test kits distributed), `TX_NET_NEW` (period-over-period change in TX_CURR).

## Viral Suppression Rate Calculation

PEPFAR reports TX_PVLS as separate Numerator (N) and Denominator (D) rows per Year/Quarter/Sex/Age group. This project pivots N and D onto the same row and calculates:

```
Suppression Rate = (N / D) × 100
```

## Data Time Range

- **Full range:** 2016–2025
- **Reliable analysis window:** 2018–2024 (consistent reporting density)
- **2016–2017:** Thin reporting, fewer than 20 data points per quarter — interpret with caution
- **2025:** Q4 results only, per PEPFAR's own data release notes

## Age Band Handling

See [`DATA_QUALITY_LOG.md`](DATA_QUALITY_LOG.md) item 4. All age-based analysis uses the **Narrow** age family exclusively (`<01, 1-4, 5-9, 10-14, 15-19, 20-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-54, 55-59, 60-64, 65+`) to avoid double-counting.

## Known Limitations

- Retention is proxied via TX_CURR/TX_NET_NEW, not directly reported (TX_RET deprecated — see log item 6)
- Low-N groups (particularly "Missing Sex" and pediatric age bands) can show volatile suppression percentages; sample size context should accompany any headline claim about these groups
- Causal claims (e.g., "program improvement" vs. "changing tested population") cannot be fully distinguished using aggregate MER data alone
