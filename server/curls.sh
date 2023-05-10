# Create the invoice, pricing based on the query length
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the capital of France?"}' \
     http://localhost:5000/query

# Checking payment (if success, you'll get a chatgpt response)
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{ "r_hash": "23cb5236d9bc32e2b90e9926608af26173e02f947511d5574615ff22ff26b24e"}' \
     http://localhost:5000/query
