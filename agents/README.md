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

## Setting Up Environment

Before running any agent script, ensure you have:

1. **Python Environment Activated**:
   ```bash
   cd /Users/noordeenmalango/Desktop/research_projects/agenticai_systems
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
