from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model_name = "RussianNLP/FRED-T5-Summarizer"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

input_text = "Каковы основные преимущества использования трансформеров в машинном обучении?"

inputs = tokenizer(input_text, return_tensors="pt")

output = model.generate(**inputs, max_length=50, num_beams=5, early_stopping=True)
answer = tokenizer.decode(output[0], skip_special_tokens=True)

print("Вопрос:", input_text)
print("Ответ модели:", answer)

