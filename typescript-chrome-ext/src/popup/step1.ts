export function step1(): Promise<string[][]> {
  console.log("hello from step 1");

  return new Promise((resolve, reject) => {
    const s1UploadFileInput = document.getElementById(
      "s1UploadFileInput"
    ) as HTMLInputElement;
    const csvUploadLabel = document.getElementById(
      "s1UploadFileLabel"
    ) as HTMLLabelElement;

    let csvData: string[][] = [];

    s1UploadFileInput.addEventListener("change", (e) => {
      const file = s1UploadFileInput.files?.[0];
      if (file) {
        csvUploadLabel.textContent = file.name;

        const reader = new FileReader();
        reader.onload = (event) => {
          const result = event.target?.result as string;
          csvData = parseCSV(result);
          resolve(csvData);
        };
        reader.onerror = (error) => {
          reject(error);
        };
        reader.readAsText(file);
      } else {
        csvUploadLabel.textContent = "Upload";
      }
    });

    function parseCSV(csvText: string): string[][] {
      const rows = csvText.split("\n");
      const data = rows.map((row) => row.split(","));
      return data;
    }
  });
}
