"Importing necessary modules"
import joblib
import spacy


class NewsDetector:
    """## Class ``NewsDetector``:
    
    **Purpose:** To check news and make predictions.
    """
    
    # loading the model
    model = joblib.load(r"all_ensemble_model")
    
    # loading the vectorizer
    vector = joblib.load(r"vector.pkl")
    
    # loading pre trained english language model
    try:
        nlp = spacy.load("en_core_web_sm")
        
    except OSError:
        spacy.cli.download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")


    def nlp_apply(self, text : str) -> str:
        """### Method ``nlp_apply`` returns string:
        
        **Purpose:** To applying the nlp into new data."""
        
        # testing if any error
        try:
            # converting into lower case
            text = text.lower()

            # converting into document
            doc = self.nlp(text)

            # getting refined words using list comprehension
            refined_words = [token.lemma_ for token in doc if not (token.is_stop) and not (token.is_punct)]

            # returning as a string
            return " ".join(refined_words)
        
        # catching error here
        except Exception as e:
            print(f"Exception occured at nlp_apply() method from NewsDetector class: {e}")    
    
    def predict_news(self, text : str) -> str:
        """### Method ``predict_news`` returns string:
        
        **Purpose:** To predict the news using trained model.
        """
        # testing if any error
        try:
            # calling the nlp function
            text = [self.nlp_apply(text)]

            # applying tfidf vectorizer
            text_tfidf_form = self.vector.transform(text)

            # getting prediction value
            predicted_output = self.model.predict(text_tfidf_form)
            
            # returning the result
            return 'Real' if (predicted_output == 1) else 'Fake'

        # catching error here
        except Exception as e:
            print(f"Exception occured at predict_news() method from NewsDetector class: {e}")
            

if __name__ == "__main__":
    """**Purpose:** Checking the file is main file or not"""
    
    # checking errors here
    try:
        # creating an instance
        obj = NewsDetector()
        
        # testing news
        print(obj.predict_news(""))
    
    # catching errors here
    except Exception as e:
        print(f"Exception occured at main file: {e}")
