# 💬 Multi-Model LLM Chatbot

A Streamlit application that compares responses from multiple Large Language Model providers side-by-side in real-time.

## Features

- **Parallel Querying**: Query GPT-4, Llama 3.3 70B (via Groq), and Gemini 2.5 Flash simultaneously using async/await
- **Side-by-Side Comparison**: View responses from all models in a single interface
- **Performance Metrics**: Track response times and token usage for each model
- **Conversation History**: Maintain context across multiple conversation turns
- **Model Selection**: Choose which models to query via checkboxes

## Setup

### Prerequisites

- Python 3.11+
- API keys for:
  - OpenAI (for GPT-4)
  - Groq (for Llama 3.1 70B)
  - Google AI (for Gemini)

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r ../requirements.txt
   ```

2. **Set up environment variables:**
   
   Add to your `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_key
   GROQ_API_KEY=your_groq_key
   GOOGLE_API_KEY=your_google_key
   ```

3. **Run the application:**
   ```bash
   streamlit run multi_llm_chat/app.py
   ```

## Usage

1. **Select Models**: Use checkboxes in the sidebar to choose which models to query
2. **Type Your Message**: Enter your question in the chat input
3. **View Responses**: See all model responses side-by-side
4. **Check Metrics**: Expand "Performance Metrics" to see response times and token usage
5. **Compare**: Use the comparison table at the bottom to see performance differences

## Architecture

### File Structure

```
multi_llm_chat/
├── app.py          # Streamlit UI and main application
├── llm_apis.py     # API wrapper classes for each provider
├── config.py       # Configuration settings
└── README.md       # This file
```

### Key Components

**llm_apis.py:**
- `OpenAIAPI`: Wraps OpenAI's GPT-4
- `AnthropicAPI`: Wraps Claude 3.5 Sonnet
- `GeminiAPI`: Wraps Google Gemini 2.5 Flash
- `query_all_models()`: Async function to query all models in parallel

**app.py:**
- Streamlit interface
- Session state management for conversation history
- Side-by-side response display
- Performance metrics visualization

## API Integration Details

### OpenAI (GPT-4)
- Model: `gpt-4` (configurable to `gpt-3.5-turbo`)
- Provides: Token usage, response time
- Rate limits: Varies by tier

### Groq (Llama 3.3 70B)
- Model: `llama-3.3-70b-versatile` (configurable to other Llama models)
- Provides: Token usage, response time
- Rate limits: Free tier available, very fast inference

### Google (Gemini 2.5 Flash)
- Model: `gemini-2.5-flash`
- Provides: Response time (token usage limited)
- Rate limits: Free tier available

## Performance

- **Parallel Execution**: All models queried simultaneously
- **Average Response Time**: 2-5 seconds total (vs 6-15 seconds sequential)
- **Efficiency**: ~60-70% time savings compared to sequential calls

## Troubleshooting

### "Model not available" Error
- Check that API key is set in `.env` file
- Verify API key is valid and has credits/quota
- For Groq: Get free API key from https://console.groq.com/
- Restart Streamlit after updating `.env`

### Async Event Loop Errors
- Streamlit handles async differently - the code uses `run_in_executor()` for compatibility
- If issues persist, try restarting the Streamlit app

### Missing Responses
- Some models may fail while others succeed - this is expected behavior
- Check error messages in the Performance Metrics expander

## Future Enhancements

- [ ] Streaming responses for real-time updates
- [ ] Response caching to reduce API calls
- [ ] Model-specific parameter controls (temperature, max_tokens)
- [ ] Support for additional models (Llama via Groq, etc.)
- [ ] Export conversation history
- [ ] Cost estimation calculator

## Notes

- API usage incurs costs - monitor your usage
- Response quality varies by model and use case
- Token usage tracking helps understand cost implications
- Conversation history is maintained in session state (cleared on refresh)

---

**Part of the tiny-project-llm-platform project**

