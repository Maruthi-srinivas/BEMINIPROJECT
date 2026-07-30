# BE Mini Lab Frontend

Interactive console for all ten backend mini-services.

## Setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open `http://localhost:5173`. Start each backend with its own Compose stack when you
want that console to be online (ports `8001`–`8010`).

## Notes

- Service base URLs are configured via `VITE_*_URL` in `.env`.
- Backends allow CORS from `http://localhost:5173` by default (`CORS_ORIGINS`).
- Health badges poll `/health` every few seconds.
