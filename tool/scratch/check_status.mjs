const task = await taskSpace(35);
const tabs = await task.tabs();
console.log("Current tabs in Space 35:");
for (const t of tabs) {
  console.log(`- Tab id=${t.id}, title=${t.title}, url=${t.url}`);
}
