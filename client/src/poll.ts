interface QueryData {
  query: string;
}

async function queryServer(query: string): Promise<any> {
  //   const url = process.env.API_URL || "https://localhost:5000/query";
  const url = process.env.API_URL;
  const headers = { "Content-Type": "application/json" };
  const data: QueryData = { query };

  const response = await fetch(url, {
    method: "POST",
    headers,
    body: JSON.stringify(data),
  });

  const responseData = await response.json();
  return responseData;
}

async function pollServer(query: string) {
  while (true) {
    try {
      const response = await queryServer(query);
      const statusCode = response.status;

      if (statusCode === 200) {
        console.log("Success!");
        break;
      } else if (statusCode !== 402) {
        console.log("Unexpected status code:", statusCode);
        break;
      }

      await delay(5000); // Wait for 5 seconds before making the next request
    } catch (error) {
      console.error("Request failed:", error.message);
      break;
    }
  }
}

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
