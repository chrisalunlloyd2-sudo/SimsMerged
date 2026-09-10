# Preserve and Protect: Safe GUI Harvest Plan
[TIMESTAMP: 2026-06-08T04:00:00.000Z]
[PROJECT_ID: SimsMerged-v1.4-Metropolis]

Instead of replacing what you built, we are going to treat your existing GUI as sacred ground. Our only job now is to hook into your current code, find the missing gaps mentioned in your chat logs, and inject them cleanly without breaking a single line of your layout.

Here is the revised 30-step engineering plan to safely harvest, audit, and finish *your* current GUI.

---

## Phase 1: Deep Diagnostic Auditing of Your Existing GUI (Steps 1–10)
This phase maps out your current codebase so we know exactly where the safe integration hooks are.

### Structural Mapping
1. **Analyze Your Current Entry Point:** Map out your existing GUI initialization file (e.g., `main.js`, `app.py`, or `index.html`) to understand how your window loops and state cycles currently load.
2. **Expose Existing Event Listeners:** Code a quick runtime script to log every active event listener or IPC channel your GUI is currently using, preventing namespace collisions.
3. **Audit the Current DOM/Widget Tree:** Run a structural scan across your interface components to locate the exact containers handling your chat history, terminal, and settings viewports.
4. **Isolate Current Global State Variables:** Identify how your GUI currently tracks variables like connection status, active user inputs, and message arrays.

### Breakage Prevention
5. **Establish a Local Git Branch Sandbox:** Before injecting a single line of new code, force an automated commit of your current pristine layout to a protected branch: `git checkout -b feature/harvested-integration`.
6. **Deploy Snapshot Regression Assertions:** Take a pixel-perfect visual snapshot of your GUI in its current working state to serve as an unchanging baseline for automated comparison.
7. **Trace Existing Audio/WebSocket Dependencies:** Locate your existing chat engine or sound player scripts, marking their API methods so we can call them natively without duplicating resources.
8. **Map Your Extracted Style Sheets:** Scan your existing CSS or styling dictionaries to ensure any new components seamlessly inherit your exact color tokens and margins.
9. **Pin Current Performance Marks:** Measure your GUI's current idle memory footprint and frame-time delta to ensure our background hooks don't introduce performance degradation.
10. **Lock Down the Safe Hook Manifest:** Save a localized mapping file (`gui_hooks.json`) detailing the exact function names and element IDs where external chat logs can safely append data.

---

## Phase 2: Surgical Extraction & Low-Impact Patching (Steps 11–20)
This phase mines your chat logs for missing pieces and hooks them directly into your existing architecture using non-destructive decorators or append-only methods.

### Extraction & Formatting
11. **Scan Chat Logs for Missing Features:** Run the log harvester *only* to find explicit functional elements you discussed but haven't written yet (e.g., a specific context-clearing button or logit tracking chart).
12. **Format Harvested Code to Match Your Style:** Pass extracted snippets through a code formatter (like Prettier or Black) configured to match the exact indentation, linting rules, and naming conventions of your current codebase.
13. **Wrap New Logic in Independent Modules:** Save all harvested features into completely isolated extension files (e.g., `gui_extensions.js` or `patches.py`) rather than pasting code directly into your core files.

### Safe Ingestion
14. **Utilize Safe Event Delegation:** Instead of modifying your existing button click handlers, attach separate, non-blocking event listeners to your UI components that fire alongside your current logic.
15. **Use Append-Only DOM Fragment Updates:** When injecting harvested chat components into your UI, use safe insertion methods (`appendChild` or structural layouts) that leave your surrounding markup completely undisturbed.
16. **Route Background Processing via Non-Blocking Channels:** Connect the harvested SLM/RAG backend pipelines strictly through your existing IPC/WebSocket pathways, treating them as passive data streams.
17. **Inject Isolated Error Boundaries:** Wrap every newly integrated feature inside an independent try/catch block, guaranteeing that if a harvested chat routine throws an exception, your main GUI stays alive and perfectly functional.
18. **Implement Non-Destructive Style Merging:** If a harvested component requires custom styling, load its CSS through a unique, deeply nested namespace class to avoid contaminating your layout selectors.
19. **Apply Polyfill Bridges for Broken Methods:** If a harvested chat feature relies on a method or variable your current GUI handles differently, build a simple translation adapter function to bridge the gap.
20. **Validate Modular Integration Isolation:** Run a targeted unit test verifying that the new expansion files can be completely commented out or removed without breaking your core interface.

---

## Phase 3: Targeted Testing & Final Hardening (Steps 21–30)
This final phase uses precise automation to scan your chat interface for broken elements, fix un-scrolled overflows, and finalize your software for release.

### Chat Diagnostics & Repairs
21. **Deploy Headless Automation to Your Chat Viewport:** Launch a testing worker (like Playwright or a native UI driver) targeted specifically at your existing chat panel inputs.
22. **Locate Broken Input Handlers:** Simulate a user typing a 10,000-character string into your chat box; verify that your existing code handles long strings smoothly without freezing the layout tree.
23. **Verify Automatic Scroll Containment:** Feed 100 consecutive rapid text responses into your chat container to test if it automatically scrolls to the bottom or if it breaks your layout container boundaries.
24. **Expose and Destroy Event Handler Leaks:** Monitor your GUI's memory allocations while opening and closing your chat panes repeatedly, killing any loose listeners that fail to disconnect.

### Integration Hardening
25. **Run a Visual Regression Pass Counter:** Automatically trigger a comparison check between your active interface and the step 6 baseline snapshot, flagging any unintended visual shifting or broken pixels.
26. **Automate Missing Component Auto-Fixes:** If the test suite flags an unwritten reference error from your harvested code, let a local agent write a micro-patch file to declare the missing variable safely.
27. **Execute Stress Testing Under Model Loads:** Fire up your slow-throttled Ollama agents on their fenced SSD lanes while actively interacting with your chat UI, confirming zero micro-stutters.
28. **Consolidate Code Assembly and Linting:** Run a final compilation validation across your merged source directory, verifying that all files pass strict type definitions and structural boundaries cleanly.
29. **Pack Verified Distributions Natively:** Run your native compiler tools (like PyInstaller or Electron-Builder) directly against your finalized folder structure to produce a clean, self-contained desktop executable.
30. **Enterprise Release Sign-Off:** Confirm that your existing GUI layout remains $100\%$ untouched and intact, tag your safe production release build in Git, and open your completely finished, stable interface deck.