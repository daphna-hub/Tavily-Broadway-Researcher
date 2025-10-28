"""
Simple test script to verify the system works
"""

from main import run_pipeline

def test():
    """Test with a simple show"""
    print("Testing Broadway Research System...")
    print("=" * 60)
    
    try:
        result = run_pipeline("Hamilton")
        print("\n✅ SUCCESS!")
        print(result[:500] + "...")
        print("\n" + "=" * 60)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nMake sure you:")
        print("1. Created the .env file with your API keys")
        print("2. Installed dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    test()
