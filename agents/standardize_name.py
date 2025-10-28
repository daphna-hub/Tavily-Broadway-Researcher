"""
Agent to standardize and validate Broadway show names
"""

from typing import TypedDict
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4.1", temperature=0)


class StandardizeNameState(TypedDict):
    """State for name standardization"""
    input_name: str
    standardized_name: str
    is_valid: bool


class StandardizeNameAgent:
    """Agent that standardizes and validates Broadway show names"""
    
    def __init__(self):
        self.llm = llm
    
    def standardize(self, show_name: str) -> dict:
        """
        Standardize the Broadway show name
        
        Args:
            show_name: Input show name (may be informal or misspelled)
            
        Returns:
            dict with standardized_name and is_valid
        """
        prompt = f"""Given the following input that may be an informal or incomplete Broadway show name, 
provide the complete, official, correctly spelled Broadway show name.

Input: "{show_name}"

Please provide:
1. The official, complete Broadway show name
2. Whether this appears to be a valid, currently running or popular Broadway show (yes/no)

Respond in JSON format:
{{
    "standardized_name": "Official Broadway Show Name",
    "is_valid": true
}}

If you're not sure if it's a valid Broadway show, set is_valid to false."""

        response = self.llm.invoke([{"role": "user", "content": prompt}])
        
        # Try to extract JSON from response
        import json
        import re
        
        content = response.content
        # Look for JSON in the response
        json_match = re.search(r'\{[^}]*\}', content, re.DOTALL)
        
        if json_match:
            try:
                result = json.loads(json_match.group())
                return {
                    "standardized_name": result.get("standardized_name", show_name),
                    "is_valid": result.get("is_valid", True)
                }
            except json.JSONDecodeError:
                pass
        
        # Fallback: just use the show name
        return {
            "standardized_name": show_name,
            "is_valid": True
        }
    
    def __call__(self, state: StandardizeNameState) -> StandardizeNameState:
        """Execute the standardization"""
        result = self.standardize(state["input_name"])
        
        return {
            "standardized_name": result["standardized_name"],
            "is_valid": result["is_valid"]
        }
