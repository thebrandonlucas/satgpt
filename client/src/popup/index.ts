import "../app.css";
import Prompt from "../components/Prompt.svelte";

const target = document.getElementById("app");

// Inject the Counter component into the DOM at element with id "app"
async function render() {
  // TODO: store conversation
  //   const { count } = await chrome.storage.local.get({ count: 0 });
  //   new Counter({ target, props: { count } });
  new Prompt({ target });
}

document.addEventListener("DOMContentLoaded", render);
