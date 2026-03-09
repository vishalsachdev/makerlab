# When One AI Puppeteers Another: Testing a Kids' 3D Printing Camp with Agent Inception

*Claude Code pretends to be a 12-year-old. Codex becomes a patient camp coach. Blender builds a chess king. A 143KB STL file pops out the other end. Welcome to agent orchestration for education.*

---

Saturday afternoon. I'm staring at a chess king on my screen — a tall cylinder with four pointy cones and a ball on top. Not bad for a kid who's never opened Blender.

Except there is no kid. Claude Code is pretending to be one.

It's typing messages like "make it way taller! like 4 times taller. a chess king is tall and skinny" into OpenAI's Codex desktop app — an Electron application that Claude Code is puppeteering through Chrome DevTools Protocol via a tool called [agent-browser](https://github.com/vercel-labs/agent-browser). Codex reads the camp's teaching script, adopts the persona of a friendly AI coach, and sends modeling commands to Blender through [Blender MCP](https://github.com/ahujasid/blender-mcp). Objects appear in the viewport. The "kid" critiques the shapes. The coach iterates.

Three AI systems. Zero humans in the loop. A real STL file at the end.

## Why Would You Do This?

I'm building a summer camp for the [Illinois MakerLab](https://makerlab.illinois.edu) — "Generative AI + 3D Printing" for ages 12 and up, five days, three hours a day, eight kids max. The premise: kids describe what they want to build in plain English. An AI coach builds it in Blender while they watch, teaches them the software along the way, and exports their design for 3D printing. By day five, they're presenting printed objects to their parents.

The question wasn't whether the tech stack works in isolation. Blender MCP has been around. Codex can talk to it. The question was whether the *teaching experience* works — whether a 12-year-old sitting at an iMac, typing into a chat window, would actually learn Blender basics while creating something they're proud of.

I needed to test the full loop. Not a unit test. An integration test. With a simulated student.

## The Stack: Three AIs Deep

Here's the chain:

```
Claude Code (simulating a kid)
    → agent-browser (CDP automation)
        → Codex desktop app (Electron, GPT-5.4)
            → AGENTS.md teaching scripts (camp curriculum)
                → Blender MCP (TCP socket, port 9876)
                    → Blender viewport (objects appear live)
                        → STL export (143KB chess king)
```

Each layer does one job:

**Claude Code** is the test harness. It launches the Codex Electron app with `--remote-debugging-port=9333`, connects agent-browser to the Chrome DevTools Protocol, finds the ProseMirror chat input via JavaScript (`document.querySelector("[data-codex-composer]")`), and types messages as a 12-year-old would. It watches for responses, takes screenshots, and evaluates whether the coaching flow makes sense.

**Codex** is the camp instructor. It reads the AGENTS.md teaching scripts I wrote — course-in-a-box style, with `Say:`, `STOP:`, and `ACTION:` blocks — and follows them like a lesson plan. It uses Blender MCP tools to build objects, take viewport screenshots, and verify its own work. It teaches one Blender concept per interaction loop (viewport navigation, then selection, then Scene Collection, then materials).

**Blender MCP** is the hands. It receives Python commands from Codex and executes them in the live Blender viewport. Add a cylinder. Scale it. Apply a material. Join meshes. Export STL.

The kid never sees code. They see shapes appearing on screen and a friendly chat explaining what's happening.

## The Course-in-a-Box Pattern

A few weeks ago, I built an [entire interactive course in a single afternoon](https://chatwithgpt.substack.com/p/the-ai-course-that-teaches-itself) — 14 lessons teaching business students to use Codex, delivered from inside Codex itself. The insight: if you write AGENTS.md files as teaching scripts with structured markers, the AI becomes a patient, context-aware instructor. A root orchestration file handles progress detection and navigation. The course teaches itself.

That pattern — which I've been calling "course-in-a-box" — maps perfectly onto a summer camp for kids. The camp facilitator is a student employee, new to this. They can't memorize 15 hours of lesson plans. But they don't have to. The AGENTS.md scripts are the lesson plan. The AI follows them. The facilitator walks around troubleshooting and managing energy.

For the 3D printing camp, I wrote a main conductor (`AGENTS.md`) defining the coach persona, the OODA interaction loop (Observe → Orient → Decide → Act), Blender concepts in teaching order, and a progressive handoff from "AI builds everything" to "kid builds independently." Then five daily scripts — one per day — with specific Say/STOP/ACTION blocks for each phase of the MakerLab Design Loop: IMAGINE → SKETCH → BUILD → CHECK → IMPROVE → SHARE.

The scripts encode teaching philosophy as executable context. When to offer choices (always 2-3, never open-ended — reduces decision paralysis for kids). When to let the kid struggle (2-3 minutes before jumping in). When to teach a new concept (only when it becomes relevant, never ahead of time). How to handle criticism ("Good eye — let's fix that" not "That's wrong").

Context engineering *is* curriculum design.

## What the Test Revealed

The good news: it mostly works. Codex read both AGENTS.md files, adopted the coach persona immediately, and followed the OODA loop through five iterations. It taught Blender concepts in order. It offered structured choices. It handled shape iteration gracefully when the "kid" said the body looked like a plain tube instead of a chess king. It mentioned FDM printing constraints naturally when colors came up ("The printer uses one color of melted plastic. Colors on screen are just for us."). It exported a valid 143KB STL file.

The bad news — which is actually useful news:

**Visual fidelity gaps.** Codex told the kid "I reshaped the body with curves — wider at the bottom, thinner in the middle." The viewport still showed a plain cylinder. The AI described what it intended, not what it achieved. I added a rule to the scripts: "After describing a change, verify the screenshot actually shows that change. If the screenshot still shows a plain cylinder, your code didn't work — fix it before telling the kid it's done."

**Viewport framing.** After making the king four times taller, the crown disappeared off-screen. A real kid would panic. The coach eventually figured out it needed to zoom out, but only after the kid reported the problem. I added `bpy.ops.view3d.view_all()` as a mandatory action after scale changes.

**The body was still a cylinder.** For a chess king, you need stacked torus and sphere shapes to create the classic silhouette — wide base, narrow waist, flared collar, crown. A single scaled cylinder reads as a tube. Added a note: "For chess pieces, use stacked shapes of varying widths to create curves."

These aren't showstoppers. They're exactly the kind of discoveries you want before eight 12-year-olds sit down with real expectations.

## Agent Inception Is Becoming Normal

What felt strange a year ago — one AI controlling another — is becoming [the dominant architecture pattern of 2026](https://machinelearningmastery.com/7-agentic-ai-trends-to-watch-in-2026/). Gartner reported a 1,445% surge in multi-agent system inquiries from Q1 2024 to Q2 2025. Deloitte predicts the autonomous AI agent market will [reach $8.5 billion by 2026](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/ai-agent-orchestration.html). Anthropic's Model Context Protocol and Google's Agent-to-Agent Protocol are establishing standards for how agents talk to each other.

But most of the conversation is about enterprise workflows — incident response, data pipelines, customer support routing. What's underexplored is agent orchestration for *education*. Specifically:

**AI-as-student for curriculum testing.** Before I put a real kid in front of this system, I had an AI simulate the experience. It found three bugs in the teaching flow that would have derailed a real session. That's a QA pattern borrowed from software engineering and applied to pedagogy.

**AI-as-instructor with structured scripts.** The AGENTS.md pattern turns any domain expert's teaching instincts into a repeatable, auditable, forkable course. Your expertise is the moat. The AI is the delivery mechanism.

**AI-as-hands for physical output.** Through Blender MCP, the kid's words become 3D objects become physical prints. The feedback loop from imagination to artifact is compressed from weeks (traditional CAD learning curve) to minutes.

## What This Means for Augmentation

I keep coming back to the same frame: **AI amplifies expertise, it doesn't replace it.**

I've been teaching for years. I know that 12-year-olds need 2-3 choices, not open-ended prompts. I know that peer feedback needs structure ("Two Stars and a Wish," not "what do you think?"). I know that sketching on paper before touching a computer prevents the "I don't know what to make" paralysis. I know that a failed 3D print with bad overhangs is the best teaching prop for FDM constraints.

None of that knowledge came from AI. It came from watching students in the MakerLab — what makes them light up, what makes them shut down. AI let me encode all of it into executable teaching scripts in an afternoon, then stress-test the entire flow without a single real student present.

The camp runs this summer. Eight kids. Five days. Three AI systems deep. And the thing they'll remember isn't the AI. It's the chess king they designed, printed, and showed their parents.

That's augmentation.

---

*The camp curriculum (AGENTS.md scripts, lesson plans, facilitator guide, and setup checklist) is in the [MakerLab repository](https://github.com/vishalsachdev/makerlab). The course-in-a-box pattern for business students is at [codex-for-business-students](https://github.com/vishalsachdev/codex-for-business-students). Both are open source.*
