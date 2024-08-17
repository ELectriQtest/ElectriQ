# -*- coding: utf-8 -*-
import openai
import csv
from tqdm import tqdm

def process_row(row):
    #print(row)
    output_row = []
    if 'None' in row:
        return None
    #print(item)
    item = row.replace("<s>", "").replace("</s>", "").replace(" <|endoftext|>","").strip()
    split_text = item.split("Please reply in the voice of the customer service staff of the power supply company：")
    content = split_text[0].strip().replace("<s>","")
    #content = content.split("Additional knowledge:")[0]
    #print("上文",content)

    answer = split_text[1].strip().replace("</s>","")
    #print(answer)
    prompt_kdx = (
              f'You are a marketing and customer service QC for a power supply company.The following conversations between customer service and users of the power supply company include preliminary conversations and critical replies.Please rate the readability of key responses from a power marketing perspective on a scale of 1 to 5 from poor to good.'
              f'Readability rating criteria are as follows: '
              f'(1 point) many errors, grammar confusion, lack of logic, difficult to understand.'
              f'(2 marks) There are some grammatical errors or logic ambiguities that affect understanding.'
              f'(3 marks) Most of the content is correct and easy to understand, but there are some grammatical errors or logical ambiguities.'
              f' (4 points) All content is correct and easy to understand, with only a few grammatical errors or logical ambiguities.'
              f' (5 points) All content is correct and easy to understand, without any grammatical errors or logical ambiguities.'
f' Output corresponds to readability score, template:'
              f'Output corresponds to readability score, template:'
              f'Readability score: 2 '
              f' The previous dialogue is as follows: '
              f'{content}'
              f'The key responses are as follows:'
              f'{answer}')
    prompt_zyx = (
            f'You are a marketing and customer service QC for a power supply company.The following conversations between customer service and users of the power supply company include preliminary conversations and critical replies.Please rate key responses from a power marketing perspective on a scale of 1 to 5 from poor to good on a professional scale.'
            f' Professional rating criteria are as follows: '
            f' (1 score) uses terms and concepts that are inaccurate and lack understanding of the power industry.'
            f' (2 marks) Only some of the terms and concepts are accurate, demonstrating only a basic understanding of the power industry.'
            f' (3 marks) Most of the terms and concepts are accurate and show a good understanding of the power industry.'
            f' (4 points) All terms and concepts are accurate and can be correctly applied to answer questions, demonstrating an in-depth understanding of the power industry.'
            f' (5 points) In addition to being accurate in all terms and concepts, it is also able to proactively explain complex concepts, demonstrating a professional and in-depth understanding of the power industry.'
            f' Output corresponds to professional score, template: '
            f' Professional Rating: 2 points'
            f' The previous dialogue is as follows: '
            f'{content}'
            f'The key responses are as follows:'
            f'{answer}')
    prompt_tsx = (
            f' You are a marketing and customer service QC for a power supply company.The following conversations between customer service and users of the power supply company include preliminary conversations and critical replies.Please rate the accessibility of key responses from a power marketing perspective on a scale of 1 to 5 from poor to good.'
            f' Accessibility rating criteria are as follows: '
            f' (1 score) Although professional words are used, no explanation is provided or the explanation is not clear, and it is difficult for ordinary users to understand.'
            f' (2 points) uses specialized vocabulary and provides an explanation, but the explanation is too complex and still difficult for the average user to understand.'
            f' (3 points) uses specialized vocabulary and provides explanations that are mostly understandable to the average user.'
            f' (4 points) uses specialized vocabulary and provides explanations that are easy to understand and accessible to the average user.'
            f' (5 points) not only uses professional vocabulary and provides explanations, the content of the explanations is very easy to understand, but also enables ordinary users to understand professional concepts in a vivid way.'
            f' Output corresponding to the popularity score, template: '
            f' Accessibility score: 2 '
            f' The previous dialogue is as follows: '
            f'{content}'
            f'The key responses are as follows:'
            f'{answer}')
    prompt_yhyhx = (
            f' You are a marketing and customer service QC for a power supply company.The following conversations between customer service and users of the power supply company include preliminary conversations and critical replies.Please rate the user friendliness of key responses from a power marketing perspective on a scale of 1 to 5 from poor to good.'
            f' User-friendliness rating criteria are as follows: '
            f' (1 score) answers appear cold and mechanical, without any personalized care or concern.'
            f' (2 points) There was only a small amount of personalized care or concern in the responses.'
            f' (3 points) There is some personalized care or concern in the responses, but it is not common.'
            f' (4 points) answers are filled with personalized care and concern, making users feel comfortable and welcome.'
            f" (5 points) answers are not only full of personalized care and concern, but also proactively anticipate and meet the user's possible needs."
            f' Output corresponding to user-friendliness score, template: '
            f' User friendliness score: 2 '
            f' The previous dialogue is as follows: '
            f'{content}'
            f'The key responses are as follows:'
            f'{answer}')
    try:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                  messages=[{"role": "user", "content": prompt_kdx  }])
        generated_content = completion.choices[0].message.content
        output_row.append(generated_content)
        return output_row
    except Exception as e:
        print(f"Error processing row: {e}")
        return None

def main():
    openai.api_key = "sk-CoEQvrkLbHOz5uIWamsLYcVN7t513d8adnfBHRYohrdAz8Hp"
    openai.api_base = "https://api.chatanywhere.com.cn/v1"

    with open('llama3-8b/训练后/llama3-8b-训练后（1000）.csv', 'r', encoding='utf-8') as f, \
            open('llama3-8b/训练后/llama3-8b-训练后（1000）可读性.csv', 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(f)
        writer = csv.writer(outfile)
        # 初始化行计数器
        row_count = 0
        # 创建进度条
        num=100
        pbar = tqdm(total=num)
        # 外侧循环读取行
        for row in reader:
            # 如果已经读取100行，则退出循环
            if row_count == num:
                break
            # 初始化结果列表
            result_row = []
            # 内侧循环读取列
            i = 0
            for cell in row:
                try:
                    result = process_row(row[i])
                    i+=1
                    print(result)
                except:
                    print("错误")
                    continue
                # 将结果添加到结果列表
                result_row.append(result)
            # 将结果行写入新的CSV文件
            writer.writerow(result_row)
            # 行计数器增加
            row_count += 1
            # 更新进度条
            pbar.update(1)
        # 关闭进度条
        pbar.close()


if __name__ == "__main__":
    main()
