# 🤖 Customizable Dataset Generator using GPT

This project provides a flexible framework for generating synthetic datasets using OpenAI's GPT model. It can be easily adapted to generate various types of text data based on user-defined topics and prompts, with a focus on creating realistic interactions between two roles (e.g., customer and support agent).

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Output](#-output)
- [Fine-tuning Compatibility](#-fine-tuning-compatibility)
- [Error Handling](#-error-handling)
- [Advanced Features](#-advanced-features)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Disclaimer](#-disclaimer)

## 🛠 Prerequisites

- Python 3.6+
- OpenAI API key
- Git (for cloning the repository)

## 🚀 Quick Start

1. Clone this repository and navigate into the project directory:
   ```bash
   git clone https://github.com/Royofficely/Customizable-Dataset-Generator-using-GPT.git
   cd Customizable-Dataset-Generator-using-GPT
   ```
   
   > ⚠️ Note: The `cd` command is crucial. It ensures you're in the correct directory to run the setup script and use the project files.

2. Run the setup script:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
   
   This script will:
   - ✅ Check for Python 3.6+
   - 🌿 Create a virtual environment
   - 📦 Install dependencies
   - 🔑 Prompt you for your OpenAI API key and save it securely
   - 🔗 Create an alias for easy execution

3. After setup, you can run the main script from any directory by simply typing:
   ```bash
   run
   ```

> 💡 Tip: If the `run` command doesn't work immediately, you may need to restart your terminal or source your shell configuration file (`source ~/.bashrc` or `source ~/.zshrc`) for the alias to take effect.

## 🖥 Usage

After the initial setup, you can generate datasets using the following steps:

1. Ensure you're in the project directory or any directory if you've set up the alias.
2. Run the script:
   ```bash
   run
   ```
   or if the alias isn't working:
   ```bash
   ./run.sh
   ```
3. The script will use the configurations from `config.yaml` and `prompts.yaml` to generate your dataset.

## ⚙ Configuration

Edit the `config.yaml` and `prompts.yaml` files to customize:

- `use_text_file`: Set to true if you want to use a text file as input
- `text_file_path`: Path to the input text file (if `use_text_file` is true)
- `use_chunking`: Enable text chunking for large input files
- `language`: Set the language of the generated content
- `subject`: The type of text being generated (e.g., "customer support interactions")
- `model`: The GPT model to use (e.g., "gpt-3.5-turbo")
- `num_interactions`: Number of data points to generate
- `delay`: Delay between API calls (in seconds)
- `output_file`: Name of the output CSV file
- `role1` and `role2`: The two roles in the interaction (e.g., "Customer" and "Agent")
- `prompt_llm`: The prompt template for generating text when not using a text file
- `prompt_text_file`: The prompt template for generating text when using a text file
- `topics`: List of topics or categories for generation (optional)

## 📤 Output

The script generates two output files:

1. 📄 A CSV file (specified by `output_file` in the config) containing the raw generated text and topics.
2. 📊 A JSONL file (same name as the CSV but with `.jsonl` extension) containing a structured version of the interactions, parsed into a more usable format.

## 🧠 Fine-tuning Compatibility

The JSONL output of this generator is designed to be compatible with common LLM fine-tuning processes. Each entry in the JSONL file follows this structure:

```json
{
  "messages": [
    {"role": "system", "content": "This is a conversation about [topic]. [role1] is the customer and [role2] is the support agent."},
    {"role": "user", "content": "User message"},
    {"role": "assistant", "content": "Assistant response"},
    ...
  ]
}
```

This format is suitable for fine-tuning models like those offered by OpenAI. However, always check the specific requirements of your chosen LLM platform, as formats may vary.

To use this data for fine-tuning:

1. Ensure your JSONL file is generated using the latest version of the `convert_to_jsonl.py` script.
2. Follow the fine-tuning instructions provided by your LLM platform, using this JSONL file as your training data.

> Note: Fine-tuning requirements and processes can change. Always refer to the most up-to-date documentation of your LLM provider.

## 🛡 Error Handling

The script includes robust error handling for:
- 🕒 API rate limit errors (waits and retries)
- 🔒 Authentication errors
- 🚫 Unexpected errors (waits and retries)
- 🔍 File not found errors
- 📝 YAML parsing errors

## 🔬 Advanced Features

- 📚 **Text File Input**: Use a text file as input for generating interactions.
- 🧩 **Text Chunking**: Split large input files into manageable chunks.
- 🏷 **Topic Generation**: Automatically generate a topic for each interaction based on the content.
- 🔧 **Custom Parsing**: Implement custom parsing logic to extract specific fields from generated text.
- 📦 **Batch Processing**: Generate large datasets in batches to manage API usage and processing time.
- 🔌 **Extensibility**: Modular design allows for easy addition of new features or integration with other data processing pipelines.

## 🔍 Troubleshooting

- 🔑 **API Key Issues**: Ensure your OpenAI API key is correctly set in the `.env` file or as an environment variable.
- ⏱ **Rate Limiting**: If you encounter frequent rate limit errors, try increasing the `delay` value in your config file.
- 🤖 **Model Availability**: Make sure the specified model in your config file is available in your OpenAI plan.
- 🖥 **Script Execution**: If you're having trouble running the script, ensure you're in the correct directory and the `run` alias is set up correctly.
- 🌿 **Virtual Environment**: If you see an error about missing modules, make sure you've activated the virtual environment or use the `run` command.
- 📄 **Input File Issues**: If using a text file as input, ensure the file exists and the path is correct in the config file.
- 🐚 **Shell Configuration**: If the `run` command doesn't work, try sourcing your shell configuration file (`source ~/.bashrc` or `source ~/.zshrc`) or restart your terminal.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## ⚠️ Disclaimer

This project is for educational and research purposes only. Ensure you comply with OpenAI's use-case policy and terms of service when using their API. The generated data should not be used for any malicious purposes or to create misleading information.
