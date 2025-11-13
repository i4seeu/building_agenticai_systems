"""Prompt chaining (Pipeline pattern)

Prompt chaining, sometimes referred to as the Pipeline pattern, represents a powerful
paradigm for handling intricate tasks when leveraging large language models (LLMs).
Rather than expecting an LLM to solve a complex problem in a single, monolithic step,
prompt chaining advocates for a divide-and-conquer strategy. The core idea is to break
down the original, daunting problem into a sequence of smaller, more manageable
sub-problems. Each sub-problem is addressed individually through a specifically
designed prompt, and the output generated from one prompt is strategically fed as
input into the subsequent prompt in the chain.

Use this module to implement chains of prompts where each step focuses on a
well-scoped subtask and hands off results to the next step. This improves
interpretability, reliability, and makes debugging easier compared to monolithic
prompts.
"""

# (Add your prompt-chaining utilities, classes, and examples below.)

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# For better security, load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv("../.env")
# Make sure your OPENAI_API_KEY is set in the .env file
# Initialize the Language Model (using ChatOpenAI is recommended)
llm = ChatOpenAI(temperature=0)
# --- Prompt 1: Extract Information ---
prompt_extract = ChatPromptTemplate.from_template("Extract the technical specifications from the following text:\n\n{text_input}")
# --- Prompt 2: Transform to JSON ---
prompt_transform = ChatPromptTemplate.from_template("Transform the following specifications into a JSON object with 'cpu', 'memory', and 'storage' as keys:\n\n{specifications}")
# --- Build the Chain using LCEL ---
# The StrOutputParser() converts the LLM's message output to a simple string.
extraction_chain = prompt_extract | llm | StrOutputParser()
# The full chain passes the output of the extraction chain into the 'specifications'
# variable for the transformation prompt.
full_chain = (
{"specifications": extraction_chain}
| prompt_transform
| llm
| StrOutputParser()
)
# --- Run the Chain ---
input_text = "The new laptop model features a 3.5 GHz octa-core processor, 16GB of RAM, and a 1TB NVMe SSD."
# Execute the chain with the input text dictionary.
final_result = full_chain.invoke({"text_input": input_text})
print("\n--- Final JSON Output ---")
print(final_result)