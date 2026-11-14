// Script inspect chi tiết thanh công cụ dưới đáy của Google Flow
const task = await taskSpace("Google Flow Production");
const page = task.page("p1");

const controlsInfo = await page.evaluate(() => {
  // Tim o nhap prompt
  const editor = document.querySelector("[contenteditable='true'], textarea, [data-slate-editor='true']");
  const editorInfo = editor ? {
    tag: editor.tagName,
    classes: editor.className,
    placeholder: editor.getAttribute("placeholder") || editor.getAttribute("data-placeholder") || editor.innerText,
    hasSlate: editor.hasAttribute("data-slate-editor")
  } : null;

  // Tim cac nut o thanh duoi
  const buttons = Array.from(document.querySelectorAll("button")).map(b => ({
    text: (b.innerText || '').trim(),
    ariaLabel: b.getAttribute("aria-label"),
    role: b.getAttribute("role")
  })).filter(b => b.text || b.ariaLabel);

  return { editorInfo, buttons };
});

console.log("[Ego] Editor:", JSON.stringify(controlsInfo.editorInfo, null, 2));
console.log("[Ego] Buttons Count:", controlsInfo.buttons.length);
console.log("[Ego] Buttons Sample:", JSON.stringify(controlsInfo.buttons.filter(b => 
  b.text.includes("Video") || b.text.includes("Tác nhân") || b.text.includes("giây") || b.ariaLabel
), null, 2));

await task.finish({ keep: ["p1"] });
