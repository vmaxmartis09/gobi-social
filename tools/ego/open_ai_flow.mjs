// Script kiểm tra và điều khiển Ego Lite mở WorkflowFree / Google Flow
const task = await taskSpace("AI Flow Video Production");
const pWorkflow = task.page("workflowfree");
await pWorkflow.goto("https://workflowfree.com");
console.log("Navigated to WorkflowFree:", pWorkflow.url);

const pGoogleFlow = task.page("google_flow");
await pGoogleFlow.goto("https://flow.google.com");
console.log("Navigated to Google Flow:", pGoogleFlow.url);

await pWorkflow.screenshot({ path: "shots/ego_workflowfree.png" });
await pGoogleFlow.screenshot({ path: "shots/ego_google_flow.png" });

console.log("Successfully opened AI Flow & Google Flow on Ego Lite!");
