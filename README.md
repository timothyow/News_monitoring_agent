
# Email summary AI Agent (news monitoring reports)

This Streamlit app uses LangGraph and OpenAI to read weekly news monitoring reports in `.docx` format, extract key country-level updates, summarize regional insights, and auto-generate a polished professional email draft for executive stakeholders.

## Project Features

- Upload `.docx` report with country updates
- Auto-analyze country-level insights using LLM such as GPT-4o
- Generate a regional summary
- Auto-draft an executive email for managment team
- Built using Streamlit + LangGraph + LangChain

## File Structure

```
├── streamlit_app.py          # Main application logic
├── requirements.txt          # Python dependencies
└── .streamlit
    └── config.toml           # UI configuration
```

## Deployment on Streamlit Cloud

1. **Clone or upload this repo to GitHub**
2. **Visit [https://streamlit.io/cloud](https://streamlit.io/cloud)** and sign in with GitHub
3. **Create a new app** and select this repo and `streamlit_app.py`
4. **Set environment variable** in the app settings:
    - `OPENAI_API_KEY`: Your OpenAI API Key
5. **Click Deploy** and get your live app URL!

## Requirements

Install dependencies locally for testing:
```bash
pip install -r requirements.txt
```

## Security

- This app runs your uploaded documents through OpenAI's API.
- For enterprise usage, consider securing via login and storing sensitive docs securely.

## Example Use Case

> Upload weekly regional news monitoring document every Monday. Get email-ready summary for the management with minimal editing.

---
