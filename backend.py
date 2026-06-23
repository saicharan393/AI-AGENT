
from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
import os

load_dotenv()

client = OpenAI(
    base_url="http://localhost:11434/v1/",
    api_key="ollama"   # Required but ignored by Ollama
)

# -------------------------
# TOOLS
# -------------------------

def get_weather(city: str):
    """Get current weather information."""
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=%C+%t",
            timeout=10
        )

        if response.status_code == 200:
            return f"The weather in {city} is {response.text}."

        return "Unable to fetch weather information."

    except Exception as e:
        return f"Weather API Error: {str(e)}"


def get_stockprice(symbol: str):
    """Get latest stock price."""
    try:
        api_key = "NQKTFVU9LY44R7LL"

        url = (
            "https://www.alphavantage.co/query"
            f"?function=GLOBAL_QUOTE"
            f"&symbol={symbol.upper()}"
            f"&apikey={api_key}"
        )

        response = requests.get(url, timeout=10)
        data = response.json()

        if "Note" in data:
            return "Alpha Vantage API limit reached. Please try later."

        quote = data.get("Global Quote")

        if not quote:
            return f"No stock data found for '{symbol}'."

        price = float(quote["05. price"])
        change = float(quote["09. change"])
        percent = quote["10. change percent"]

        change_text = (
            f"-${abs(change):.2f}"
            if change < 0
            else f"${change:.2f}"
        )

        return (
            f"📈 {symbol.upper()} Stock Price: ${price:.2f}\n"
            f"💵 Change: {change_text} ({percent})"
        )

    except Exception as e:
        return f"Stock API Error: {str(e)}"


def run_command(cmd: str):
    """
    Execute system commands.
    WARNING: Dangerous. Remove if not needed.
    """
    try:
        result = os.popen(cmd).read()

        if result.strip():
            return result

        return "Command executed."

    except Exception as e:
        return f"Command Error: {str(e)}"


available_tools = {
    "get_weather": get_weather,
    "get_stockprice": get_stockprice,
    "run_command": run_command,
}

# -------------------------
# SYSTEM PROMPT
# -------------------------

SYSTEM_PROMPT = """
You are a helpful AI assistant.

You work in:

plan -> action -> observe -> output

Rules:
- Always respond in valid JSON.
- Perform only one step at a time.
- After observation, provide the final output.
- When using get_stockprice, preserve the '$' symbols exactly.
- Do not rewrite tool outputs.

JSON Format:

{
    "step": "plan|action|output",
    "content": "text",
    "function": "tool name",
    "input": "tool input"
}

Available Tools:
- get_weather: Gets weather using city name.
- get_stockprice: Gets stock prices using symbols (AAPL, TSLA, MSFT).
- run_command: Executes system commands.

Examples:

User: What is the weather in Hyderabad?

{"step":"plan","content":"User wants weather information."}
{"step":"action","function":"get_weather","input":"Hyderabad"}
{"step":"output","content":"The weather in Hyderabad is sunny."}

User: What is the stock price of Tesla?

{"step":"plan","content":"User wants Tesla stock price."}
{"step":"action","function":"get_stockprice","input":"TSLA"}
{"step":"output","content":"📈 TSLA Stock Price: $328.75\\n💵 Change: -$2.12 (-0.64%)"}
"""

# -------------------------
# AGENT
# -------------------------

def run_agent(query, chat_history=None):

    if chat_history is None:
        chat_history = []

    logs = []

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ] + chat_history + [
        {
            "role": "user",
            "content": query
        }
    ]

    max_iterations = 10

    try:
        for _ in range(max_iterations):

            response = client.chat.completions.create(
                model="qwen2.5-coder:14b",
                response_format={"type": "json_object"},
                messages=messages,
            )

            content = response.choices[0].message.content
            print("MODEL RESPONSE:", content)

            try:
                parsed = json.loads(content)

            except Exception:
                return {
                    "answer": content,
                    "logs": logs
                }

            logs.append(parsed)

            step = parsed.get("step", "").lower()

            # PLAN
            if step == "plan":

                messages.append({
                    "role": "assistant",
                    "content": json.dumps(parsed)
                })

                continue

            # ACTION
            elif step == "action":

                tool_name = parsed.get("function")
                tool_input = parsed.get("input")

                if tool_name not in available_tools:
                    return {
                        "answer": f"Unknown tool: {tool_name}",
                        "logs": logs
                    }

                output = available_tools[tool_name](tool_input)

                observation = {
                    "step": "observe",
                    "output": output
                }

                logs.append(observation)

                # Return tool output directly
                if tool_name in ["get_stockprice", "get_weather"]:
                    return {
                        "answer": output,
                        "logs": logs
                    }

                messages.append({
                    "role": "assistant",
                    "content": json.dumps(parsed)
                })

                messages.append({
                    "role": "user",
                    "content": json.dumps(observation)
                })

                continue

            # OUTPUT
            elif step == "output":

                return {
                    "answer": parsed.get("content", ""),
                    "logs": logs
                }

            else:
                return {
                    "answer": f"Unexpected step: {step}",
                    "logs": logs
                }

        return {
            "answer": "Agent stopped after reaching maximum iterations.",
            "logs": logs
        }

    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "logs": logs
        }