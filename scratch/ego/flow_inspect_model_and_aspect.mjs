/**
 * Inspect model selector and aspect ratio in Google Flow
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

const projectUrl = "https://flow.google.com/project/97437688-2b73-4a07-9091-77969b802e73";
await page.goto(projectUrl, { waitUntil: "domcontentloaded" });
await page.waitForTimeout(3000);

// Inspect the settings / model trigger button
const settingsInfo = await page.evaluate(() => {
  const settingsBtn = document.querySelector(".settings-trigger-button") || 
                      Array.from(document.querySelectorAll("button")).find(b => (b.innerText || '').includes("Nano Banana") || (b.innerText || '').includes("crop_"));

  return settingsBtn ? { text: settingsBtn.innerText, className: settingsBtn.className } : null;
});

console.log("[Ego] Settings Button:", JSON.stringify(settingsInfo));

// Click the settings trigger button to see available models and aspect ratios
if (settingsInfo) {
  console.log("[Ego] Clicking settings trigger button...");
  await page.click(".settings-trigger-button");
  await page.waitForTimeout(2000);

  const menuOptions = await page.evaluate(() => {
    const options = Array.from(document.querySelectorAll("[role='menuitem'], [role='option'], .mat-mdc-menu-item, button")).map(el => ({
      text: (el.innerText || '').trim(),
      className: el.className
    })).filter(o => o.text && o.text.length < 50);

    return options.slice(0, 25);
  });

  console.log("[Ego] Settings Menu Options:", JSON.stringify(menuOptions, null, 2));

  const shotMenu = "/Volumes/Data/gobi-social/shots/google_flow_settings_menu.png";
  await page.screenshot({ path: shotMenu });
  console.log("[Ego] Settings menu screenshot saved to:", shotMenu);
}

await task.finish({ keep: [page.label] });
