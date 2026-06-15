# FormBuilder — Chrome navigation for cancellations

Exact click-path for cancelling/editing a response in ATLAS FormBuilder admin via the claude-in-chrome MCP. Load claude-in-chrome tools with ToolSearch first.

## Contents
- Login handoff
- Reach the response list
- Find & verify the response
- Full cancel vs partial answer-edit
- Phantom-seat check + Max-Registrants bump

## Login handoff

- Admin entry point: **`https://appserv7.admin.uillinois.edu/FormBuilderAdmin/`**
- Do NOT use the survey root (`/FormBuilderSurvey/`); its "Log In" link 500s (`/Authentication/~`).
- Navigate there, then **STOP and wait for the user to complete SSO** (NetID + Duo). Never enter credentials. Resume only when the user confirms they're logged in. If the page shows the form-group home, they're authenticated.

## Reach the response list

Form Group Home → **Forms** → on the "2026 Summer Camp Registration" row click **DASHBOARD** → in Quick Links click **FORM RESPONSE LIST**.
(Direct URL pattern, current form: `.../Form/7af850be-522a-4f8e-83b0-b3e601399c5f/FormResponses`. The form-group/form IDs can change between periods — prefer clicking through if unsure.)

Avoid the gear (⚙) menu on the Forms row — it's copy/delete/move form actions, not responses.

## Find & verify the response

- Use the **Search** box (top-right of the Responses table); type the **camper's or parent's last name**. The table filters live (wait for the spinner).
- Click **DETAILS** on the matching row.
- **Verify the page title is `Form Response <reference-number>`** and matches the reference from the request (e.g. `t6o1-eyyy-yyyy-y`). This is the definitive identity check — do it before any action.
- Scroll to the **Answers** block and confirm: `camper_first_name_1`/`camper_last_name_1`, and which camp checkboxes are set (`camps_list_1`, `build_your_own_robot_arm`, `minecraft_and_3d_printing`, etc.). This tells you whether it's a single-camp (full cancel) or multi-camp (partial) response.
- "View Form Response" opens the survey-side viewer which needs separate auth — skip it; read the Answers block on the admin page instead.

## Full cancel (camper's only camp / whole response)

1. **Install a dialog guard first** (FormBuilder may fire a native confirm that freezes the extension). Run via javascript_tool:
   `window.__dialogs=[]; window.confirm=function(m){window.__dialogs.push(m);return true;}; window.alert=function(m){window.__dialogs.push(m);};`
2. In the **Actions** panel click the red **CANCEL REGISTRATION**. The **DELETE FORM RESPONSE** button is directly below it — do not click that.
3. Confirm **Registration Status → "Cancelled"** and that the Actions panel now shows "Register Response"/"Add to Waitlist". The payment record is preserved.

## Partial cancel (camper keeps other camps)

Do NOT "Cancel Registration" (it voids the whole response). Instead use **EDIT THESE ANSWERS** in the DETAILS view and **uncheck only the camp being cancelled** (checkbox in the camp field), then save. Editing answers in DETAILS keeps multi-select intact; the "Edit Answer" inline button collapses multi-selects, so use the DETAILS-view checkboxes.

## Phantom-seat check + Max-Registrants bump

- After a **full** Cancel Registration, the form's seat is released: the Dashboard's **Number Registered** decrements by 1, and `update_availability.py --dry-run` shows the freed seat. No bump needed.
- A **partial answer-edit** (or a cancelled response whose camp box is still checked) leaves a **phantom seat**: the live registration form still counts it and may refuse a new sign-up, even though the data endpoint/website badge correctly show an opening. Tell-tale: a session's capacity table shows registered ≥ max.
- To unblock a real sign-up against a phantom seat: **Periods → EDIT SESSIONS** (period 2026) → scroll to the camp section → the session row → **EDIT** → bump **Maximum Registrants** by the phantom count. Revert to true cap once the seat fills or the phantom is cleaned (uncheck the cancelled camp box). **Never leave Max above true cap on a hard-capacity camp** (robot camps = 6) or the form can over-register.
- The EDIT SESSIONS dialog shows Max Registrants but not the live registered count; judge "is a bump needed?" from whether the live form actually blocks the family, not from this screen.
