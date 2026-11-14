const spaces = await taskSpaces();
console.log("Current task spaces:", spaces.map(s => ({ id: s.id, name: s.name })));
