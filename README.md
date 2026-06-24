# Conversion Funnel ETL

Transform raw user event logs into structured session-level datasets for **conversion funnel analysis** and digital product download trends.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-ETL-150458?style=flat-square&logo=pandas&logoColor=white)

---

## Architecture

```
┌──────────────────┐     classify      ┌─────────────────────┐
│ Raw event logs   │ ────────────────► │  Device / route     │
│ (CSV / parquet)  │     aggregate     │  classification     │
└────────┬─────────┘                   └──────────┬──────────┘
         │                                          │
         └──────────────────┬───────────────────────┘
                            ▼
                 ┌─────────────────────┐
                 │  Session dataset    │
                 │  (one row / user)   │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │  Rolling-avg plots  │
                 │  by product/cookie  │
                 └─────────────────────┘
```

---

## Quick start (employers — no API keys)

```bash
pip install -r requirements.txt
python etl.py
```

Output chart saved to `output/download_trends.png`.

---

## Input schema

| Column | Description |
|--------|-------------|
| `timestamp` | Event time |
| `log_type` | e.g. `download`, `view` |
| `cookie_id` | Session / CloudID |
| `sub_product_code` | Product code (`AUD01`, `VID01`, …) |
| `route` | User route path |

Extend `build_download_trends()` for your production event pipeline.

---

## License

MIT — see [LICENSE](LICENSE).
