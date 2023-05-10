<script lang="ts">
  let selectedOption = ""; // Holds the selected option value

  // Function to handle dropdown selection
  function handleOptionSelect(event: Event) {
    const target = event.target as HTMLSelectElement;
    selectedOption = target.value;
  }

  function handleSubmit(event: Event) {
    event.preventDefault();
    const input = document.getElementById("input") as HTMLInputElement;
    const prompt = input.value;
    console.log(prompt);
  }
</script>

<main class="bitcoin-orange-theme">
  <h1>SatGPT</h1>

  <form on:submit={handleSubmit}>
    <label for="input">Input:</label>
    <input type="text" id="input" placeholder="Prompt" />

    <label for="dropdown">Dropdown:</label>
    <select id="dropdown" on:change={handleOptionSelect}>
      <option value="">Select an option</option>
      <option value="GPT-3.5">GPT-3.5</option>
      <option value="GPT-4">GPT-4</option>
    </select>

    <button type="submit">Submit</button>
  </form>

  <p>Selected Option: {selectedOption}</p>
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
