<script lang="ts">
  import {
    queryServer,
    type InvoiceResponse,
    type ChatGPTResponse,
  } from "../poll";

  let selectedOption = ""; // Holds the selected option value
  let prompt = "";

  // paymentRequest and paymentHash are two different names for invoice and r_hash
  let paymentRequest = "";
  let paymentHash = "";
  let chatGPTMessage = "";

  // Function to handle dropdown selection
  function handleOptionSelect(event: Event) {
    const target = event.target as HTMLSelectElement;
    selectedOption = target.value;
  }

  async function handleSubmit(event: Event) {
    event.preventDefault();

    // TODO: allow user to select model
    const { invoice, r_hash } = (await queryServer(prompt)) as InvoiceResponse;
    paymentRequest = invoice;
    paymentHash = r_hash;
  }

  async function checkPaid() {
    const { message, status } = (await queryServer(
      paymentHash,
      false
    )) as ChatGPTResponse;

    console.log({ message, status });

    // Show the chatgpt response (or a payment required error)
    chatGPTMessage = message;
  }
</script>

<main>
  <h1>SatGPT</h1>

  <form on:submit={handleSubmit}>
    <input
      type="text"
      id="input"
      placeholder="Send a message"
      bind:value={prompt}
    />

    <label for="dropdown">Model:</label>
    <select id="dropdown" on:change={handleOptionSelect}>
      <option value="">Select an option</option>
      <option value="GPT-3.5">GPT-3.5</option>
      <option value="GPT-4">GPT-4</option>
    </select>

    <button type="submit">Submit</button>
  </form>

  <p>Selected Option: {selectedOption}</p>

  {#if paymentRequest}
    <p class="break-all">Invoice: {paymentRequest}</p>
    <button on:click={checkPaid}>Check payment</button>
  {/if}

  {#if chatGPTMessage}
    <p>{chatGPTMessage}</p>
  {/if}
</main>

<style>
  main {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f7931a;
    color: #ffffff;
    font-family: Arial, sans-serif;
  }

  h1 {
    font-size: 24px;
    margin-bottom: 20px;
  }

  label {
    font-size: 16px;
  }

  input,
  select {
    width: 100%;
    padding: 10px;
    font-size: 14px;
    margin-bottom: 10px;
    border: none;
    border-radius: 4px;
    @apply text-black;
  }

  p {
    font-size: 14px;
    margin-top: 20px;
  }
</style>
