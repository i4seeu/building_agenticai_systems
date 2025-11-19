# Agent Examples

This folder contains practical examples of agentic AI systems demonstrating different techniques and patterns.

## Examples

### 1. Prompt Chaining (`prompt_chaining.py`)

**Purpose**: Demonstrates the pipeline pattern for breaking down complex tasks into a sequence of smaller, manageable sub-problems.

**Technique**: 
- Step 1: Extract technical specifications from raw text
- Step 2: Transform specifications into structured JSON format
- Output: Well-formed JSON with key specifications

**Key Concepts**:
- Divide-and-conquer strategy for complex problems
- Each step has a specific, well-scoped task
- Output from one prompt feeds into the next
- Improves interpretability and debuggability

**Usage**:
```bash
# Ensure OPENAI_API_KEY is set in ../.env
python prompt_chaining.py
```

**Requirements**:
- `langchain-openai`
- `langchain-core`
- `dotenv`
- OpenAI API key in `../.env`

---

### 2. Herbs Information Extraction (`herbs_info_extraction.py`)

**Purpose**: Extracts structured medicinal plant information from research papers using prompt chaining with validation and re-extraction.

**Technique**:
- **Step 1 (Extract)**: Use targeted LLM prompts to extract 16 fields from paper text
  - Title, Authors, Year
  - Scientific names, Medicinal use, Biological activity
  - Dose, Phytochemicals, Plant parts
  - Formulation, Botanic description
  - Toxicity, Adverse reactions
  - Health benefits, Nutritional benefits
  - Reference (APA formatted)

- **Step 2 (Validate)**: Check extraction completeness and identify missing/incomplete fields

- **Step 3 (Re-extract)**: Use focused prompts to fill gaps in missing data

**Key Concepts**:
- Multi-step prompt chaining with validation
- Targeted re-extraction for improved accuracy
- Structured data extraction from unstructured text
- Error handling and graceful degradation

**Usage**:
```bash
# Ensure OPENAI_API_KEY is set in ../.env
python herbs_info_extraction.py
```

The script will:
1. Extract information from the dummy research paper
2. Display validation results
3. Re-extract any missing fields
4. Output results in JSON and table formats

**Output Example**:
```
================================================================================
HERB INFORMATION EXTRACTION - PROMPT CHAINING PIPELINE
================================================================================

[STEP 1] Extracting initial information from the research paper...
✓ Initial extraction complete.

[STEP 2] Validating extracted information...
✓ Validation complete. 2 field(s) need attention:
  - year: partial (confidence: 30.0%)
  - formulation: partial (confidence: 30.0%)

[STEP 3] Re-extracting missing or incomplete fields...
✓ Re-extraction complete.

[FINAL VALIDATION]
Complete fields: 15/16
```

**Requirements**:
- `langchain-openai`
- `langchain-core`
- `dotenv`
- OpenAI API key in `../.env`

---

### 3. Routing Lesson (`routing_lesson.py`)

**Purpose**: Demonstrates how to route user requests or intermediate outputs to different sub-agents or tools based on intent or content. Useful for building multi-tool agents where specific tasks (e.g., search, calculator, database lookup) are handled by specialized components.

**Technique**:
- Use a lightweight classifier (LLM-based or rule-based) to determine intent or required capability.
- Route the request to the appropriate handler (tool/agent) and collect responses.
- Optionally aggregate or summarize results with a final LLM step.

**Key Concepts**:
- Intent classification and routing
- Tool/agent interfaces and contracts (inputs/outputs)
- Fallback strategies and confidence thresholds
- Aggregation and final summary prompts

**Usage**:
```bash
# Ensure OPENAI_API_KEY is set in ../.env
python routing_lesson.py
```

**Requirements**:
- `langchain-openai`
- `langchain-core`
- `dotenv`
- Any tool-specific client libraries used by handlers (documented in the file)
- OpenAI API key in `../.env`

---

### 4. Parallel Agents (`parellel_agents.py`)

**Purpose**: Demonstrates concurrent execution of multiple independent tasks using `RunnableParallel` for efficient multi-step processing with final synthesis.

**Technique**:
- **Step 1 (Parallel Execution)**: Run three independent chains in parallel:
  - **Summarize Chain**: Generates a concise summary of the topic
  - **Questions Chain**: Generates three interesting questions about the topic
  - **Terms Chain**: Identifies 5-10 key terms from the topic

- **Step 2 (Synthesis)**: Combine parallel results using a synthesis prompt that creates a comprehensive answer integrating all outputs

**Key Concepts**:
- `RunnableParallel` for concurrent execution of independent tasks
- `RunnablePassthrough` to preserve original input while processing
- Async processing with `ainvoke()` for non-blocking execution
- Efficient resource utilization by executing independent chains simultaneously
- Final aggregation step to synthesize parallel outputs

**Workflow**:
```
Input Topic
    ↓
┌───────────────────────────────────┐
│   Execute in Parallel:            │
├───────────────────────────────────┤
│ • Summarize      (Chain 1)        │
│ • Generate Q's   (Chain 2)        │
│ • Extract Terms  (Chain 3)        │
│ • Pass Through   (Original input) │
└───────────────────────────────────┘
    ↓
Combine Results (summary, questions, terms, topic)
    ↓
Synthesis Prompt
    ↓
LLM Processing
    ↓
Final Comprehensive Answer
```

**Usage**:
```bash
# Ensure OPENAI_API_KEY is set in ../.env
python parellel_agents.py
```

**Output Example**:
```
--- Running Parallel LangChain Example for Topic: 'The history of space exploration' ---

--- Final Response ---
[Comprehensive synthesis combining summary, questions, key terms, and original topic]
```

**Requirements**:
- `langchain-openai`
- `langchain-core`
- `dotenv`
- OpenAI API key in `../.env`
- Python 3.7+ (for `asyncio.run()`)

**Performance Benefit**:
Instead of executing tasks sequentially (Sum of all execution times), parallel execution reduces total runtime to the longest individual chain's execution time, ideal for I/O-bound operations like LLM API calls.

---

### 5. Reflection Code (`reflection_code.py`)

**Purpose**: Demonstrates an iterative self-improvement loop where an AI agent generates code, reflects on it critically, and refines it based on feedback until it meets all requirements.

**Technique**:
- **Iteration Loop** (up to 3 cycles):
  - **Stage 1 (Generate/Refine)**: Generate initial Python code or refine it based on previous critiques
  - **Stage 2 (Reflect)**: Act as a senior code reviewer and provide detailed critiques
  - **Stage 3 (Stopping Condition)**: Check if code is perfect; if yes, exit; if no, loop back to refine

**Key Concepts**:
- Self-reflection and iterative improvement
- Multi-role agent (generator + code reviewer)
- Message history for conversational context
- Code review checklist (bugs, style, edge cases, requirements)
- Stopping conditions based on quality criteria

**Workflow**:
```
Input Task Description
    ↓
┌─────────────────────────────────────┐
│  ITERATION LOOP (max 3 cycles):     │
├─────────────────────────────────────┤
│                                     │
│  Stage 1: Generate/Refine Code      │
│       ↓                             │
│  Stage 2: Critique as Code Reviewer │
│       ↓                             │
│  Stage 3: Check if CODE_IS_PERFECT  │
│       ↓ (if not)                    │
│  Add critique to history            │
│  Loop back to Stage 1               │
│       ↓ (if perfect)                │
│  Exit Loop                          │
└─────────────────────────────────────┘
    ↓
Output Final Refined Code
```

**Example Workflow**:
The script demonstrates generating a `calculate_factorial()` function:
1. **Iteration 1**: Generate initial factorial function
2. **Iteration 2**: Critique code (e.g., add better docstrings, handle edge cases)
3. **Iteration 3**: Refine based on feedback; if perfect, return final result

**Usage**:
```bash
# Ensure OPENAI_API_KEY is set in ../.env
python reflection_code.py
```

**Output Example**:
```
========================= REFLECTION LOOP: ITERATION 1 ==========================

>>> STAGE 1: GENERATING initial code...

--- Generated Code (v1) ---
def calculate_factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n == 0:
        return 1
    return n * calculate_factorial(n - 1)

========================= REFLECTION LOOP: ITERATION 2 ==========================

>>> STAGE 1: REFINING code based on previous critique...

>>> STAGE 2: REFLECTING on the generated code...

--- Critique ---
- Add type hints for clarity
- Include more detailed docstring
- Consider iterative approach for large inputs (avoid stack overflow)

========================= FINAL RESULT ===========================

Final refined code after the reflection process:
def calculate_factorial(n: int) -> int:
    """
    Calculate the factorial of a non-negative integer.
    ...
    """
```

**Requirements**:
- `langchain-openai`
- `langchain-core`
- `dotenv`
- OpenAI API key in `../.env` (uses `gpt-4o` for better reasoning)

**Use Cases**:
- Code generation and iterative refinement
- Automated code review and improvement
- Educational demonstrations of AI-driven development
- Multi-stage problem solving with feedback loops

---

### 6. Tool Use Agents (`tool_use_agents.py`)

**Purpose**: Demonstrates how agents can use external tools and functions to answer queries more accurately. The agent decides when and which tools to call based on user input.

**Technique**:
- **Define Tools**: Create reusable tools as decorated functions with clear docstrings describing their purpose
- **Create Agent**: Use `create_agent()` to build an agent with access to tools
- **Agent Loop**: The agent receives a query, decides if it needs a tool, calls it, and synthesizes the result
- **Stream Processing**: Use LangGraph's `.stream()` API to get real-time updates as the agent processes queries

**Key Concepts**:
- Tool definition with `@langchain_tool` decorator
- LangChain's tool-calling mechanism for function invocation
- Agent reasoning and tool selection
- Message-based interaction model
- Event streaming for real-time feedback

**Tool Example**:
The script includes a `search_information` tool that simulates a search engine:
```python
@langchain_tool
def search_information(query: str) -> str:
    """Provides factual information on a given topic."""
    # Simulated search results
    return f"Result for '{query}': ..."
```

**Workflow**:
```
User Query
    ↓
Agent (LLM) processes query
    ↓
Does query need a tool? 
    ├─ Yes → Call appropriate tool(s)
    │         ↓
    │    Tool executes and returns result
    │         ↓
    │    Agent synthesizes tool output into response
    │
    └─ No → Agent provides direct response
    ↓
Stream result to user in real-time
```

**Usage**:
```bash
# Ensure OPENAI_API_KEY is set in ../.env
python tool_use_agents.py
```

**Example Queries**:
- "What is the capital of France?"
- "Can you tell me the weather in London?"
- "What's the population of Earth?"
- "Which is the tallest mountain?"

**Output Example**:
```
=== Tool-Using Agent Demo ===

>>> User Query: What is the capital of France?

--- 🛠 Tool Called: search_information with query: 'capital of france' ---
--- TOOL RESULT: The capital of France is Paris. ---

--- Agent Response ---
The capital of France is Paris.
```

**Requirements**:
- `langchain-openai`
- `langchain-core`
- `langchain` (for `create_agent`)
- `dotenv`
- OpenAI API key in `../.env`

**Key Features**:
- **Tool Discovery**: Tools are automatically available to the agent
- **Semantic Understanding**: Agent understands which tool matches user intent
- **Error Handling**: Graceful fallback if tool calls fail
- **Extensibility**: Easy to add new tools by creating new decorated functions
- **Debug Mode**: `debug=True` enables verbose logging of agent reasoning

**Use Cases**:
- Customer support agents with access to knowledge bases
- Code analysis tools that can search documentation
- Data retrieval agents with database access
- Multi-capability assistants (calculator, search, translation, etc.)
- Task automation with tool-assisted decision making

---

## Setting Up Environment

Before running any agent script, ensure you have:

1. **Python Environment Activated**:
   ```bash
   python -m venv venv
   source .venv/bin/activate
   ```

2. **Dependencies Installed**:
   ```bash
   pip install -r requirements.txt
   ```

3. **OpenAI API Key Set**:
   Create a `.env` file in the parent directory (`../.env` relative to this folder):
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

---

## Common Patterns Demonstrated

### Prompt Chaining
Both examples use the **prompt chaining (pipeline)** pattern:
- Break complex tasks into smaller steps
- Each step is a focused LLM call
- Output flows from one step to the next
- Improves reliability and debuggability

### Error Handling
- Graceful fallback to default values
- Try-catch blocks for API failures
- Informative error messages

### Structured Output
- Data classes for type safety
- JSON serialization for easy integration
- Validation against expected formats

---

## Extending These Examples

To add your own agent example:

1. Create a new file (e.g., `my_agent.py`)
2. Import LLM components:
   ```python
   from langchain_openai import ChatOpenAI
   from langchain_core.prompts import ChatPromptTemplate
   from langchain_core.output_parsers import StrOutputParser
   from dotenv import load_dotenv
   
   load_dotenv("../.env")
   llm = ChatOpenAI(temperature=0)
   ```
3. Define your prompts and chains
4. Build the pipeline with the pipe operator (`|`)
5. Test with sample inputs
6. Document with a similar README

---

## References

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API](https://platform.openai.com/docs/)
- [Prompt Chaining Guide](https://platform.openai.com/docs/guides/prompt-engineering)
