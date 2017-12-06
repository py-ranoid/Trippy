from textblob import Word, TextBlob
import pandas as pd
from nltk.corpus import stopwords
from word2vecmodel import sim

stopWords = set(stopwords.words('english')).union(
    set(['city', 'palace', 'Palace', 'Udaipur', 'If', 'if', 'udaipur']))

# import os
# os.chdir('TrippyMain/AI')

df = pd.read_pickle('../Warehouse/UdpRevFin.pkl')


def get_phrase_list(place='Bagore Ki Haveli'):
    texts = list(df[df['Venue_title'] == place]['Text'])
    full = '. '.join(texts)
    npr = TextBlob(full.lower()).noun_phrases
    c = {}
    for i in npr:
        c[i] = c.get(i, 0) + 1
    d = pd.Series(c)
    phrase_list = d.sort_values(ascending=False)[:100].index
    # print phrase_list
    return phrase_list, d[list(phrase_list)]


def lemmatize_and_drop(phrase_list, d):
    phrase_set = {}
    for p in phrase_list:
        pos_list = TextBlob(p).tags
        # print p
        end_phrase = []
        for i in pos_list:
            if i[0] in stopWords:
                continue
            else:
                w = Word(i[0])
                try:
                    end_phrase.append(w.lemmatize(i[1][0].lower()))
                except:
                    end_phrase.append(w.lemmatize())
        end_phrase = ' '.join(end_phrase)
        if end_phrase in phrase_set:
            phrase_set[end_phrase] += d[p]
        else:
            # print "---------------------"
            found = False
            # print p, phrase_set
            for p_exist in phrase_set:
                if end_phrase in p_exist:
                    phrase_set[p_exist] += d[p]
                    found = True
                    break
                elif p_exist in end_phrase:
                    val = phrase_set[p_exist]
                    # print p, d[p], val
                    phrase_set[end_phrase] = d[p] + val
                    del phrase_set[p_exist]
                    found = False
                    break
            if found == False:
                phrase_set[end_phrase] = d[p]
    return phrase_set


def similar(pos_list, pos_list2, method, word_index):
    if method == 'w2v':
        nn1 = pos_list[word_index][0]
        nn2 = pos_list2[word_index][0]
        try:
            score = sim(nn1, nn2)
        except KeyError:
            # print "not in vocab :", nn1, "or", nn2
            return 0
        if score > 0.5:
            return 1
        else:
            return 0
    elif method == 'synsets':
        nn1 = pos_list[word_index][0]
        nn1_pos = pos_list[word_index][1][0].lower()
        nn2 = pos_list2[word_index][0]
        nn2_pos = pos_list2[word_index][1][0].lower()

        a = nn1.get_synsets(pos=nn1_pos)[0]
        b = nn2.get_synsets(pos=nn2_pos)[0]
        score = a.path_similarity(b)
        if score is None:
            return -1
        elif score > 0.09:
            return 1
        else:
            return 0


def droppable_phrases_adj(phrase_set):
    ignore = set()
    # Iterating over all phrases
    for p in phrase_set:
        if p in ignore:
            continue
        # print "-----", p
        # Tagging POS of words in phrase P
        pos_list = TextBlob(p).tags
        w_list = []
        if len(pos_list) == 2:
            # If phrase is 2 words long and first word is not in ignore set
            for p2 in phrase_set:
                # Iterating over all phrases in phrases set to compare with P
                if p2 in ignore:
                    # Ignore p if already encountered
                    continue
                # print "->", p2
                # Tagging POS of words in phrase P2
                pos_list2 = TextBlob(p2).tags
                if len(pos_list2) == 2:
                    # If P2 is 2 words long
                    if pos_list2[0][0] == pos_list[0][0] and pos_list2[0][1] == pos_list[0][1] and not p == p2:
                        # If 1st word of P and P2 are same along with their POS
                        # print pos_list[1][0], ' ||', pos_list2[1][0]
                        try:
                            # A and B are 1st synsets of the 2nd Word of P and P2
                            # print '=========', a, b, a.path_similarity(b)
                            if similar(pos_list, pos_list2, method='w2v', word_index=1):
                                # If path similarity of 2nd words is greater than 0.09,
                                # add counts of P2 to P and add P2 to ignore list
                                phrase_set[p] += phrase_set[p2]
                                ignore.add(p2)
                        except IndexError:
                            pass
    return ignore, phrase_set


def droppable_phrases_noun(phrase_set):
    ignore = set()
    # Iterating over all phrases
    for p in phrase_set:
        if p in ignore:
            continue
        # print "-----", p
        # Tagging POS of words in phrase P
        pos_list = TextBlob(p).tags
        w_list = []
        if len(pos_list) == 2:
            # If phrase is 2 words long and first word is not in ignore set
            for p2 in phrase_set:
                # Iterating over all phrases in phrases set to compare with P
                if p2 in ignore:
                    # Ignore p if already encountered
                    continue
                # print "->", p2
                # Tagging POS of words in phrase P2
                pos_list2 = TextBlob(p2).tags
                if len(pos_list2) == 2:
                    # If P2 is 2 words long
                    if pos_list2[1][0] == pos_list[1][0] and pos_list2[1][1] == pos_list[1][1] and not p == p2:
                        # If 1st word of P and P2 are same along with their POS
                        # print pos_list[0][0], ' ||', pos_list2[0][0]
                        try:
                            # A and B are 1st synsets of the 2nd Word of P and P2
                            # print '=========', a, b, a.path_similarity(b)
                            if similar(pos_list, pos_list2, method='w2v', word_index=0):
                                # If path similarity of 2nd words is greater than 0.09,
                                # add counts of P2 to P and add P2 to ignore list
                                phrase_set[p] += phrase_set[p2]
                                ignore.add(p2)
                        except (IndexError) as e:
                            # print adj1, adj2, adj1_pos, adj2_pos
                            # print p, '|||', p2, e
                            pass
    return ignore, phrase_set


def highlighter(place='Garden of the Maidens (Sahelion Ki Bari)'):
    plist, count_dict = get_phrase_list(place)
    d1 = pd.Series(count_dict)
    d1.sort_values(ascending=False)[:100].index
    reduced_list = lemmatize_and_drop(plist, count_dict)
    len(reduced_list)

    wordnet_eliminations_adj, new_counts_adj = droppable_phrases_adj(
        reduced_list)
    reduced_list_adj = {}
    for i in reduced_list:
        if i not in wordnet_eliminations_adj:
            reduced_list_adj[i] = new_counts_adj[i]
    len(reduced_list_adj)

    wordnet_eliminations_noun, new_counts_noun = droppable_phrases_noun(
        reduced_list_adj)
    reduced_list_noun = {}
    for i in reduced_list_adj:
        if i not in wordnet_eliminations_noun:
            reduced_list_noun[i] = new_counts_noun[i]

    len(reduced_list_noun)
    final_series = pd.Series(reduced_list_noun)
    final_series.sort_values(ascending=False)
    final_list = list(final_series.sort_values(ascending=False)[:20].index)
    packets = []
    for i in range(len(final_list)):
        packets.append(final_list[i].title() + "::" +
                       str(reduced_list_noun[final_list[i]]))
    return "##".join(packets)


if __name__ == "__main__":
    highlights_dict = {}
    for i in list(df['Venue_title'].unique()):
        print i
        val = highlighter(i)
        print val
        highlights_dict[i] = val
    pd.Series(highlights_dict).to_pickle('highlights.pkl')
