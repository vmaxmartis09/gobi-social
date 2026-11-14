const task = await taskSpace();
console.log("Connected to task space id:", task.id);
const tabs = await task.tabs();
console.log("Tabs:", tabs.map(t => ({ title: t.title, url: t.url })));
