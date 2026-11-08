# Two Mock API Connectors

**Public synthetic educational demo; not a production client service.**

HMAC demonstration and synthetic inventory/CRM adapters.

## Run offline

```bash
python demo.py
python -m unittest discover -s tests -v
```

Expected output: one JSON line with synthetic data only. See `sample_output.json`.

## Verified and not verified

- Implemented: bounded local demonstration of the described behavior.
- Tested: Python `unittest` test cases in this folder.
- Mocked: all tenants, calls, APIs, provider decisions and identifiers are fabricated.
- Client customization required: yes; identity, data model, APIs, security settings and tests.
- Security and license review required: yes; this project cannot be deployed as-is.
- **Production approved: NO**. No live client data, credentials, payments or messages.
