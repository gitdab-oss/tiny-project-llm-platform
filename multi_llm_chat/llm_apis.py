"""
Multi-LLM API Integration Module
Supports parallel async calls to OpenAI, Llama (via Groq), and Google Gemini
"""
import os
import asyncio
import time
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

# Import API clients
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class LLMAPI:
    """Base class for LLM API integrations"""
    
    def __init__(self):
        self.client = None
        self.model_name = ""
    
    async def query(self, user_input: str, conversation_history: list = None) -> Tuple[str, Dict]:
        """
        Query the LLM and return response with metadata
        Returns: (response_text, metadata_dict)
        """
        raise NotImplementedError


class OpenAIAPI(LLMAPI):
    """OpenAI GPT-4/GPT-3.5-turbo integration"""
    
    def __init__(self, model: str = "gpt-4"):
        super().__init__()
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model_name = model
    
    async def query(self, user_input: str, conversation_history: list = None) -> Tuple[str, Dict]:
        """Query OpenAI API"""
        start_time = time.time()
        
        try:
            # Build messages from history
            messages = []
            if conversation_history:
                messages.extend(conversation_history)
            messages.append({"role": "user", "content": user_input})
            
            # Make API call (OpenAI client is synchronous, so we run in executor)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.7
                )
            )
            
            response_text = response.choices[0].message.content
            elapsed_time = time.time() - start_time
            
            metadata = {
                "model": self.model_name,
                "response_time": round(elapsed_time, 2),
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None,
                "prompt_tokens": response.usage.prompt_tokens if hasattr(response, 'usage') else None,
                "completion_tokens": response.usage.completion_tokens if hasattr(response, 'usage') else None,
                "status": "success"
            }
            
            return response_text, metadata
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            error_msg = f"Error: {str(e)}"
            metadata = {
                "model": self.model_name,
                "response_time": round(elapsed_time, 2),
                "status": "error",
                "error": error_msg
            }
            return error_msg, metadata


class LlamaAPI(LLMAPI):
    """Llama integration via Groq"""
    
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        super().__init__()
        if not GROQ_AVAILABLE:
            raise ImportError("Groq package not installed. Run: pip install groq")
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=api_key)
        self.model_name = model
    
    async def query(self, user_input: str, conversation_history: list = None) -> Tuple[str, Dict]:
        """Query Groq API (Llama models)"""
        start_time = time.time()
        
        try:
            # Build messages from history
            messages = []
            if conversation_history:
                # Groq uses OpenAI-compatible format
                for msg in conversation_history:
                    messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": user_input})
            
            # Make API call
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1024
                )
            )
            
            response_text = response.choices[0].message.content
            elapsed_time = time.time() - start_time
            
            metadata = {
                "model": self.model_name,
                "response_time": round(elapsed_time, 2),
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None,
                "prompt_tokens": response.usage.prompt_tokens if hasattr(response, 'usage') else None,
                "completion_tokens": response.usage.completion_tokens if hasattr(response, 'usage') else None,
                "status": "success"
            }
            
            return response_text, metadata
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            error_msg = f"Error: {str(e)}"
            metadata = {
                "model": self.model_name,
                "response_time": round(elapsed_time, 2),
                "status": "error",
                "error": error_msg
            }
            return error_msg, metadata


class GeminiAPI(LLMAPI):
    """Google Gemini integration"""
    
    def __init__(self, model: str = "gemini-2.5-flash"):
        super().__init__()
        if not GEMINI_AVAILABLE:
            raise ImportError("Google Generative AI package not installed. Run: pip install google-generativeai")
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self.model_name = model
    
    async def query(self, user_input: str, conversation_history: list = None) -> Tuple[str, Dict]:
        """Query Google Gemini API"""
        start_time = time.time()
        
        try:
            # Build conversation context
            prompt = user_input
            if conversation_history:
                # Gemini doesn't have built-in chat history, so we prepend context
                context = "\n".join([
                    f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                    for msg in conversation_history[-5:]  # Last 5 messages for context
                ])
                prompt = f"{context}\n\nUser: {user_input}"
            
            # Make API call
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(prompt)
            )
            
            response_text = response.text
            elapsed_time = time.time() - start_time
            
            # Gemini doesn't always provide token usage in the same way
            metadata = {
                "model": self.model_name,
                "response_time": round(elapsed_time, 2),
                "tokens_used": None,  # Gemini API doesn't always expose this easily
                "status": "success"
            }
            
            return response_text, metadata
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            error_msg = f"Error: {str(e)}"
            metadata = {
                "model": self.model_name,
                "response_time": round(elapsed_time, 2),
                "status": "error",
                "error": error_msg
            }
            return error_msg, metadata


async def query_all_models(user_input: str, conversation_history: list = None, models: Dict = None) -> Dict:
    """
    Query all available models in parallel
    
    Args:
        user_input: User's message
        conversation_history: List of previous messages
        models: Dict of model instances to use (optional)
    
    Returns:
        Dict with responses from each model
    """
    if models is None:
        models = {}
    
    # Initialize models if not provided or if explicitly requested (even if None)
    tasks = []
    model_instances = {}
    
    # OpenAI - initialize if not in models dict, or if in dict but value is None (user selected it)
    if "openai" not in models or models.get("openai") is None:
        try:
            model_instances["openai"] = OpenAIAPI(model="gpt-4")
        except Exception as e:
            model_instances["openai"] = None
            print(f"OpenAI initialization failed: {e}")
    else:
        model_instances["openai"] = models["openai"]
    
    # Llama (via Groq) - initialize if not in models dict, or if in dict but value is None
    if "llama" not in models or models.get("llama") is None:
        try:
            model_instances["llama"] = LlamaAPI()
        except Exception as e:
            model_instances["llama"] = None
            print(f"Llama/Groq initialization failed: {e}")
    else:
        model_instances["llama"] = models["llama"]
    
    # Gemini - initialize if not in models dict, or if in dict but value is None
    if "gemini" not in models or models.get("gemini") is None:
        try:
            model_instances["gemini"] = GeminiAPI()
        except Exception as e:
            model_instances["gemini"] = None
            print(f"Gemini initialization failed: {e}")
    else:
        model_instances["gemini"] = models["gemini"]
    
    # Create async tasks for available models
    async def safe_query(model_name: str, model_instance: LLMAPI):
        if model_instance is None:
            return model_name, ("Model not available (check API key)", {"status": "unavailable"})
        try:
            return model_name, await model_instance.query(user_input, conversation_history)
        except Exception as e:
            return model_name, (f"Error: {str(e)}", {"status": "error", "error": str(e)})
    
    # Run all queries in parallel
    tasks = [
        safe_query(name, instance)
        for name, instance in model_instances.items()
        if instance is not None
    ]
    
    if not tasks:
        return {"error": "No models available. Please check your API keys."}
    
    results = await asyncio.gather(*tasks)
    
    # Format results
    formatted_results = {}
    for model_name, (response, metadata) in results:
        formatted_results[model_name] = {
            "response": response,
            "metadata": metadata
        }
    
    return formatted_results

