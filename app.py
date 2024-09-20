from flask import Flask, jsonify, request, redirect, url_for
import random
from dialogpt_chatbot import * 
from gemini_chatbot import *
from negotiate import extract_price, get_happiness_level, calculate_new_price

products = {
    "Laptop": {"price": 55000, "last_price": 50000},
    "Tablet": {"price": 18000, "last_price": 15000},
    "Smart Watch": {"price": 12000, "last_price": 10000},
    "Headphones": {"price": 7000, "last_price": 6000},
    "Bluetooth Speaker": {"price": 4000, "last_price": 3500},
    "Camera": {"price": 45000, "last_price": 42000},
    "Gaming Console": {"price": 35000, "last_price": 33000},
    "Smart TV": {"price": 60000, "last_price": 55000},
    "Monitor": {"price": 15000, "last_price": 13000},
    "Phone": {"price": 25000, "last_price": 21000}
}

app = Flask(__name__)

# Set up pricing rules
MIN_PRICE = 80
MAX_PRICE = 100

@app.route('/products_admin', methods=['GET'])
def get_products():
    return jsonify(products)

# Route to return only product names
@app.route('/products', methods=['GET'])
def get_product_names():
    product_names = list(products.keys())
    return jsonify(product_names)

# Route to handle negotiation initiation
@app.route('/negotiate', methods=['POST'])
def negotiate():
    data = request.json
    product_name = data.get('product_name')

    if product_name not in products:
        return jsonify({"error": "Product not found"}), 404

    # Redirect to /start-negotiate with the product name and price
    return redirect(url_for('start_negotiate', product_name=product_name))


# Route to handle negotiation process
@app.route('/start-negotiate/<product_name>', methods=['POST'])
def start_negotiate(product_name):
    if product_name not in products:
        return jsonify({"error": "Product not found"}), 404

    initial_price = products[product_name]['price']
    lowest_price = products[product_name]['last_price']

    # Get user input and extract the offered price and sentiment
    user_text = request.json.get('user_text')
    user_price = extract_price(user_text)
    happiness_level = get_happiness_level(user_text)

    if user_price is None:
        return jsonify({"error": "No valid price found in the user's input."}), 400

    # Perform negotiation rounds
    new_price = calculate_new_price(initial_price, lowest_price, happiness_level)

    # Response back to the user
    response = {
        "initial_price": initial_price,
        "lowest_price": lowest_price,
        "user_price": user_price,
        "happiness_level": happiness_level,
        "new_price": new_price,
        "message": f"After considering your input, the new negotiated price for {product_name} is {new_price}."
    }

    return jsonify(response)



@app.route('/negotiate_dialogpt', methods=['POST'])
def negotiate_dialogpt():
    user_offer = float(request.json['offer'])
    last_price = float(request.json['last_price'])
    user_message = request.json['message']
    
    # Generate AI-based response using DialoGPT (can replace with Gemini later)
    ai_response = get_chatbot_response(f"User says: {user_message}. The last price was {last_price}.")
    
    if user_offer >= last_price:
        return jsonify({"bot_message": ai_response + " Offer accepted!", "final_price": user_offer})
    
    elif user_offer < MIN_PRICE:
        return jsonify({"bot_message": ai_response + f" Can't go below ${MIN_PRICE}. Final offer: ${MIN_PRICE}", "final_price": MIN_PRICE})
    
    else:
        counter_offer = max(user_offer + random.randint(5, 10), MIN_PRICE)
        return jsonify({"bot_message": ai_response + f" How about we meet at ${counter_offer}?", "price": counter_offer})

@app.route('/negotiate_gemini', methods=['POST'])
def negotiate_gemini():
    user_offer = float(request.json['offer'])
    last_price = float(request.json['last_price'])
    user_message = request.json['message']
    
    # Generate AI-based response using Gemini
    prompt=f"The customer says: '{user_message}'. The last price was {last_price}. Respond as a negotiating chatbot.",

    ai_response = get_gemini_response(prompt)
    
    if user_offer >= last_price:
        return jsonify({"bot_message": ai_response + " Offer accepted!", "final_price": user_offer})
    
    elif user_offer < MIN_PRICE:
        return jsonify({"bot_message": ai_response + f" We can't go below ${MIN_PRICE}. Final offer: ${MIN_PRICE}", "final_price": MIN_PRICE})
    
    else:
        counter_offer = max(user_offer + random.randint(5, 10), MIN_PRICE)
        return jsonify({"bot_message": ai_response + f" How about we meet at ${counter_offer}?", "price": counter_offer})



if __name__ == "__main__":
    app.run(debug=True)
