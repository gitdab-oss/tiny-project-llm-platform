# AI Tool Usage Log

## Project: Teeth X-ray Detection with Vision LLM

### Setup Phase - 12/22/2025

**Tool Used:** Claude AI / ChatGPT
**Purpose:** Project setup and architecture planning
**Prompts:**
- "Help me plan a teeth X-ray detection system using Vision LLMs"
- "Walk me through GitHub and Cursor IDE setup for this project"

**Outcome:** Successfully created project structure and setup guide

---

### Implementation Phase

**Tool Used:** GPT-4 Vision API
**Purpose:** Wisdom tooth detection in X-rays
**Prompt Design:**
```
"You are a dental X-ray analysis assistant. 
Analyze this dental X-ray image and identify the wisdom teeth (third molars) regions.
Provide the approximate locations as bounding box coordinates if visible."
```

**Reasoning:** Clear role definition helps model understand context. Requesting structured output (JSON) makes parsing easier.

---

### Bounding Box Detection Enhancement - 12/22/2025

**Tool Used:** GPT-4 Vision API (GPT-4o)
**Purpose:** Improve precision of wisdom tooth bounding box coordinates
**Prompt Evolution:**

**Initial Prompt:**
```
"Analyze this dental X-ray image and identify the wisdom teeth (third molars) regions.
Provide the approximate locations as bounding box coordinates if visible."
```

**Enhanced Prompt (Current):**
```
You are an expert dental radiologist analyzing a dental X-ray image.

IMAGE DIMENSIONS: Width={img_width}px, Height={img_height}px

TASK: Carefully examine this X-ray image and provide a detailed analysis of the wisdom teeth (third molars) with precise bounding box coordinates.

REQUIREMENTS:
1. Look at the image carefully and identify if wisdom teeth are present
2. For each detected wisdom tooth, provide PRECISE bounding box coordinates in pixels
3. Coordinates should be in format [x1, y1, x2, y2] where:
   - (x1, y1) is the top-left corner of the wisdom tooth (including crown and root)
   - (x2, y2) is the bottom-right corner of the wisdom tooth
   - The bounding box should tightly surround the ENTIRE wisdom tooth structure
   - Include a small margin (5-10 pixels) around the tooth for better visibility
   - All coordinates must be valid pixel positions within the image dimensions
4. BOUNDING BOX PRECISION:
   - The box should be centered on the wisdom tooth
   - For upper wisdom teeth: boxes should be in the upper portion of the image
   - For lower wisdom teeth: boxes should be in the lower portion of the image
   - For left wisdom teeth: boxes should be on the left side of the image
   - For right wisdom teeth: boxes should be on the right side of the image
   - The box should encompass the entire visible tooth structure (crown + visible root)
```

**Key Improvements:**
- Added explicit image dimensions to provide spatial context
- Specified exact coordinate format requirements
- Added quadrant-specific positioning guidance
- Included margin specifications for better visibility
- Emphasized precision and accuracy requirements

**System Message:**
```
"You are an expert dental radiologist with years of experience analyzing dental X-rays. 
You can analyze X-ray images in detail and identify specific dental structures including wisdom teeth. 
Provide accurate, detailed analysis based on what you observe in the images. 
You MUST provide bounding box coordinates in pixel coordinates relative to the image dimensions."
```

**Output Format:**
Structured JSON with:
- `bounding_boxes`: Array of objects with coordinates, quadrant, label, status, confidence
- `analysis`: Quadrant-specific analysis (upper_left, upper_right, lower_left, lower_right)
- `overall_description`: Summary of findings
- `recommendations`: Additional observations

**Results:**
- Successfully generates bounding box coordinates for detected wisdom teeth
- Coordinates are generally accurate but may require slight manual adjustment
- Provides detailed quadrant-specific analysis
- Returns structured JSON for easy parsing and visualization

**Lessons Learned:**
1. Providing image dimensions helps the model understand spatial relationships
2. Explicit coordinate format requirements reduce ambiguity
3. Quadrant-specific guidance improves positioning accuracy
4. System message reinforcement helps overcome model hesitancy
5. Structured output format (JSON) enables programmatic processing

**Technical Implementation:**
- Coordinates are validated and refined to ensure they're within image bounds
- Bounding boxes are drawn with yellow outline (3px) and red semi-transparent fill (100/255 opacity)
- Annotated images are saved separately to prevent cluttering sample images directory
- Error handling for coordinate validation and edge cases (needs improvement)

---

### Multi-Model LLM Chatbot - 12/22/2025

**Tool Used:** GPT-4, Llama 3.1 70B (via Groq), Gemini-2.5-flash (Google)
**Purpose:** Build a comparison interface to evaluate responses from multiple LLM providers side-by-side
**Architecture:** Parallel async API calls using asyncio

**Implementation Strategy:**
1. Created modular API wrapper classes for each provider (OpenAI, Groq/Llama, Google)
2. Implemented async parallel querying using `asyncio.gather()`
3. Built Streamlit interface with side-by-side comparison
4. Added performance metrics tracking (response time, token usage)

**Key Design Decisions:**

**1. Async Architecture:**
```python
async def query_all_models(user_input, conversation_history, models):
    tasks = [
        safe_query(name, instance)
        for name, instance in model_instances.items()
    ]
    results = await asyncio.gather(*tasks)
    return formatted_results
```
- Uses `asyncio.gather()` for true parallel execution
- Each model query runs concurrently, reducing total wait time
- Wrapped in `run_in_executor()` since some API clients are synchronous

**2. Modular API Classes:**
- `OpenAIAPI`: Wraps OpenAI's GPT-4/GPT-3.5-turbo
- `LlamaAPI`: Wraps Llama 3.3 70B via Groq (free tier friendly, very fast)
- `GeminiAPI`: Wraps Google Gemini 2.5 Flash
- Each class implements consistent interface: `query(user_input, conversation_history)`

**3. Error Handling:**
- Graceful degradation: If one model fails, others continue
- Clear error messages displayed in UI
- Metadata includes status (success/error/unavailable)

**4. Conversation History:**
- Maintains context across multiple turns
- Each model receives same conversation history
- History stored in Streamlit session state

**Prompt Strategy:**
- No special prompting needed - using default model behavior
- Conversation history provides context automatically
- Temperature set to 0.7 for balanced creativity/consistency

**UI Features:**
- Side-by-side response comparison
- Performance metrics (response time, token usage)
- Conversation history sidebar
- Model selection checkboxes
- Comparison table for metrics

**Results:**
- Successfully queries 3 models in parallel
- Average response time: ~2-5 seconds total (vs 6-15 seconds sequential)
- Clear comparison of response quality and performance
- Token usage tracking helps understand cost implications

**Lessons Learned:**
1. Async programming essential for parallel API calls
2. Error handling critical when dealing with multiple external APIs
3. Consistent interface design makes adding new models easier
4. Performance metrics help users understand trade-offs
5. Streamlit's session state perfect for conversation management

**Technical Challenges:**
- OpenAI and Groq clients are synchronous, requiring `run_in_executor()`
- Gemini API has different response structure
- Streamlit's async handling requires careful event loop management
- Token usage not always available from all providers
- Groq uses OpenAI-compatible API format, making integration straightforward

**Model Selection Rationale:**
- **GPT-4**: Industry standard, high quality responses
- **Llama 3.3 70B (Groq)**: Free tier available, extremely fast inference, open-source model
- **Gemini 2.5 Flash**: Good alternative perspective, Google's offering

**Future Improvements:**
- Add streaming responses for real-time updates
- Implement response caching
- Add model-specific temperature/parameter controls
- Support for additional models (Claude, etc.)
- Export conversation history

---