# Customizable Dataset Generator using GPT

This project provides a flexible framework for generating synthetic datasets using OpenAI's GPT model. It can be easily adapted to generate various types of text data based on user-defined topics and prompts, with a focus on creating realistic interactions between two roles (e.g., customer and support agent).

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Manual Setup](#manual-setup)
- [Usage](#usage)
- [Customization](#customization)
- [Output](#output)
- [Error Handling](#error-handling)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## Prerequisites

- Python 3.6+
- OpenAI API key
- Git (for cloning the repository)

## Quick Start

1. Clone this repository:
   ```bash
   git clone https://github.com/Royofficely/Customizable-Dataset-Generator-using-GPT.git
   cd Customizable-Dataset-Generator-using-GPT
   ```

2. Run the setup script:
   ```bash
   chmod +x setup.sh
   sh setup.sh
   ```
   This script will:
   - Check for Python 3.6+
   - Create a virtual environment
   - Install dependencies
   - Prompt you for your OpenAI API key and save it securely
   - Activate the virtual environment
   - Run the main script automatically

After running the setup script, you're all set! The script will have generated your dataset based on the default configuration.

## Manual Setup

If you prefer to set up manually:

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add the following line to the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

## Usage

If you've used the Quick Start method, the script will have run automatically after setup. For subsequent runs or if you've done a manual setup:

1. Ensure your virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```

2. Run the script with your configuration file:
   ```bash
   ./venv/bin/python main-script.py config-file.yaml
   ```

The script will generate the dataset based on your configuration and save it to the specified output files.

## Customization

Edit the `config-file.yaml` to customize:

- `use_text_file`: Set to true if you want to use a text file as input, false otherwise
- `text_file_path`: Path to the input text file (if `use_text_file` is true)
- `use_chunking`: Set to true to enable text chunking for large input files
- `language`: Set the language of result.
- `subject`: The type of text being generated (e.g., "customer support interactions")
- `model`: The GPT model to use (e.g., "gpt-3.5-turbo")
- `num_interactions`: Number of data points to generate
- `delay`: Delay between API calls (in seconds)
- `output_file`: Name of the output CSV file
- `role1` and `role2`: The two roles in the interaction (e.g., "Customer" and "Agent")
- `prompt_llm`: The prompt template for generating text when not using a text file
- `prompt_text_file`: The prompt template for generating text when using a text file
- `topics`: List of topics or categories for generation (optional)

Example `config-file.yaml`:

```yaml
use_text_file: false
text_file_path: "knowledge_base.txt"
use_chunking: false
subject: "customer support interactions"
model: "gpt-3.5-turbo"
num_interactions: 5
delay: 1
output_file: "synthetic_dataset.csv"
role1: "Customer"
role2: "Agent"
language: "English"
topics:
  - "product returns"
  - "billing issues"
  - "technical support"
  - "account management"
  - "shipping inquiries"
prompt_llm: "Generate a detailed and realistic {subject} interaction between a {role1} and a {role2}. The interaction should include:
1. A specific inquiry or problem from the {role1} related to {topic}
2. A detailed and helpful response from the {role2}
3. Any relevant technical details, error messages, or specific examples that would typically be part of such an interaction
4. A natural flow of conversation, including any necessary follow-up questions or clarifications
Format the interaction as:
'{role1}: [{role1}'s detailed message]
{role2}: [{role2}'s comprehensive response]
{role1}: [any follow-up question if applicable]
{role2}: [follow-up response if applicable]'
Ensure the example is as realistic and detailed as possible, mimicking a real-life scenario."
prompt_text_file: "IMPORTANT: Respond ONLY in the same language as the provided information. Do not translate or use any other language.

Generate a detailed and realistic interaction between a {role1} and a {role2} based on the following information: {context}

The interaction should include:
1. A specific inquiry or problem from the {role1} related to the provided information
2. A detailed and helpful response from the {role2}, using only the information provided
3. Any relevant technical details, error messages, or specific examples mentioned in the provided information
4. A natural flow of conversation, including any necessary follow-up questions or clarifications

Format the interaction as:
'{role1}: [{role1}'s detailed message]
{role2}: [{role2}'s comprehensive response]
{role1}: [any follow-up question if applicable]
{role2}: [follow-up response if applicable]'

Ensure the example is as realistic and detailed as possible, mimicking a real-life scenario.

FINAL REMINDER: Your entire response must be in the same language as the provided information. Do not use any knowledge outside of the given context."
prompt_generate_topic: "Based on the following conversation, generate a short, concise topic (1-5 words) that best describes the main subject of the interaction. Respond ONLY with the topic, nothing else. Use the same language as the conversation.

Conversation:
{conversation}"
```

## Output

The script generates two output files:

1. A CSV file (specified by `output_file` in the config) containing the raw generated text and topics.
2. A JSONL file (same name as the CSV but with `.jsonl` extension) containing a structured version of the interactions, parsed into a more usable format.

## Error Handling

The script includes error handling for:
- API rate limit errors (waits and retries)
- Authentication errors
- Unexpected errors (waits and retries)
- File not found errors
- YAML parsing errors

## Advanced Features

- **Text File Input**: The script can now use a text file as input for generating interactions.
- **Text Chunking**: For large input files, the script can split the text into manageable chunks.
- **Topic Generation**: The script now generates a topic for each interaction based on the content.
- **Custom Parsing**: Implement custom parsing logic in `parse_conversation()` function to extract specific fields from generated text.
- **Batch Processing**: The script supports generating large datasets in batches to manage API usage and processing time.
- **Extensibility**: The modular design allows for easy addition of new features or integration with other data processing pipelines.

## Troubleshooting

- **API Key Issues**: Ensure your OpenAI API key is correctly set in the `.env` file or as an environment variable.
- **Rate Limiting**: If you encounter frequent rate limit errors, try increasing the `delay` value in your config file.
- **Model Availability**: Make sure the specified model in your config file is available in your OpenAI plan.
- **Script Execution**: If you're having trouble running the script, ensure you're in the correct directory and using the correct path to the Python interpreter in your virtual environment: `./venv/bin/python main-script.py config-file.yaml`
- **Virtual Environment**: If you see an error about missing modules, make sure you've activated the virtual environment with `source venv/bin/activate` before running the script.
- **Input File Issues**: If using a text file as input, ensure the file exists and the path is correct in the config file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Disclaimer

This project is for educational and research purposes only. Ensure you comply with OpenAI's use-case policy and terms of service when using their API. The generated data should not be used for any malicious purposes or to create misleading information.
