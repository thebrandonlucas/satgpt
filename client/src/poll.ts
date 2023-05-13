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

// There are two ways to query the server to get different responses:
// When a r_hash isn't included in the request, we just get the invoice back
// To check a payment, we send the r_hash
export async function queryServer(
  queryData: string,
  isRequestingInvoice: boolean = true
): Promise<InvoiceResponse | ChatGPTResponse> {
  const baseUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000/query";
  const url = `${baseUrl}/query`;
  const headers = { "Content-Type": "application/json" };
  const data = isRequestingInvoice
    ? { query: queryData }
    : { r_hash: queryData };

  const response = await fetch(url, {
    method: "POST",
    headers,
    body: JSON.stringify(data),
  });

  const responseData = await response.json();
  return { ...responseData, status: response.status };
}

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
