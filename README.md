# 🤖 Customizable Dataset Generator using GPT

A flexible framework for generating synthetic datasets using OpenAI's GPT model. Easily adaptable for various types of text data with a focus on creating realistic interactions between two roles (e.g., customer and support agent).

## ✨ Features

- 🤖 **GPT-Powered Generation** – Leverages OpenAI's advanced language models
- 🎯 **Customizable Prompts** – Flexible prompt templates for different use cases
- 📚 **Text File Input Support** – Generate datasets from existing text files
- 🧩 **Smart Chunking** – Handles large input files efficiently
- 🌍 **Multi-Language Support** – Generate content in different languages
- 📊 **Multiple Output Formats** – CSV and JSONL for various applications
- 🧠 **Fine-Tuning Ready** – Output compatible with LLM fine-tuning processes
- 🛡️ **Robust Error Handling** – Built-in rate limiting and retry mechanisms

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [Output Formats](#output-formats)
- [Fine-Tuning Compatibility](#fine-tuning-compatibility)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Prerequisites

- **Python 3.6+**
- **OpenAI API key** ([Get one here](https://platform.openai.com/api-keys))
- **Git** (for cloning the repository)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/Royofficely/Customizable-Dataset-Generator-using-GPT.git
cd Customizable-Dataset-Generator-using-GPT
```

> ⚠️ **Important**: The `cd` command is crucial for proper setup and execution.

### 2. Run Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:
- ✅ Verify Python 3.6+ installation
- 🌿 Create and configure virtual environment
- 📦 Install required dependencies
- 🔑 Securely store your OpenAI API key
- 🔗 Create convenient run alias

### 3. Start Generating

After setup, run from any directory:

```bash
run
```

> 💡 **Tip**: If the `run` command doesn't work immediately, restart your terminal or run `source ~/.bashrc` (or `~/.zshrc`).

## 🖥️ Usage

### Basic Usage

```bash
# Using the alias (recommended)
run

# Or directly
./run.sh
```

### Configuration-Based Generation

The generator uses `config.yaml` and `prompts.yaml` files for customization. Simply edit these files and run the script to generate your custom dataset.

## ⚙️ Configuration

### Main Configuration (`config.yaml`)

```yaml
# Input Settings
use_text_file: false           # Use existing text file as input
text_file_path: "input.txt"    # Path to input file
use_chunking: true             # Enable text chunking for large files

# Generation Settings
language: "English"            # Output language
subject: "customer support"    # Type of interactions
model: "gpt-3.5-turbo"        # GPT model to use
num_interactions: 100          # Number of data points to generate
delay: 1                       # Delay between API calls (seconds)

# Output Settings
output_file: "generated_data.csv"  # Output filename
role1: "Customer"              # First role in interactions
role2: "Agent"                 # Second role in interactions

# Topics (optional)
topics:
  - "billing issues"
  - "technical support"
  - "product questions"
```

### Prompt Templates (`prompts.yaml`)

```yaml
# Prompt for text file input
prompt_text_file: |
  Generate a realistic conversation between a {role1} and {role2} based on this content: {chunk}
  
# Prompt for topic-based generation
prompt_llm: |
  Create a {language} conversation between a {role1} and {role2} about {subject}.
  Make it realistic and helpful.
```

## 📤 Output Formats

The generator creates two complementary output files:

### 1. CSV Format (`generated_data.csv`)

```csv
topic,generated_text,role1,role2
billing issues,"Customer: I have a question about my bill...",Customer,Agent
```

### 2. JSONL Format (`generated_data.jsonl`)

```json
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

## 🧠 Fine-Tuning Compatibility

The JSONL output is designed for LLM fine-tuning with the standard conversation format:

```json
{
  "messages": [
    {
      "role": "system", 
      "content": "This is a conversation about [topic]. Customer is seeking help from Agent."
    },
    {
      "role": "user", 
      "content": "Customer message here"
    },
    {
      "role": "assistant", 
      "content": "Agent response here"
    }
  ]
}
```

### Using for Fine-Tuning

1. Generate your dataset using this tool
2. Use the `.jsonl` file as training data
3. Follow your LLM platform's fine-tuning documentation

> 📚 **Note**: Always check your specific platform's requirements as formats may vary.

## 🔬 Advanced Features

### Text File Processing

```yaml
use_text_file: true
text_file_path: "knowledge_base.txt"
use_chunking: true
```

Process existing documentation or knowledge bases to generate relevant conversations.

### Batch Processing

Generate large datasets efficiently with built-in rate limiting and retry mechanisms.

### Custom Parsing

Implement custom parsing logic in the `convert_to_jsonl.py` script for specific field extraction.

### Multi-Language Support

```yaml
language: "Spanish"  # or French, German, etc.
```

Generate datasets in multiple languages for international applications.

## 🛡️ Error Handling

The system includes comprehensive error handling:

- **🕒 Rate Limiting** – Automatic backoff and retry
- **🔒 Authentication** – Clear API key validation
- **🚫 API Errors** – Graceful error recovery
- **📁 File Operations** – Robust file handling
- **📝 Configuration** – YAML parsing validation

## 🔍 Troubleshooting

### Common Issues

**API Key Problems**
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Re-run setup if needed
./setup.sh
```

**Rate Limiting**
```yaml
# Increase delay in config.yaml
delay: 2  # or higher
```

**Model Availability**
```yaml
# Use available model
model: "gpt-3.5-turbo"  # instead of gpt-4 if not available
```

**Script Execution Issues**
```bash
# Make sure you're in the project directory
pwd

# Activate virtual environment manually if needed
source venv/bin/activate
python main.py
```

### Getting Help

1. Check the [Issues](https://github.com/Royofficely/Customizable-Dataset-Generator-using-GPT/issues) page
2. Review the troubleshooting section above
3. Ensure all prerequisites are met
4. Verify your OpenAI API key has sufficient credits

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

### Development Setup

```bash
# Fork and clone your fork
git clone https://github.com/YOUR_USERNAME/Customizable-Dataset-Generator-using-GPT.git
cd Customizable-Dataset-Generator-using-GPT

# Create feature branch
git checkout -b feature/amazing-feature

# Make your changes and commit
git commit -m 'Add amazing feature'

# Push and create PR
git push origin feature/amazing-feature
```

### Contribution Guidelines

- Write clear, descriptive commit messages
- Add tests for new features
- Update documentation as needed
- Follow existing code style
- Open an issue for major changes first

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Important Disclaimers

- **Educational Use**: This project is for educational and research purposes
- **API Compliance**: Ensure compliance with OpenAI's use-case policy and terms of service
- **Responsible Use**: Generated data should not be used for malicious purposes or creating misleading information
- **API Costs**: Be aware that generating large datasets will consume OpenAI API credits
- **Data Quality**: Always review and validate generated content before use in production

---

**Made with ❤️ by Roy Nativ**

**⭐ Star this repo if you find it helpful!**
