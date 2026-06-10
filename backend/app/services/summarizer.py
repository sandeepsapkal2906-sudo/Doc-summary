import re
from typing import Dict, List
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class Summarizer:
    """Handle document summarization and insights extraction"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def summarize(self, text: str, num_sentences: int = 5) -> str:
        """
        Generate a summary of the document using extractive summarization
        
        Args:
            text: Document text to summarize
            num_sentences: Number of sentences in the summary
            
        Returns:
            Summary text
        """
        if not text or len(text.split()) < 50:
            return "Document too short to summarize."
        
        try:
            # Tokenize into sentences
            sentences = sent_tokenize(text)
            
            if len(sentences) <= num_sentences:
                return text
            
            # Calculate sentence scores based on word frequency
            words = word_tokenize(text.lower())
            words = [word for word in words if word.isalnum()]
            
            # Remove stopwords
            important_words = [word for word in words if word not in self.stop_words]
            
            # Calculate word frequencies
            word_freq = Counter(important_words)
            
            # Score sentences
            sentence_scores = {}
            for sentence in sentences:
                words_in_sentence = word_tokenize(sentence.lower())
                for word in words_in_sentence:
                    if word in word_freq:
                        if sentence not in sentence_scores:
                            sentence_scores[sentence] = 0
                        sentence_scores[sentence] += word_freq[word]
            
            # Get top sentences
            top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
            
            # Sort by original order
            summary_sentences = sorted([s[0] for s in top_sentences], 
                                     key=lambda x: sentences.index(x))
            
            return " ".join(summary_sentences)
        
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def extract_insights(self, text: str) -> Dict:
        """
        Extract key insights from the document
        
        Args:
            text: Document text
            
        Returns:
            Dictionary containing insights
        """
        try:
            # Basic metrics
            words = word_tokenize(text.lower())
            sentences = sent_tokenize(text)
            
            # Word count and reading time
            word_count = len([w for w in words if w.isalnum()])
            reading_time = max(1, word_count // 200)  # Average reading speed
            
            # Extract key topics (most frequent important words)
            important_words = [word for word in words 
                             if word.isalnum() and word not in self.stop_words 
                             and len(word) > 3]
            
            word_freq = Counter(important_words)
            key_topics = [word for word, _ in word_freq.most_common(10)]
            
            # Extract entities (simple approach - capitalized words)
            entities = self._extract_entities(text)
            
            # Simple sentiment analysis
            sentiment = self._analyze_sentiment(text)
            
            return {
                "key_topics": key_topics,
                "entities": entities[:15],  # Top 15 entities
                "sentiment": sentiment,
                "word_count": word_count,
                "sentence_count": len(sentences),
                "average_sentence_length": word_count // len(sentences) if sentences else 0,
                "reading_time_minutes": reading_time,
                "document_complexity": self._assess_complexity(word_count, len(sentences))
            }
        
        except Exception as e:
            return {
                "error": f"Error extracting insights: {str(e)}",
                "key_topics": [],
                "entities": [],
                "sentiment": "neutral"
            }
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract named entities (simple approach)"""
        # Match capitalized words (potential names/entities)
        entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        return list(set(entities))
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis based on positive/negative words"""
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 
                         'positive', 'best', 'love', 'perfect', 'fantastic'}
        negative_words = {'bad', 'poor', 'terrible', 'awful', 'horrible', 
                         'negative', 'worst', 'hate', 'difficult', 'problem'}
        
        text_lower = text.lower()
        words = word_tokenize(text_lower)
        
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _assess_complexity(self, word_count: int, sentence_count: int) -> str:
        """Assess document complexity"""
        if word_count == 0 or sentence_count == 0:
            return "unknown"
        
        avg_words_per_sentence = word_count / sentence_count
        
        if avg_words_per_sentence < 10:
            return "simple"
        elif avg_words_per_sentence < 20:
            return "moderate"
        else:
            return "complex"
