import math

def norm(vec):


    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    dot_product = 0
    for key in vec1:
        dot_product += vec1[key]*vec2.get(key, 0)
    magvec1 = 0
    magvec2 = 0
    for i in vec1.values():
        magvec1 = magvec1+i**2
    for j in vec2.values():
        magvec2 = magvec2+j**2
    return dot_product/(math.sqrt(magvec2) * math.sqrt(magvec1))


def build_semantic_descriptors(sentences):


    dict_keys = {}
    for sent in sentences:
        set_a = set([x.lower() for x in sent])
        for elem in set_a:
            temp = set_a.copy()
            temp.remove(elem)
            for key in temp:
                if elem not in dict_keys:
                    dict_keys[elem] = {}
                    dict_keys[elem][key] = 0
                if key in dict_keys[elem]:
                    dict_keys[elem][key] +=1
                else:
                    dict_keys[elem][key] = 1

    return dict_keys



def build_semantic_descriptors_from_files(filenames):
    g_list = []
    sub_list = []
    for i in range(len(filenames)):
        file = open(filenames[i], "r", encoding ="latin1")
        text = file.read()
        file.close()
        text = text.replace(".", "   ")
        text = text.replace("?", "   ")
        text = text.replace("!", "   ")
        text = text.replace(";", "")
        text = text.replace(",", "")
        text = text.replace("-", "")
        text = text.replace("--", "")
        text = text.replace(":", "")
        g_list = text.split("   ")

    w = 0
    sub_list = []
    sub_sub_list = []
    g2_list = []
    num = len(g_list)

    while w <= num-1:
        sub_sub_list.append(g_list[w])
        sub_list.append(g_list[w])
        g2_list.append(sub_list)
        sub_list = []
        w += 1

    g3_list = []

    for i in range(len(g2_list)):
        for j in range(len(g2_list[i])):
            word = g2_list[i][j]
            n_word = word.split()
            g3_list.append(n_word)

    g3_list = [x for x in g3_list if x]
    return build_semantic_descriptors(g3_list)



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    word_and_seman_descript = []
    similarity_index = []
    values = []
    for i in choices:
        if i not in semantic_descriptors:
            word_and_seman_descript.append([i,-1])
        else:
            k = semantic_descriptors[i]
            word_and_seman_descript.append([i,k])
    if word not in semantic_descriptors:
        word_vector = [word, -1]
    else:
        word_vector = semantic_descriptors[word]
    for j in range(len(word_and_seman_descript)):
        if word_and_seman_descript[j][1] == -1 or word_vector == [word, -1]:
            similarity_index.append([choices[j],-1])
        else:
            similarity_index.append([choices[j],similarity_fn(word_vector,word_and_seman_descript[j][1])])
    print(similarity_index)
    for i in range(len(similarity_index)):
        values.append(similarity_index[i][1])
    values = values.index(max(values))
    return similarity_index[values][0]


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    file = open(filename, "r", encoding ="latin1")
    text = file.read()
    file.close
    lines = text.split("\n")

    dict = []
    correct = 0

    for w in range(len(lines)):
        p = lines[w]
        p = p.split()
        dict.append(p)

    for x in range(len(dict)-1):
        choices = []
        word = dict[x][0]
        answer = dict[x][1]
        choices = dict[x][2:]
        response = most_similar_word(word, choices, semantic_descriptors, similarity_fn)
        if response == answer:
            correct += 1
    percent = (correct/len(dict))*100
    return(percent)










































