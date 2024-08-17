import torch
import sys, getopt
from transformers import BloomTokenizerFast, AutoModelForCausalLM, TextStreamer
import pandas as pd
import csv
import os
import pandas as pd
import re
from collections import Counter
# 设置环境变量，建议在脚本运行之前通过命令行设置
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"

# 读取csv文件
df = pd.read_csv('数据集10000（英文）关键性回复提取.csv')
xlsx_file_path = 'power_marketing_database.xlsx'
def extract_max_context(provided_text, xlsx_file_path):
    def remove_stopwords(text):
        stop_words = set([
            "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
            "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers",
            "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
            "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are",
            "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does",
            "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
            "while", "of", "at", "by", "for", "with", "about", "against", "between", "into",
            "through", "during", "before", "after", "above", "below", "to", "from", "up", "down",
            "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here",
            "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more",
            "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
            "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"
        ])
        words = re.findall(r'\b\w+\b', text.lower())
        filtered_words = set(word for word in words if word not in stop_words)
        return filtered_words

    # 提供的文本
    provided_text_words = remove_stopwords(provided_text)

    # 读取xlsx文件
    df = pd.read_excel(xlsx_file_path)

    max_row = None
    max_count = 0

    for index, row in df.iterrows():
        # 获取当前行的文本内容
        context = row["context"]

        # 去除停用词
        context_words = remove_stopwords(context)

        # 计算提供的文本中的词在当前行中出现的不同单词的数量
        count = sum(1 for word in provided_text_words if word in context_words)

        # 更新最大出现次数及对应的行
        if count > max_count:
            max_count = count
            max_row = row

    # 返回结果
    if max_row is not None:
        return max_row["context"]
    else:
        return "No matching row found."
# 只读取前1000行
df = df.head(1000)
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# 设定模型路径
model_path = ("/media/wjz/新加卷/Firefly-master/script/checkpoint/firefly-bloom-7b1-sft-qlora/数据集20000(EN)-epoch20")
tokenizer = BloomTokenizerFast.from_pretrained(model_path, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto")
streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

def clear_screen():
    # 统一使用'clear'命令
    os.system('clear')

def find_and_print_previous_content(text, sentences_to_find):
    sentences_to_find = str(sentences_to_find).replace('?', '.').replace('\n','').replace('(','').replace(')','').replace('nan','')
    csv_row = []
    found = False
    for sentence_to_find in sentences_to_find.split("customer service:"):
        for line in text.split("\n"):
            if sentence_to_find in line:
                found = True
                index = text.index(line)
                prompt_text = text[:index]
                if prompt_text == '':
                    break

                prompt_text = prompt_text
                prompt = (f"{prompt_text}Please reply in the voice of the customer service staff of the power supply company：")
                input_ids = tokenizer(prompt, return_tensors='pt').input_ids.to(device)
                generate_ids = model.generate(input_ids, max_new_tokens=1024, streamer=streamer)
                generate_text = tokenizer.decode(generate_ids[0])
                generate_text_QA = \
                    generate_text.split(
                        "Please reply in the voice of the customer service staff of the power supply company：")
                generate_text_Q = generate_text_QA[0].split("Customer: ")[-1]
                generate_text_A = generate_text_QA[1].replace('<|endoftext|>', '')
                #print(generate_text_Q)
                #print(generate_text_A)
                Knowledge_enhancement = generate_text_Q + generate_text_A
                Additional_knowledge = extract_max_context(Knowledge_enhancement, xlsx_file_path)
                #print(Additional_knowledge)
                last_prompt = generate_text_QA[0] + "Additional knowledge:" + Additional_knowledge
                last_prompt = (f"{last_prompt}Please reply in the voice of the customer service staff of the power supply company：")
                input_ids = tokenizer(last_prompt, return_tensors='pt').input_ids.to(device)
                generate_ids = model.generate(input_ids, max_new_tokens=1024, streamer=streamer)
                last_generate_text = tokenizer.decode(generate_ids[0])
                print(last_generate_text)
                clear_screen()
                csv_row.append(last_generate_text)
                del input_ids, generate_ids, generate_text,last_generate_text
                break
        if not found:
            print(f"The sentence '{sentence_to_find}' was not found in the text.")
    return csv_row

# 遍历每行数据
csv_data = []
for index, row in df.iterrows():
    print(f"Processing row {index+1}")
    gpt_content = row['翻译']
    key_content = row['提取关键性回复']
    try:
        csv_row = find_and_print_previous_content(gpt_content, key_content)
        csv_data.append(csv_row)
    except Exception as e:
        print(f"An error occurred: {e}")

    # 清除 CUDA 缓存，建议在处理完一个batch后调用
    if device == 'cuda':
        torch.cuda.empty_cache()

    # 每处理100行保存一次
    if (index + 1) % 100 == 0:
        with open('bloom-7b-训练后-知识增强（2w-20epoch）（1000）.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(csv_data)
            csv_data = []  # 清空列表以便重新开始

# 保存最后一批数据到CSV文件中
with open('bloom-7b-训练后-知识增强（2w-20epoch）（1000）.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)
