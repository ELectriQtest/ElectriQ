import pandas as pd
import re

def clean_text(text):
    # 正则表达式调整为保留中文字符、ASCII字母数字以及常见的标点符号
    cleaned_text = text
    return cleaned_text

def find_and_print_previous_content(text, sentences_to_find):
    if not isinstance(text, str):  # Check if text is not a string
        text = str(text)  # Convert it to a string
    sentences_to_find = str(sentences_to_find)  # 如果是，则转换为字符串
    sentences_to_find = sentences_to_find.replace('\n','').replace('(','').replace(')','').replace('nan','')
    output_data = []
    for sentence_to_find in sentences_to_find.split("customer service:"):
        found = False
        for line in text.split("\n"):
            if sentence_to_find in line:
                found = True
                index = text.index(line)
                if sentence_to_find == "":
                    continue
                if text[:index] == "":
                    continue
                content = text[:index] + "Key response:" + sentence_to_find
                print(content)
                content.replace('/n/n', '/n')
                # 清理文本
                content = clean_text(content)
                output_data.append(content)
                break
        if not found:
            print(f"The sentence '{sentence_to_find}' was not found in the text.")
    return output_data

# 读取csv文件
df = pd.read_csv('datasets/数据集1-20000（英文）关键性回复提取.csv')
#df = df[:3]
output_data = []

# 遍历每行数据
for index, row in df.iterrows():
    gpt_content = row['翻译']
    key_content = row['提取关键性回复']

    output_data.extend(find_and_print_previous_content(gpt_content, key_content))

# Convert list into DataFrame
df_output = pd.DataFrame(output_data, columns=['Content'])

# Save DataFrame to a CSV file
df_output.to_csv('datasets/数据集1-20000（英文）关键性回复提取预处理.csv', index=False, encoding='utf_8_sig')
