export function step2(csvData: string[][]): Promise<number> {
  console.log("hello from step 2");

  return new Promise((resolve, reject) => {
    const s2NextBTN = document.getElementById("s2NextBTN") as HTMLButtonElement;
    const s2UsernameColumnSelect = document.getElementById(
      "s2UsernameColumnSelect"
    ) as HTMLSelectElement;

    populateColumnDropdown();

    s2NextBTN.addEventListener("click", () => {
      const selectedOption =
        s2UsernameColumnSelect.options[s2UsernameColumnSelect.selectedIndex];

      if (selectedOption) {
        const selectedUsernameColumn = parseInt(selectedOption.value, 10);
        resolve(selectedUsernameColumn);
      } else {
        reject(new Error("Please select a valid username column."));
      }
    });

    function populateColumnDropdown() {
      s2UsernameColumnSelect.innerHTML = "";

      if (csvData.length > 0) {
        const headerRow = csvData[0];

        for (let index = 0; index < headerRow.length; index++) {
          const columnName = headerRow[index];

          if (columnName.trim() !== "") {
            const option = document.createElement("option");
            option.text = `Column ${index + 1}: ${columnName}`;
            option.value = `${index}`;
            s2UsernameColumnSelect.appendChild(option);
          }
        }
      } else {
        reject(
          new Error("No data available. Please upload a valid CSV file first.")
        );
      }
    }
  });
}
