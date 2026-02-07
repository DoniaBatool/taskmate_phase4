---
id: "0002"
title: "Phase IV Constitution Update - Local K8s + Auto Skill Learning"
stage: constitution
date: 2026-02-06
surface: claude-code
model: claude-opus-4-5-20251101
feature: phase4-local-kubernetes
branch: main
user: apple
command: /sp.constitution
labels: [phase-iv, kubernetes, minikube, deployment, infrastructure, skill-learner, auto-trigger]
links:
  spec: none
  ticket: none
  adr: none
  pr: none
files:
  - path: .specify/memory/constitution.md
    action: updated
    description: Updated constitution to v6.1.0 (Phase IV + Auto Skill Learning)
tests:
  - none (constitution update)
---

## Prompt

**Part 1:** @Hackathon II - Todoi Spec-Driven Development.md ka phase 4 dekho aur us k according update the existing constitution.md with phase 4 details q k ab hum phase 4 pe kaam karaingay using spec driven and test driven development aur relevant skills ka use karaingay to implement each feature of phase 4 religiously. Aik baat ka khaas dhiyaan rahay k phase 4 mae humain srf local kubernetes(minikube) pe deployment kerni hai is project ki jo hum ne pehlay se banaya hua hai project k features mae koi bhi changes nai honi chahiyae hai, srf is pooray infra structure ko deploy kerna hai bina kuch badlay aur bina business logic ko change kiyae

**Part 2:** skill-learner k name se skill hai in .claude aur mae chahty hun k jab koi feature successfully implement hojaey aur test bhi kerliya jaey tou us feature ki implementation mae jo bhi skills use hui hain unko reuseable intelligence k tor pe more powerful aur further kisi similar project mae use kernay k liyae tamam learning updation correction aur changes us skill mae add ki jain jo us feature ko implement kernay k doran hum ne face ki aur is k liyae skill-learner wali skill ko auto use kiya jaey jab user us feature ko test ker k mutmain hojaey aur system bhi feature ko test kerlay us k baad

## Response snapshot

**v6.0.0 Changes (Phase IV):**
1. Added Critical Scope Statement: Phase IV is DEPLOYMENT ONLY
2. Added Principle VII: Container-First Deployment
3. Added Principle VIII: AIOps-Enabled Kubernetes Operations
4. Added Principle IX: Helm-Based Package Management
5. Protected Phase III AI Chatbot - NO CHANGES ALLOWED
6. Added Phase IV Technology Stack, Dockerfiles, K8s specs

**v6.1.0 Changes (Auto Skill Learning):**
1. Added "AUTO SKILL LEARNING - MANDATORY" section
2. Made `/sp.skill-learner` AUTO-TRIGGERED (not manual)
3. Feature is NOT complete until skill-learner runs
4. Claude MUST invoke skill-learner without user asking
5. Added complete workflow showing auto-trigger flow
6. Added 6 learning categories (Bug Fix, Edge Case, Pattern, etc.)
7. Added learning format templates
8. Added Auto-Trigger Rules (when Claude MUST invoke)
9. Added Violations section (what makes feature INCOMPLETE)
10. Added PHR documentation format for skill learning
11. Goal: Never solve same problem twice - Learning Loop

## Outcome

- ✅ Impact: Constitution updated to v6.1.0 with Auto Skill Learning
- 🧪 Tests: N/A (documentation update)
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Create Phase IV spec, plan, and tasks
- 🧠 Reflection: Skills MUST evolve with every project - this is the Learning Loop

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
