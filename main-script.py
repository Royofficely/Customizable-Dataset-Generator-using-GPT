#!/usr/bin/env python
import random
import pandas as pd
import time
import asyncio
from tqdm import tqdm
import yaml
import os
import sys
import argparse
from openai import AsyncOpenAI
from convert_to_jsonl import convert_to_jsonl
import tiktoken
import hashlib

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

async def generate_text_from_llm(prompt, model, client):
    try:
        response = await client.chat.completions.create(
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
            await asyncio.sleep(60)
            return await generate_text_from_llm(prompt, model, client)
        elif "Authentication" in str(e):
            print("Authentication error. Please check your API key.")
            sys.exit(1)
        else:
            print(f"An unexpected error occurred: {e}")
            await asyncio.sleep(20)  # Wait for 20 seconds before retrying
            return await generate_text_from_llm(prompt, model, client)

def load_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please ensure the file exists.")
        sys.exit(1)

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def split_text_into_chunks(text, max_tokens=4000, overlap=200):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]
        chunk = encoding.decode(chunk_tokens)
        chunks.append(chunk)
        start = end - overlap
    return chunks

async def summarize_text(text, client, model):
    summarize_prompt = f"Please summarize the following text in a concise manner, focusing on the most important information:\n\n{text}\n\nSummary:"
    return await generate_text_from_llm(summarize_prompt, model, client)

async def generate_text_from_file(prompt, text_content, client, model, role1, role2, use_chunking=True):
    if not use_chunking:
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Use the provided information to answer questions."},
                    {"role": "user", "content": prompt.format(role1=role1, role2=role2, context=text_content)}
                ],
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"An error occurred while generating text from file: {e}")
            await asyncio.sleep(20)
            return await generate_text_from_file(prompt, text_content, client, model, role1, role2, use_chunking)

    chunks = split_text_into_chunks(text_content)
    summaries = await asyncio.gather(*[summarize_text(chunk, client, model) for chunk in chunks])
    combined_summary = " ".join(summaries)

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Use the provided information to answer questions."},
                {"role": "user", "content": prompt.format(role1=role1, role2=role2, context=combined_summary)}
            ],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred while generating text from file: {e}")
        await asyncio.sleep(20)
        return await generate_text_from_file(prompt, text_content, client, model, role1, role2, use_chunking)

async def generate_topic(conversation, model, client):
    topic_prompt = f"Based on the following conversation, generate a short, concise topic (1-5 words) that best describes the main subject of the interaction. Respond ONLY with the topic, nothing else. Use the same language as the conversation:\n\n{conversation}"
    return await generate_text_from_llm(topic_prompt, model, client)

async def main(config_file):
    config = load_config(config_file)
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: API key not found. Please set the OPENAI_API_KEY environment variable.")
        sys.exit(1)

    client = AsyncOpenAI(api_key=api_key)
    
    if config['use_text_file']:
        print("Loading text file...")
        text_content = load_text_file(config['text_file_path'])
        print(f"Text file loaded. Size: {len(text_content)} characters")
    
    data = []
    async def process_interaction(i):
        if config['use_text_file']:
            prompt = config['prompt_text_file']
            print(f"Generating text for interaction {i+1}...")
            generated_text = await generate_text_from_file(prompt, text_content, client, config['model'], config['role1'], config['role2'], config['use_chunking'])
        else:
            topic = random.choice(config['topics'])
            prompt = config['prompt_llm'].format(
                subject=config['subject'],
                topic=topic,
                role1=config['role1'],
                role2=config['role2']
            )
            generated_text = await generate_text_from_llm(prompt, config['model'], client)
        
        # Generate topic for the conversation
        topic = await generate_topic(generated_text, config['model'], client)
        
        return generated_text, topic

    tasks = [process_interaction(i) for i in range(config['num_interactions'])]
    results = await asyncio.gather(*tasks)

    for generated_text, topic in results:
        data.append({
            "topic": topic,
            "generated_text": generated_text,
            "role1": config['role1'],
            "role2": config['role2']
        })

    df = pd.DataFrame(data)
    try:
        df.to_csv(config['output_file'], index=False, encoding='utf-8')
        print(f"Dataset saved to {config['output_file']}")
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
    asyncio.run(main(args.config))
