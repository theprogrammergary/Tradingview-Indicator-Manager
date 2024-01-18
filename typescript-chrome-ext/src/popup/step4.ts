export function step4(usernames: string[]): Promise<void> {
  console.log("hello from step 4");

  chrome.storage.local
    .set({ tradingviewUsernames: usernames })
    .catch((error) => console.log(error));

  chrome.runtime.sendMessage({
    action: "new list management",
    data: { activeUsers: usernames },
  });

  return new Promise((resolve, reject) => {});
}
