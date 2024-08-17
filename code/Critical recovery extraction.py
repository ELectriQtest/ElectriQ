import openai
import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from itertools import islice

openai.api_key = "sk-CoEQvrkLbHOz5uIWamsLYcVN7t513d8adnfBHRYohrdAz8Hp"
openai.api_base = "https://api.chatanywhere.com.cn/v1"

def process_row(row):
    tag = row[2]  # 假设标签在第3列（索引为2）
    content = row[5]  # 假设内容在第4列（索引为3）
    # 检查content中是否包含"非居民用户"
    prompt = (
        f'{content}'
        f'Please output the key reply to the customer service in the above dialogue, only output the original sentence, and include (customer service:) before each sentence output, do not output the serial number and quotation marks'
        )
    #print(prompt)
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    generated_content = completion.choices[0].message.content
    return generated_content

times = []
# 多线程并发处理前400行
with open('10000-20000条.csv', 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    headers = next(reader)  # 跳过表头
    data = [row for row in islice(reader, 1, 10000)]  # 读取第3001行到第10000行数据

    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(process_row, row): row for row in data}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing"):
            row = futures[future]
            try:
                generated_content = future.result()
                row.append(generated_content)  # 将生成的内容添加到行数据中
            except Exception as e:
                print(f"An error occurred: {e}")

# 添加表头
headers.append('提取关键性回复')

# 将更新后的数据写入到新的文件
with open('数据集10000-20000（英文）关键性回复提取.csv', 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(headers)  # 写入表头
    writer.writerows(data)  # 写入数据
