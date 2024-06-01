import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


text = """In the early medieval era, Christianity, Islam, Judaism, and Zoroastrianism became e
stablished on India's southern and western coasts.[44] Muslim armies from Central Asia intermittently overran 
India's northern plains,[45] eventually founding
 the Delhi Sultanate, and drawing northern India
   into the cosmopolitan networks of medieval Islam.
   [46] In the 15th century, the Vijayanagara Empire
     created a long-lasting composite Hindu culture 
     in south India.[47] In the Punjab, Sikhism 
     emerged, rejecting institutionalised religion.
        [48] The Mughal Empire, in 1526, ushered in 
        two centuries of relative peace,[49] leaving 
        a legacy of luminous architecture.[m][50] 
        Gradually expanding rule of the British East India Company followed, turning India into a colonial economy, but also consolidating its sovereignty.[51] British Crown 
        rule began in 1858. The rights promised to Indians were granted slowly,[52][53]
          but technological ch
          ce and became the major factor in e
          nding British rule.[55][56] In 1947 the British Indian Empire """
def summarizer(Rawdocs):
    stopwards  = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(Rawdocs)
    # print(doc) 
    tokens = [token.text for token in doc]
    # print(tokens)
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwards and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    # print(word_freq)

    max_freq = max(word_freq.values())
    # print(max_freq)
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq
    # print(word_freq)
    sent_tokens = [sent for sent in doc.sents]
    # print(sent_tokens)
    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]
    # print(sent_scores)
    select_len = int(len(sent_tokens)*0.3)
    # print(select_len)
    summary = nlargest(select_len,sent_scores,key=sent_scores.get)
    # print(summary) 
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    # print(text)
    # print(summary)
    # print("the total length in text ",len(text.split(' ')))
    # print("the total length in summary ",len(summary.split(' ')))
    return summary,doc,len(Rawdocs.split(' ')),len(summary.split(' '))
