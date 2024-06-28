"""
#####################
Simple Python class for performing text pre-processing on a CSV file.
Developed as part of the BRAID project at the University of Sheffield.

Run with -h flag for a list of optional arguments.
#####################
"""

import os
import sys
import argparse
import re
from datetime import datetime
import pandas as pd
from nltk import download
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


class Preprocessing():
    def __init__(self):
        self.date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.output_dir = 'output' # set up directory for output files
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        self.inputs = self.parse_args()
        self.df = pd.read_csv('data.csv', encoding='latin-1')
        self.df = self.df.fillna('') # fill nan with the empty string
        self.column_name = 'Description: (Collection Details)/Description' # set column name
        self.all_tokens = {}  # count tokens
        self.types = set()  # count types

    def parse_args(self):
        """
        Parse command line arguments.
        """
        parser = argparse.ArgumentParser(
            description='Text pre-processing for BRAID project. Pass in optional arguments to apply stopword removal, stemming or lemmatization. Stemming and Lemmatization are mutually exclusive.')
        parser.add_argument(
            '--stop', action=argparse.BooleanOptionalAction, default=False, help='Applies stopword removal to text.')

        # stemming and lemmatization are mutually exclusive
        xor_group = parser.add_mutually_exclusive_group(required=False)
        xor_group.add_argument(
            '--stem', action=argparse.BooleanOptionalAction, default=False, help='Applies stemming to text. Cannot be used in conjunction with --lemma.')
        xor_group.add_argument(
            '--lemma', action=argparse.BooleanOptionalAction, default=False, help='Applies lemmatization to text. Cannot be used in conjunction with --stem.')

        args = parser.parse_args()

        return args

    def lowercase(self):
        """
        Lowercase text.
        """
        self.df[self.column_name] = self.df[self.column_name].str.lower()

    def remove_punctuation(self):
        """
        Removes punctuation. In a second step, also turns double spaces into single spaces.
        """
        # remove punctuation using regex - this pattern will preserve hypens in the middle of words
        pattern = re.compile(r'(?<!\w)-(?!\w)|[^\w\s-]')
        self.df[self.column_name] = self.df[self.column_name].apply(
            lambda x: re.sub(pattern, '', str(x)))

        # remove double spaces
        double_space_re = re.compile(r"\s{2}")
        self.df[self.column_name] = self.df[self.column_name].str.replace(
            double_space_re, ' ', regex=True)

    def remove_numbers(self):
        """
        Remove numerical digits from the text.
        """
        self.df[self.column_name] = self.df[self.column_name].apply(
            lambda x: re.sub(r'\d+', '', x))

    def remove_stopwords(self):
        """
        Remove common stoplist words.
        """
        download('stopwords')
        stopwords_en = stopwords.words('english')

        def remove_stop_words(phrase):
            words = phrase.split()
            filtered = [w for w in words if w.lower() not in stopwords_en]
            return ' '.join(filtered)

        self.df[self.column_name] = self.df[self.column_name].apply(
            remove_stop_words)

    def stem_words(self):
        """
        Perform stemming on words in the text.
        """
        stemmer = PorterStemmer()

        def stem_phrase(phrase):
            words = phrase.split()
            stemmed = [stemmer.stem(w) for w in words]
            return ' '.join(stemmed)

        self.df[self.column_name] = self.df[self.column_name].apply(
            stem_phrase)

    def lemmatize_words(self):
        """
        Perform lemmatization on words in the text.
        """
        lemmatizer = WordNetLemmatizer()
        download('wordnet')

        def lemmatize_phrase(phrase):
            words = phrase.split()
            lemmatized = [lemmatizer.lemmatize(w) for w in words]
            return ' '.join(lemmatized)

        self.df[self.column_name] = self.df[self.column_name].apply(
            lemmatize_phrase)

    def create_bow(self):
        """
        Create a bag-of-words representation of the text and output to CSV.
        """
        self.bow = self.df[self.column_name].str.split(
            expand=True).stack().value_counts()
        self.bow.reset_index().to_csv(f'{self.output_dir}/{str(self.date)}_bow.csv', header=[
            'word', 'count'], index=False)

    def count_types_and_tokens(self):
        """
        Counts the number of types and tokens in sentences.
        These are stored in the class variables self.types and self.all_tokens.
        """
        def count_tokens(sentence):
            """
            Helper function for counting tokens in a sentence
            """
            tokens = sentence.split()  # Split the sentence into tokens (words)

            for token in tokens:
                self.types.add(token)  # Put unique tokens (types) into the set

                # If token not in the dictionary of all tokens, add it, else bump the count
                if token not in self.all_tokens:
                    self.all_tokens[token] = 1
                else:
                    self.all_tokens[token] += 1

        self.df[self.column_name].apply(count_tokens)

    def main(self):
        self.lowercase()
        self.remove_numbers() # we need to remove numbers before punctuation removal to catch date ranges e.g. AD 1530-1, or serial numbers e.g. 59-4-2-25
        self.remove_punctuation()

        if self.inputs.stop:
            self.remove_stopwords()

        if self.inputs.stem:
            self.stem_words()

        if self.inputs.lemma:
            self.lemmatize_words()

        self.create_bow()
        self.count_types_and_tokens()

        # write out pre-processed descriptions to csv
        filename = f'{self.output_dir}/{str(self.date)}{sys.argv[1:]}.txt'
        self.df[self.column_name].to_csv(filename, index=True, header=False)


if __name__ == '__main__':
    preprocessing_instance = Preprocessing()
    preprocessing_instance.main()
