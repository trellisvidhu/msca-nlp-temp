import pandas as pd
import nltk as nltk
import wget
from textblob import TextBlob

stopwords = set(nltk.corpus.stopwords.words('english'))

def get_data(filepath):
  raw_text = wget.download(filepath)
  with open(raw_text,'r')  as f:
    data = f.read()
  return data

def nltk_pre_process(text_data):
  
  #Word Tokenizer
  print('Running NLTK Word Tokenizer')
  words = nltk.tokenize.word_tokenize(text_data)

  #Remove Stop Words
  words = [word for word in words if word not in stopwords]

  # Remove single-character tokens (mostly punctuation)
  words = [word for word in words if len(word) > 1]

  # Remove numbers
  #words = [word for word in words if not word.isnumeric()]

  # Remove punctuation
  words = [word for word in words if word.isalpha()]

  # Lowercase all words (default_stopwords are lowercase too)
  words = [word.lower() for word in words]

  #Print Number of clean words
  print(f"Total Number of clean words {len(words)}")

  #FreqDist
  words_freqdist = nltk.FreqDist(words)
  print('10 Most Common Tokens')  
  print(words_freqdist.most_common(10))

  return words

def ngram_compare_files(file1,file2,n):
    # Takes two files
    # hashes their n-grams into twos lists
    # calculates the intersection and union
    # of the two lists, and returns
    # Jacard similarity value
 
    stop = stopwords.words('english')
    f1 = open(file1)
    raw = f1.read()
    f1.close()
    f1_grams = nltk.ngrams(raw.split(),n)
    
    array_1 = []
    
    for gram in f1_grams:
        array_1.append(hash(gram))
    f2 = open(file2)
    raw = f2.read()
    f2.close()
    f2_grams = nltk.ngrams(raw.split(),n)
    
    array_2 = []
    
    for gram in f2_grams:
        array_2.append(hash(gram))
        
    intersection = len(list(set(array_1).intersection(array_2)))    
    union = len(set(array_1)) + len(set(array_2)) - intersection
    jacard_similarity = intersection / union
    return jacard_similarity

def pairs_of_files(directory):
    # returns combination of two files given
    # all files in a directory
    
    dir = os.listdir(directory)
    combo = combinations(dir, 2)
    return combo

def compare_files(directory,ngram_size,threshold):
    # compares all pairs of files in a directory
    # for similarity.
    # RETURNS: Dictionary, with key as
    # comma-separated string of two files
    # and value of similarity index as decimal
    # where similarity index is above threshold
    # value.
    
    compare_dictionary = {}
    
    ngram = ngram_size
    combo = pairs_of_files(directory)
    
    for i in combo:
        
        sim = ngram_compare_files(directory+str(i[0]),directory+str(i[1]),ngram)
        if sim > threshold:
            
            key = str(i[0]) + "," + str(i[1])
            value = sim
            compare_dictionary[key]=value
            
    return compare_dictionary            

if __name__ == '__main__':
  
  #----------------------------------------
  #  CHECKING LENGTH OF FILES AND ARTICLES
  #----------------------------------------
  book_list = ['3boat10',
               'Adventures_of_Sherlock_Holmes',
               'Hound_of_the_Baskervilles',
               'Return_of_Sherlock_Holmes']

  for i in range(0,4):
    link = 'https://raw.githubusercontent.com/trellisvidhu/msca-nlp-temp/main/'+ book_list[i] +'.txt'
    text_data = get_data(link)
    words = nltk.tokenize.word_tokenize(text_data)
    print(f'Number of tokens in {book_list[i]} = {len(words)}')

  for i in range(1,41):
    link = 'https://raw.githubusercontent.com/trellisvidhu/msca-nlp-temp/main/article'+str(i)+'.txt'
    text_data = get_data(link)
    words = nltk.tokenize.word_tokenize(text_data)
    print(f'Number of tokens in article {i} = {len(words)}')

  #----------------------------------------
  #  TOKENIZING
  #----------------------------------------
  filepath = 'https://raw.githubusercontent.com/trellisvidhu/msca-nlp-temp/main/article1.txt'
  text_data = get_data(filepath)
  words = nltk_pre_process(text_data)

  #----------------------------------------
  #  NGRAMS
  #----------------------------------------
  words_ngram = nltk_ngrams(words,2)
  nltk.FreqDist(words_ngram).most_common(5)
