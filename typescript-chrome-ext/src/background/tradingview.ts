interface ResponseJson {
  results: any;
  next?: string;
}

(function () {
  class Tradingview {
    ADD_ACCESS_URL: string = "https://www.tradingview.com/pine_perm/add/";
    REMOVE_ACCESS_URL: string = "https://www.tradingview.com/pine_perm/remove/";
    USER_ACCESS_LIST_URL: string =
      "https://www.tradingview.com/pine_perm/list_users/?limit=10&order_by=-created";

    async add(username: string, pine_id: string): Promise<string> {
      try {
        const payload = new FormData();
        payload.append("pine_id", pine_id);
        payload.append("username_recip", username);
        payload.append("noExpiration", "true");

        const response = await fetch(this.ADD_ACCESS_URL, {
          method: "POST",
          body: payload,
        });

        switch (response.status) {
          case 200:
            return `✅ ALREADY HAD ACCESS: ${username}`;
          case 201:
            return `✅ ADDED: ${username}`;
          case 422:
            return `❌ TV USERNAME NOT VALID: ${username}`;
          default:
            return `❌ FAILED TO ADD: ${username}`;
        }
      } catch (error) {
        console.error(`Error in adding ${username}:`, error);
        return `❗️ ERROR IN ADDING: ${username}`;
      }
    }

    async remove(username: string, pine_id: string): Promise<string> {
      try {
        const payload = new FormData();
        payload.append("pine_id", pine_id);
        payload.append("username_recip", username);
        payload.append("noExpiration", "true");

        const response = await fetch(this.REMOVE_ACCESS_URL, {
          method: "POST",
          body: payload,
        });

        switch (response.status) {
          case 200:
          case 201:
            return `✅ REMOVED: ${username}`;
          case 422:
            return `❌ TV USERNAME NOT VALID: ${username}`;
          default:
            return `❌ FAILED TO REMOVE: ${username}`;
        }
      } catch (error) {
        console.error(`Error in removing ${username}:`, error);
        return `❗️ ERROR IN REMOVING: ${username}`;
      }
    }

    async getUserList(pine_id: string): Promise<string[]> {
      const user_list: string[] = [];

      try {
        const payload = new FormData();
        payload.append("pine_id", pine_id);

        let next_url: string | null =
          "/pine_perm/list_users/?limit=10&order_by=user__username";

        while (next_url !== null) {
          const response = await fetch(
            `https://www.tradingview.com${next_url}`,
            {
              method: "POST",
              body: payload,
            }
          );

          const responseJson: ResponseJson = await response.json();

          responseJson.results.forEach((user: any) => {
            user_list.push(user.username.toLowerCase());
          });

          next_url = responseJson.next || null;
        }
      } catch (error) {
        console.error(`Error in getting user list for ${pine_id}:`, error);
      }

      console.log(user_list);
      return user_list;
    }
  }

  async function main() {
    const tradingview = new Tradingview();
    const pineID = await readPineID();
    const activeUsers = await readActiveUsers();
    if (!activeUsers || !pineID) {
      return;
    }

    const tradingviewUsers = await tradingview.getUserList(pineID);
    if (!tradingviewUsers) {
      return;
    }

    const [addList, removeList] = compareUserLists(
      tradingviewUsers,
      activeUsers
    );

    if (!addList && !removeList) {
      return;
    }

    await chrome.runtime.sendMessage({
      action: "list management",
      data: {
        id: pineID,
        tvUsers: tradingviewUsers,
        activeUsers: activeUsers,
        add: addList,
        remove: removeList,
      },
    });

    await listManagement(tradingview, pineID, addList, removeList);
  }

  async function readActiveUsers(): Promise<string[]> {
    const usernames = await new Promise<string[]>((resolve) => {
      chrome.storage.local.get(["tradingviewUsernames"], function (result) {
        console.log(result);
        resolve(result.tradingviewUsernames || []);
      });
    });

    return usernames;
  }

  async function readPineID(): Promise<string> {
    const pineID = await new Promise<string>((resolve) => {
      chrome.storage.local.get(["pineID"], function (result) {
        console.log(result);
        resolve(result.pineID || "");
      });
    });

    return pineID;
  }

  function compareUserLists(
    tvList: string[],
    newList: string[]
  ): [string[], string[]] {
    const adding: string[] = newList.filter((user) => !tvList.includes(user));
    const removing: string[] = tvList.filter((user) => !newList.includes(user));

    return [adding, removing];
  }

  async function listManagement(
    tradingview: Tradingview,
    pineID: string,
    addList: string[],
    removeList: string[]
  ): Promise<void> {
    if (pineID) {
      for (const username of addList) {
        const result = await tradingview.add(username, pineID);
        chrome.runtime.sendMessage({ action: "adding - ", data: result });
      }

      for (const username of removeList) {
        const result = await tradingview.remove(username, pineID);
        chrome.runtime.sendMessage({ action: "removing - ", data: result });
      }
    }
  }
  main();
})();
