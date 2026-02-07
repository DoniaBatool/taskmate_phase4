# Minikube Login Issue – Root Cause & Resolution

Future reference: kya issue aaya, kyun aaya, aur aakhir mein kaise resolve kiya.

---

## 1. Issue Summary

- **App:** Todo Chatbot on Minikube (Docker driver, Helm, port-forward).
- **Symptom:** Login pe "Not Found" / "Backend service unavailable: fetch failed" / "503 Service Unavailable".
- **Expected:** Login localhost ya todo.minikube.local pe kaam kare.

---

## 2. Root Causes (Learning)

### 2.1 NEXT_PUBLIC_* is build-time, not runtime

- Next.js **client bundle** mein `NEXT_PUBLIC_API_URL` **build time** pe inject hota hai.
- Runtime env (Helm `env` / container env) se client-side URL **change nahi hota**.
- Agar build ke waqt value set na ho to fallback (`/api/proxy`) use hota hai, jo Minikube setup pe backend tak nahi pahunchta.

**Learning:** Client-side API base URL ke liye either (a) build-time `ARG`/`ENV` in Dockerfile, ya (b) browser-only logic (e.g. `window.location.origin`) use karo.

### 2.2 Ingress Host header with port (todo.minikube.local:8080)

- Browser se `http://todo.minikube.local:8080` open karne pe **Host** header hota hai: `todo.minikube.local:8080`.
- Ingress rule sirf `host: todo.minikube.local` (bina port) match karta hai.
- Kubernetes Ingress **host** field mein port **allow nahi** karta.
- Isliye request catch-all pe bhi sahi se route nahi ho pa rahi thi / 404/503 aa rahe thay.

**Learning:** Port-forward se custom port (e.g. 8080) use karoge to Host header mein port aata hai; Ingress host matching isse handle nahi karta. Isliye **direct port-forward** (frontend + backend alag ports) zyada reliable.

### 2.3 Frontend image cache (Docker + Kubernetes)

- `docker build` **cache** ki wajah se purani layers use ho rahi thi; naya `api.ts` **image mein nahi ja raha tha**.
- `kubectl rollout restart` ke baad bhi pod **purani image** (same tag `latest`) use kar sakta hai jab tak nayi image explicitly load/rebuild na ho.

**Learning:** Frontend mein API URL / auth logic change ho to:
- Frontend build **cache break** karo: `docker build --no-cache ...` (ya equivalent).
- Build ke baad **image Minikube mein load** karo aur **frontend deployment restart** karo: `kubectl rollout restart deployment todo-app-frontend`.

### 2.4 Browser cache (purana JavaScript)

- Purana bundle (`API BASE_URL: /api/proxy`, `Fetching: /api/proxy/api/auth/login`) **browser cache** se serve ho raha tha.
- Naya code deploy karne ke baad bhi browser purana JS chala raha tha, isliye 503 / "fetch failed" / wrong URL dikh rahe thay.

**Learning:** Frontend deploy ke baad **browser cache clear** karo (Hard Reload, Clear site data, ya incognito) taake naya bundle load ho.

### 2.5 API URL path (/api/proxy vs backend /api)

- Fallback `/api/proxy` use hone pe full path ban raha tha: `/api/proxy/api/auth/login`.
- Ingress `/api` prefix backend ko bhejta hai; backend route **`/api/auth/login`** hai, **`/api/proxy/...`** nahi.
- Isliye backend pe 404 / Not Found aa raha tha.

**Learning:** Client-side base URL aur backend route prefix match hone chahiye; proxy path use karte waqt backend ko **prefix strip** karke bhejna padta hai, ya phir client ko seedha backend base use karna chahiye (e.g. same origin ya explicit backend URL).

---

## 3. How We Resolved It

### 3.1 Frontend: dynamic API base (same origin + localhost:3000 → 8000)

- **File:** `frontend/lib/api.ts`
- **Logic:** `getApiBaseUrl()`:
  - Agar `NEXT_PUBLIC_API_URL` set hai → woh use karo.
  - Agar browser mein **localhost:3000** pe ho → **`http://localhost:8000`** (direct backend).
  - Warna **`window.location.origin`** (same origin).
  - Server-side fallback: **`/api/proxy`**.
- **Fayda:** Minikube pe **direct port-forward** (frontend 3000, backend 8000) use karne pe login bina Ingress/Host issue ke kaam karta hai.

### 3.2 Direct port-forward (no Ingress for browser traffic)

- **Script:** `scripts/minikube-port-forward.sh`
- **Kaam:** Backend **8000**, frontend **3000** dono port-forward karta hai.
- **Use:** Browser **http://localhost:3000** kholo; API calls **http://localhost:8000** pe jati hain (frontend logic se).
- **Fayda:** Host header / Ingress port issue khatam; CORS backend pe `*` se allow.

### 3.3 Deploy script: host Docker build + Minikube load

- **File:** `scripts/deploy-minikube.sh`
- **Change:** Build **host** Docker pe (working DNS), phir **`minikube image load`** (Minikube ke andar build pe "no such host" aa raha tha).
- **Frontend:** `docker build --no-cache` taake API URL wala naya code **har bar** image mein aaye.

### 3.4 Ingress: catch-all rule (optional, for todo.minikube.local:8080)

- **File:** `helm/todo-app/templates/ingress.yaml`
- **Change:** Host **na** hone wala ek rule add kiya (catch-all) taake `Host: todo.minikube.local:8080` jaisi requests bhi route hon.
- **Note:** Final working flow **direct port-forward** pe hai; Ingress option B ki tarah document hai.

### 3.5 Clear deployment + cache flow

- **Deploy:** `./scripts/deploy-minikube.sh` (frontend `--no-cache` build, images load, Helm upgrade).
- **Restart frontend:** `kubectl rollout restart deployment todo-app-frontend` taake nayi image use ho.
- **Browser:** Localhost:3000 ke liye site data / cache clear, phir **http://localhost:3000** open karke login.

---

## 4. Final Working Flow (Reference)

```text
1. Minikube start:     ./scripts/minikube-setup.sh
2. Deploy app:         ./scripts/deploy-minikube.sh
3. Port-forward:       ./scripts/minikube-port-forward.sh   (chalti rehne do)
4. Browser:            http://localhost:3000
5. Login:              Same page pe login — kaam karega.
```

**Agar frontend code (e.g. api.ts) change ho:**

- `./scripts/deploy-minikube.sh` (no-cache frontend build)
- `kubectl rollout restart deployment todo-app-frontend`
- Browser: cache clear / hard refresh, phir http://localhost:3000

---

## 5. Files Touched (Summary)

| File | Change |
|------|--------|
| `frontend/lib/api.ts` | `getApiBaseUrl()`: env → localhost:3000→8000 → same origin → /api/proxy |
| `scripts/minikube-port-forward.sh` | New: port-forward backend 8000, frontend 3000 |
| `scripts/deploy-minikube.sh` | Host Docker build, `minikube image load`; frontend `--no-cache` |
| `helm/todo-app/templates/ingress.yaml` | Catch-all rule (no host) for Host-with-port |
| `helm/todo-app/values-minikube.yaml` | `NEXT_PUBLIC_API_URL` for Minikube (optional with direct port-forward) |
| `specs/phase-4-local-kubernetes/RUN-MINIKUBE.md` | Option A: direct port-forward; Option B: ingress :8080; troubleshooting |

---

## 6. One-Line Takeaway

**Minikube + Docker driver pe login theek karne ke liye:** Frontend ko **localhost:3000 pe hone par API ke liye http://localhost:8000** use karne do, aur app access **direct port-forward** (frontend 3000, backend 8000) se karo; deploy ke baad frontend restart + browser cache clear karo.
