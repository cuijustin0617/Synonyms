
import math

import re
# import txt as txt




def cosine_similarity(vec1, vec2): #vec1 and 2 are dictionaries
    dot_prod = 0
    sum_squared_vec1 = 0
    sum_squared_vec2 = 0
    for word in vec1:
        if word  in vec2:
            dot_prod += (vec1[word]*vec2[word])
    for word in vec1:
        sum_squared_vec1 += vec1[word]**2
    for word in vec2:
        sum_squared_vec2 += vec2[word]**2
    res = dot_prod/(math.sqrt(sum_squared_vec1)*math.sqrt(sum_squared_vec2))
    return res
#print(cosine_similarity({"a":1,"b":2,"c":3,},{"b":4,"c":5,"d":6}))



def build_semantic_descriptors(sentences):
    returned_dict = {}
    for sentence in sentences:
        simplified = []
        for word in sentence:
            if word not in simplified:
                simplified.append(word)

        for word1 in simplified:
            for word2 in simplified:
                if word1 not in returned_dict.keys():
                    returned_dict[word1] = {}
                if word2 != word1:
                    if word2 in returned_dict[word1].keys():
                        returned_dict[word1][word2] += 1
                    else:
                        returned_dict[word1][word2] = 1

    return returned_dict


def build_semantic_descriptors_from_files(filenames):
    '''take in many files(a list of file names) and put them all as one list of lists(sentences), then perform the build_semantic_descriptors '''


    all_texts = []
    for file in filenames:
        '''make each file into a list of lists(sentences)'''
        text = open(file, "r", encoding="latin1").read().lower()

        #puncs
        text = text.replace(","," ")
        text = text.replace("-"," ")
        text = text.replace("--"," ")
        text = text.replace(":"," ")
        text = text.replace(";"," ")

        #weird ones
        text = text.replace("\n"," ")
        text = text.replace('"'," ")
        text = text.replace("'"," ")
        text = text.replace("\s"," ")


        #separations
        text = text.replace("!",".")
        text = text.replace("?",".")


        text = text.replace("\ufeff", " ") #idk
        text = text.split(".")
        for sentence in text:
            sentence = sentence.split() #a list of words in the sentence
            all_texts.append(sentence)
    return build_semantic_descriptors(all_texts)






def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    res = choices[0]
    vec1 = semantic_descriptors[word.lower()]
    value_counter = -1
    similarity = 0

    if word not in semantic_descriptors.keys():
        return res #the silimarity cant be computed with any choices cuz word doesnt exist in text

    for i in range(len(choices)):
        if choices[i].lower() not in semantic_descriptors.keys():
            similarity = -1
        else:
            vec2 = semantic_descriptors[choices[i].lower()]
            similarity = similarity_fn(vec1,vec2)


        if similarity > value_counter:
            value_counter = similarity
            res = choices[i]

    return res





def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    file = open(filename, "r", encoding="latin1").read()
    lines_of_file = file.split("\n")
    del lines_of_file[-1]
    wordlist_of_lines = []
    correct_answers = 0
    for i in range(len(lines_of_file)):
        wordlist_of_lines.append(lines_of_file[i].split())

    for line in wordlist_of_lines:

        word = line[0]
        rightanswer = line[1]
        choices = line[2:]


        if most_similar_word(word, choices, semantic_descriptors, similarity_fn) == rightanswer:
            correct_answers += 1

    total = len(lines_of_file)

    return float((correct_answers / total) * 100)





#sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
#print(sem_descriptors)
#res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
#print(res, "of the guesses were correct")