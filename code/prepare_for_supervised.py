
badSummaries = open('data/generated_summaries.txt', 'r').read().strip().split('\n')[:-1]
goodSummaries = open('data/summaries.txt', 'r').read().split('\n')[:len(badSummaries)]

print [len(goodSummaries), len(badSummaries)]

file = open('data/summaries.train', 'w')
for summary in goodSummaries[:int(0.9*len(goodSummaries))]:
    file.write('__label__0 ' + summary + '\n')
for summary in badSummaries[:int(0.9*len(badSummaries))]:
    file.write('__label__1 ' + summary + '\n')
file.close()

file = open('data/summaries.test', 'w')
for summary in goodSummaries[int(0.9*len(goodSummaries)):]:
    file.write('__label__0 ' + summary + '\n')
for summary in badSummaries[int(0.9*len(badSummaries)):]:
    file.write('__label__1 ' + summary + '\n')
file.close()
