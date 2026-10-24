const task = await claimTaskSpace(2);
const tabs = await task.tabs();
console.log("Tabs:", tabs.map(t => ({ id: t.id, title: t.title, label: t.label })));
if (tabs.length > 0) {
  const p = await task.adopt(tabs[tabs.length - 1]);
  const btn = await p.evaluate(() => {
    const b = Array.from(document.querySelectorAll("button")).find(el => (el.innerText || '').includes("Generate"));
    return b ? { text: b.innerText, disabled: b.disabled || b.className.includes("is-disabled") } : null;
  });
  console.log("Generate Button:", btn);
  await task.finish({ keep: tabs.map(t => t.label) });
} else {
  await task.finish({ keep: [] });
}
