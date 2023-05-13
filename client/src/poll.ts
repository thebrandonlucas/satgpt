export interface InvoiceResponse {
  invoice: string;
  r_hash: string;
  message: string;
  status: number;
}

export interface ChatGPTResponse {
  message: string;
  status: number;
}

export interface QueryRequest {
  query?: string;
  r_hash?: string;
  model_selected?: string;
}

// There are two ways to query the server to get different responses:
// When a r_hash isn't included in the request, we just get the invoice back
// To check a payment, we send the r_hash
export async function queryServer(
  queryData: QueryRequest
): Promise<InvoiceResponse | ChatGPTResponse> {
  const baseUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000/query";
  const url = `${baseUrl}/query`;
  const headers = { "Content-Type": "application/json" };

  const response = await fetch(url, {
    method: "POST",
    headers,
    body: JSON.stringify(queryData),
  });

  const responseData = await response.json();
  return { ...responseData, status: response.status };
}

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
