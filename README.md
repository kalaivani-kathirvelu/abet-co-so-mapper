# ABET Initial CO–SO Mapping Web App + API

Faculty-reviewed curriculum mapping for ABET CAC and EAC. Calculates PI coverage, 3/2/0 correlation and nonzero averages; **not** an attainment calculator.

**Cloud deployment:** See [DEPLOY_RENDER.md](DEPLOY_RENDER.md). No local Python required when deploying through GitHub + Render.

**Local development (optional):** `pip install -r requirements.txt` then `uvicorn main:app --reload`.

**API:** `/docs` · `/api/frameworks` · `/api/map` · `/api/export/csv` · `/health`.

**Security:** No authentication or database. Do not use for confidential data. Production institutional use requires access control and persistent storage.
