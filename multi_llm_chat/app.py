"""
Multi-LLM Chatbot Interface
Compare responses from OpenAI, Llama (via Groq), and Google Gemini side-by-side
"""
import streamlit as st
import asyncio
from llm_apis import query_all_models

# Page configuration
st.set_page_config(
    page_title="Multi-LLM Chatbot Comparison",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("💬 Multi-LLM Chatbot Comparison")
st.markdown("Compare responses from GPT-4, Llama 3.3 70B (Groq), and Gemini 2.5 Flash side-by-side")

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "all_responses" not in st.session_state:
    st.session_state.all_responses = []

# Sidebar for settings and history
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Model selection
    st.subheader("Available Models")
    use_openai = st.checkbox("GPT-4 (OpenAI)", value=True)
    use_llama = st.checkbox("Llama 3.3 70B (Groq)", value=True)
    use_gemini = st.checkbox("Gemini 2.5 Flash (Google)", value=True)
    
    st.markdown("---")
    
    # Conversation history
    st.subheader("📜 Conversation History")
    if st.button("Clear History", type="secondary"):
        st.session_state.conversation_history = []
        st.session_state.all_responses = []
        st.rerun()
    
    # Display conversation count
    st.info(f"Messages in conversation: {len(st.session_state.conversation_history) // 2}")
    
    # Show recent messages
    if st.session_state.conversation_history:
        with st.expander("View Recent Messages"):
            for i, msg in enumerate(st.session_state.conversation_history[-6:]):
                role = "👤 User" if msg["role"] == "user" else "🤖 Assistant"
                st.text(f"{role}: {msg['content'][:50]}...")

# Main chat interface
st.markdown("---")

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to history
    st.session_state.conversation_history.append({
        "role": "user",
        "content": user_input
    })
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Query all models
    with st.spinner("Querying all models in parallel..."):
        # Determine which models to use
        models_to_use = {}
        if use_openai:
            models_to_use["openai"] = None  # Will be initialized in query_all_models
        if use_llama:
            models_to_use["llama"] = None
        if use_gemini:
            models_to_use["gemini"] = None
        
        # Run async query - Streamlit-compatible approach
        try:
            # Try to get existing event loop
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            results = loop.run_until_complete(
                query_all_models(
                    user_input,
                    st.session_state.conversation_history[:-1],  # Exclude current message
                    models_to_use if models_to_use else None
                )
            )
        except Exception as e:
            st.error(f"Error querying models: {str(e)}")
            results = {"error": str(e)}
    
    # Store results
    st.session_state.all_responses.append({
        "user_input": user_input,
        "results": results
    })
    
    # Display results in columns
    model_names = {
        "openai": "GPT-4o (OpenAI)",
        "llama": "Llama 3.3 70B (Groq)",
        "gemini": "Gemini 2.5 Flash (Google)"
    }
    
    available_models = [k for k in model_names.keys() if k in results and results[k].get("metadata", {}).get("status") != "unavailable"]
    
    if not available_models:
        # Show detailed error message
        error_details = []
        if "error" in results:
            st.error(f"❌ {results['error']}")
        else:
            missing_keys = []
            if use_openai and ("openai" not in results or results.get("openai", {}).get("metadata", {}).get("status") == "unavailable"):
                missing_keys.append("OPENAI_API_KEY")
            if use_llama and ("llama" not in results or results.get("llama", {}).get("metadata", {}).get("status") == "unavailable"):
                missing_keys.append("GROQ_API_KEY")
            if use_gemini and ("gemini" not in results or results.get("gemini", {}).get("metadata", {}).get("status") == "unavailable"):
                missing_keys.append("GOOGLE_API_KEY")
            
            if missing_keys:
                st.error(f"❌ No models available. Missing API keys: {', '.join(missing_keys)}")
                st.info("💡 **Quick Fix:**\n1. Check your `.env` file exists in the project root\n2. Make sure it contains the required API keys\n3. Run `python multi_llm_chat/check_keys.py` to diagnose issues")
            else:
                st.error("❌ No models available. Please check your API keys in the .env file.")
    else:
        # Create columns dynamically based on available models
        cols = st.columns(len(available_models))
        
        for idx, model_key in enumerate(available_models):
            with cols[idx]:
                model_display_name = model_names.get(model_key, model_key)
                st.subheader(f"🤖 {model_display_name}")
                
                result = results[model_key]
                response = result.get("response", "No response")
                metadata = result.get("metadata", {})
                
                # Display response
                with st.chat_message("assistant"):
                    st.write(response)
                
                # Display metadata
                with st.expander("📊 Performance Metrics"):
                    if metadata.get("status") == "success":
                        st.metric("Response Time", f"{metadata.get('response_time', 0)}s")
                        
                        if metadata.get("tokens_used"):
                            st.metric("Total Tokens", metadata.get("tokens_used"))
                        
                        if metadata.get("prompt_tokens"):
                            st.metric("Prompt Tokens", metadata.get("prompt_tokens"))
                        
                        if metadata.get("completion_tokens"):
                            st.metric("Completion Tokens", metadata.get("completion_tokens"))
                    else:
                        st.error(f"Status: {metadata.get('status', 'unknown')}")
                        if metadata.get("error"):
                            st.error(metadata.get("error"))
                
                # Add assistant response to history (use first successful response)
                if idx == 0 and metadata.get("status") == "success":
                    st.session_state.conversation_history.append({
                        "role": "assistant",
                        "content": response
                    })

# Display comparison metrics
if st.session_state.all_responses:
    st.markdown("---")
    st.subheader("📈 Performance Comparison")
    
    # Calculate averages
    last_response = st.session_state.all_responses[-1]
    results = last_response["results"]
    
    comparison_data = []
    for model_key, model_name in model_names.items():
        if model_key in results:
            metadata = results[model_key].get("metadata", {})
            if metadata.get("status") == "success":
                comparison_data.append({
                    "Model": model_name,
                    "Response Time (s)": metadata.get("response_time", 0),
                    "Tokens Used": metadata.get("tokens_used", "N/A"),
                    "Status": "✅ Success"
                })
            else:
                comparison_data.append({
                    "Model": model_name,
                    "Response Time (s)": metadata.get("response_time", 0),
                    "Tokens Used": "N/A",
                    "Status": f"❌ {metadata.get('status', 'Error')}"
                })
    
    if comparison_data:
        st.dataframe(comparison_data, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
**About:** This tool compares responses from multiple LLM providers in real-time.  
**Note:** API keys required for OpenAI, Groq (Llama), and Google Gemini. Set them in your `.env` file.
""")

