from spellchecker import SpellChecker
from typing import List, Dict
import re


class SpellCheckService:
    """Handle spell checking functionality"""
    
    def __init__(self):
        self.spell = SpellChecker()
    
    def check_spelling(self, text: str) -> Dict:
        """
        Check spelling in text and return misspelled words with suggestions
        
        Args:
            text: Text to check
            
        Returns:
            Dictionary with misspelled words and their suggestions
        """
        try:
            # Find misspelled words
            misspelled = self.spell.unknown(text.split())
            
            corrections = {}
            for word in misspelled:
                # Get correction suggestions
                suggestions = self.spell.correction(word)
                corrections[word] = {
                    "suggestion": suggestions,
                    "alternatives": list(self.spell.candidates(word))[:5]  # Top 5 alternatives
                }
            
            return {
                "misspelled_count": len(misspelled),
                "misspelled_words": list(misspelled),
                "corrections": corrections,
                "accuracy_percentage": round(((len(text.split()) - len(misspelled)) / len(text.split()) * 100), 2) if text.split() else 0
            }
        
        except Exception as e:
            return {
                "error": f"Error checking spelling: {str(e)}",
                "misspelled_count": 0,
                "corrections": {}
            }
    
    def correct_text(self, text: str) -> str:
        """
        Auto-correct text by replacing misspelled words
        
        Args:
            text: Text to correct
            
        Returns:
            Corrected text
        """
        try:
            words = text.split()
            corrected_words = []
            
            for word in words:
                if word.lower() in self.spell.unknown([word.lower()]):
                    # Get the best correction
                    corrected = self.spell.correction(word.lower())
                    corrected_words.append(corrected)
                else:
                    corrected_words.append(word)
            
            return " ".join(corrected_words)
        
        except Exception as e:
            return text
    
    def add_word_to_dictionary(self, word: str):
        """Add a word to the spell checker dictionary"""
        self.spell.word_probability[word] = 1
    
    def remove_word_from_dictionary(self, word: str):
        """Remove a word from the spell checker dictionary"""
        if word in self.spell.word_probability:
            del self.spell.word_probability[word]
