# README

## Project Overview

This project implements a price negotiation system with three methods for handling customer negotiations:

1. **Custom Negotiation Logic**: Based on the user's input, including sentiment analysis and price offers.
2. **DialogGPT-based Negotiation**: Uses the DialogGPT model to generate chatbot responses.
3. **Gemini-based Negotiation**: Uses Google's Generative AI (Gemini) to handle negotiation dialogue.

## Table of Contents
1. [Installation](#installation)
2. [API Endpoints](#api-endpoints)
3. [Custom Negotiation Logic](#custom-negotiation-logic)
4. [DialogGPT-based Negotiation](#dialoggpt-based-negotiation)
5. [Gemini-based Negotiation](#gemini-based-negotiation)
6. [Configuration](#configuration)

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-repo/negotiation-system.git
cd negotiation-system
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Set up your API keys:
   - For Gemini integration, create an environment variable `API_KEY` containing your Google Gemini API key.

4. Download NLTK data for sentiment analysis:

```bash
python -m nltk.downloader vader_lexicon
```

---

## API Endpoints

### 1. `/products_admin` (GET)
- Returns the full list of products with their current and last prices.

### 2. `/products` (GET)
- Returns the list of product names.

### 3. `/negotiate` (POST)
- Starts the negotiation process for a specific product.

  **Request:**
  ```json
  {
    "product_name": "Laptop"
  }
  ```

  **Response:**
  Redirects to `/start-negotiate/<product_name>`.

### 4. `/start-negotiate/<product_name>` (POST)
- Conducts the price negotiation for the product based on user input and sentiment analysis.

  **Request:**
  ```json
  {
    "user_text": "I can pay $45000 for the Laptop. Please offer a discount."
  }
  ```

  **Response:**
  ```json
  {
    "initial_price": 55000,
    "lowest_price": 50000,
    "user_price": 45000,
    "happiness_level": 7,
    "new_price": 52500,
    "message": "After considering your input, the new negotiated price for Laptop is 52500."
  }
  ```

### 5. `/negotiate_dialogpt` (POST)
- Uses DialogGPT to handle negotiation conversations.

  **Request:**
  ```json
  {
    "offer": 45000,
    "last_price": 50000,
    "message": "I can't afford more than $45000."
  }
  ```

  **Response:**
  ```json
  {
    "bot_message": "How about we meet at $48000?",
    "price": 48000
  }
  ```

### 6. `/negotiate_gemini` (POST)
- Uses Google's Gemini AI to handle negotiation conversations.

  **Request:**
  ```json
  {
    "offer": 45000,
    "last_price": 50000,
    "message": "I can't afford more than $45000."
  }
  ```

  **Response:**
  ```json
  {
    "bot_message": "After considering your offer, how about we meet at $47500?",
    "price": 47500
  }
  ```

---

## Custom Negotiation Logic

The custom logic calculates a new price based on:
- **Initial Price**: The current price of the product.
- **Lowest Price**: The lowest price the system can offer.
- **User's Happiness Level**: Determined using sentiment analysis (VADER).
- **User's Offer**: Extracted from the user's input using Named Entity Recognition (NER).

The system ensures that the final price doesn't drop below the lowest price.

---

## DialogGPT-based Negotiation

This method uses the `microsoft/DialoGPT-medium` model to handle customer dialogues and generate natural responses based on user input.

### Example:
- User: "I can only pay $45000."
- DialogGPT: "How about $47500? Does that work for you?"

---

## Gemini-based Negotiation

This method leverages **Google's Gemini AI** to handle the negotiation. You must set your API key as an environment variable (`API_KEY`).

### Example:
- User: "I can only pay $45000."
- Gemini: "Let's meet at $47500. How does that sound?"

---

## Configuration

### Environment Variables
- **API_KEY**: Required for Gemini integration.

```bash
export API_KEY=your_gemini_api_key
```

### Dependencies
- Flask
- Transformers (for DialoGPT)
- google-generativeai (for Gemini)
- Spacy (for NER)
- NLTK (for sentiment analysis)

Make sure to configure these correctly before running the server.

---

## Run the Application

To run the application in development mode, use:

```bash
python app.py
```

The Flask app will start at `http://127.0.0.1:5000/`.

---

This project allows for flexible negotiation strategies, making it ideal for various e-commerce or customer service platforms.
