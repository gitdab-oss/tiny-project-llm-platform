"""
Quick test script to verify your OpenAI API key is working.
Run this to check if your .env file is being read correctly.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load .env from project root
project_root = Path(__file__).parent
env_path = project_root / ".env"

print("=" * 60)
print("Testing OpenAI API Key")
print("=" * 60)

# Check if .env exists
if env_path.exists():
    print(f"✓ Found .env file at: {env_path}")
    load_dotenv(env_path)
else:
    print(f"✗ .env file not found at: {env_path}")
    print("  Trying default location...")
    load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("\n✗ ERROR: OPENAI_API_KEY not found in environment!")
    print("\nPlease create a .env file in the project root with:")
    print("OPENAI_API_KEY=sk-your-actual-key-here")
    exit(1)

# Show key preview (first 7 chars)
key_preview = api_key[:7] + "..." + api_key[-4:] if len(api_key) > 11 else "***"
print(f"✓ API Key found: {key_preview}")

# Test the API key with a simple request
print("\nTesting API key with a simple request...")
try:
    client = OpenAI(api_key=api_key)
    
    # Try to get organization info (if available)
    try:
        # This will show which account/org the key belongs to
        org_info = client.models.list()
        print("✓ API Key is valid and connected to your account")
    except:
        pass
    
    # Make a very small test request
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'test'"}],
        max_tokens=5
    )
    
    print("✓ API Key is valid and working!")
    print(f"  Response: {response.choices[0].message.content}")
    print("\n" + "=" * 60)
    print("IMPORTANT: Account/Project Verification")
    print("=" * 60)
    print("\nTo verify this API key matches the account you're viewing:")
    print("1. Go to: https://platform.openai.com/api-keys")
    print("2. Find the key that starts with:", key_preview.split("...")[0])
    print("3. Check which project/organization it belongs to")
    print("4. Make sure you're viewing the Usage dashboard for THAT project")
    print("\nThe API key determines which account/project is used for:")
    print("  • Billing and quota limits")
    print("  • Usage tracking")
    print("  • Rate limits")
    print("\nIf you see $0 usage but get quota errors, you might be:")
    print("  • Viewing a different project's dashboard")
    print("  • Using an API key from a different account")
    print("\nYour API key should work with the Streamlit app now.")
    
except Exception as e:
    error_str = str(e).lower()
    
    if '429' in error_str or 'quota' in error_str or 'insufficient_quota' in error_str:
        print("\n⚠️  QUOTA ERROR:")
        print("   You're getting a quota/rate limit error.")
        print("   This could mean:")
        print("   - Rate limit (too many requests per minute)")
        print("   - The API key belongs to a different account")
        print("   - Temporary rate limiting")
        print("\n   Check: https://platform.openai.com/account/rate-limits")
    elif '401' in error_str or 'unauthorized' in error_str:
        print("\n✗ AUTHENTICATION ERROR:")
        print("   Your API key is invalid or expired.")
        print("   Get a new key from: https://platform.openai.com/api-keys")
    else:
        print(f"\n✗ ERROR: {e}")
        print("\n   Check your API key and try again.")

print("=" * 60)

