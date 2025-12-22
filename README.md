# 🦷 Tiny Project LLM Platform

A comprehensive platform featuring two main applications:
1. **Teeth X-ray Wisdom Tooth Detector** - Uses GPT-4 Vision API to detect and annotate wisdom teeth in dental X-rays
2. **Multi-Model LLM Chatbot** - Compares responses from GPT-4, Llama 3.3 70B (Groq), and Gemini 2.5 Flash side-by-side

Built with Streamlit, featuring async parallel API calls and modern LLM integration patterns.

## ✨ Features

### Teeth X-ray Detector
- **AI-Powered Detection**: Uses GPT-4 Vision to identify wisdom teeth in panoramic dental X-rays
- **Visual Annotations**: Automatically draws bounding boxes (yellow outline, red semi-transparent fill) around detected wisdom teeth
- **Detailed Analysis**: Provides quadrant-specific analysis (upper left, upper right, lower left, lower right)
- **Sample Images**: Includes sample X-ray images for testing
- **Interactive UI**: Clean, user-friendly Streamlit interface with side-by-side input/output comparison

### Multi-Model LLM Chatbot
- **Parallel Querying**: Query GPT-4, Llama 3.3 70B (Groq), and Gemini 2.5 Flash simultaneously
- **Side-by-Side Comparison**: View responses from all models in a single interface
- **Performance Metrics**: Track response times and token usage for each model
- **Conversation History**: Maintain context across multiple conversation turns
- **Model Selection**: Choose which models to query via checkboxes
- **Free Tier Friendly**: Groq offers free tier with fast inference

### Shared Features
- **Error Handling**: Comprehensive error messages for API issues, quota limits, and authentication problems
- **Async Architecture**: Efficient parallel API calls using asyncio
- **Environment Configuration**: Easy setup via `.env` file

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher (tested with Python 3.13)
- OpenAI API key with GPT-4 Vision access
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tiny-project-llm-platform
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   Get your API key from: https://platform.openai.com/api-keys

5. **Run the applications**
   
   **Teeth X-ray Detector:**
   ```bash
   streamlit run teeth_detector/app.py
   ```
   
   **Multi-Model LLM Chatbot:**
   ```bash
   streamlit run multi_llm_chat/app.py
   ```

   The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
tiny-project-llm-platform/
├── teeth_detector/
│   ├── app.py                 # Teeth detection Streamlit app
│   ├── vision_api.py          # OpenAI Vision API integration
│   └── sample_images/         # Sample X-ray images for testing
├── multi_llm_chat/
│   ├── app.py                 # Multi-LLM chatbot Streamlit app
│   ├── llm_apis.py            # API wrappers for OpenAI, Anthropic, Gemini
│   ├── config.py              # Configuration settings
│   └── README.md              # Chatbot-specific documentation
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── AI_USAGE.md                 # AI tool usage log
└── README.md                   # This file
```

## 🎯 Usage

### Teeth X-ray Detector

1. **Upload an X-ray image** or select a sample from the sidebar
2. Click **"🔍 Analyze X-ray"** button
3. View the results:
   - **Input**: Original X-ray image
   - **Output**: Annotated X-ray with bounding boxes around detected wisdom teeth
   - **Analysis**: Detailed text analysis and structured JSON data

### Multi-Model LLM Chatbot

1. **Select models** to query using checkboxes in the sidebar
2. **Type your message** in the chat input
3. **View responses** from all selected models side-by-side
4. **Check metrics** in the expandable sections to see performance data
5. **Compare** responses and performance in the comparison table

## 🔧 Configuration

### API Key Setup

**Required API Keys:**
- `OPENAI_API_KEY` - For GPT-4 (teeth detector) and GPT-4 (chatbot)
- `GROQ_API_KEY` - For Llama 3.3 70B (chatbot) - Free tier available
- `GOOGLE_API_KEY` - For Gemini 2.5 Flash (chatbot)

The applications look for API keys in the following order:
1. `.env` file in the project root
2. Environment variables

**Example `.env` file:**
```env
OPENAI_API_KEY=sk-your-openai-key-here
GROQ_API_KEY=your-groq-api-key-here
GOOGLE_API_KEY=your-google-api-key-here
```

To update your API keys:
1. Edit the `.env` file
2. Restart the Streamlit app (or clear cache: ⋮ menu > Clear cache)

## 📦 Dependencies

**Core:**
- **streamlit** (1.29.0): Web application framework
- **python-dotenv** (1.0.0): Environment variable management

**LLM APIs:**
- **openai** (>=1.12.0): OpenAI API client (GPT-4)
- **groq** (>=0.4.0): Groq API client (Llama 3.1 70B)
- **google-generativeai** (>=0.3.0): Google AI client (Gemini)

**Image Processing:**
- **Pillow** (>=10.2.0): Image processing
- **numpy** (>=1.26.0): Numerical operations
- **opencv-python** (4.8.1.78): Image processing

**Async Support:**
- **aiohttp** (3.9.1): Async HTTP client

See `requirements.txt` for the complete list.

## 🐛 Troubleshooting

### API Quota Exceeded (429 Error)

- Check your usage: https://platform.openai.com/usage
- Add credits: https://platform.openai.com/account/billing
- Wait for quota reset if on a free tier

### API Key Not Found

- Ensure `.env` file exists in the project root
- Verify the file contains: `OPENAI_API_KEY=sk-...`
- Restart Streamlit after updating `.env`

### Package Installation Issues

If you encounter issues installing packages (especially on Python 3.13):
- Some packages may need newer versions (see `requirements.txt`)
- Try upgrading pip: `python -m pip install --upgrade pip setuptools wheel`

### Annotated Images in Dropdown

Annotated images are automatically excluded from the sample images dropdown. They are saved to `temp_annotations/` folder to keep the sample images directory clean.

## 🎨 Features in Detail

### Bounding Box Visualization

- **Yellow outline**: 3px width border around detected wisdom teeth
- **Red semi-transparent fill**: 100/255 opacity overlay
- **Labels**: Text labels above each bounding box indicating quadrant

### Analysis Output

The AI provides:
- Quadrant-specific detection (upper left, upper right, lower left, lower right)
- Status information (erupted, partially erupted, impacted)
- Detailed descriptions and recommendations
- Structured JSON data for programmatic access

## ⚠️ Important Notes

- **Medical Disclaimer**: This is a demonstration project and should NOT be used for actual medical diagnosis
- **API Costs**: GPT-4 Vision API usage incurs costs. Monitor your usage at https://platform.openai.com/usage
- **Accuracy**: AI detection accuracy depends on image quality and X-ray type

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

See `LICENSE` file for details.

## 🔗 Resources

- [OpenAI Platform](https://platform.openai.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [GPT-4 Vision API Docs](https://platform.openai.com/docs/guides/vision)

## 📝 Changelog

### Version 2.0.0 (2025-12-22)
- Added Multi-Model LLM Chatbot
- Parallel async API calls
- Side-by-side response comparison
- Performance metrics tracking

### Version 1.0.0 (2025-12-22)
- Initial release
- GPT-4 Vision integration for teeth detection
- Bounding box visualization
- Sample image support
- Comprehensive error handling

---

**Made with ❤️ using GPT-4 Vision and Streamlit**
