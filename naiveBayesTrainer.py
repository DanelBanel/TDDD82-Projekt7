# -*- coding: cp1252 -*-
import os
from time import time
from pandas import DataFrame
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix, f1_score

# Some constants
NEWLINE = '\n'
REAL = 'real'
FAKE = 'fake'
EVALUATION = [
    ('./data/news/LinksUnknownFake/', FAKE),
    ('./data/news/LinksUnknownReal/', REAL)
]
SOURCES = [
    ('./data/news/training_fake/', FAKE),
    #('./data/news/LinksFakeExtra/', FAKE),
    ('./data/news/training_real/', REAL)
    #('./data/news/LinkBBC/', REAL)
]
param_grid  = {
    'vectorizer__max_df': (0.5, 0.75, 1.0),
    'vectorizer__max_features': (None, 200, 800, 1600),
    'vectorizer__ngram_range': ((1, 1), (1, 2), (1, 3), (1, 4), (1, 5)),  # unigrams to 5-grams
    'vectorizer__stop_words': ('english', None),
    'vectorizer__lowercase': (True, False),
    'tfidf_transformer__use_idf': (True, False),
    'tfidf_transformer__norm': ('l1', 'l2'),
    'classifier__alpha': (1.0, 0.75, 0.5, 0.25, 0.1),
    'classifier__fit_prior': (True, False),
}

def read_files(path):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path) and os.path.getsize(file_path) > 200L: # Only files larger than 200 Bytes
            lines = []
            f = open(file_path)
            for line in f:
                lines.append(line)
            f.close()
            content = NEWLINE.join(lines)
            yield file_path, content

def build_data_frame(path, classification):
    rows = []
    index = []
    for file_name, text in read_files(path):
        rows.append({'text': text, 'class': classification})
        index.append(file_name)
    data_frame = DataFrame(rows, index=index)
    return data_frame

pipeline = Pipeline([
    ('vectorizer',  CountVectorizer()),
    ('tfidf_transformer',  TfidfTransformer()),
    ('classifier',  MultinomialNB))
])

grid = GridSearchCV(estimator = pipeline, param_grid = param_grid, n_jobs = 1, cv = 8)

training_data = DataFrame({'text': [], 'class': []})
for path, classification in SOURCES:
    training_data = training_data.append(build_data_frame(path, classification))

training_data = training_data.reindex(numpy.random.permutation(training_data.index))

start = time()

grid.fit(training_data['text'].values, training_data['class'].values)

print("GridSearchCV took %.2f seconds" % (time() - start))
print("Best score: %0.3f" % grid.best_score_)
print("Best parameters set:")
best_parameters = grid.best_estimator_.get_params()
#for param_name in sorted(best_parameters.keys()):
#    print("\t%s: %r" % (param_name, best_parameters[param_name]))

evaluation_data = DataFrame({'text': [], 'class':[]})
for path, classification in EVALUATION:
    evaluation_data = evaluation_data.append(build_data_frame(path, classification))

evaluation_data = evaluation_data.reindex(numpy.random.permutation(evaluation_data.index))

#pipeline.fit(training_data['text'].values, training_data['class'].values)
predicted_classes = grid.predict(evaluation_data['text'].values)

score = f1_score(evaluation_data['class'].values, predicted_classes, pos_label=FAKE)

path = './data/classifiers/'
strScoreEVAL = str("{0:.4f}".format(score))
strScoreTEST = str("{0:.4f}".format(grid.best_score_))
file_path_and_name = path+'classifierSettings ' + strScoreEVAL + ' ' + strScoreTEST + '.txt'
path = path + 'pickles/'
estimatorPath = path+'classifierSettings ' + strScoreEVAL + ' ' + strScoreTEST + '.pkl'
if not os.path.exists(os.path.dirname(path)):
    try:
        os.makedirs(os.path.dirname(file_path_and_name))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
joblib.dump(grid.best_estimator_, estimatorPath)
savedEstimator = open(file_path_and_name,"w")
for param_name in sorted(best_parameters.keys()):
    line = "\t%s: %r" % (param_name, best_parameters[param_name]) + NEWLINE      
    savedEstimator.write(line.encode("utf8"))
    savedEstimator.flush()
savedEstimator.close

print 'Evaluation-set results:'
print('Total articles classified:', len(evaluation_data))
print("Score: %.2f" % score)
print('Confusion matrix:')
print confusion_matrix(evaluation_data['class'].values, predicted_classes)

print 'Article:     Actual class:     Predicted class:'
for article, actual, predicted in zip(evaluation_data.index.values, evaluation_data['class'].values, predicted_classes):
    if actual != predicted:
        newArticle = ""
        i = 0
        for word in article.split(" "):
            if i != 0:
                newArticle = newArticle + word + " "
            i = i + 1
        print newArticle, actual, predicted
print("Total time was %.2f seconds" % (time() - start))
