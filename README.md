# ResumeParser with Local Agentic AI

A powerful, privacy-focused Resume Parser that uses **Local LLMs (Large Language Models)** to extract information and generate insights from Resumes/CVs. 

> **New:** Now fully migrated from `pyresparser` to **Agentic AI** using `Qwen2.5-1.5B`!

## 🚀 Features

-   **AI Power**: Uses `Qwen2.5-1.5B-Instruct` (GGUF) for high-speed, accurate extraction.
-   **Smart Extraction**: Extracts Name, Email, Mobile, Skills, Education, Experience, Companies, and more.
-   **Intelligent Insights**: Automatically generates a **Professional Summary** and identifies **Key Strengths** for each candidate.
-   **Structured Data**: Outputs strict JSON format for easy integration.
-   **Zero API Cost**: Runs 100% locally. No OpenAI/Anthropic/Gemini keys required.
-   **Cross-Platform**: Windows, macOS (Intel/Silicon), Linux.
-   **Portable**: Can be built into a standalone executable.

## 🛠️ Technical Details

-   **Model**: `Qwen2.5-1.5B-Instruct` (Quantized: `q4_k_m`)
    -   *Why Qwen?* It is significantly faster and more accurate for structured data extraction than many 7B models, while being lightweight (~1GB).
-   **Inference Engine**: `llama-cpp-python` (with Metal/CUDA support).
-   **Context Window**: `2048` tokens (input text is truncated to ~1500 chars to fit).
-   **Hardware Requirements**:
    -   **RAM**: Minimum 4GB (8GB recommended).
    -   **Disk**: ~2GB free space (Repository + 1GB Model).
    -   **GPU**: Optional.
        -   *macOS*: Supports Metal acceleration (though configured to CPU-fallback by default for stability).
        -   *NVIDIA*: Supports CUDA if configured.
    -   **CPU**: Any modern CPU (AVX2 support recommended).

## 📦 Installation

### 1. Clone & Setup
```bash
git clone https://github.com/YourUsername/ResumeParser.git
cd ResumeParser
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 2. Download AI Model
We use a script to automatically verify and download the GGUF model from Hugging Face.
```bash
python download_model.py qwen
```
*This will download `qwen2.5-1.5b-instruct-q4_k_m.gguf` to `resume_parser/models/`.*

### 3. Run the App
```bash
python resume_parser/manage.py makemigrations
python resume_parser/manage.py migrate
python resume_parser/manage.py runserver
```
Visit `http://127.0.0.1:8000/` to access the GUI.

## 🐳 Running with Docker

```bash
docker-compose up --build
```
*Note: The Docker image includes the model download step automatically.*

## 🔨 Building Portable App (macOS)

You can create a standalone executable that doesn't require Python to be installed on the target machine.

```bash
./build_mac.sh
```
The output zip `ResumeParser_Mac.zip` will be generated in the project root.

## 📊 Result Format

The AI extracts data in the following JSON structure:

```json
{
    "name": "Omkar Pathak",
    "email": "omkarpathak27@gmail.com",
    "mobile_number": "xxxxxxx34",
    "skills": ["Python", "Django", "Machine Learning", "AI"],
    "education": "BE in Computer Science, Pune University",
    "experience": "5+ years in Full Stack Development...",
    "company_names": ["Ellicium Solutions", "Numerator"],
    "ai_summary": "Highly skilled Python Developer with...",
    "ai_strengths": "Strong problem-solving, System Design..."
}
```

## 📜 License
MIT License
