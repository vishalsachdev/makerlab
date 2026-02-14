# Illinois MakerLab — Summer 2026 Camp Schedule

## Overview

- **Duration**: Monday June 1 – Friday July 31, 2026 (8 weeks)
- **Holiday skip**: Week of June 29 – July 3 (July 4th week)
- **Daily format**: 3 hours/day, 5 days/week
  - Morning session: **9:00 AM – 12:00 PM**
  - Afternoon session: **1:00 PM – 4:00 PM**
- **Location**: BIF Room 3030, UIUC
- **Pricing**: $250 regular / $225 early bird (until March 15)
- **Max campers**: 8 per session (5 for robot camps — see below)

---

## The Five Camps

### Existing Camps

| # | Camp | Ages | Description |
|---|------|------|-------------|
| 1 | **Minecraft + 3D Printing** | 10+ | Build worlds in Minecraft, export and 3D print your creations. *Flagship camp — highest demand.* |
| 2 | **Adventures in 3D Modeling** | 10–17 | Learn Fusion 360 and 3D printing fundamentals through design challenges. |
| 3 | **Generative AI + 3D Printing** | 12+ | Use AI tools (image generators, text-to-3D) to design and 3D print unique objects. |

### Two New Camps

| # | Camp | Ages | Robot | Description |
|---|------|------|-------|-------------|
| 4 | **AI Robotics with Reachy Mini** | 12+ | Pollen Robotics / Hugging Face Reachy Mini (1 unit) | Program an open-source desktop robot to see, listen, talk, and react using Python and Hugging Face AI models. Max 5 campers. |
| 5 | **Build Your Own Robot Arm** | 12+ | SO-ARM100/101 (1 kit) | 3D print the shell, assemble a real robot arm from a kit, then train it to pick and place objects. Max 5 campers. |

---

## Equipment Inventory (Critical Constraints)

### Robots

| Robot | Qty | Notes |
|-------|-----|-------|
| **Reachy Mini Lite** (Pollen Robotics / Hugging Face) | **1** | Desktop robot — 28cm tall, 6-DOF head, 360° body rotation, HD camera, 2-mic array, speaker, expressive LED eyes + antennas. USB-powered (tethered to iMac). Open-source Python SDK. $299. |
| **SO-ARM100** (TheRobotStudio) | **1 kit** | 6-DOF robot arm kit — motors and wiring included, we 3D print the shell. Leader-follower teleoperation. Open-source, Hugging Face LeRobot compatible. |

**One of each robot → robot camps capped at 5 campers. All other camps capped at 8.**

### Lab Computers

| Equipment | Qty | Notes |
|-----------|-----|-------|
| **iMacs** | **10** | macOS — handles all camps. Reachy Mini SDK runs on Mac, LeRobot runs on Mac, Minecraft/Fusion 360 run on Mac. |

**No Windows PC or VR headset needed.** Reachy Mini Lite connects via USB to an iMac (tethered — no battery).

---

## Scheduling Rules

1. **Minecraft + 3D Printing** runs **every week** (8 out of 8 weeks) = 50% of all slots
2. Minecraft is in the **morning in June** and **afternoon in July**
3. The other 4 camps each get **2 weeks**, filling the opposite slot from Minecraft
4. No two sessions of the same camp run in the same week

---

## Weekly Calendar

### June (Weeks 1–4) — Minecraft in the Morning

| Week | Dates | Morning (9 AM–12 PM) | Afternoon (1–4 PM) |
|------|-------|----------------------|---------------------|
| 1 | Jun 1–5 | Minecraft + 3D Printing | Adventures in 3D Modeling |
| 2 | Jun 8–12 | Minecraft + 3D Printing | **Build Your Own Robot Arm** (SO-ARM100) |
| 3 | Jun 15–19 | Minecraft + 3D Printing | Generative AI + 3D Printing |
| 4 | Jun 22–26 | Minecraft + 3D Printing | **AI Robotics with Reachy Mini** |
| — | Jun 29–Jul 3 | ⛱️ **NO CAMP — July 4th Holiday Week** | ⛱️ **NO CAMP** |

### July (Weeks 5–8) — Minecraft in the Afternoon

| Week | Dates | Morning (9 AM–12 PM) | Afternoon (1–4 PM) |
|------|-------|----------------------|---------------------|
| 5 | Jul 6–10 | Adventures in 3D Modeling | Minecraft + 3D Printing |
| 6 | Jul 13–17 | **Build Your Own Robot Arm** (SO-ARM100) | Minecraft + 3D Printing |
| 7 | Jul 20–24 | Generative AI + 3D Printing | Minecraft + 3D Printing |
| 8 | Jul 27–31 | **AI Robotics with Reachy Mini** | Minecraft + 3D Printing |

---

## Summary Stats

| Camp | Total Weeks | June Weeks | July Weeks | Slot |
|------|-------------|------------|------------|------|
| Minecraft + 3D Printing | **8** (50%) | 4 (AM) | 4 (PM) | Alternates |
| Adventures in 3D Modeling | 2 (12.5%) | 1 (PM) | 1 (AM) | Alternates |
| Build Your Own Robot Arm | 2 (12.5%) | 1 (PM) | 1 (AM) | Alternates |
| Generative AI + 3D Printing | 2 (12.5%) | 1 (PM) | 1 (AM) | Alternates |
| AI Robotics with Reachy Mini | 2 (12.5%) | 1 (PM) | 1 (AM) | Alternates |
| **Total camp-weeks** | **16** | 8 | 8 | |

---

## New Camp Details

### Camp 4: AI Robotics with Reachy Mini

**Robot**: [Reachy Mini Lite](https://huggingface.co/blog/reachy-mini) by Pollen Robotics / Hugging Face — open-source desktop robot ($299, USB-powered)
**Ages**: 12+
**Cap**: 5 campers (1 robot)

**What makes it special**: Reachy Mini is a 28cm desktop robot that sees, hears, talks, and reacts — and kids program all of it in Python. It has an HD camera, a dual-microphone setup for hearing, a speaker for talking back, expressive LED eyes, animated antennas, and a head that moves in 6 directions. The real hook: it plugs directly into Hugging Face's ecosystem of 1.7 million AI models. So on Day 1 kids are writing Python, and by Day 3 they're loading real AI models onto a robot that recognizes their face, answers their questions, and turns to look at whoever is speaking. It ships as a kit, so assembly is part of the experience too.

**5-Day Curriculum Outline**:

| Day | Theme | Activities |
|-----|-------|------------|
| **Mon** | Build Your Robot | Unbox the kit, assemble Reachy Mini (~2 hrs). Connect to iMac. Run first behaviors from the Hugging Face Hub — make it look around, blink, wiggle its antennas. Intro to the Python SDK. |
| **Tue** | Teach It to See | How does a robot see? Access the camera feed in Python. Write code to detect faces, recognize colors, track objects. Each kid programs a different visual reaction — Reachy looks at you when you wave, follows a colored ball, etc. |
| **Wed** | Teach It to Listen & Talk | Reachy has a microphone and speaker — hook up a speech-to-text model from Hugging Face so it understands what you say. Then add text-to-speech so Reachy talks back. Build a simple conversation loop: you talk, it listens, it responds. |
| **Thu** | Give It a Brain | Connect a language model (from Hugging Face Hub) so Reachy can answer questions, tell jokes, or play a quiz game. Each camper designs a unique "personality" — a greeter, a trivia host, a storyteller, a translator. |
| **Fri** | Robot Personality Showcase | Each camper demos the personality they built. Reachy recognizes who's talking, responds in character, and reacts expressively. Vote on funniest, smartest, most creative. Discussion: where is AI + robotics headed? |

**Why 5 campers works well**:
- One robot means everyone takes turns at the keyboard, but the small group keeps wait times short (~30 min each per session)
- While one kid codes, others plan their personality, test prompts, or sketch interaction flows
- The robot is a natural conversation piece — kids coach each other ("make it funnier," "it should look left when it hears you")
- Assembly on Day 1 is a team activity — everyone has a part to build

**Key Specs for Instructors**:
- Hardware: 28cm tall, 1.5 kg, 6-DOF head, 360° body rotation, 2 animated antennas, LED eyes
- Sensors: wide-angle HD camera, 2 microphones, 5W speaker
- Connectivity: USB to iMac (Lite version — tethered, no battery). Compute runs on the iMac, not onboard.
- Software: Python SDK, Hugging Face Hub integration (1.7M+ models), 15+ pre-built behaviors
- Runs on: **macOS** (iMacs) — no Windows needed
- Assembly: ships as kit, ~2 hours to build
- Docs: [GitHub SDK](https://github.com/pollen-robotics/reachy_mini) | [Hugging Face Docs](https://huggingface.co/docs/reachy_mini/index)

---

### Camp 5: Build Your Own Robot Arm

**Robot**: [SO-ARM100/101](https://github.com/TheRobotStudio/SO-ARM100) — open-source robot arm kit (motors + wiring included, we 3D print the shell)
**Ages**: 12+
**Cap**: 5 campers (1 kit with 1 set of motors)

**What makes it special**: Kids 3D print the robot's shell, snap it onto the kit's motors and wiring, and by mid-week they have a working robot arm they trained to pick up and place objects. The leader-follower setup is the magic moment — one arm mirrors the other in real-time, so kids physically guide the "leader" arm and the "follower" copies every move. It's tactile, visual, and genuinely fun.

**5-Day Curriculum Outline**:

| Day | Theme | Activities |
|-----|-------|------------|
| **Mon** | Print the Shell | What's a robot arm? — joints, motors, grippers. Tour the kit parts (motors, wiring, controller). Start 3D printing shell pieces (some pre-staged, some live). Each kid picks a part to "own." |
| **Tue** | Build the Arm | Snap the printed shell onto the motors. Connect wiring. Attach the gripper. Power it on — first wiggle! Calibrate each joint. Celebrate: you just built a robot. |
| **Wed** | Teach It by Hand | Leader-follower teleoperation — physically guide the leader arm, watch the follower copy in real-time. Record movement sequences. Each kid records their own pick-and-place demo. |
| **Thu** | Train the Brain | Feed the recorded demonstrations into the Hugging Face LeRobot framework. The arm learns to repeat the task on its own. Tweak and improve — make it faster, more accurate, try new objects. |
| **Fri** | Pick & Place Challenge | Fun challenge: arm must sort colored blocks, stack cups, or move gummy bears into bowls — autonomously using what they trained. Vote on best run. Take-home: each kid keeps a 3D-printed mini gripper they designed. |

**Why 5 campers works well**:
- One set of motors means one arm being assembled/operated at a time
- With 5 kids, everyone has a role during assembly (each "owns" a joint/section)
- Parallel activity: while some work on the arm, others are at the printers designing custom gripper tips or printing spare shell pieces
- Leader-follower is naturally collaborative — one guides, others coach and plan

**Key Specs for Instructors**:
- Kit includes: STS3215 bus servos (30 kg·cm torque), wiring harness, controller board
- We 3D print: shell/housing (~800g PLA+, 0.4mm nozzle, 0.2mm layers), TPU 95A gripper finger
- Software: Hugging Face LeRobot framework, UART communication
- Pre-print structural shell pieces before camp; campers print gripper variations and accessories during the week
- Full BOM and assembly guide on [GitHub](https://github.com/TheRobotStudio/SO-ARM100)

---

## Image Assets for Web Updates

Located in `summer/images/`:

| File | Source | Use for |
|------|--------|---------|
| `reachy2-full-robot.webp` (51 KB) | [pollen-robotics.com/reachy](https://www.pollen-robotics.com/reachy/) | ⚠️ **Wrong robot** — this is Reachy 2 (full humanoid), not Reachy Mini. Need new image. |
| `so-arm100-follower.webp` (134 KB) | [GitHub SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100) | Build Your Own Robot Arm camp hero |

---

## Confirmed Decisions

- [x] Holiday skip: week of **June 29–July 3** (July 4th is Saturday)
- [x] Camp caps: **8 max** for standard camps, **5 max** for robot camps (Reachy Mini and SO-ARM100)
- [x] Lab computers: **10 iMacs** (macOS). Sufficient for all camps — no Windows PC needed. Reachy Mini SDK and LeRobot both run on Mac.
- [x] Both robot camps: **ages 12+**
- [x] Registration: UIUC registration system (not Eventbrite)
- [x] Marketing angle: "First university maker lab to offer AI robotics camps for kids" — two camps where kids build, program, and train real robots using Python and Hugging Face AI models. Hero moments: kid talks to Reachy Mini and it answers back; kid trains a robot arm to sort objects autonomously.
- [x] Reachy Mini camp focus: AI + human-robot interaction — vision, speech, language models, personality design. No VR, no arms. Desktop robot that sees, hears, and talks.
- [x] SO-ARM100 camp: kit comes with motors + wiring; we print the shell; focus on assembly + training for pick-and-place
- [x] Early bird deadline: **March 15** (extended from Feb 28)
- [x] ~~Windows PC / VR headset~~: **NOT needed**. Reachy Mini is a desktop robot (no VR teleoperation). Runs on iMacs via USB.
- [x] Reachy Mini version: **Lite** ($299, USB-powered, tethered to iMac, 2 mics). Compute runs on iMac, not onboard.

## Open Questions

- [ ] **SO-ARM100 camp**: Pre-print shell pieces before camp starts? (~800g PLA, ~10 hour print)
- [ ] Staffing: Reachy Mini camp needs Python + comfort with Hugging Face models. SO-ARM100 camp needs 3D printing + basic wiring skills.

---

## Schedule by Camp (for Registration Form)

### 1. Minecraft + 3D Printing (Ages 10+, max 8 campers)

| Session | Dates | Time | Weeks |
|---------|-------|------|-------|
| Session 1 | Mon Jun 1 – Fri Jun 5 | 9:00 AM – 12:00 PM | Week 1 |
| Session 2 | Mon Jun 8 – Fri Jun 12 | 9:00 AM – 12:00 PM | Week 2 |
| Session 3 | Mon Jun 15 – Fri Jun 19 | 9:00 AM – 12:00 PM | Week 3 |
| Session 4 | Mon Jun 22 – Fri Jun 26 | 9:00 AM – 12:00 PM | Week 4 |
| Session 5 | Mon Jul 6 – Fri Jul 10 | 1:00 PM – 4:00 PM | Week 5 |
| Session 6 | Mon Jul 13 – Fri Jul 17 | 1:00 PM – 4:00 PM | Week 6 |
| Session 7 | Mon Jul 20 – Fri Jul 24 | 1:00 PM – 4:00 PM | Week 7 |
| Session 8 | Mon Jul 27 – Fri Jul 31 | 1:00 PM – 4:00 PM | Week 8 |

**8 sessions total** · Morning in June, Afternoon in July

---

### 2. Adventures in 3D Modeling (Ages 10–17, max 8 campers)

| Session | Dates | Time | Weeks |
|---------|-------|------|-------|
| Session 1 | Mon Jun 1 – Fri Jun 5 | 1:00 PM – 4:00 PM | Week 1 |
| Session 2 | Mon Jul 6 – Fri Jul 10 | 9:00 AM – 12:00 PM | Week 5 |

**2 sessions total**

---

### 3. Generative AI + 3D Printing (Ages 12+, max 8 campers)

| Session | Dates | Time | Weeks |
|---------|-------|------|-------|
| Session 1 | Mon Jun 15 – Fri Jun 19 | 1:00 PM – 4:00 PM | Week 3 |
| Session 2 | Mon Jul 20 – Fri Jul 24 | 9:00 AM – 12:00 PM | Week 7 |

**2 sessions total**

---

### 4. AI Robotics with Reachy Mini (Ages 12+, max 5 campers)

| Session | Dates | Time | Weeks |
|---------|-------|------|-------|
| Session 1 | Mon Jun 22 – Fri Jun 26 | 1:00 PM – 4:00 PM | Week 4 |
| Session 2 | Mon Jul 27 – Fri Jul 31 | 9:00 AM – 12:00 PM | Week 8 |

**2 sessions total**

---

### 5. Build Your Own Robot Arm (Ages 12+, max 5 campers)

| Session | Dates | Time | Weeks |
|---------|-------|------|-------|
| Session 1 | Mon Jun 8 – Fri Jun 12 | 1:00 PM – 4:00 PM | Week 2 |
| Session 2 | Mon Jul 13 – Fri Jul 17 | 9:00 AM – 12:00 PM | Week 6 |

**2 sessions total**

---

### Quick Reference — All 16 Sessions

| # | Camp | Dates | Time | Max |
|---|------|-------|------|-----|
| 1 | Minecraft + 3D Printing | Jun 1–5 | 9 AM–12 PM | 8 |
| 2 | Adventures in 3D Modeling | Jun 1–5 | 1–4 PM | 8 |
| 3 | Minecraft + 3D Printing | Jun 8–12 | 9 AM–12 PM | 8 |
| 4 | Build Your Own Robot Arm | Jun 8–12 | 1–4 PM | 5 |
| 5 | Minecraft + 3D Printing | Jun 15–19 | 9 AM–12 PM | 8 |
| 6 | Generative AI + 3D Printing | Jun 15–19 | 1–4 PM | 8 |
| 7 | Minecraft + 3D Printing | Jun 22–26 | 9 AM–12 PM | 8 |
| 8 | AI Robotics with Reachy Mini | Jun 22–26 | 1–4 PM | 5 |
| — | ⛱️ NO CAMP (July 4th week) | Jun 29–Jul 3 | — | — |
| 9 | Adventures in 3D Modeling | Jul 6–10 | 9 AM–12 PM | 8 |
| 10 | Minecraft + 3D Printing | Jul 6–10 | 1–4 PM | 8 |
| 11 | Build Your Own Robot Arm | Jul 13–17 | 9 AM–12 PM | 5 |
| 12 | Minecraft + 3D Printing | Jul 13–17 | 1–4 PM | 8 |
| 13 | Generative AI + 3D Printing | Jul 20–24 | 9 AM–12 PM | 8 |
| 14 | Minecraft + 3D Printing | Jul 20–24 | 1–4 PM | 8 |
| 15 | AI Robotics with Reachy Mini | Jul 27–31 | 9 AM–12 PM | 5 |
| 16 | Minecraft + 3D Printing | Jul 27–31 | 1–4 PM | 8 |

**Total capacity**: 16 sessions × avg ~7 = ~112 camper-slots (max 118 if all sessions full)

---

*Plan updated February 14, 2026*
