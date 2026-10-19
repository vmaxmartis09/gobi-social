const { taskSpace } = require('ego-browser');
const ts = taskSpace();
console.log('SPACES:', JSON.stringify(ts.spaces.map(s => ({ id: s.id, name: s.name, pages: s.pages.map(p => ({ title: p.title, url: p.url })) })), null, 2));
