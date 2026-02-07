# 002-helm-charts – Verification Guide

Feature implement hone ke baad ye checks karo ke sab theek hai.

---

## 1. Bina Helm ke check (files + content)

### 1.1 Chart files maujood hon

Terminal mein ye chalao (project root se):

```bash
cd /Users/apple/Documents/Projects/todo_phase4

# Chart root
test -f helm/todo-app/Chart.yaml && echo "OK Chart.yaml" || echo "MISSING Chart.yaml"
test -f helm/todo-app/values.yaml && echo "OK values.yaml" || echo "MISSING values.yaml"
test -f helm/todo-app/values-minikube.yaml && echo "OK values-minikube.yaml" || echo "MISSING values-minikube.yaml"

# Templates
for f in _helpers.tpl backend-deployment.yaml backend-service.yaml frontend-deployment.yaml frontend-service.yaml configmap.yaml secret.yaml ingress.yaml; do
  test -f helm/todo-app/templates/$f && echo "OK $f" || echo "MISSING $f"
done
```

Sab lines par **OK** aana chahiye.

### 1.2 Important content check

- **Backend probes:**  
  `grep -l "/health" helm/todo-app/templates/backend-deployment.yaml` aur  
  `grep -l "/ready" helm/todo-app/templates/backend-deployment.yaml`  
  dono file ko point karen (same file).

- **Frontend probe:**  
  `grep "/api/health" helm/todo-app/templates/frontend-deployment.yaml`  
  Isme `/api/health` dikhna chahiye.

- **Ingress paths:**  
  `grep -E "path: /api|path: /" helm/todo-app/templates/ingress.yaml`  
  `/api` aur `/` dono paths dikhne chahiye.

- **Secret (no real secrets in repo):**  
  `grep "b64enc" helm/todo-app/templates/secret.yaml`  
  Secret template values se bana hai, repo mein plain secret nahi hona chahiye.

---

## 2. Helm se check (jab Helm install ho)

### 2.1 Helm install

**macOS (Homebrew):**
```bash
brew install helm
```
*(Latest = Helm 4; already on PATH. Sirf Helm 3 chahiye ho to `brew install helm@3` karo, phir PATH mein `/opt/homebrew/opt/helm@3/bin` add karna padega.)*

**Verify install:**
```bash
helm version
```

**Other OS / scripts:** https://helm.sh/docs/intro/install/

### 2.2 Lint (syntax + best practices)

```bash
cd /Users/apple/Documents/Projects/todo_phase4

helm lint helm/todo-app
```

Expected: `1 chart(s) linted, 0 chart(s) failed`

### 2.3 Template (default values)

```bash
helm template todo-app helm/todo-app
```

- Koi error nahi aana chahiye.
- Output mein ye resources hon:  
  Deployment (backend, frontend), Service (backend, frontend), ConfigMap, Secret, Ingress.

### 2.4 Template (Minikube values)

```bash
helm template todo-app helm/todo-app -f helm/todo-app/values-minikube.yaml
```

- Ingress ka `host` `todo.minikube.local` hona chahiye.
- Frontend env mein `NEXT_PUBLIC_API_URL` set hona chahiye.

### 2.5 Dry-run install (cluster bina bhi chal sakta hai)

```bash
helm install todo-app helm/todo-app -f helm/todo-app/values-minikube.yaml --dry-run --debug 2>&1 | head -100
```

- Syntax error nahi aani chahiye.
- Real install ke liye pehle Minikube + images ready hon (003-minikube-deployment).

---

## 3. README check

- Root **README.md** mein "Helm Chart" ya "Helm" section hon.
- Usme `helm lint` aur `helm template` ke commands hon.
- 003-minikube-deployment ka zikr ho (Minikube deploy ke liye).

```bash
grep -A2 "Helm Chart" README.md
```

---

## 4. Tasks completion

- `specs/phase-4-local-kubernetes/002-helm-charts/tasks.md` mein T001–T017 sab `[x]` hon.

```bash
grep "\- \[ \]" specs/phase-4-local-kubernetes/002-helm-charts/tasks.md || echo "No unchecked tasks (good)"
```

Agar koi unchecked task bache to woh line dikhegi; sab complete hon to "No unchecked tasks (good)" aana chahiye.

---

## 5. One-liner summary (Helm optional)

Project root se:

```bash
cd /Users/apple/Documents/Projects/todo_phase4

echo "=== Files ==="
ls -la helm/todo-app/
ls -la helm/todo-app/templates/

echo "=== Probes ==="
grep -E "path: /health|path: /ready|path: /api/health" helm/todo-app/templates/*.yaml

echo "=== Ingress paths ==="
grep "path:" helm/todo-app/templates/ingress.yaml
```

Ye confirm karta hai: chart + templates maujood hain, probes sahi paths par hain, ingress paths set hain.

---

## Short checklist

| Check | Command / Action |
|-------|-------------------|
| Chart files exist | `ls helm/todo-app/` and `ls helm/todo-app/templates/` |
| Backend /health, /ready | `grep -E "/health|/ready" helm/todo-app/templates/backend-deployment.yaml` |
| Frontend /api/health | `grep "/api/health" helm/todo-app/templates/frontend-deployment.yaml` |
| Ingress / and /api | `grep "path:" helm/todo-app/templates/ingress.yaml` |
| Helm lint | `helm lint helm/todo-app` |
| Helm template | `helm template todo-app helm/todo-app` |
| README Helm section | `grep -A5 "Helm Chart" README.md` |
| All tasks done | Open tasks.md and confirm T001–T017 are [x] |

In sab se tum verify kar sakte ho ke **002-helm-charts** feature ka implementation hua hai aur chart use karne ke liye tayyar hai.
