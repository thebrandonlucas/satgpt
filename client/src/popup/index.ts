import "../app.css";
import Counter from "../components/Counter.svelte";

const target = document.getElementById("app");

// Inject the Counter component into the DOM at element with id "app"
async function render() {
  const { count } = await chrome.storage.local.get({ count: 0 });
  new Counter({ target, props: { count } });
}

document.addEventListener("DOMContentLoaded", render);
