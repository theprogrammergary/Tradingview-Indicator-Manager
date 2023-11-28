async function getList(pineId: string, sessionid: string): Promise<string[]> {
  const userList: string[] = [];
  let counter = 1;
  let user_count = 1;
  let nextUrl: string | null = `/pine_perm/list_users/?limit=10&order_by=-created`;

  while (nextUrl !== null) {
      const listHeaders = {
          cookie: `sessionid=${sessionid}`,
          origin: 'https://www.tradingview.com',
          referer: 'https://www.tradingview.com',
          contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
      };

      const nextRequest = await fetch(`https://www.tradingview.com${nextUrl}`, {
          method: 'POST',
          body: "pine_id="+pineId,
          headers: listHeaders,
      });

      const requestJSON = await nextRequest.json();
      console.log(requestJSON);

      // const responseBody = requestJSON.results;

      // for (const user of responseBody) {
      //     user_count++;
      //     userList.push(user.username.toLowerCase());
      // }

      // if ('next' in requestJSON) {
      //     nextUrl = requestJSON.next;
      //     counter++;
      // } else {
      //     nextUrl = null;
      // }
  }

  return userList;
  }





