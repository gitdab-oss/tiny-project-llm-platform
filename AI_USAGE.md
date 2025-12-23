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

### API Debugging Phase - 12/22/2025

**Issue Encountered:** Model deprecation and API compatibility errors
**Tools Used:** Claude AI for troubleshooting and documentation review

**Problems:**
1. **Groq Error:** `llama-3.1-70b-versatile` model decommissioned
2. **Gemini Error:** `gemini-pro` and `gemini-1.5-flash` returning 404 errors

**Debugging Process:**

**Groq Model Update:**
- Original model: `llama-3.1-70b-versatile` (deprecated)
- Updated to: `llama-3.3-70b-versatile` (current)
- Source: https://console.groq.com/docs/models
- **Prompt to AI:** "The Groq model llama-3.1-70b-versatile is deprecated. What's the current model name?"
- **Outcome:** Successfully updated and working

**Gemini Model Investigation:**
- Attempted models: `gemini-pro`, `gemini-1.5-flash`, `models/gemini-1.5-flash`
- Issue: 404 errors despite documentation suggesting these should work
- **Debugging Strategy:** Created script to list all available models via API
- **Prompt to AI:** "Google Gemini is returning 404 for gemini-1.5-flash. Help me list available models and find the correct model name"

**Lessons Learned:**
1. **API Evolution:** Model names and availability change frequently
2. **Documentation Lag:** Official docs may not reflect latest API changes
3. **Dynamic Discovery:** Always implement model listing/discovery in production code
4. **Version Pinning:** Consider pinning SDK versions in requirements.txt to avoid breaking changes
5. **Graceful Degradation:** Implement fallback mechanisms when models are unavailable

**Scientific Approach:**
- Used systematic debugging: list available resources → test variations → identify root cause
- Documented each attempt and result
- Leveraged AI assistant to accelerate troubleshooting process
- Applied iterative problem-solving methodology

---

---

### Debugging & Documentation - 12/22/2025

**Issue:** Need to create comprehensive project report
**Tool Used:** Claude AI
**Purpose:** Structure project documentation to highlight honest effort, short timeline, and transparent AI usage

**Prompt:**
"Help me create a short project report for my tiny project. This took 2-3 hours total of non-stop work. Need to emphasize: project duration, learning outcomes, challenges, and AI tool usage. Keep it concise but comprehensive."

**Outcome:** Generated structured report template that accurately reflects the rapid development timeline and extensive AI collaboration

**Key Sections Created:**
1. Executive Summary - One paragraph overview
2. Project Duration - Detailed breakdown of 2-3 hour timeline
3. Learning Outcomes - Technical skills and practical insights gained
4. Challenges - 3 major challenges with solutions (model deprecations, bounding box accuracy, Windows setup)
5. AI Tool Usage - Transparent documentation of prompts, contributions, and my value-add

**Reflection:**
This report demonstrates that:
- AI tools dramatically accelerate development when used strategically
- 2-3 hours of focused work can produce significant results with AI assistance
- Transparency in AI usage shows scientific thinking, not lack of skill
- Rapid iteration (test → learn → improve) more valuable than slow perfection

**Statistics:**
- Total development time: 2-3 hours
- API costs: ~$2-3 (well under budget)
- Lines of code: ~500-600 (including AI-generated boilerplate)
- AI assistance percentage: ~40-60% depending on task
- My contribution: Architecture decisions, integration, testing, iteration, debugging

**Honesty Statement:**
This project heavily leveraged AI tools as encouraged. The value I brought was:
- Strategic decision-making (which approaches to take)
- Prompt engineering and iteration (improving AI outputs)
- Integration and testing (making components work together)
- Problem-solving (debugging API issues in real-time)
- Critical evaluation (validating AI suggestions before implementing)

The short timeline demonstrates efficiency, not corner-cutting. Both applications are functional MVPs that could be expanded with more time.

---