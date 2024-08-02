#!/usr/bin/env python
import json
import re
import csv
import codecs
import sys

def parse_conversation(text, role1, role2):
    pattern = f'({role1}|{role2}): (.+?)(?=\n(?:{role1}|{role2}):|\Z)'
    matches = re.findall(pattern, text, re.DOTALL)
    return [{"role": "user" if role == role1 else "assistant", "content": message.strip()} for role, message in matches]

def convert_to_jsonl(input_file, output_file, role1, role2):
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
             codecs.open(output_file, 'w', encoding='utf-8') as outfile:
            reader = csv.DictReader(infile)
            for row in reader:
                topic = row['topic']
                generated_text = row['generated_text']
                conversation = parse_conversation(generated_text, role1, role2)
                
                # Add a system message at the beginning of each conversation
                conversation.insert(0, {"role": "system", "content": f"This is a conversation about {topic}. {role1} is the customer and {role2} is the support agent."})
                
                json_obj = {
                    "messages": conversation
                }
                json_str = json.dumps(json_obj, ensure_ascii=False)
                outfile.write(json_str + '\n')
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python convert_to_jsonl.py <input_file> <output_file> <role1> <role2>")
        sys.exit(1)
    
    input_file, output_file, role1, role2 = sys.argv[1:]
    convert_to_jsonl(input_file, output_file, role1, role2)
    print(f"Conversion complete. Output saved to {output_file}")
