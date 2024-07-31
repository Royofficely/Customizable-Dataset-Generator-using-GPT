#!/usr/bin/env python
import random
import pandas as pd
import time
from tqdm import tqdm
import yaml
import os
import sys
import argparse
from openai import OpenAI
from convert_to_jsonl import convert_to_jsonl

def load_config(config_file):
    try:
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: {config_file} not found. Please ensure it exists in the project root.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing {config_file}: {e}")
        sys.exit(1)

def generate_text_from_llm(prompt, model, client):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        if "Rate limit" in str(e):
            print("Rate limit exceeded. Waiting for 60 seconds before retrying...")
            time.sleep(60)
            return generate_text_from_llm(prompt, model, client)
        elif "Authentication" in str(e):
            print("Authentication error. Please check your API key.")
            sys.exit(1)
        else:
            print(f"An unexpected error occurred: {e}")
            time.sleep(20)  # Wait for 20 seconds before retrying
            return generate_text_from_llm(prompt, model, client)

def load_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please ensure the file exists.")
        sys.exit(1)

def generate_text_from_file(prompt, text_content, client, model):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"You are a helpful assistant. Use the following information to answer questions: {text_content}"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred while generating text from file: {e}")
        time.sleep(20)
        return generate_text_from_file(prompt, text_content, client, model)

def main(config_file):
    config = load_config(config_file)
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: API key not found. Please set the OPENAI_API_KEY environment variable.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    
    if config['use_text_file']:
        text_content = load_text_file(config['text_file_path'])
    
    data = []
    for _ in tqdm(range(config['num_interactions'])):
        if config['use_text_file']:
            prompt = config['prompt_text_file'].format(
                role1=config['role1'],
                role2=config['role2'],
                context=text_content
            )
            generated_text = generate_text_from_file(prompt, text_content, client, config['model'])
        else:
            topic = random.choice(config['topics'])
            prompt = config['prompt_llm'].format(
                subject=config['subject'],
                topic=topic,
                role1=config['role1'],
                role2=config['role2']
            )
            generated_text = generate_text_from_llm(prompt, config['model'], client)
        
        data.append({
            "topic": topic if not config['use_text_file'] else "N/A",
            "generated_text": generated_text,
            "role1": config['role1'],
            "role2": config['role2']
        })
        time.sleep(config['delay'])  # To avoid hitting API rate limits

    df = pd.DataFrame(data)
    try:
        df.to_csv(config['output_file'], index=False)
        print(f"Dataset saved to {config['output_file']}")
        # Convert to JSONL
        jsonl_output = config['output_file'].replace('.csv', '.jsonl')
        convert_to_jsonl(config['output_file'], jsonl_output, config['role1'], config['role2'])
        print(f"Dataset converted to JSONL format. Saved to {jsonl_output}")
    except PermissionError:
        print(f"Error: Permission denied when trying to write to {config['output_file']}. Please check your file permissions.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a dataset using GPT")
    parser.add_argument("config", help="Path to the configuration file")
    args = parser.parse_args()
    main(args.config)
