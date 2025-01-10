import os
import google.generativeai as genai

# Load API key from environment
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in environment variables.")

# Configure the API key
genai.configure(api_key=gemini_api_key)

# Example generation config; adjust as needed
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the model with system instructions
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "You are a financial assistant. When a user requests a financial operation "
        "(e.g., buy_stock, sell_stock, transfer_funds, pay_credit_card, get_account_balance, get_brokerage_value), "
        "respond ONLY with a JSON object following this exact format:\n"
        "You are a financial assistant. When a user requests a financial operation (e.g., buy_stock, sell_stock, transfer_funds, pay_credit_card, get_account_balance, get_brokerage_value), respond ONLY with a JSON object describing the intent and parameters. No extra text or disclaimers.",

        # ==============================
        # 3 EXAMPLES: TRANSFER_FUNDS
        # ==============================
        "input: Can you move 300 dollars from my savings account to my brokerage so I can buy more stocks?",
        "output: \"{\\n\"\n        '  \"intent\": \"TRANSFER_FUNDS\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"amount\": 300,\\n'\n        '      \"from_account\": \"savings\",\\n'\n        '      \"to_account\": \"brokerage\"\\n'\n        \"  }\\n}\\n\\n\"",

        "input: I want to take 800 out of my checking and deposit it into my savings.",
        "output: \"{\\n\"\n        '  \"intent\": \"TRANSFER_FUNDS\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"amount\": 800,\\n'\n        '      \"from_account\": \"checking\",\\n'\n        '      \"to_account\": \"savings\"\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Please transfer 120 from checking to savings for a quick deposit.",
        "output: \"{\\n\"\n        '  \"intent\": \"TRANSFER_FUNDS\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"amount\": 120,\\n'\n        '      \"from_account\": \"checking\",\\n'\n        '      \"to_account\": \"savings\"\\n'\n        \"  }\\n}\\n\\n\"",

        # ==============================
        # 3 EXAMPLES: GET_ACCOUNT_BALANCE
        # ==============================
        "input: What’s my balance in checking right now?",
        "output: \"{\\n\"\n        '  \"intent\": \"GET_ACCOUNT_BALANCE\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"account_type\": \"checking\"\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Could you tell me how much I have in my savings?",
        "output: \"{\\n\"\n        '  \"intent\": \"GET_ACCOUNT_BALANCE\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"account_type\": \"savings\"\\n'\n        \"  }\\n}\\n\\n\"",

        "input: What's my current balance on that credit card?",
        "output: \"{\\n\"\n        '  \"intent\": \"GET_ACCOUNT_BALANCE\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"account_type\": \"credit card\"\\n'\n        \"  }\\n}\\n\\n\"",

        # ==============================
        # 3 EXAMPLES: BUY_STOCK
        # ==============================
        "input: I’d like to buy 5 shares of AAPL in my brokerage, can you handle that?",
        "output: \"{\\n\"\n        '  \"intent\": \"BUY_STOCK\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 1,\\n'\n        '      \"ticker\": \"AAPL\",\\n'\n        '      \"shares\": 5\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Purchase 10 shares of TSLA in brokerage account number 2.",
        "output: \"{\\n\"\n        '  \"intent\": \"BUY_STOCK\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 2,\\n'\n        '      \"ticker\": \"TSLA\",\\n'\n        '      \"shares\": 10\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Buy 2 shares of AMZN using my main brokerage account.",
        "output: \"{\\n\"\n        '  \"intent\": \"BUY_STOCK\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 1,\\n'\n        '      \"ticker\": \"AMZN\",\\n'\n        '      \"shares\": 2\\n'\n        \"  }\\n}\\n\\n\"",

        # ==============================
        # 3 EXAMPLES: SELL_STOCK
        # ==============================
        "input: Please sell 2 shares of Apple stock from my brokerage.",
        "output: \"{\\n\"\n        '  \"intent\": \"SELL_STOCK\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 1,\\n'\n        '      \"ticker\": \"AAPL\",\\n'\n        '      \"shares\": 2\\n'\n        \"  }\\n}\\n\\n\"",

        "input: I want to offload 5 TSLA shares from brokerage account 1.",
        "output: \"{\\n\"\n        '  \"intent\": \"SELL_STOCK\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 1,\\n'\n        '      \"ticker\": \"TSLA\",\\n'\n        '      \"shares\": 5\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Sell 3 shares of MSFT for me, I have them in brokerage #2.",
        "output: \"{\\n\"\n        '  \"intent\": \"SELL_STOCK\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 2,\\n'\n        '      \"ticker\": \"MSFT\",\\n'\n        '      \"shares\": 3\\n'\n        \"  }\\n}\\n\\n\"",

        # ==============================
        # 3 EXAMPLES: PAY_CREDIT_CARD
        # ==============================
        "input: Could you pay 150 dollars toward my credit card from checking?",
        "output: \"{\\n\"\n        '  \"intent\": \"PAY_CREDIT_CARD\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"from_account\": \"checking\",\\n'\n        '      \"credit_card_account\": \"credit card\",\\n'\n        '      \"amount\": 150\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Make a 100-dollar payment on my card using my savings.",
        "output: \"{\\n\"\n        '  \"intent\": \"PAY_CREDIT_CARD\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"from_account\": \"savings\",\\n'\n        '      \"credit_card_account\": \"credit card\",\\n'\n        '      \"amount\": 100\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Send 75 from my checking to pay off my credit card balance.",
        "output: \"{\\n\"\n        '  \"intent\": \"PAY_CREDIT_CARD\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"from_account\": \"checking\",\\n'\n        '      \"credit_card_account\": \"credit card\",\\n'\n        '      \"amount\": 75\\n'\n        \"  }\\n}\\n\\n\"",

        # ==============================
        # 3 EXAMPLES: GET_BROKERAGE_VALUE
        # ==============================
        "input: How much is my brokerage account worth right now?",
        "output: \"{\\n\"\n        '  \"intent\": \"GET_BROKERAGE_VALUE\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 1\\n'\n        \"  }\\n}\\n\\n\"",

        "input: What’s the total value of my stock portfolio?",
        "output: \"{\\n\"\n        '  \"intent\": \"GET_BROKERAGE_VALUE\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 1\\n'\n        \"  }\\n}\\n\\n\"",

        "input: I need to see how much my brokerage is currently worth, please.",
        "output: \"{\\n\"\n        '  \"intent\": \"GET_BROKERAGE_VALUE\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 1\\n'\n        \"  }\\n}\\n\\n\"",
    ),
)

def generate_text(prompt: str) -> str:
    """
    Sends a prompt to Gemini and returns its text response.
    """
    response = model.generate_content(prompt)
    return response.text

def generate_text_stream(prompt: str):
    """
    Streams a response from Gemini (if needed).
    """
    response_stream = model.generate_content(prompt, stream=True)
    for chunk in response_stream:
        yield chunk.text

#
# Example: Demonstrate how you can pass multiple lines in a single iteration
#
def generate_multi_example():
    """
    Showcases 3 examples for each of the 6 operations (total 18 examples)
    in the input/output format. The response will be a single LLM output
    that attempts to interpret or follow these instructions.
    """
    lines = [
        "You are a financial assistant. When a user requests a financial operation (e.g., buy_stock, sell_stock, transfer_funds, pay_credit_card, get_account_balance, get_brokerage_value), respond ONLY with a JSON object describing the intent and parameters. No extra text or disclaimers.",

        # ==============================
        # 3 EXAMPLES: TRANSFER_FUNDS
        # ==============================
        "input: Can you move 300 dollars from my savings account to my brokerage so I can buy more stocks?",
        "output: \"{\\n\"\n        '  \"intent\": \"TRANSFER_FUNDS\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"amount\": 300,\\n'\n        '      \"from_account\": \"savings\",\\n'\n        '      \"to_account\": \"brokerage\"\\n'\n        \"  }\\n}\\n\\n\"",

        "input: I want to take 800 out of my checking and deposit it into my savings.",
        "output: \"{\\n\"\n        '  \"intent\": \"TRANSFER_FUNDS\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"amount\": 800,\\n'\n        '      \"from_account\": \"checking\",\\n'\n        '      \"to_account\": \"savings\"\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Please transfer 120 from checking to savings for a quick deposit.",
        "output: \"{\\n\"\n        '  \"intent\": \"TRANSFER_FUNDS\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"amount\": 120,\\n'\n        '      \"from_account\": \"checking\",\\n'\n        '      \"to_account\": \"savings\"\\n'\n        \"  }\\n}\\n\\n\"",

        # ==============================
        # 3 EXAMPLES: GET_ACCOUNT_BALANCE
        # ==============================
        "input: What’s my balance in checking right now?",
        "output: \"{\\n\"\n        '  \"intent\": \"GET_ACCOUNT_BALANCE\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"account_type\": \"checking\"\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Could you tell me how much I have in my savings?",
        "output: \"{\\n\"\n        '  \"intent\": \"GET_ACCOUNT_BALANCE\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"account_type\": \"savings\"\\n'\n        \"  }\\n}\\n\\n\"",

        "input: What's my current balance on that credit card?",
        "output: \"{\\n\"\n        '  \"intent\": \"GET_ACCOUNT_BALANCE\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"account_type\": \"credit card\"\\n'\n        \"  }\\n}\\n\\n\"",

        "input: What is my credit card balance?",
        "output: \"{\\n\"\n        '  \"intent\": \"GET_ACCOUNT_BALANCE\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"account_type\": \"credit card\"\\n'\n        \"  }\\n}\\n\\n\"",

        "input: How much do I owe on my credit card right now?",
        "output: \"{\\n\"\n        '  \"intent\": \"GET_ACCOUNT_BALANCE\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"account_type\": \"credit card\"\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Could you check the balance on my credit card account?",
        "output: \"{\\n\"\n        '  \"intent\": \"GET_ACCOUNT_BALANCE\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"account_type\": \"credit card\"\\n'\n        \"  }\\n}\\n\\n\"",

        # ==============================
        # 3 EXAMPLES: BUY_STOCK
        # ==============================
        "input: I’d like to buy 5 shares of AAPL in my brokerage, can you handle that?",
        "output: \"{\\n\"\n        '  \"intent\": \"BUY_STOCK\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 1,\\n'\n        '      \"ticker\": \"AAPL\",\\n'\n        '      \"shares\": 5\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Purchase 10 shares of TSLA in brokerage account number 2.",
        "output: \"{\\n\"\n        '  \"intent\": \"BUY_STOCK\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 2,\\n'\n        '      \"ticker\": \"TSLA\",\\n'\n        '      \"shares\": 10\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Buy 2 shares of AMZN using my main brokerage account.",
        "output: \"{\\n\"\n        '  \"intent\": \"BUY_STOCK\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 1,\\n'\n        '      \"ticker\": \"AMZN\",\\n'\n        '      \"shares\": 2\\n'\n        \"  }\\n}\\n\\n\"",

        # ==============================
        # 3 EXAMPLES: SELL_STOCK
        # ==============================
        "input: Please sell 2 shares of Apple stock from my brokerage.",
        "output: \"{\\n\"\n        '  \"intent\": \"SELL_STOCK\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 1,\\n'\n        '      \"ticker\": \"AAPL\",\\n'\n        '      \"shares\": 2\\n'\n        \"  }\\n}\\n\\n\"",

        "input: I want to offload 5 TSLA shares from brokerage account 1.",
        "output: \"{\\n\"\n        '  \"intent\": \"SELL_STOCK\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 1,\\n'\n        '      \"ticker\": \"TSLA\",\\n'\n        '      \"shares\": 5\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Sell 3 shares of MSFT for me, I have them in brokerage #2.",
        "output: \"{\\n\"\n        '  \"intent\": \"SELL_STOCK\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 2,\\n'\n        '      \"ticker\": \"MSFT\",\\n'\n        '      \"shares\": 3\\n'\n        \"  }\\n}\\n\\n\"",

        # ==============================
        # 3 EXAMPLES: PAY_CREDIT_CARD
        # ==============================
        "input: Could you pay 150 dollars toward my credit card from checking?",
        "output: \"{\\n\"\n        '  \"intent\": \"PAY_CREDIT_CARD\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"from_account\": \"checking\",\\n'\n        '      \"credit_card_account\": \"credit card\",\\n'\n        '      \"amount\": 150\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Make a 100-dollar payment on my card using my savings.",
        "output: \"{\\n\"\n        '  \"intent\": \"PAY_CREDIT_CARD\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"from_account\": \"savings\",\\n'\n        '      \"credit_card_account\": \"credit card\",\\n'\n        '      \"amount\": 100\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Send 75 from my checking to pay off my credit card balance.",
        "output: \"{\\n\"\n        '  \"intent\": \"PAY_CREDIT_CARD\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"from_account\": \"checking\",\\n'\n        '      \"credit_card_account\": \"credit card\",\\n'\n        '      \"amount\": 75\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Send 75 from my checking to pay off my credit card balance.",
        "output: \"{\\n\"\n        '  \"intent\": \"PAY_CREDIT_CARD\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"from_account\": \"checking\",\\n'\n        '      \"credit_card_account\": \"credit card\",\\n'\n        '      \"amount\": 75\\n'\n        \"  }\\n}\\n\\n\"",

        "input: Pay 100 dollars on my credit card using funds from my savings account.",
        "output: \"{\\n\"\n        '  \"intent\": \"PAY_CREDIT_CARD\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"from_account\": \"savings\",\\n'\n        '      \"credit_card_account\": \"credit card\",\\n'\n        '      \"amount\": 100\\n'\n        \"  }\\n}\\n\\n\"",

        "input: I need to transfer 50 to my credit card from checking to reduce my balance.",
        "output: \"{\\n\"\n        '  \"intent\": \"PAY_CREDIT_CARD\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"from_account\": \"checking\",\\n'\n        '      \"credit_card_account\": \"credit card\",\\n'\n        '      \"amount\": 50\\n'\n        \"  }\\n}\\n\\n\"",

        # ==============================
        # 3 EXAMPLES: GET_BROKERAGE_VALUE
        # ==============================
        "input: How much is my brokerage account worth right now?",
        "output: \"{\\n\"\n        '  \"intent\": \"GET_BROKERAGE_VALUE\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 1\\n'\n        \"  }\\n}\\n\\n\"",

        "input: What’s the total value of my stock portfolio?",
        "output: \"{\\n\"\n        '  \"intent\": \"GET_BROKERAGE_VALUE\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 1\\n'\n        \"  }\\n}\\n\\n\"",

        "input: I need to see how much my brokerage is currently worth, please.",
        "output: \"{\\n\"\n        '  \"intent\": \"GET_BROKERAGE_VALUE\",\\n'\n        '  \"parameters\": {\\n'\n        '      \"brokerage_id\": 1\\n'\n        \"  }\\n}\\n\\n\"",
    ]
    response = model.generate_content(lines)
    return response.text
