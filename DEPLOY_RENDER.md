# Deploy ABET CO–SO Mapper on Render

## What you get
A public HTTPS web interface and FastAPI endpoints. The system is **faculty-reviewed, rule-based**: it does not auto-generate PI selections and does not calculate attainment.

## Before deployment
- You need a GitHub account and a Render account. A hosted URL cannot be created by downloading this ZIP alone.
- **Important:** This starter app has **no authentication or server-side database**. Do **not** enter confidential student data or sensitive institutional information. The public URL is accessible to anyone who knows it. Mapping work is held in the browser and can be downloaded as JSON.
- The Render free tier, if offered to your account, may spin down when idle and can have changing limits. Review current Render pricing and terms.

## Steps (no Python installation required)
1. Extract `co_so_mapper_render.zip` on your Mac.
2. Sign in to [github.com](https://github.com) and create a new repository, e.g. `abet-co-so-mapper`. For an institutional project, choose **Private** if your Render/GitHub connection supports it.
3. On the new repository page, select **Add file → Upload files**. Upload the **contents** of the extracted `co_so_mapper_render` folder, **not** the containing folder. Include `main.py`, `engine.py`, `requirements.txt`, `render.yaml`, `.python-version`, `static/index.html`, and this guide. GitHub's browser uploader may hide dotfiles; `.python-version` is optional because Render can choose a compatible Python version, but including it is preferred. Alternatively use GitHub Desktop to upload all files.
4. Sign in to [dashboard.render.com](https://dashboard.render.com) and connect your GitHub account, granting access to this repository.
5. Select **New → Blueprint**, choose the repository and branch, and apply the configuration from `render.yaml`. Review the service plan before confirming; the sample requests `free` and may need to be changed to an available plan.
6. Wait for the deploy status to show **Live**. Render provides an HTTPS address such as `https://abet-co-so-mapper-xxxx.onrender.com` (example only; your actual address is shown in the dashboard).
7. Open the URL in Safari. Choose **Load Computer Networks example** and select PIs to generate the CAC/EAC matrix. Check `https://YOUR-RENDER-URL/health` for `{"status":"ok"}` and `/docs` for API documentation.
8. To update the application, upload/commit changes to the same GitHub repository. Render will deploy updates according to its configuration.

## If you prefer manual Render setup
- New → Web Service → Connect repository
- Language/runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Health check: `/health`
- Root directory: blank, provided `main.py` is at repository root.

## Troubleshooting
- **404 / module import error**: confirm `main.py`, `engine.py`, and `static/` are at repository root, not nested one folder too deep.
- **Deploy fails at dependencies**: check Render build logs and the configured Python version.
- **Application does not load**: check Render deploy status and runtime logs; `/health` should return JSON.
- **First visit slow**: free instances can sleep and need time to start.
- **Blank matrix**: this is expected until you select PIs. The sample does not prepopulate claims.

## API endpoints
- `GET /health`
- `GET /api/frameworks`
- `POST /api/map`
- `POST /api/export/csv`
- `GET /docs`

## Production roadmap
Before rollout to multiple faculty, add institutional sign-in, authorization, persistent storage, approval workflow, backups, and audit logs. Do not treat browser-only saved data as a shared database.
