# Minikube pe app kaise chalayein (step-by-step)

Variables `docker/.env` mein set ho chuke hain. Ab ye steps follow karo.

---

## Step 0: Minikube install (sirf ek baar)

Agar `minikube: command not found` aaye to pehle Minikube install karo. **Homebrew** se (Docker Desktop pehle se chalu hona chahiye):

```bash
brew install minikube
brew install kubectl
```

Verify:

```bash
minikube version
kubectl version --client
```

---

## Step 1: Minikube start karo

Project **root** se (jahan `package.json` / `backend` / `frontend` folders hain):

```bash
cd /Users/apple/Documents/Projects/todo_phase4
./scripts/minikube-setup.sh
```

Ye Minikube cluster start karega (thoda time lag sakta hai pehli baar). Script 6GB memory use karta hai taake Docker Desktop (jo ~7.8GB deta hai) ke andar chal jaye. Agar `memory` error aaye to Docker Desktop → Settings → Resources mein memory badha sakte ho, ya script mein `--memory=6144` ko kam karke `--memory=4096` try karo. Jab `Minikube ready` dikhe, aage badho.

---

## Step 2: Deploy karo (images build + Helm install)

Same project root se:

```bash
./scripts/deploy-minikube.sh
```

Ye script:
- `docker/.env` se `DATABASE_URL`, `BETTER_AUTH_SECRET`, `OPENAI_API_KEY` load karega
- Backend aur frontend images build karega (Minikube ke andar)
- Helm se app deploy karega

Deploy khatam hone ke baad script kuch aise lines print karega:

```
Add to /etc/hosts: 192.168.49.2 todo.minikube.local
Then open: http://todo.minikube.local:30475 (NodePort; port 30475 zaroori hai jab tunnel na chala ho.)
```

(IP alag ho sakta hai, tumhare output wali value use karo.)

---

## Step 3: `/etc/hosts` mein line add karo – ye kya hai?

**Simple matlab:**  
Browser jab `http://todo.minikube.local` open karega to computer ko pata hona chahiye ke "todo.minikube.local" = Minikube ka IP. Ye mapping **`/etc/hosts`** file mein hoti hai.

**Kya karna hai:**  
Script ne jo line di hai (jaise `192.168.49.2 todo.minikube.local`), woh **ek line** `/etc/hosts` file ke end mein add karni hai.

**Mac pe kaise:**

1. Terminal kholo.
2. Ye command chalao (apna IP script output se lo; example: `192.168.49.2`):

   ```bash
   echo "192.168.49.2 todo.minikube.local" | sudo tee -a /etc/hosts
   ```

   Jab password puche to apna Mac login password do.

   **Ya** file hand-se edit karo:

   ```bash
   sudo nano /etc/hosts
   ```

   Last line pe jao, new line pe likho: `192.168.49.2 todo.minikube.local` (script wali exact line). Save: Ctrl+O, Enter, phir Ctrl+X.

3. Check karo:

   ```bash
   grep todo.minikube.local /etc/hosts
   ```

   Output mein `192.168.49.2 todo.minikube.local` (ya jo IP script ne di) dikhna chahiye.

---

## Step 4: Browser se app kholo

Browser mein ye URL kholo:

**http://todo.minikube.local:30475** (NodePort; agar tunnel use karo to sirf http://todo.minikube.local bhi chal sakta hai.)

- **Login:** Sign in / sign up karo (Better Auth).
- **Tasks:** Tasks page se create/list/update/delete/complete karo.
- **AI chat:** Chat kholo, likho "Add a task to buy milk" — chatbot kaam karega (MCP tools).

Agar page nahi khulta ya **connection timeout** aaye (Docker driver pe 192.168.49.2 reach nahi hota):

**Option: Port-forward + 127.0.0.1**

1. **Ingress ko localhost pe forward karo** (ye terminal **chalti rehne do**):
   ```bash
   kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80
   ```
2. **/etc/hosts** mein `todo.minikube.local` ko **127.0.0.1** se map karo. Pehle purani line hatao, phir:
   ```bash
   sudo sed -i '' '/todo.minikube.local/d' /etc/hosts
   echo "127.0.0.1 todo.minikube.local" | sudo tee -a /etc/hosts
   ```
3. Browser mein kholo: **http://todo.minikube.local:8080**

Port-forward wala terminal band mat karna; jab kaam khatam ho to Ctrl+C.

---

## Har baar app chalane ke liye (quick)

### Option A: Direct port-forward (login guaranteed — recommended)

**/etc/hosts ki zaroorat nahi.** Sirf ye script chalao (aur **chalti rehne do**):

```bash
./scripts/minikube-port-forward.sh
```

Phir browser mein kholo: **http://localhost:3000** (login bhi yahi kaam karega).

Band karne ke liye: Ctrl+C.

**Agar "Backend service unavailable: fetch failed" aaye:** nayi terminal mein ye chalao (jab port-forward script chal rahi ho): `curl -s http://localhost:8000/health`. Agar response aaye to backend reachable hai — browser cache clear karke dobara try karo. Agar curl bhi fail ho to port 8000 pe koi aur app toh nahi (e.g. local backend)? Script band karo (Ctrl+C), phir dobara `./scripts/minikube-port-forward.sh` chalao.

---

### Option B: Ingress port-forward (todo.minikube.local:8080)

1. **Terminal** mein ye chalao (aur **chalti rehne do**):
   ```bash
   kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80
   ```
2. **/etc/hosts** mein: `127.0.0.1 todo.minikube.local`
3. **Browser:** **http://todo.minikube.local:8080** ya **http://todo.minikube.local:8080/login**

(Pehle Option A try karo agar login pe "Not Found" aaye.)

---

**Pehli baar ya cluster band karne ke baad:** pehle `./scripts/minikube-setup.sh`, phir `./scripts/deploy-minikube.sh`, phir upar wala port-forward (A ya B).

---

Agar sirf "page nahi khulta" ho (timeout nahi):
- Check: `kubectl get pods` — dono pods `Running` hon.
- Check: `/etc/hosts` mein line sahi add hui hai (correct IP).

---

## Short summary

| Step | Command / Action |
|------|------------------|
| 1 | `./scripts/minikube-setup.sh` |
| 2 | `./scripts/deploy-minikube.sh` (docker/.env se vars load honge) |
| 3 | `/etc/hosts`: `127.0.0.1 todo.minikube.local` (port-forward use karte ho to) |
| 4 | Terminal: `kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80` (chalti rehne do) |
| 5 | Browser: **http://todo.minikube.local:8080** (ya :8080/login) |

**Project root** = `cd /Users/apple/Documents/Projects/todo_phase4` — yahi se dono scripts chalao.
