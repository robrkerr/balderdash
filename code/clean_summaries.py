import re
import nltk.data

# TODO: replace all types of " with "
# TODO: replace multiple space with single

sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def parseSentences(text):
    decoded_text = text.strip().decode('utf-8')
    sentences = sentence_detector.tokenize(decoded_text)
    return map(lambda x: x.encode('utf8'), sentences)

def cleanText(text):
    return re.sub("{\{.*?\}}", "", re.sub("<.*?>", "", re.sub("<.*?\}}", "", re.sub("<.*?]", "", re.sub("<.*?}", "", re.sub("\(\[\[", "", re.sub("<!--", "", text)))))))

def parseSummaryLine(line, n=2):
    splitLine = line.split('\t')
    full = cleanText('\t'.join(splitLine[1:]))
    uncleanable = re.search('[\<\>\[\]\{\}]', full) is not None
    sentences = parseSentences(full)
    shortened = ' '.join(sentences[0:n])
    return dict(id=splitLine[0], full=full, uncleanable=uncleanable, sentences=sentences, shortened=shortened)

summaryLines = open('data/original_summaries.txt', 'r').read().split('\n')
summaries = map(parseSummaryLine, summaryLines)

file = open('data/summaries.txt', 'w')
ignored = 0
for summary in summaries:
    if not summary['uncleanable']:
        file.write(summary['shortened'] + '\n')
    else:
        ignored += 1
print ignored
file.close()
