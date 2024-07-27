# setup
import google.generativeai as genai
import PIL.Image
import json
import os
import tqdm
import time
import sys

#填入自己的google_api_key
google_api_key = ''


questions_file = open("../data/coco_pope_random.json", "r")
out_file = "../output/pope_random_gemini_single.jsonl"
lines = list(questions_file.readlines())


for line in tqdm.tqdm(lines):
    
    data = json.loads(line)
    object = data["text"].replace("Is there a ", "").replace("Is there an ", "").replace(" in the image?", "")
    prompt = data["text"]
    question_id = data["question_id"]
    
    print("google_api_key: ", google_api_key)
    genai.configure(api_key=google_api_key, transport='rest')  # 填入自己的api_key
    model = genai.GenerativeModel(model_name="gemini-pro-vision")

    image_path = data["image"]
    image_path = "../data/val2014/" + image_path
    img = PIL.Image.open(image_path)

    try:
        response = model.generate_content([prompt, img])
        response.resolve()
        print(response.text)
        with open(out_file, "a") as f:
            f.write(json.dumps({
                "question": prompt,
                "answer": response.text,
                "question_id": question_id,
            }) + '\n')
    except:
        with open(out_file, "a") as f:
            f.write(json.dumps({
                "question": prompt,
                "answer": "error",
                "question_id": question_id,
            }) + '\n')
    time.sleep(2)