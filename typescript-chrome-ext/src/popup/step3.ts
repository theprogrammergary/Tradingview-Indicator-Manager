export function step3(
  csvData: string[][],
  selectedUsernameColumn: number
): Promise<string[]> {
  return new Promise((resolve, reject) => {
    if (selectedUsernameColumn < 0) {
      reject(new Error("Invalid username column."));
      return;
    }

    const usernames = csvData
      .map((row) => row[selectedUsernameColumn])
      .filter(Boolean)
      .slice(1);

    const s3UsernamesList = document.getElementById(
      "s3UsernamesList"
    ) as HTMLDivElement;
    s3UsernamesList.innerHTML = usernames
      .map((username) => `<div>${username}</div>`)
      .join("");

    const s3StartBTN = document.getElementById(
      "s3StartBTN"
    ) as HTMLButtonElement;
    s3StartBTN.addEventListener("click", () => resolve(usernames));
  });
}
