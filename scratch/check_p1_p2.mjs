const task = await taskSpace(35);
const p1 = task.page("p1");
const p2 = task.page("p2");

console.log("P1 URL:", p1.url());
console.log("P2 URL:", p2.url());

await p1.screenshot({ path: "/Volumes/Data/gobi-social/shots/p1_openai_auth.png" });
await p2.screenshot({ path: "/Volumes/Data/gobi-social/shots/p2_gmail.png" });

console.log("Screenshots captured to shots/");
