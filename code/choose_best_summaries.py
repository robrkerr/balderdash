
summaries = open('data/generated_summaries.txt', 'r').read().strip().split('\n')[:-1]
predictions = open('data/generated_summary_predictions.txt', 'r').read().strip().split('\n')[:-1]

def combineWithPrediction(x):
    prediction = x[1].split(' ')
    label = prediction[0].split('__label__')[1]
    confidence = float(prediction[1])
    rating = confidence if (label == '0') else (1 - confidence)
    summary = ' '.join(x[0].split(' ')[1:])
    return dict(summary=summary, rating=rating)

summariesWithPredictions = map(combineWithPrediction, zip(summaries, predictions))

best = sorted(summariesWithPredictions, key=lambda x: -x['rating'])[0:5]
for item in best:
    print item['summary']
