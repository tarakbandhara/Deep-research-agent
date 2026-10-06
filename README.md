# 🔎 Research Agent

An AI-powered deep research assistant built with **Chainlit**, **OpenAI Agents SDK**, **OpenRouter**, and **SerpAPI**.

Research a topic, let the agent plan the investigation, search the web, synthesize the findings, and generate a detailed research report through a clean conversational interface.

---

## ✨ Features

- 🔎 AI-powered deep research workflow
- 🧭 Automatic research planning
- 🌐 Web search through SerpAPI
- ✍️ AI-generated research reports
- ⚡ Asynchronous research execution
- 📊 Live research progress indicator
- ● Animated active-stage indicator while research is running
- ⚠️ Clear rate-limit and error handling
- 🚀 Starter prompt for quick research


---

## 🚀 Live Demo

The Research Agent is deployed and available to try online.

👉 **Try the Research Agent:** https://research.tarakbandhara.in

The deployed application runs the complete research workflow, including planning, web search, AI-powered research synthesis, and final report generation.

> **⚠️ API & Model Rate Limits**
>
> The live demo uses third-party AI models and APIs that are subject to usage and rate limits. Depending on current usage, you may occasionally see a rate-limit error or the research workflow may be temporarily unavailable.
>
> If you encounter a rate-limit message, please try again later.

---

## 🧠 How It Works

The application follows a multi-stage research pipeline:

```text
User Question
      │
      ▼
┌───────────────┐
│ Planner Agent │
└───────┬───────┘
        │
        ▼
 Research Plan
        │
        ▼
┌───────────────┐
│  Search Agent │
└───────┬───────┘
        │
        ▼
   Web Research
     (SerpAPI)
        │
        ▼
┌───────────────┐
│  Writer Agent │
└───────┬───────┘
        │
        ▼
 Final Research Report
```

During research, the interface displays the active stage:

```text
● Planning
✓ Planning
● Searching
✓ Planning
✓ Searching
● Writing
✓ Planning
✓ Searching
✓ Writing
● Finalizing
✓ Research complete
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application and agent logic |
| Chainlit | Conversational web interface |
| OpenAI Agents SDK | Agent orchestration |
| OpenRouter | LLM access |
| Gemini | Research report writing |
| SerpAPI | Web search |
| python-dotenv | Environment variable management |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/tarakbandhara/Deep-research-agent
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your API credentials:

```env
open_router_base_url=YOUR_OPENROUTER_BASE_URL
openrouter_api_key=YOUR_OPENROUTER_API_KEY
serpapi_api_key=YOUR_SERPAPI_API_KEY
gemini_api_key=YOUR_GOOGLE_API_KEY
```

---

## ▶️ Running the Application

Start the application with:

```bash
chainlit run app.py
```

Then open the local URL shown in the terminal.

---

## 🔬 Example

Try a question such as:

```text
What are the latest developments in AI agents?
```

The application will:

1. Receive the research question.
2. Create a research plan.
3. Perform web searches.
4. Process the search results.
5. Generate the final research report.
6. Display the completed report in the chat.

---

## ⚠️ Rate Limits and Errors

The application includes handling for API rate limits.

If a provider returns a rate-limit response, the interface displays a clear message rather than presenting the failure as a generic research error.

Depending on the provider, you may need to wait before running another research request.

---

## 📜 License

This project is licensed under the MIT License.

See [`LICENSE`](LICENSE) for the complete license text.

---

## 👤 Author

**Tarak Bandhara**

Built as an AI-powered research assistant for exploring topics and generating detailed research reports.

---

## 🤝 Contributing

Contributions, improvements, and suggestions are welcome.

For substantial changes:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the application.
5. Submit a pull request.

---

## ⚠️ Disclaimer

AI-generated research can contain mistakes or inaccuracies.

**AI agents can make mistakes. Always verify important information using the original sources.**
