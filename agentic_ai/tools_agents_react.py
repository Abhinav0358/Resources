"""
AI Foundations: 10.2 Tools, Agents, and ReAct

This script demonstrates how an AI 'Agent' works by implementing a
ReAct (Reason + Act) loop from scratch.

ECOSYSTEM OVERVIEW:
- Hugging Face: The 'GitHub' of AI. Provides models (Transformers), datasets, and tools (Spaces).
- LangChain: A framework for building LLM apps. It provides standard interfaces for
  Chains, Agents, and Memory.

WHAT IS AN AGENT?
An agent is an LLM that is given 'Tools' (functions) and a control loop to solve tasks.
The most common pattern is ReAct:
1. Question: The user's goal.
2. Thought: The model reasoning about what to do next.
3. Action: The model choosing a tool to call.
4. Observation: The output of that tool.
5. (Repeat until finished)
6. Final Answer: The result.
"""

import json


# --- 1. DEFINE TOOLS ---
def get_stock_price(symbol):
    """Returns the price of a stock."""
    # Mock data
    stocks = {"AAPL": 175.50, "GOOGL": 140.20, "TSLA": 210.10}
    price = stocks.get(symbol.upper(), "Unknown")
    return f"The price of {symbol} is ${price}."


def calculate(expression):
    """Evaluates a simple mathematical expression."""
    try:
        # Note: eval is dangerous in production, used here for simplicity.
        return f"Result: {eval(expression)}"
    except Exception as e:
        return f"Error: {str(e)}"


# Tool Registry
AVAILABLE_TOOLS = {"get_stock_price": get_stock_price, "calculate": calculate}

# --- 2. THE SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are an AI Agent with access to the following tools:
- get_stock_price(symbol): Get the current price of a stock.
- calculate(expression): Perform math calculations.

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [get_stock_price, calculate]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!
"""


# --- 3. MOCK LLM (Simulating an LLM response) ---
def mock_llm_response(prompt):
    """
    In a real app, this would call OpenAI, Ollama, or Anthropic.
    Here, we simulate the 'next step' the LLM would generate.
    """
    if (
        "Question: How much is 5 shares of AAPL worth?" in prompt
        and "Observation" not in prompt
    ):
        return "Thought: I need to find the price of AAPL first.\nAction: get_stock_price\nAction Input: AAPL"

    if (
        "Observation: The price of AAPL is $175.5." in prompt
        and "Final Answer" not in prompt
    ):
        return "Thought: I have the price ($175.5). Now I need to multiply it by 5.\nAction: calculate\nAction Input: 175.5 * 5"

    if "Observation: Result: 877.5" in prompt:
        return "Thought: I have the total value.\nFinal Answer: 5 shares of AAPL are worth $877.5."

    return "Thought: I am not sure how to help."


# --- 4. THE AGENT LOOP (The Engine) ---
def run_agent(question):
    print(f"--- STARTING AGENT ---")
    print(f"User Question: {question}\n")

    # Initialize the prompt with the system instructions and the question
    current_prompt = SYSTEM_PROMPT + f"\nQuestion: {question}"

    for i in range(5):  # Max 5 steps to prevent infinite loops
        # 1. Ask the LLM for the next thought/action
        response = mock_llm_response(current_prompt)
        print(response)

        current_prompt += "\n" + response

        # 2. Check if the LLM provided a Final Answer
        if "Final Answer:" in response:
            break

        # 3. Parse the Action and Action Input (Regex or String split)
        if "Action:" in response and "Action Input:" in response:
            action = response.split("Action:")[1].split("\n")[0].strip()
            action_input = response.split("Action Input:")[1].split("\n")[0].strip()

            # 4. Call the tool (Observation)
            if action in AVAILABLE_TOOLS:
                observation = AVAILABLE_TOOLS[action](action_input)
                print(f"Observation: {observation}")
                current_prompt += f"\nObservation: {observation}"
            else:
                print(f"Observation: Error - Tool {action} not found.")
                current_prompt += f"\nObservation: Error - Tool {action} not found."

    print("\n--- AGENT FINISHED ---")


if __name__ == "__main__":
    run_agent("How much is 5 shares of AAPL worth?")
