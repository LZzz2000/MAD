import json

# ans_file = './pope_random_multi-gemini-0517-best.jsonl'
# ans_file = './pope_random_gemini-single-worst.jsonl'
# ans_file = './pope_random_gemini-0705_singleWhy_1&2.jsonl'
# ans_file = './pope_random_gemini-0705_singleWhy.jsonl'
# ans_file = './pope_random_gemini-0706_single_self-reflection_Re.jsonl'
# ans_file = './pope_random_openai-0612_2.jsonl' # gpt-4o
# ans_file = './pope_random_multi-openai-0613.jsonl'
# ans_file = './pope_random_gemini_sro.jsonl'
# ans_file = './pope_random_multi-gemini-0717_message-propagation_1.jsonl'
# ans_file = './pope_random_multi-gemini-0717_role-play_2.jsonl'
# ans_file = './pope_random_multi-gemini-0517_3.jsonl'
# ans_file = './pope_random_gemini-1.5_single-0724_3.jsonl'
ans_file = './pope_random_multi_gpt4o_0725_messageAndrole_Re_4.jsonl'
# ans_file = './pope_random_multi_gpt4o_0725_role_Re_4.jsonl'



# ans_file = './pope_popular_gemini-0505_2.jsonl'
# ans_file = './pope_popular_multi-gemini-0706_1_Re_7.jsonl'
# ans_file = './pope_popular_gemini-0706_single_self-reflection_Re_4.jsonl'
# ans_file = './pope_popular_gemini_sro.jsonl'

# ans_file = './pope_adversarial_gemini-0505_3.jsonl'
# ans_file = './pope_adversarial_multi-gemini-0706_1_Re_3.jsonl'
# ans_file = './pope_adversarial_gemini-0706_single_self-reflection_Re_14.jsonl'
# ans_file = './file/pope_random_gemini_multi.jsonl'
# ans_file = './pope_adversarial_gemini_sro.jsonl'

label_file = './coco_pope_random_newgt_0720.json'
# label_file = './coco_pope_random.json'
# label_file = './coco_pope_popular.json'
# label_file = './coco_pope_adversarial.json'

yuan_label_file = './coco_pope_random.json'
# yuan_label_file = './coco_pope_adversarial.json'
# yuan_label_file = './coco_pope_popular.json'

output_file = './badcase_list/pope_random-0720_gpt-4o-badcaselist-multi_0725_messageAndrole_Re_4.json'
out = True
quanji = False

answers = [json.loads(q) for q in open(ans_file, 'r')]
label_list = [json.loads(q)['label'] for q in open(label_file, 'r')]
yuan_label_list = [json.loads(q)['label'] for q in open(yuan_label_file, 'r')]
img_list = [json.loads(q)['image'] for q in open(label_file, 'r')]

badcase_list = []

for answer in answers:
    text = answer['answer']

    # Only keep the first sentence
    if ans_file.find('sro') == -1:
        if text.find('.') != -1:
            text = text.split('.')[0]

        text = text.replace(',', '')
        words = text.split(' ')
        if 'No' in words or 'not' in words or 'no' in words:
            answer['answer'] = 'no'
        else:
            answer['answer'] = 'yes'
    else:
        # kk = text.split('\n')
        # if 'No' in kk[0] or 'not' in kk[0] or 'no' in kk[0]:
        #     answer['answer'] = 'no'
        # elif text.find("Question4:")!= -1 and text.find("Question4: Y") == -1:
        #     answer['answer'] = 'no'
        # elif text.find("4. ") != -1 and text.find("4. Y") == -1:
        #     answer['answer'] = 'no'
        # else:
        #     answer['answer'] = 'yes'
        kk = text.split('\n')
        length = len(kk) - 1

        if 'No' in kk[0] or 'not' in kk[0] or 'no' in kk[0]:
            answer['answer'] = 'no'
        elif 'Yes' in kk[length] or 'yes' in kk[length] and length != 0:
            answer['answer'] = 'yes'
        elif 'also' in kk[length] or 'not sure' in kk[length] or 'might be' in kk[length] or 'no' in kk[
            length] or 'No' in kk[length] or 'but' in kk[length] and length != 0:
            answer['answer'] = 'no'
        else:
            answer['answer'] = 'yes'



for i in range(len(label_list)):
    if label_list[i] == 'no':
        label_list[i] = 0
    elif label_list[i] == 'yes':
        label_list[i] = 1
    elif label_list[i] == 'uncertain':
        label_list[i] = -1

for i in range(len(yuan_label_list)):
    if yuan_label_list[i] == 'no':
        yuan_label_list[i] = 0
    elif yuan_label_list[i] == 'yes':
        yuan_label_list[i] = 1


pred_list = []
for answer in answers:
    if answer['answer'] == 'no':
        pred_list.append(0)
    else:
        pred_list.append(1)

pos = 1
neg = 0
yes_ratio = pred_list.count(1) / len(pred_list)

TP, TN, FP, FN = 0, 0, 0, 0
question_id = 1
for pred, label in zip(pred_list, label_list):
    kk = {}
    if pred == pos and label == pos:
        TP += 1
    elif pred == pos and label == neg:
        FP += 1
        if out:
            kk['image_id'] = question_id
            kk['image'] = img_list[question_id-1]
            kk['question'] = answers[question_id-1]['question']
            kk['pred'] = answers[question_id-1]['answer']
            kk['label'] = label_list[question_id-1]
            # kk['discussion_process'] = answers[question_id-1]['discussion_process']
            badcase_list.append(kk)
        # badcase_list.append(question_id)
    elif pred == neg and label == neg:
        TN += 1
    elif pred == neg and label == pos:
        FN += 1
        if out:
            kk['image_id'] = question_id
            kk['image'] = img_list[question_id-1]
            kk['question'] = answers[question_id-1]['question']
            kk['pred'] = answers[question_id-1]['answer']
            kk['label'] = label_list[question_id-1]
            # kk['discussion_process'] = answers[question_id-1]['discussion_process']
            badcase_list.append(kk)
        # badcase_list.append(question_id)
    else:
        if quanji == True and label == -1:
            label = yuan_label_list[question_id-1]
            if pred == pos and label == pos:
                TP += 1
            elif pred == pos and label == neg:
                FP += 1
                if out:
                    kk['image_id'] = question_id
                    kk['image'] = img_list[question_id - 1]
                    kk['question'] = answers[question_id - 1]['question']
                    kk['pred'] = answers[question_id - 1]['answer']
                    kk['label'] = label_list[question_id - 1]
                    # kk['discussion_process'] = answers[question_id - 1]['discussion_process']
                    badcase_list.append(kk)
                # badcase_list.append(question_id)
            elif pred == neg and label == neg:
                TN += 1
            elif pred == neg and label == pos:
                FN += 1
                if out:
                    kk['image_id'] = question_id
                    kk['image'] = img_list[question_id - 1]
                    kk['question'] = answers[question_id - 1]['question']
                    kk['pred'] = answers[question_id - 1]['answer']
                    kk['label'] = label_list[question_id - 1]
                    # kk['discussion_process'] = answers[question_id - 1]['discussion_process']
                    badcase_list.append(kk)
                # badcase_list.append(question_id)


    question_id += 1

if out == True:
    print(badcase_list)
    print(len(badcase_list))
    json.dump(badcase_list, open(output_file, 'w'))


print('TP\tFP\tTN\tFN\t')
print('{}\t{}\t{}\t{}'.format(TP, FP, TN, FN))

#TP：T，对了，P：预测为Positive，label也是Positive
#TN：T，对了，N：预测为Negative，label也是Negative
#FP：F，错了，P：预测为Positive，label是Negative
#FN：F，错了，N：预测为Negative，label是Positive

acc = (TP + TN) / (TP + TN + FP + FN) # 整体对了多少
precision = float(TP) / float(TP + FP) # 预测为Positive的对了多少
recall = float(TP) / float(TP + FN) #label是Positive的对了多少
f1 = 2*precision*recall / (precision + recall) # F1分数结合了precision和recall的结果。因为precision和recall是此消彼长的关系，用F1分数来反应结果好坏比较合理

print('Accuracy: {}'.format(acc))
print('Precision: {}'.format(precision))
print('Recall: {}'.format(recall))
print('F1 score: {}'.format(f1))
print('Yes ratio: {}'.format(yes_ratio))
