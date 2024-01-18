(function () {
  async function main() {
    const pineID = await getPineID();

    if (pineID) {
      chrome.storage.local
        .set({ pineID: pineID })
        .catch((error) => console.log(error));
    }

    async function getPineID(): Promise<string | null> {
      try {
        const PINE_ID_SELECTOR: string = `#tv-content > div > div > div.tv-chart-view__section > div.tv-chart-view__permission-block.tv-chart-view__permission-block--invite-only-access-granted > div.tv-chart-view__script-actions > button.tv-social-stats__item.i-checked.js-chart-view__manage-access.apply-common-tooltip.tv-social-stats__item--button`;

        const element = document.querySelector(PINE_ID_SELECTOR);

        if (element) {
          const dataScriptIdPart = element.getAttribute("data-script-id-part");

          if (dataScriptIdPart) {
            return dataScriptIdPart;
          }
        }

        return null;
      } catch (error) {
        return null;
      }
    }
  }

  main();
})();
