const task = await claimTaskSpace(2);
console.log("Task methods:", Object.getOwnPropertyNames(Object.getPrototypeOf(task)));
console.log("Task properties:", Object.keys(task));
await task.finish({ keep: [] });
