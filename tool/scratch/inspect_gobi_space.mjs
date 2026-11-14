try {
  console.log("Claiming task space 3 (Gobi-space)...");
  const task = await claimTaskSpace(3);
  console.log("Task space claimed, spaceId:", task.spaceId);
  
  const userPage = task.userPage();
  console.log("userPage label:", userPage?.label);
  
  const title = await userPage.title();
  const url = userPage.url();
  console.log("Page title:", title, "URL:", url);
  
  await userPage.screenshot({ path: "/Volumes/Data/gobi-social/shots/ego_userpage.png" });
  console.log("Screenshot saved to shots/ego_userpage.png");
  
  // Also check all pages in task
  // Do not finish task space so we keep user's space open!
} catch (e) {
  console.error("Error inspecting task space 3:", e);
}
