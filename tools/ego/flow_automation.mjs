/**
 * Ego Lite Automation Bridge for Google Flow (labs.google/flow)
 * Implements resilient browser interactions based on Slate DOM injection,
 * thumbnail progress tracking, and screenshot verification.
 */

export async function initFlowSession() {
  const task = await taskSpace("Google Flow Production");
  const page = task.page("flow_app");
  
  console.log("[Ego Flow] Navigating to Google Flow...");
  await page.goto("https://labs.google/flow");
  await page.waitForLoadState();
  
  // Take status screenshot
  const shotPath = "C:/Users/HAI/OneDrive/Tài liệu/vmax/shots/ego_flow_current_state.png";
  await page.screenshot({ path: shotPath });
  console.log(`[Ego Flow] State captured at: ${shotPath}`);
  
  // Inspect authentication & UI status
  const pageInfo = await page.evaluate(() => {
    const title = document.title;
    const isLoginButton = !!document.querySelector("a[href*='accounts.google.com'], button:has-text('Sign in'), button:has-text('Log in')");
    const hasNewProject = !!document.querySelector("button:has-text('New project'), [aria-label*='New project']");
    const slateEditor = !!document.querySelector("[data-slate-editor='true'], [contenteditable='true']");
    return { title, isLoginButton, hasNewProject, slateEditor, url: window.location.href };
  });

  console.log("[Ego Flow] Page Diagnostics:", JSON.stringify(pageInfo, null, 2));
  return { task, page, pageInfo };
}

export async function injectSlatePrompt(page, promptText) {
  console.log(`[Ego Flow] Injecting prompt (${promptText.length} chars)...`);
  
  const success = await page.evaluate((text) => {
    const editor = document.querySelector("[data-slate-editor='true']") || document.querySelector("[contenteditable='true']");
    if (!editor) return false;
    
    editor.focus();
    // Clear and set content
    document.execCommand("selectAll", false, null);
    document.execCommand("insertText", false, text);
    
    // Dispatch input events so Slate state synchronizes
    editor.dispatchEvent(new Event("input", { bubbles: true }));
    editor.dispatchEvent(new Event("change", { bubbles: true }));
    return true;
  }, promptText);

  if (!success) {
    console.warn("[Ego Flow] Fallback to keyboard paste...");
    await page.click("[data-slate-editor='true'], [contenteditable='true']");
    await page.keyboard.paste({ text: promptText });
  }

  // Screenshot to verify input is populated
  await page.screenshot({ path: "C:/Users/HAI/OneDrive/Tài liệu/vmax/shots/ego_flow_prompt_injected.png" });
}

// Standalone runner when invoked via: ego-browser nodejs tools/ego/flow_automation.mjs
if (process.argv[1]?.includes("flow_automation.mjs")) {
  try {
    const { pageInfo } = await initFlowSession();
    console.log("[Ego Flow] Session initialized successfully.");
  } catch (err) {
    console.error("[Ego Flow] Error during initialization:", err);
  }
}
