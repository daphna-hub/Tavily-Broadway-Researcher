"""
Main orchestrator for Broadway Show Research System
"""

from agents.standardize_name import StandardizeNameAgent
from agents.ratings_agent import FindRatingsAgent
from agents.tickets_agent import FindTicketsAgent
from agents.compile_report import CompileReportAgent
from agents.image_agent import FindImageAgent
from agents.extended_report_agent import ExtendedReportAgent
import sys


def run_pipeline(show_name: str):
    """Run the complete research pipeline"""
    # Agent 1: Standardize name
    standardize_agent = StandardizeNameAgent()
    name_result = standardize_agent.standardize(show_name)
    
    if not name_result["is_valid"]:
        return f"""⚠️ Warning: "{show_name}" may not be a valid Broadway show, 
or we couldn't find sufficient information. Please verify the show name and try again."""
    
    standardized_name = name_result["standardized_name"]
    
    # Agent 2: Find ratings
    ratings_agent = FindRatingsAgent()
    ratings_result = ratings_agent.find(standardized_name)
    
    # Agent 3: Find tickets
    tickets_agent = FindTicketsAgent()
    tickets_result = tickets_agent.find(standardized_name)
    
    # Agent 4: Find image
    image_agent = FindImageAgent()
    image_result = image_agent.find(standardized_name)
    
    # Agent 5: Compile TLDR report (for UI)
    compile_agent = CompileReportAgent()
    tldr_report = compile_agent.compile(
        standardized_name,
        ratings_result["ratings_summary"],
        tickets_result["ticket_recommendations"]
    )
    
    # Agent 6: Compile extended report (for download)
    extended_agent = ExtendedReportAgent()
    extended_report = extended_agent.compile(
        standardized_name,
        ratings_result["ratings_summary"],
        tickets_result["ticket_recommendations"]
    )
    
    return {
        "report": tldr_report,
        "extended_report": extended_report,
        "image_url": image_result["image_url"]
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py '<Broadway Show Name>'")
        print("\nExamples:")
        print("  python main.py 'The Lion King'")
        print("  python main.py 'Hamilton'")
        print("  python main.py 'Wicked'")
        sys.exit(1)
    
    show_name = sys.argv[1]
    
    print(f"\n🎭 Broadway Show Research System")
    print("=" * 70)
    print(f"📋 Researching: '{show_name}'")
    print("=" * 70)
    
    try:
        result = run_pipeline(show_name)
        print("\n" + result["report"])
        if result["image_url"]:
            print(f"\n[Image: {result['image_url']}]")
        print("\n" + "=" * 70)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)