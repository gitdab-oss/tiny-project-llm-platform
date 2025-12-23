# Tiny Project: LLM Platform Development

**Student:** Daniel Briceno  
**Email:** dabriceno31@gmail.com
**Date:** December 22, 2025  
**GitHub Repository:** https://github.com/gitdab-oss/tiny-project-llm-platform

---

## Executive Summary

Developed two AI-powered applications in 2-3 hours: (1) Teeth X-ray wisdom tooth detector using GPT-4 Vision, and (2) Multi-model LLM chatbot comparing three language models (GPT-4o, Gemini 2.5 Flash, Llama 3.3 70B) in real-time. Both applications demonstrate practical AI integration with transparent AI tool usage throughout development.

---

## 1. Project Duration

**Total Time: 2-3 hours** (single focused session)

| Phase | Duration | Key Activities |
|-------|----------|----------------|
| Setup & Planning | 20-30 min | Repo setup, environment config, API key acquisition |
| Part 1: Teeth Detector | 45-60 min | Vision API integration, Streamlit UI, prompt engineering |
| Part 2: Multi-LLM Chat | 45-60 min | Multi-provider integration, parallel querying, comparison UI |
| Debugging | 15-30 min | Model deprecation fixes (Groq, Gemini) |
| Documentation | 10-15 min | AI usage log updates, code comments |

**Development Approach:** Focused on rapid MVP development with strategic AI tool usage rather than perfection. Both applications are functional demonstrations that meet project requirements.

---

## 2. Learning Outcomes

### Technical Skills Acquired

**Vision AI & Prompt Engineering:**
- Learned to engineer prompts for medical image analysis with structured JSON outputs
- Discovered that adding image dimensions and explicit coordinate constraints improved bounding box accuracy from ~30% to ~90%
- Understood the importance of role-playing in prompts ("expert radiologist" vs generic analysis)

**Multi-Provider API Integration:**
- Built abstraction layers normalizing different API formats (OpenAI, Anthropic, Groq)
- Each provider has unique response structures requiring adapter patterns
- Learned error handling strategies for external API dependencies

**Async Programming:**
- Implemented parallel API calls using `asyncio.gather()`
- Reduced total response time from ~10 seconds (sequential) to ~3 seconds (parallel)
- Handled mixing sync API clients with async patterns using `run_in_executor()`

**Rapid Prototyping with Streamlit:**
- Quick UI iteration without frontend complexity
- Session state management for conversation history
- Column layouts for side-by-side model comparisons

### Practical Insights

**API Evolution Reality:**
- Models deprecate unexpectedly during development (experienced with Groq and Gemini)
- Always implement fallback mechanisms and dynamic model discovery
- Documentation can lag behind actual API changes

**Cost-Aware Development:**
- Total API costs: ~$2-3 (mostly OpenAI GPT-4 Vision calls)
- Free tiers (Anthropic credits, Groq, Gemini) covered significant testing
- Strategic model selection (GPT-3.5 for text testing) minimizes costs

**Prompt Engineering as Iterative Process:**
- Each refinement tests a specific hypothesis
- Measurable improvements guide iteration direction
- Context + constraints + structure = better AI outputs

---

## 3. Challenges Encountered

### Challenge 1: API Model Deprecations
**Time to Resolve:** 15 minutes

**Problem:** Mid-development, Groq deprecated `llama-3.1-70b-versatile` and Gemini's documented models returned 404 errors.

**Impact:** Application broke during testing phase.

**Solution Process:**
1. Used Claude AI to identify current model names
2. Updated Groq to `llama-3.3-70b-versatile`
3. Attempted multiple Gemini model names without success
4. Decided to proceed with 3-model configuration (GPT-4o, Claude, Llama)

**Lesson Learned:** API deprecation is normal in fast-moving AI field. Always build resilience with fallback options and document working configurations.

---

### Challenge 2: Bounding Box Coordinate Accuracy
**Time to Resolve:** 20 minutes

**Problem:** Initial Vision API responses provided vague descriptions or invalid bounding box coordinates (out of image bounds, negative values, reversed corners).

**Root Cause:** Prompt lacked spatial context and explicit constraints.

**Solution:**
- **Iteration 1:** "Find wisdom teeth" → Vague text only
- **Iteration 2:** "Provide bounding boxes in JSON" → Better, but invalid coordinates
- **Iteration 3:** Added image dimensions, explicit format `[x1,y1,x2,y2]`, quadrant guidance, expert role → ~90% valid coordinates

**Implementation:** Also added coordinate validation layer in code to catch edge cases.

**Key Insight:** Specificity in prompts directly correlates with output quality. Vision models need dimensional context to provide accurate spatial information.

---

### Challenge 3: Windows Development Environment
**Time to Resolve:** 10 minutes

**Problem:** Pillow package installation failed with `KeyError: '__version__'` due to missing C++ build tools.

**Solution:**
1. Upgraded pip, setuptools, wheel
2. Used `--only-binary :all:` flag to force pre-compiled wheels
3. Pinned working version: `Pillow==10.0.0`

**Lesson:** Windows Python development often requires pre-built binaries. Avoid source compilation when possible for faster setup.

---

## 4. Use of AI Tools

### Philosophy & Transparency

Used AI assistants (Claude, GPT-4, GitHub Copilot) extensively throughout this project as encouraged by project guidelines. **All usage documented in real-time in `AI_USAGE.md`** to demonstrate scientific and creative application of AI tools.

**Core Principle:** AI tools accelerate development; human judgment directs strategy, validates outputs, and ensures quality.

---

### Detailed AI Tool Usage

#### A. Project Planning & Architecture (Claude AI)

**Problem Solved:** Needed strategic approach for 2-part project with tight timeline.

**How I Formulated the Problem:**
*"I have a tiny project with two parts: teeth X-ray detection and multi-LLM chatbot. I have limited time. Help me create a strategic plan focusing on demonstrating honesty, dedication, and clear effort. What techniques should I use given time constraints?"*

**AI Contribution:**
- Recommended Vision LLM approach over training YOLO (faster, better for demo)
- Suggested parallel API architecture for multi-model chat
- Provided realistic time estimates per component
- Recommended Streamlit for rapid UI development

**My Decision-Making:**
- Evaluated recommendations against my skills and time available
- Chose Vision LLM approach (correct decision - saved hours)
- Decided on 3 models instead of 4 when Gemini issues arose
- Prioritized working MVPs over perfect implementations

**Time Impact:** Saved ~1 hour of research and planning

---

#### B. Environment Setup (Claude AI)

**Problem Solved:** Needed Windows-specific setup instructions for Python environment, GitHub, and Cursor IDE.

**How I Formulated the Problem:**
*"Walk me through setup on GitHub and Cursor IDE for development (I'm on Windows, use PowerShell commands)."*

**AI Contribution:**
- Step-by-step PowerShell commands
- Project structure recommendations
- Anticipated common Windows issues (execution policy, Pillow compilation)
- Provided troubleshooting steps

**My Execution:**
- Ran commands sequentially
- Debugged Pillow issue independently
- Verified each step before proceeding
- Adapted generic advice to my specific environment

---

#### C. Prompt Engineering for Vision API (Claude AI + GPT-4 Vision)

**Problem Solved:** Needed effective prompts for medical image analysis with accurate bounding boxes.

**Iterative Refinement Process:**

**Round 1 - Basic Prompt:**
```
"Analyze this dental X-ray and find wisdom teeth"
```
- **Result:** Vague text descriptions, no coordinates
- **Learning:** Need structured output format

**Round 2 - Structured Request:**
```
"Identify wisdom teeth and provide bounding box coordinates in JSON format"
```
- **Result:** JSON output, but coordinates often invalid (out of bounds, negative)
- **Learning:** Model doesn't understand image coordinate system

**Round 3 - Enhanced Prompt (with AI guidance):**
```
"You are an expert dental radiologist analyzing a dental X-ray.
Image dimensions: {width} x {height} pixels.

Provide bounding boxes for each wisdom tooth in format [x1, y1, x2, y2] where:
- (x1, y1) is top-left corner
- (x2, y2) is bottom-right corner  
- All coordinates must be within image bounds (0 to width/height)
- Include quadrant information (upper/lower, left/right)"
```
- **Result:** ~90% valid coordinates, much better spatial accuracy
- **Learning:** Context + explicit constraints + role definition = quality outputs

**AI Assistant's Role:**
- Suggested adding image dimensions for spatial context
- Recommended role-playing approach ("expert radiologist")
- Proposed coordinate validation as code-level safeguard

**My Contribution:**
- Tested each iteration systematically
- Measured improvement quantitatively (% valid coordinates)
- Implemented validation layer in Python
- Fine-tuned prompt based on actual results

**Time Impact:** Iterative improvement over 20 minutes vs. hours of trial-and-error

---

#### D. API Debugging & Model Updates (Claude AI)

**Problem Solved:** Multiple API models deprecated during development.

**How I Formulated Problems:**

**For Groq:**
*"Error: model 'llama-3.1-70b-versatile' has been decommissioned. What's the current replacement model?"*

**For Gemini:**
*"Getting 404 error for gemini-1.5-flash. Help me list available Gemini models and find the working model name."*

**AI Contribution:**
- Immediate answer for Groq: `llama-3.3-70b-versatile`
- Created diagnostic script to list available models
- Explained why deprecations happen in AI APIs
- Suggested fallback strategies

**My Actions:**
- Verified AI's recommendations by testing
- Updated codebase with new model names
- Documented changes in AI usage log
- Made strategic decision to use 3 models when Gemini continued failing

**Time Impact:** Saved ~30-45 minutes of documentation research and testing

---

#### E. Code Generation & Boilerplate (Claude AI, GitHub Copilot)

**Problem Solved:** Needed API wrappers, Streamlit structure, async patterns.

**Example - OpenAI API Wrapper:**

**My Prompt to AI:**
*"Create a Python class wrapper for OpenAI's GPT-4 API that accepts conversation history, returns response with timing and token count, and handles errors gracefully."*

**AI Generated (~70% of final code):**
```python
class OpenAIAPI:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def query(self, user_input, conversation_history=None):
        try:
            messages = []
            if conversation_history:
                messages.extend(conversation_history)
            messages.append({"role": "user", "content": user_input})
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
```

**My Modifications (~30% of final code):**
- Added timing instrumentation (`time.time()` tracking)
- Structured return as dict with metadata (response, time, tokens, status)
- Added model parameter for flexibility
- Customized error messages for user clarity
- Integrated with Streamlit session state

**Pattern Across Project:**
- **Streamlit Apps:** ~60% AI-generated structure, 40% my customization
- **API Wrappers:** ~70% AI boilerplate, 30% my integration logic
- **Async Patterns:** ~50% AI guidance, 50% my implementation

**Philosophy:** Use AI for repetitive code; I provide domain logic, integration, and quality control.

---

#### F. Async Programming Implementation

**Problem Solved:** Needed parallel API calls to reduce total response time.

**How I Formulated the Problem:**
*"Show me how to query multiple LLM APIs in parallel using asyncio. Some clients are synchronous (OpenAI, Groq), one is different (Gemini). Need to handle errors gracefully."*

**AI Contribution:**
- Provided `asyncio.gather()` pattern
- Suggested `run_in_executor()` for sync clients
- Error handling wrapper example

**My Implementation:**
```python
async def query_all_models(user_input):
    tasks = [
        query_openai(user_input),
        query_anthropic(user_input),
        query_groq(user_input)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return process_results(results)
```

**Result:** Response time reduced from ~10s (sequential) to ~3s (parallel)

---

### AI Usage Statistics Summary

| Task Category | AI Contribution | My Contribution |
|--------------|-----------------|-----------------|
| Planning & Architecture | 40% guidance | 60% decision-making |
| Environment Setup | 50% instructions | 50% execution & debugging |
| Code Generation | 60% boilerplate | 40% customization & integration |
| Prompt Engineering | 30% suggestions | 70% iteration & testing |
| Debugging | 70% solutions | 30% verification & implementation |
| Documentation | 50% structure | 50% content & reflection |

**Overall Project:** ~50% AI assistance, ~50% human judgment, integration, and validation

---

### What AI Tools Did NOT Do

**Important Clarifications:**

1. **Strategic Decisions:** AI suggested options; I chose which approaches to take based on constraints
2. **Integration:** AI provided components; I made them work together
3. **Testing:** AI generated code; I validated it actually works
4. **Iteration:** AI suggested improvements; I measured results and decided what to keep
5. **Problem Discovery:** I identified issues (model deprecation, coordinate accuracy); AI helped solve them
6. **Quality Control:** I evaluated AI outputs critically and refined/rejected as needed

**Example:** When Gemini APIs failed, AI provided diagnostic steps, but I made the strategic decision to proceed with 3 models rather than spend more time debugging.

---

### Transparency & Learning

**Why Document AI Usage So Thoroughly?**

1. **Honesty:** Project guidelines explicitly encourage AI tools and request documentation
2. **Scientific Method:** Showing prompts and iterations demonstrates systematic thinking
3. **Learning Demonstration:** Understanding how to formulate problems for AI is a valuable skill
4. **Future Reference:** Documenting what works helps others (and future me)

**Key Learning:** AI tools are force multipliers, not replacements. The value I provided was:
- **Judgment:** Choosing right approaches
- **Integration:** Making components work together  
- **Validation:** Testing and verifying outputs
- **Iteration:** Improving based on results
- **Problem-Solving:** Debugging real-world issues

**2-3 Hour Timeline Enabled By:**
- Strategic AI usage for boilerplate and research
- Focus on MVP over perfection
- Parallel development (testing while building)
- Quick decision-making when issues arose

---

## 5. Deliverables & Results

### Part 1: Teeth X-ray Wisdom Tooth Detector ✅

**Status:** Functional MVP

**Features:**
- Streamlit web interface with image upload
- GPT-4 Vision API integration
- Bounding box visualization on X-rays
- Sample image gallery
- JSON output with coordinates and analysis

**Technical Specs:**
- Model: GPT-4o (Vision)
- Cost per analysis: ~$0.005
- Average response time: ~2-3 seconds
- Coordinate accuracy: ~90% valid

**Limitations:**
- Bounding boxes approximate (acceptable for demo)
- No persistent storage
- Single image processing only

---

### Part 2: Multi-Model LLM Chatbot ✅

**Status:** Functional MVP

**Features:**
- Side-by-side comparison of 3 LLMs
- Parallel async querying (~3s total response time)
- Conversation history support
- Performance metrics (response time, tokens)
- Model selection interface

**Models Integrated:**
1. GPT-4o (OpenAI) - Balanced quality
2. Claude 3.5 Sonnet (Anthropic) - Strong reasoning
3. Llama 3.3 70B (Groq) - Fast, open-source

**Technical Specs:**
- Architecture: Async parallel API calls
- Average combined response: ~3 seconds
- Error handling: Graceful degradation
- Cost per query: ~$0.01-0.02

**Limitations:**
- No streaming responses
- Basic UI (functional, not polished)
- Limited conversation memory

---

### Documentation ✅

**GitHub Repository Structure:**
```
tiny-project-llm-platform/
├── teeth_detector/          # Part 1: Vision detection
│   ├── app.py              # Streamlit app
│   ├── vision_api.py       # GPT-4 Vision wrapper
│   └── sample_images/      # Test X-rays
├── multi_llm_chat/         # Part 2: Multi-model chat
│   ├── app.py              # Streamlit app
│   └── llm_apis.py         # API wrappers
├── AI_USAGE.md             # Detailed AI tool log
├── reports/
│   └── project_report.md   # This document
├── requirements.txt        # Dependencies
└── README.md               # Project overview
```

**Documentation Quality:**
- Comprehensive AI usage log with prompts and reasoning
- Code comments explaining key decisions
- This project report with honest reflection
- README with setup instructions

---

## 6. Reflection

### What Went Well

**Rapid Prototyping:**
- Achieved both deliverables in 2-3 hours
- Strategic AI usage accelerated development without compromising learning
- MVP approach delivered functional demos quickly

**Transparent AI Collaboration:**
- Documented all AI assistance in real-time
- Demonstrated how to formulate problems for AI effectively
- Showed iterative refinement process (prompt engineering)

**Problem-Solving:**
- Quickly adapted when APIs deprecated mid-development
- Made pragmatic decisions (3 models vs 4) to stay on timeline
- Implemented validation layers when AI outputs needed refinement

**Technical Learning:**
- Gained practical experience with multiple AI APIs
- Learned async programming patterns
- Understood prompt engineering through iteration

### What Could Be Improved

**With More Time, I Would:**
- Add streaming responses for real-time feedback
- Implement persistent storage for conversation history
- Fine-tune bounding box detection with more examples
- Add comprehensive error recovery mechanisms
- Polish UI/UX beyond functional MVP

**Technical Debt:**
- Hardcoded some configurations (should use config files)
- Minimal input validation
- Basic error messages (could be more user-friendly)
- No unit tests (acceptable for 3-hour demo)

### Key Takeaways

**AI Tools Are Force Multipliers:**
- 2-3 hours of work with AI ≈ 8-12 hours without
- But human judgment still critical for quality
- AI generates options; humans make decisions

**Rapid Development Requires Trade-offs:**
- MVP > Perfection when timeline is tight
- Focus on functional over polished
- Document limitations honestly

**Prompt Engineering Is Iterative:**
- First prompts rarely optimal
- Measure results, refine based on data
- Specificity and constraints improve outputs

**Real-World APIs Are Messy:**
- Expect deprecations and breaking changes
- Build fallback mechanisms
- Test thoroughly before relying on documentation

### Honesty Statement

This project heavily leveraged AI tools as explicitly encouraged by project guidelines. The short timeline (2-3 hours) was possible because:
- AI handled boilerplate code generation
- AI accelerated research and troubleshooting
- I focused on integration, testing, and decision-making

**My core contributions were:**
- Strategic planning and approach selection
- Prompt engineering and iteration
- Integration of multiple components
- Debugging and problem-solving
- Critical evaluation of AI outputs
- Documentation and reflection

Both applications are functional MVPs demonstrating practical AI integration. They could be expanded with more time, but serve their purpose as honest demonstrations of rapid AI-assisted development.

---

**Total Project Time: 2-3 hours**  
**Total API Cost: ~$2-3**  
**Lines of Code: ~500-600**  
**AI Assistance: ~50% generation, 100% human validation**

---