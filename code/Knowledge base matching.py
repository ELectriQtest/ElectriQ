import pandas as pd
import re
from collections import Counter

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

# 测试函数
provided_text = """
Customer: do not use a lot of electrical appliances recently, usually turn off the lights and air conditioners on time, and there is no peak electricity consumption period.
I will make further inquiries for you. Please wait a moment. 
"""
xlsx_file_path = 'power_marketing_database.xlsx'
max_context = extract_max_context(provided_text, xlsx_file_path)
print("Max Context:", max_context)
