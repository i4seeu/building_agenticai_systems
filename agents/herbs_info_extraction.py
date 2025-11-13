"""Herbs Information Extraction using Prompt Chaining

This module demonstrates the prompt chaining technique applied to extract structured
information about medicinal plants from research paper text.

The extraction follows a three-step chain:
1. Extract: Parse the research paper text and extract all 16 fields.
2. Validate: Check if all required fields have been extracted; identify missing fields.
3. Re-extract: For any missing or incomplete fields, run targeted extraction prompts.

This approach improves reliability, interpretability, and makes it easier to debug
which specific fields need attention.
"""

import json
import os
from typing import Dict, List
from dataclasses import dataclass, asdict
from enum import Enum

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("../.env")

# Initialize the Language Model
llm = ChatOpenAI(temperature=0)


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class HerbExtractionResult:
    """Container for extracted herb information from a research paper."""
    title: str
    authors: str
    year: str
    scientific_name: str
    medicinal_use: str
    biological_activity: str
    dose: str
    phytochemicals: str
    plant_part_used: str
    formulation: str
    botanic_description: str
    toxicity: str
    adverse_reactions: str
    health_benefits: str
    nutritional_benefits: str
    reference: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to formatted JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class ExtractionStatus(Enum):
    """Status indicator for extracted fields."""
    COMPLETE = "complete"
    PARTIAL = "partial"
    MISSING = "missing"


@dataclass
class FieldValidation:
    """Validation result for a single field."""
    field_name: str
    value: str
    status: ExtractionStatus
    confidence: float  # 0.0 to 1.0


# ============================================================================
# Step 1: Initial Extraction using LLM
# ============================================================================

def extract_initial_information(paper_text: str) -> HerbExtractionResult:
    """
    Step 1 of the prompt chain: Extract all 16 fields from the research paper text using LLM.
    
    This uses LangChain with ChatOpenAI to parse the paper and extract structured information.
    Each field is extracted with a targeted prompt for precision.
    """
    
    # Define extraction prompts for each field
    extraction_prompts = {
        "title": "Extract the full title of the research paper from the following text. If not available, respond with 'Not available':\n\n{text}",
        "authors": "Extract all authors of the research paper from the following text, separated by commas. If not available, respond with 'Not available':\n\n{text}",
        "year": "Extract the year of publication from the following text. If not available, respond with 'Not available':\n\n{text}",
        "scientific_name": "Extract all scientific names of medicinal plants mentioned in the following text. List them all. If not available, respond with 'Not mentioned':\n\n{text}",
        "medicinal_use": "Extract any medicinal uses mentioned in the following text, i.e., the application of herbs to prevent, diagnose, treat, or manage diseases. If not available, respond with 'Not mentioned':\n\n{text}",
        "biological_activity": "Describe the biological activities of the medicinal plants mentioned in detail from the following text. If not covered, respond with 'Not mentioned':\n\n{text}",
        "dose": "Extract any dosage information including amounts and units from the following text. If not mentioned, respond with 'Not mentioned':\n\n{text}",
        "phytochemicals": "List all phytochemicals present in the medicinal plants mentioned in the following text. If not available, respond with 'Not mentioned':\n\n{text}",
        "plant_part_used": "Describe which part of the plant is used for medicinal purposes from the following text. If not available, respond with 'Not mentioned':\n\n{text}",
        "formulation": "Extract details about the formulation of the medicinal plants (e.g., tablets, capsules, extracts) from the following text. If not available, respond with 'Not mentioned':\n\n{text}",
        "botanic_description": "Provide a detailed botanical description of the plants from the following text, including physical characteristics, structure, and appearance. If not available, respond with 'Not mentioned':\n\n{text}",
        "toxicity": "Extract any information related to the toxicity of the medicinal plants from the following text. If not available, respond with 'Not mentioned':\n\n{text}",
        "adverse_reactions": "List any reported adverse reactions from the following text. If none are mentioned, respond with 'Not mentioned':\n\n{text}",
        "health_benefits": "Describe any health benefits offered by the medicinal plants from the following text. If no benefits are mentioned, respond with 'Not mentioned':\n\n{text}",
        "nutritional_benefits": "Extract any nutritional benefits provided by the medicinal plants from the following text. If not applicable, respond with 'Not mentioned':\n\n{text}",
        "reference": "Extract citation information (title, author(s), year, journal, volume, issue, pages, DOI) and format it as an APA 7th edition reference from the following text. If not available, respond with 'Not mentioned':\n\n{text}",
    }
    
    # Create output parser
    output_parser = StrOutputParser()
    
    # Extract each field using the LLM
    extracted_fields = {}
    for field_name, prompt_template in extraction_prompts.items():
        try:
            # Create prompt and chain
            prompt = ChatPromptTemplate.from_template(prompt_template)
            chain = prompt | llm | output_parser
            
            # Invoke the chain
            result = chain.invoke({"text": paper_text})
            extracted_fields[field_name] = result.strip()
        except Exception as e:
            print(f"Warning: Failed to extract {field_name}: {str(e)}")
            extracted_fields[field_name] = "Not mentioned"
    
    # Create result object
    result = HerbExtractionResult(
        title=extracted_fields.get("title", "Not available"),
        authors=extracted_fields.get("authors", "Not available"),
        year=extracted_fields.get("year", "Not available"),
        scientific_name=extracted_fields.get("scientific_name", "Not mentioned"),
        medicinal_use=extracted_fields.get("medicinal_use", "Not mentioned"),
        biological_activity=extracted_fields.get("biological_activity", "Not mentioned"),
        dose=extracted_fields.get("dose", "Not mentioned"),
        phytochemicals=extracted_fields.get("phytochemicals", "Not mentioned"),
        plant_part_used=extracted_fields.get("plant_part_used", "Not mentioned"),
        formulation=extracted_fields.get("formulation", "Not mentioned"),
        botanic_description=extracted_fields.get("botanic_description", "Not mentioned"),
        toxicity=extracted_fields.get("toxicity", "Not mentioned"),
        adverse_reactions=extracted_fields.get("adverse_reactions", "Not mentioned"),
        health_benefits=extracted_fields.get("health_benefits", "Not mentioned"),
        nutritional_benefits=extracted_fields.get("nutritional_benefits", "Not mentioned"),
        reference=extracted_fields.get("reference", "Not mentioned"),
    )
    
    return result


# ============================================================================
# Step 2: Validation
# ============================================================================

def validate_extraction(extraction: HerbExtractionResult) -> Dict[str, FieldValidation]:
    """
    Step 2 of the prompt chain: Validate the extracted information.
    
    Check which fields are complete, partial, or missing.
    Return a validation report for each field.
    """
    
    validations = {}
    fields = extraction.to_dict()
    
    for field_name, value in fields.items():
        # Determine status based on the value
        if value in ("Not mentioned", "Not available", ""):
            status = ExtractionStatus.MISSING
            confidence = 0.0
        elif len(value.strip()) < 5:
            status = ExtractionStatus.PARTIAL
            confidence = 0.3
        else:
            status = ExtractionStatus.COMPLETE
            confidence = 0.9
        
        validations[field_name] = FieldValidation(
            field_name=field_name,
            value=value,
            status=status,
            confidence=confidence
        )
    
    return validations


def get_missing_fields(validations: Dict[str, FieldValidation]) -> List[str]:
    """Extract the list of fields that are missing or incomplete."""
    missing = []
    for field_name, validation in validations.items():
        if validation.status in (ExtractionStatus.MISSING, ExtractionStatus.PARTIAL):
            missing.append(field_name)
    return missing


# ============================================================================
# Step 3: Re-extraction of Missing Fields using LLM
# ============================================================================

def re_extract_missing_fields(
    paper_text: str,
    missing_fields: List[str],
    initial_extraction: HerbExtractionResult
) -> HerbExtractionResult:
    """
    Step 3 of the prompt chain: Re-extract missing or incomplete fields using targeted LLM prompts.
    
    For each missing field, create a focused extraction prompt to maximize accuracy.
    """
    
    # Create a copy of the initial extraction
    updated_extraction = HerbExtractionResult(**initial_extraction.to_dict())
    
    # Detailed re-extraction prompts for each field
    re_extraction_prompts = {
        "scientific_name": "Please carefully re-read the following text and extract ALL scientific names of medicinal plants. Look for binomial nomenclature (Genus species). Provide a comprehensive list:\n\n{text}",
        "year": "Please carefully re-read the following text and extract the publication year. Look for any mention of when this work was published or conducted:\n\n{text}",
        "medicinal_use": "Please carefully re-read the following text and provide detailed information about medicinal uses. How are these herbs used to treat, prevent, or manage diseases:\n\n{text}",
        "dose": "Please carefully re-read the following text and extract ALL dosage information mentioned. Include amounts, units, frequency, and administration routes:\n\n{text}",
        "phytochemicals": "Please carefully re-read the following text and list ALL phytochemicals, active compounds, or chemical constituents mentioned:\n\n{text}",
        "plant_part_used": "Please carefully re-read the following text and describe which specific parts of the plant are used (root, leaf, stem, flower, seed, etc.):\n\n{text}",
        "formulation": "Please carefully re-read the following text and extract details about how these plants are formulated (tablets, capsules, extracts, powders, teas, etc.):\n\n{text}",
        "botanic_description": "Please carefully re-read the following text and provide a detailed botanical description including physical characteristics, structure, appearance, and growth habits:\n\n{text}",
        "toxicity": "Please carefully re-read the following text and extract any information about toxicity, safety profiles, or toxic effects:\n\n{text}",
        "adverse_reactions": "Please carefully re-read the following text and list any adverse reactions, side effects, or contraindications mentioned:\n\n{text}",
        "health_benefits": "Please carefully re-read the following text and describe all health benefits mentioned for these medicinal plants:\n\n{text}",
        "nutritional_benefits": "Please carefully re-read the following text and extract information about nutritional benefits, vitamins, minerals, or nutritional value:\n\n{text}",
        "reference": "Please carefully re-read the following text and extract complete citation information (title, authors, year, journal, volume, issue, pages, DOI). Format this as an APA 7th edition reference:\n\n{text}",
    }
    
    output_parser = StrOutputParser()
    
    for field in missing_fields:
        if field in re_extraction_prompts:
            try:
                # Create and invoke the re-extraction chain
                prompt = ChatPromptTemplate.from_template(re_extraction_prompts[field])
                chain = prompt | llm | output_parser
                result = chain.invoke({"text": paper_text})
                
                # Update the field if we got a non-empty result
                if result and result.strip() and result.strip().lower() not in ("not mentioned", "not available", ""):
                    setattr(updated_extraction, field, result.strip())
            except Exception as e:
                print(f"Warning: Failed to re-extract {field}: {str(e)}")
    
    return updated_extraction


# ============================================================================
# Dummy Research Paper
# ============================================================================

DUMMY_RESEARCH_PAPER = """
Title: Therapeutic Potential and Phytochemical Profile of Turmeric (Curcuma longa) 
and Ginger (Zingiber officinale) in Managing Inflammation and Oxidative Stress

Authors: Dr. Amelia Harris, Prof. James Mitchell, Dr. Sophia Chen

Year: 2023

Abstract:
This research paper explores the medicinal use of two widely studied herbs: turmeric and ginger. 
Both have been used in traditional medicine for thousands of years to treat various ailments.

Scientific Name:
The primary plant investigated is Curcuma longa, commonly known as turmeric. Secondary investigations 
involved Zingiber officinale, known as ginger.

Medicinal Use:
Both turmeric and ginger are used to prevent, diagnose, treat, and manage diseases and health conditions. 
Traditionally, they have been applied to manage inflammation, arthritis, digestive disorders, and metabolic syndrome.

Biological Activity:
The biological activities of Curcuma longa include anti-inflammatory, antioxidant, and hepatoprotective effects. 
Zingiber officinale exhibits anti-nausea, analgesic, and immunomodulatory activities. The active compounds 
in turmeric suppress NF-κB signaling pathways, while ginger's gingerols inhibit prostaglandin synthesis.

Dose:
Clinical studies have employed turmeric at doses ranging from 500mg to 1500mg daily, divided into 2-3 doses. 
Ginger extract has been effectively administered at 2-4 grams per day in capsule or powder form.

Phytochemicals:
Turmeric contains curcumin, demethoxycurcumin, and bisdemethoxycurcumin as primary constituents. 
Ginger is rich in 6-gingerol, 6-shogaol, zingerone, and paradol. Both plants also contain polyphenols and terpenoids.

Plant Part Used:
The rhizome (underground stem) of both Curcuma longa and Zingiber officinale is used for medicinal purposes. 
The dried rhizomes are processed into powder, extract, or used fresh in formulations.

Formulation:
Commercial formulations include tablets, capsules, extracts, and standardized powders. 
Standardized extracts typically contain 95% curcuminoids in turmeric products and 5% gingerols in ginger products.

Botanic Description:
Curcuma longa is a perennial herbaceous plant standing 60-90 cm in height with broad, elongated leaves. 
The rhizome is cylindrical, bright yellow internally, and aromatic. Zingiber officinale is a rhizomatous perennial 
with slender stems, lance-shaped leaves, and small yellowish flowers. Both thrive in tropical and subtropical climates.

Toxicity:
Both turmeric and ginger are generally recognized as safe (GRAS) by regulatory agencies. 
No significant toxicity has been observed at therapeutic doses. However, excessive doses (>8g/day for turmeric) 
may cause gastric irritation in sensitive individuals.

Adverse Reactions:
Mild gastrointestinal effects such as nausea, diarrhea, or stomach upset have been reported in some users. 
Turmeric may cause allergic reactions in individuals with turmeric allergy. Ginger can cause mild heartburn 
or mouth irritation when consumed in fresh form.

Health Benefits:
Both herbs offer significant health benefits including reduced joint pain, improved digestion, enhanced immune response, 
and better management of chronic inflammation. Epidemiological studies suggest reduced risk of cardiovascular disease 
and cognitive decline with regular consumption.

Nutritional Benefits:
Turmeric and ginger provide essential minerals including manganese, iron, and potassium. They are also rich in vitamins, 
particularly vitamin C and B vitamins. Both are excellent sources of dietary fiber and contain minimal fat and calories.

Reference:
Harris, A., Mitchell, J., & Chen, S. (2023). Therapeutic potential and phytochemical profile of turmeric (Curcuma longa) 
and ginger (Zingiber officinale) in managing inflammation and oxidative stress. Journal of Medicinal Plant Research, 15(3), 
245-267. https://doi.org/10.1234/jmpr.2023.15.3.245
"""


# ============================================================================
# Main Extraction Pipeline (Prompt Chaining)
# ============================================================================

def extract_herb_information(paper_text: str, verbose: bool = True) -> HerbExtractionResult:
    """
    Main function implementing the prompt chaining pipeline for herb information extraction.
    
    Step 1: Extract initial information from the paper.
    Step 2: Validate the extracted data.
    Step 3: Re-extract any missing or incomplete fields.
    
    Args:
        paper_text: The research paper text to extract from.
        verbose: If True, print progress information.
    
    Returns:
        HerbExtractionResult: Fully extracted herb information.
    """
    
    if verbose:
        print("\n" + "="*80)
        print("HERB INFORMATION EXTRACTION - PROMPT CHAINING PIPELINE")
        print("="*80)
    
    # ---- Step 1: Extract ----
    if verbose:
        print("\n[STEP 1] Extracting initial information from the research paper...")
    extraction = extract_initial_information(paper_text)
    if verbose:
        print("✓ Initial extraction complete.")
    
    # ---- Step 2: Validate ----
    if verbose:
        print("\n[STEP 2] Validating extracted information...")
    validations = validate_extraction(extraction)
    missing_fields = get_missing_fields(validations)
    
    if verbose:
        print(f"✓ Validation complete. {len(missing_fields)} field(s) need attention:")
        for field in missing_fields:
            validation = validations[field]
            print(f"  - {field}: {validation.status.value} (confidence: {validation.confidence:.1%})")
    
    # ---- Step 3: Re-extract ----
    if missing_fields:
        if verbose:
            print("\n[STEP 3] Re-extracting missing or incomplete fields...")
        extraction = re_extract_missing_fields(paper_text, missing_fields, extraction)
        if verbose:
            print(f"✓ Re-extraction complete. Attempting to fill {len(missing_fields)} field(s).")
    else:
        if verbose:
            print("\n[STEP 3] All fields are complete. No re-extraction needed.")
    
    # ---- Final Validation ----
    if verbose:
        print("\n[FINAL VALIDATION]")
        final_validations = validate_extraction(extraction)
        complete_count = sum(1 for v in final_validations.values() if v.status == ExtractionStatus.COMPLETE)
        print(f"Complete fields: {complete_count}/16")
    
    return extraction


# ============================================================================
# Main Execution
# ============================================================================

if __name__ == "__main__":
    # Run the extraction pipeline on the dummy research paper
    result = extract_herb_information(DUMMY_RESEARCH_PAPER, verbose=True)
    
    # Display the final extracted result
    print("\n" + "="*80)
    print("EXTRACTED INFORMATION (JSON FORMAT)")
    print("="*80)
    print(result.to_json())
    
    # Display the final extracted result as a formatted table
    print("\n" + "="*80)
    print("EXTRACTED INFORMATION (TABLE FORMAT)")
    print("="*80)
    for field_name, value in result.to_dict().items():
        print(f"{field_name:25s}: {value}")
