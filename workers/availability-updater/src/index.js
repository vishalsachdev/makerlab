/**
 * MakerLab Summer Camp Availability Updater
 *
 * Cloudflare Worker with Cron Trigger that:
 * 1. Fetches registration data from UIUC FormBuilder API
 * 2. Computes per-session availability
 * 3. Updates summer.html and detail pages via GitHub API
 * 4. Commits changes (only if availability actually changed)
 *
 * Secrets (set via `wrangler secret put`):
 *   FORMBUILDER_TOKEN - Bearer token for FormBuilder API
 *   GITHUB_TOKEN      - GitHub PAT with repo write access
 *
 * Gracefully stops if the FormBuilder token expires (401) or all sessions are sold out.
 */

// --- Camp configuration (matches data/summer-camps-2026.json) ---

const CAMPS = [
  {
    id: "minecraft",
    name: "Minecraft + 3D Printing",
    field: "Minecraft and 3D Printing",
    detailFile: "summer/minecraft-3d-printing.html",
    maxCampers: 8,
    sessions: [
      { dates: "Jun 1–5", time: "9:00 AM – 12:00 PM", summary: "Jun 1–5 (AM)" },
      { dates: "Jun 8–12", time: "9:00 AM – 12:00 PM", summary: "Jun 8–12 (AM)" },
      { dates: "Jun 15–19", time: "9:00 AM – 12:00 PM", summary: "Jun 15–19 (AM)" },
      { dates: "Jul 13–17", time: "1:00 PM – 4:00 PM", summary: "Jul 13–17 (PM)" },
      { dates: "Jul 20–24", time: "1:00 PM – 4:00 PM", summary: "Jul 20–24 (PM)" },
      { dates: "Jul 27–31", time: "1:00 PM – 4:00 PM", summary: "Jul 27–31 (PM)" },
    ],
    codes: { MINECRAFT_JUN1: 0, MINECRAFT_JUN2: 1, MINECRAFT_JUN3: 2, MINECRAFT_JUL2: 3, MINECRAFT_JUL3: 4, MINECRAFT_JUL4: 5 },
  },
  {
    id: "adventures",
    name: "Adventures in 3D Modeling",
    field: "Adventures in 3D Modeling",
    detailFile: "summer/adventures-in-3d-modeling-and-printing.html",
    maxCampers: 8,
    sessions: [
      { dates: "Jun 1–5", time: "1:00 PM – 4:00 PM", summary: "Jun 1–5 (PM)" },
      { dates: "Jul 6–10", time: "9:00 AM – 12:00 PM", summary: "Jul 6–10 (AM)" },
    ],
    codes: { "ADV3D_JUN1": 0, "ADV3D_JUL1": 1 },
  },
  {
    id: "genai",
    name: "Generative AI + 3D Printing",
    field: "GenAI and 3d Printing",
    detailFile: "summer/generative-ai-3d-printing.html",
    maxCampers: 8,
    sessions: [
      { dates: "Jun 15–19", time: "1:00 PM – 4:00 PM", summary: "Jun 15–19 (PM)" },
      { dates: "Jul 20–24", time: "9:00 AM – 12:00 PM", summary: "Jul 20–24 (AM)" },
    ],
    codes: { GENAI3D_JUN1: 0, GENAI3D_JUL1: 1 },
  },
  {
    id: "robot-arm",
    name: "Build Your Own Robot Arm",
    field: "Build Your Own Robot Arm",
    detailFile: "summer/build-your-own-robot-arm.html",
    maxCampers: 6,
    sessions: [
      { dates: "Jun 8–12", time: "1:00 PM – 4:00 PM", summary: "Jun 8–12 (PM)" },
      { dates: "Jun 22–26", time: "9:00 AM – 12:00 PM", summary: "Jun 22–26 (AM)" },
      { dates: "Jul 13–17", time: "9:00 AM – 12:00 PM", summary: "Jul 13–17 (AM)" },
    ],
    codes: { ROBOTARM_JUN1: 0, ROBOTARM_JUN2: 1, ROBOTARM_JUL1: 2 },
  },
  {
    id: "reachy",
    name: "AI Robotics with Reachy Mini",
    field: "AI Robotics with Reachy Mini",
    detailFile: "summer/ai-robotics-reachy-mini.html",
    maxCampers: 6,
    sessions: [
      { dates: "Jun 22–26", time: "1:00 PM – 4:00 PM", summary: "Jun 22–26 (PM)" },
      { dates: "Jul 6–10", time: "1:00 PM – 4:00 PM", summary: "Jul 6–10 (PM)" },
      { dates: "Jul 27–31", time: "9:00 AM – 12:00 PM", summary: "Jul 27–31 (AM)" },
    ],
    codes: { AIROBOTICS_JUN1: 0, AIROBOTICS_JUL1: 1, AIROBOTICS_JUL2: 2 },
  },
];

// --- Availability logic ---

function computeAvailability(registrations) {
  const availability = {};

  for (const camp of CAMPS) {
    const counts = new Array(camp.sessions.length).fill(0);

    for (const reg of registrations) {
      const val = (reg[camp.field] || "").trim();
      if (!val) continue;
      for (const code of val.split(", ")) {
        const idx = camp.codes[code];
        if (idx !== undefined) counts[idx]++;
      }
    }

    availability[camp.id] = camp.sessions.map((_, i) => ({
      count: counts[i],
      max: camp.maxCampers,
      remaining: Math.max(0, camp.maxCampers - counts[i]),
    }));
  }

  return availability;
}

function badgeHtml(remaining) {
  if (remaining <= 0) {
    return '<span style="color: #d32f2f; font-weight: bold;">SOLD OUT</span>';
  } else if (remaining <= 2) {
    return `<span style="color: #e04e39; font-weight: bold;">${remaining} spot${remaining === 1 ? "" : "s"} left</span>`;
  }
  return `${remaining} spots left`;
}

// --- HTML update functions ---

function updateSummerHtml(content, availability) {
  for (const camp of CAMPS) {
    const avail = availability[camp.id];
    const parts = camp.sessions.map((s) => s.summary);

    // Build regex matching existing session line (with or without badges)
    const oldParts = parts.map(
      (p) => escapeRegex(p) + String.raw`(?:\s*—\s*(?:<span[^>]*>.*?<\/span>|\d+ spots? left))?`
    );
    const oldPattern = new RegExp(oldParts.join("<br>"));

    // Build replacement with badges for every session
    const newLine = parts
      .map((p, i) => `${p} — ${badgeHtml(avail[i].remaining)}`)
      .join("<br>");

    content = content.replace(oldPattern, newLine);
  }
  return content;
}

function updateDetailPage(content, camp, avail) {
  // Add Availability header if missing
  if (!content.includes("Availability</th>")) {
    content = content.replace(
      '<th style="padding: 0.5rem; text-align: left;">Time</th>\n                </tr>',
      '<th style="padding: 0.5rem; text-align: left;">Time</th>\n                  <th style="padding: 0.5rem; text-align: left;">Availability</th>\n                </tr>'
    );
  }

  // Update each session row
  for (let i = 0; i < camp.sessions.length; i++) {
    const badge = badgeHtml(avail[i].remaining);
    const dates = escapeRegex(camp.sessions[i].dates);
    const time = escapeRegex(camp.sessions[i].time);

    // Match: date cell + time cell, optional existing availability cell, then </tr>
    const pattern = new RegExp(
      `(${dates}<\\/td><td[^>]*>${time}<\\/td>)(?:<td[^>]*>.*?<\\/td>)?(<\\/tr>)`
    );
    content = content.replace(
      pattern,
      `$1<td style="padding: 0.5rem;">${badge}</td>$2`
    );
  }

  return content;
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// --- GitHub API helpers ---

async function githubGet(path, token, repo) {
  const resp = await fetch(`https://api.github.com/repos/${repo}/contents/${path}?ref=main`, {
    headers: {
      Authorization: `token ${token}`,
      Accept: "application/vnd.github.v3+json",
      "User-Agent": "makerlab-availability-worker",
    },
  });
  if (!resp.ok) throw new Error(`GitHub GET ${path}: ${resp.status}`);
  const data = await resp.json();
  return { content: atob(data.content), sha: data.sha };
}

async function githubUpdate(path, content, sha, message, token, repo) {
  const resp = await fetch(`https://api.github.com/repos/${repo}/contents/${path}`, {
    method: "PUT",
    headers: {
      Authorization: `token ${token}`,
      Accept: "application/vnd.github.v3+json",
      "User-Agent": "makerlab-availability-worker",
    },
    body: JSON.stringify({
      message,
      content: btoa(unescape(encodeURIComponent(content))),
      sha,
      branch: "main",
    }),
  });
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`GitHub PUT ${path}: ${resp.status} ${text}`);
  }
}

// --- FormBuilder API ---

async function fetchRegistrations(endpointId, token) {
  const url = `https://appserv7.admin.uillinois.edu/FormBuilderService/api/DataEndpoint/${endpointId}`;
  const resp = await fetch(url, {
    headers: {
      Accept: "application/json",
      Authorization: `Bearer ${token}`,
    },
  });

  if (resp.status === 401) {
    return { error: "token_expired", data: null };
  }
  if (!resp.ok) {
    return { error: `http_${resp.status}`, data: null };
  }

  const data = await resp.json();
  return { error: null, data };
}

// --- Main handler ---

export default {
  async scheduled(event, env, ctx) {
    const log = [];
    const ts = new Date().toISOString();
    log.push(`[${ts}] Availability update started`);

    // 1. Fetch registrations (graceful on token expiry)
    const { error, data: registrations } = await fetchRegistrations(
      env.ENDPOINT_ID,
      env.FORMBUILDER_TOKEN
    );

    if (error === "token_expired") {
      log.push("FormBuilder token expired — skipping update (likely all sold out)");
      console.log(log.join("\n"));
      return;
    }
    if (error) {
      log.push(`FormBuilder API error: ${error}`);
      console.log(log.join("\n"));
      return;
    }

    log.push(`Fetched ${registrations.length} registrations`);

    // 2. Compute availability
    const availability = computeAvailability(registrations);

    let totalFilled = 0;
    let totalCap = 0;
    for (const camp of CAMPS) {
      for (const a of availability[camp.id]) {
        totalFilled += a.count;
        totalCap += a.max;
      }
    }
    const remaining = totalCap - totalFilled;
    log.push(`${totalFilled}/${totalCap} filled, ${remaining} spots remaining`);

    // 3. Update files via GitHub API
    const filesToUpdate = [
      { path: "summer.html", updater: (c) => updateSummerHtml(c, availability) },
      ...CAMPS.map((camp) => ({
        path: camp.detailFile,
        updater: (c) => updateDetailPage(c, camp, availability[camp.id]),
      })),
    ];

    let changedFiles = 0;

    for (const file of filesToUpdate) {
      const { content: original, sha } = await githubGet(file.path, env.GITHUB_TOKEN, env.GITHUB_REPO);
      const updated = file.updater(original);

      if (updated !== original) {
        await githubUpdate(
          file.path,
          updated,
          sha,
          `Update camp availability (${ts.split("T")[0]})`,
          env.GITHUB_TOKEN,
          env.GITHUB_REPO
        );
        changedFiles++;
        log.push(`Updated: ${file.path}`);
      }
    }

    if (changedFiles === 0) {
      log.push("No changes detected");
    } else {
      log.push(`${changedFiles} file(s) committed and deployed`);
    }

    console.log(log.join("\n"));
  },

  // HTTP handler for manual trigger / health check
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/run") {
      // Manual trigger — run the same logic as cron
      await this.scheduled({}, env, {});
      return new Response("Availability update triggered. Check logs.\n");
    }

    return new Response(
      JSON.stringify({
        name: "makerlab-availability-updater",
        status: "ok",
        schedule: "daily 7:00 AM CDT",
        tokenExpires: "2026-04-16",
      }),
      { headers: { "Content-Type": "application/json" } }
    );
  },
};
