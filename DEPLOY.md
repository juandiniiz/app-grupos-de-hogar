# Deploy Instructions

## Backend (Render.com)
1. Go to render.com → New → Web Service
2. Connect GitHub repo: juandiniiz/app-grupos-de-hogar
3. Name: grupos-de-hogar-api
4. Root Directory: backend
5. Build Command: pip install -r requirements.txt
6. Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
7. Select free plan → Create Web Service
8. Wait for deploy → copy the URL (e.g. https://grupos-de-hogar-api.onrender.com)

## Frontend (Vercel)
1. Go to vercel.com → New Project
2. Import GitHub repo: juandiniiz/app-grupos-de-hogar
3. Framework: Vite
4. Root Directory: frontend
5. Add Environment Variable: VITE_API_URL = https://YOUR-RENDER-URL.onrender.com/api
6. Deploy
7. Share the Vercel URL

## Default credentials after deploy
- admin@puntodeencuentro.es / admin1234
- carlos.mendez@ccln.es / super1234
- lucia.torres@ccln.es / resp1234
- miguel.santos@ccln.es / ayud1234

Note: Render free tier sleeps after 15 min inactivity. First request may take ~30 seconds to wake up.
