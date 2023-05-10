import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from ln import add_invoice, lookup_invoice
from db.db import (
    check_invoice_used,
    create_invoices_table,
    set_invoice_used,
    add_r_hash_and_query,
    lookup_query,
)
from util import price, base64_to_hex

# Load env vars
load_dotenv()
# Set up the OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up the Flask app
app = Flask(__name__)


def generate_invoice(query):
    amount = price(query)
    result = add_invoice(amount, f"GPT Query: {query[:20]}...")
    # result contains the payment request and the r_hash
    return result


def check_payment(r_hash):
    # Call the OpenAI API to generate a response
    invoice = lookup_invoice(r_hash)
    # Extract the response text from the API response
    paid = invoice["settled"]
    return (paid, invoice)


# standard chatgpt query
@app.route("/query", methods=["POST"])
def query_chatbot():
    # Parse the request data
    data = request.get_json()

    # if query is not in data, return error
    if "query" not in data and "r_hash" not in data:
        response = jsonify({"message": "No query provided"})
        response.status_code = 400
        print(response)
        return response

    # check if we're in the middle of a payment
    if "r_hash" in data:
        r_hash = data["r_hash"]
        (paid, invoice) = check_payment(r_hash)
        print("invoice", invoice)
        if paid:
            # Check that the invoice hasn't been used before
            if check_invoice_used(r_hash):
                # Return the response to the client
                response = jsonify({"message": "Payment already used"})
                response.status_code = 400
                print(response)
                return response
            else:
                # mark invoice as used
                set_invoice_used(r_hash)

            # lookup the query associated with the r_hash
            query = lookup_query(r_hash)

            # Call the OpenAI API to generate a response
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}]
            )

            # Extract the response text from the API response
            message = completion.choices[0].message.content.strip()

            # Return the response to the client
            response = jsonify({"message": message})
            response.status_code = 200
            print(response)
            return response
        else:
            # Return the response to the client
            response = jsonify(
                {
                    "message": "Payment Required",
                    "payment_request": invoice["payment_request"],
                    "memo": invoice["memo"],
                }
            )
            response.status_code = 402
            print(response)
            return response
    else:
        # If r_hash isn't in request, generate an invoice
        query = data["query"]
        # generate an invoice
        invoice = generate_invoice(query)
        # Return the response to the client
        # convert r_hash from base64 to hex because for some reason LND returns it in base64
        r_hash = base64_to_hex(invoice["r_hash"])
        # add r_hash and query to database
        add_r_hash_and_query(r_hash, query)
        response = jsonify(
            {
                "message": "Payment Required",
                "invoice": invoice["payment_request"],
                "r_hash": r_hash,
            }
        )
        response.status_code = 402
        print(response)
        return response


# TODO: send file data in request
# translate audio files (TODO: list which audio types are supported)
# @app.route('/audio', methods=['GET'])
# def summarize_audio():
#     # Parse the request data
#     data = request.get_json()
#     query = data['query']

#     # Call the OpenAI API to generate a response
#     f = open("testfile.mp3", "rb")
#     transcript = openai.Audio.transcribe("whisper-1", f)
#     prompt = f"Summarize the following text: {transcript}"
#     summary = openai.Completion.create(
#         engine="text-davinci-002",
#         prompt=prompt,
#         max_tokens=60,
#         n=1,
#         stop=None,
#         temperature=0.7,
#     )


#     # Extract the response text from the API response
#     message = summary.choices[0].text.strip()

#     # Return the response to the client
#     return jsonify({'message': message})


# Start the Flask app on localhost:5000
if __name__ == "__main__":
    app.run(debug=True)
    create_invoices_table()