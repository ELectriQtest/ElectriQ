from transformers import BartTokenizer, BartForConditionalGeneration

# Load tokenizer and model
keywords_tokenizer = BartTokenizer.from_pretrained("/media/wjz/新加卷/LLM/bert/tech-keywords-extractor")
keywords_model = BartForConditionalGeneration.from_pretrained("/media/wjz/新加卷/LLM/bert/tech-keywords-extractor")

# Prepare inputs
inputs = keywords_tokenizer("OK, that may be that your electricity consumption is mostly in peak hours, and the electricity price is relatively high. Are you aware that your electricity consumption habits may have an impact on electricity bills?", return_tensors="pt")

# Generate text
predicted_ids = keywords_model.generate(**inputs)
predicted_text = keywords_tokenizer.decode(predicted_ids[0], skip_special_tokens=True)
print(predicted_text)
