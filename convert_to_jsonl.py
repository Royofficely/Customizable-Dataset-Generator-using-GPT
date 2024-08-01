#!/usr/bin/env python
import json
import re
import csv
import codecs

def parse_conversation(text, role1, role2):
    pattern = f'({role1}|{role2}): (.+?)(?=\n(?:{role1}|{role2}):|\Z)'
    matches = re.findall(pattern, text, re.DOTALL)
    return [{"role": role.lower(), "message": message.strip()} for role, message in matches]

def convert_to_jsonl(input_file, output_file, role1, role2):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         codecs.open(output_file, 'w', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        for id_counter, row in enumerate(reader, 1):
            topic = row['topic']
            generated_text = row['generated_text']
            conversation = parse_conversation(generated_text, role1, role2)
            json_obj = {
                "id": str(id_counter),
                "topic": topic,
                "conversation": conversation,
                "role1": role1,
                "role2": role2
            }
            json_str = json.dumps(json_obj, ensure_ascii=False)
            outfile.write(json_str + '\n')

if __name__ == "__main__":
    convert_to_jsonl('synthetic_dataset.csv', 'customer_support_dataset.jsonl', 'Customer', 'Agent')
    print("Conversion complete. Output saved to customer_support_dataset.jsonl")
