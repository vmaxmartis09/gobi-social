// Script tim element voi userPage()
const task = await claimTaskSpace(19);
const page = task.userPage();

const result = await page.evaluate(() => {
  const all = Array.from(document.querySelectorAll('*'));
  const found = all.filter(el => {
    const text = el.innerText || el.textContent || '';
    const placeholder = el.placeholder || el.getAttribute('placeholder') || el.getAttribute('data-placeholder') || '';
    return text.includes("Bạn muốn tạo những gì") || placeholder.includes("Bạn muốn tạo những gì");
  }).map(el => ({
    tagName: el.tagName,
    className: el.className,
    placeholder: el.placeholder || el.getAttribute('placeholder'),
    id: el.id,
    contentEditable: el.contentEditable,
    role: el.getAttribute("role")
  }));

  const targetEl = all.find(el => {
    const placeholder = el.placeholder || el.getAttribute('placeholder') || el.getAttribute('data-placeholder') || '';
    return placeholder.includes("Bạn muốn tạo những gì");
  }) || all.find(el => (el.innerText || '').includes("Bạn muốn tạo những gì") && el.children.length === 0);

  let rect = null;
  if (targetEl) {
    const r = targetEl.getBoundingClientRect();
    rect = { x: r.x, y: r.y, width: r.width, height: r.height };
  }

  return { found, rect };
});

console.log("[Ego] Result:", JSON.stringify(result, null, 2));
await task.finish({ keep: [] });
