const spaces = await listTaskSpaces();
console.log("All spaces:", spaces.map(s => ({ id: s.id, name: s.name, titles: s.recentTabTitles })));

// Let's claim space 0 or open a task space to check Google Flow
const task = await claimTaskSpace(0);
console.log("Claimed space 0:", task.spaceId);
const pages = task.userPage() ? [task.userPage()] : [];
console.log("User page url:", task.userPage()?.url ? await task.userPage().url() : "none");
