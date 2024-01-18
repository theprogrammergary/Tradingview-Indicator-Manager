import { step1 } from "./step1.js";
import { step2 } from "./step2.js";
import { step3 } from "./step3.js";
import { step4 } from "./step4.js";

const step1_div = document.getElementById("step1") as HTMLDivElement;
const step2_div = document.getElementById("step2") as HTMLDivElement;
const step3_div = document.getElementById("step3") as HTMLDivElement;
const step4_div = document.getElementById("step4") as HTMLDivElement;

document.addEventListener("DOMContentLoaded", () => {
  moveToStep1();

  function moveToStep1() {
    step2_div.classList.add("hidden");
    step3_div.classList.add("hidden");
    step4_div.classList.add("hidden");
    step1_div.classList.remove("hidden");

    step1()
      .then((csvData: string[][]) => {
        moveToStep2(csvData);
      })
      .catch((error: Error) => {
        console.error("Step 1 error:", error);
      });
  }

  function moveToStep2(csvData: string[][]) {
    step1_div.classList.add("hidden");
    step3_div.classList.add("hidden");
    step4_div.classList.add("hidden");
    step2_div.classList.remove("hidden");

    step2(csvData)
      .then((selectedColumn: number) => {
        moveToStep3(csvData, selectedColumn);
      })
      .catch((error) => {
        console.error("Step 2 error:", error);
      });
  }

  function moveToStep3(csvData: string[][], selectedUsernameColumn: number) {
    step1_div.classList.add("hidden");
    step2_div.classList.add("hidden");
    step4_div.classList.add("hidden");
    step3_div.classList.remove("hidden");

    step3(csvData, selectedUsernameColumn)
      .then((usernames) => {
        moveToStep4(usernames);
      })
      .catch((error) => {
        console.error("Step 3 error:", error);
      });
  }

  function moveToStep4(usernames: string[]) {
    step1_div.classList.add("hidden");
    step2_div.classList.add("hidden");
    step3_div.classList.add("hidden");
    step4_div.classList.remove("hidden");

    step4(usernames)
      .then(() => {})
      .catch((error) => {
        console.error("Step 4 error:", error);
      });
  }
});
