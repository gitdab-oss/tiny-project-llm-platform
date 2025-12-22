"""
Quick diagnostic tool to check API keys and model availability
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"

print("=" * 60)
print("API Key Diagnostic Tool")
print("=" * 60)

# Check if .env exists
if env_path.exists():
    print(f"✓ Found .env file at: {env_path}")
    load_dotenv(env_path)
else:
    print(f"✗ .env file not found at: {env_path}")
    print("  Trying default location...")
    load_dotenv()

print("\nChecking API keys...")
print("-" * 60)

# Check OpenAI
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    key_preview = openai_key[:7] + "..." + openai_key[-4:] if len(openai_key) > 11 else "***"
    print(f"✓ OPENAI_API_KEY: {key_preview}")
else:
    print("✗ OPENAI_API_KEY: NOT FOUND")

# Check Groq
groq_key = os.getenv("GROQ_API_KEY")
if groq_key:
    key_preview = groq_key[:7] + "..." + groq_key[-4:] if len(groq_key) > 11 else "***"
    print(f"✓ GROQ_API_KEY: {key_preview}")
else:
    print("✗ GROQ_API_KEY: NOT FOUND")

# Check Google
google_key = os.getenv("GOOGLE_API_KEY")
if google_key:
    key_preview = google_key[:7] + "..." + google_key[-4:] if len(google_key) > 11 else "***"
    print(f"✓ GOOGLE_API_KEY: {key_preview}")
else:
    print("✗ GOOGLE_API_KEY: NOT FOUND")

print("\n" + "=" * 60)
print("Model Availability Test")
print("=" * 60)

# Test each model
from llm_apis import OpenAIAPI, LlamaAPI, GeminiAPI
import asyncio

async def test_models():
    results = {}
    
    # Test OpenAI
    print("\nTesting OpenAI (GPT-4)...")
    try:
        openai_api = OpenAIAPI()
        response, metadata = await openai_api.query("Say 'test'")
        if metadata.get("status") == "success":
            print("✓ OpenAI: Working!")
            results["openai"] = True
        else:
            print(f"✗ OpenAI: {metadata.get('error', 'Unknown error')}")
            results["openai"] = False
    except Exception as e:
        print(f"✗ OpenAI: {str(e)}")
        results["openai"] = False
    
    # Test Groq/Llama
    print("\nTesting Groq (Llama 3.1 70B)...")
    try:
        llama_api = LlamaAPI()
        response, metadata = await llama_api.query("Say 'test'")
        if metadata.get("status") == "success":
            print("✓ Groq/Llama: Working!")
            results["llama"] = True
        else:
            print(f"✗ Groq/Llama: {metadata.get('error', 'Unknown error')}")
            results["llama"] = False
    except Exception as e:
        print(f"✗ Groq/Llama: {str(e)}")
        results["llama"] = False
    
    # Test Gemini
    print("\nTesting Google Gemini...")
    try:
        gemini_api = GeminiAPI()
        response, metadata = await gemini_api.query("Say 'test'")
        if metadata.get("status") == "success":
            print("✓ Gemini: Working!")
            results["gemini"] = True
        else:
            print(f"✗ Gemini: {metadata.get('error', 'Unknown error')}")
            results["gemini"] = False
    except Exception as e:
        print(f"✗ Gemini: {str(e)}")
        results["gemini"] = False
    
    return results

# Run tests
try:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(test_models())
    loop.close()
except Exception as e:
    print(f"\nError running tests: {e}")
    results = {}

print("\n" + "=" * 60)
print("Summary")
print("=" * 60)

available = sum(results.values())
total = len(results)

if available == 0:
    print("\n❌ No models are available!")
    print("\nPlease:")
    print("1. Check your .env file exists and contains the API keys")
    print("2. Verify your API keys are valid")
    print("3. Make sure you've installed all packages: pip install -r requirements.txt")
elif available < total:
    print(f"\n⚠️  {available}/{total} models are available")
    print("You can still use the app with the available models")
else:
    print(f"\n✓ All {available} models are available and working!")

print("\n" + "=" * 60)

