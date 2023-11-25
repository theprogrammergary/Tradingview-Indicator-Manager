console.log("Listening to your convos");

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.text) {
      try 
      {
        sendResponse({ data: "we received your message here is your goods" });
        console.log(request);
      } catch (error) {
        console.error("error caught in contentscript");
      }

    }
  }
);
