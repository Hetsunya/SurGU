from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset

model_name = "RussianNLP/FRED-T5-Summarizer"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

device='cpu'
model.to(device)

dataset = load_dataset("RussianNLP/russian_super_glue", "muserc")

for example in dataset['test']:
    # Формирование вопроса и контекста
    paragraph = example['paragraph']
    question = example['question']
    input_text = f"Вопрос: {question}. Ответь одним или двумя словами, используя текст: {paragraph}"

    # Токенизация текста
    inputs = tokenizer(input_text, return_tensors="pt")

    # Генерация ответа
    output = model.generate(
        **inputs,
        do_sample=True
    )
    answer = tokenizer.decode(output[0], skip_special_tokens=True)

    # Вывод результатов
    print(f"Вопрос: {question}. Ответь на вопрос, используя только необходимую информацию из текста: ")

    print("Ответ модели:", answer)

    print("Ожидаемый ответ:", example['answer'])
    print("-" * 50)
