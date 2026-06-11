# 10.1.1 Best Prompting Practices

Prompting is the art of **instruction design**. To get reliable, high-quality responses from an LLM, follow these industry-standard practices (based on OpenAI & Anthropic guides).

## 1. Be Specific and Clear
Vague instructions lead to vague results. 
*   **Bad:** "Write about AI."
*   **Good:** "Write a 3-paragraph summary of the history of Generative AI, focusing on the transition from RNNs to Transformers. Use a professional tone."

## 2. Provide a Persona (Role Prompting)
Giving the model a 'job' sets the context and tone.
*   **Example:** "You are an expert Python Senior Software Engineer. Review the following code for security vulnerabilities and performance bottlenecks."

## 3. Use Few-Shot Prompting
Give the model examples of the desired input-output format. This is the most effective way to ensure consistent formatting.
*   **Example:**
    ```text
    Extract entities from the text.
    Text: "Apple released the iPhone in 2007."
    Output: {"entity": "Apple", "type": "Company", "product": "iPhone", "year": 2007}

    Text: "Tesla unveiled the Cybertruck in Texas."
    Output: {"entity": "Tesla", "type": "Company", "product": "Cybertruck", "year": null}
    ```

## 4. Use Delimiters
Help the model distinguish between instructions and the data it needs to process.
*   **Delimiters:** `###`, `"""`, `---`, `<xml_tags>`.
*   **Example:** "Summarize the text delimited by triple quotes: \"\"\" [text here] \"\"\""

## 5. Specify Output Format
Always tell the model exactly how you want the data returned (JSON, Markdown, CSV, etc.).
*   **Example:** "Return the answer as a valid JSON object with keys 'summary' and 'key_takeaways'."

## 6. Give the Model "Time to Think" (Chain of Thought)
For complex reasoning, ask the model to explain its steps before giving the final answer.
*   **Example:** "First, analyze the problem step-by-step. Then, provide the final Python solution."

## 7. Control Randomness (Temperature)
*   **Temperature = 0.0:** Deterministic, best for coding and extraction.
*   **Temperature = 0.7 - 1.0:** Creative, best for brainstorming and chat.

---

### Standard Prompt Template
```text
[System/Role]: You are a [Persona].
[Context]: Here is some background information: [Data].
[Task]: Perform [Action] on [Data].
[Constraints]: Avoid [X], use [Y] tone, and keep it under [Z] words.
[Format]: Output as [JSON/Markdown].
```
