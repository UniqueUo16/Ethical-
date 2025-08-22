import os
import re
import math
import io
import logging
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/convert-case", methods=["POST"])
def convert_case():
    """Convert text case"""
    try:
        data = request.get_json()
        text = data.get("text", "")
        case_type = data.get("case_type", "")
        
        if case_type == "uppercase":
            result = text.upper()
        elif case_type == "lowercase":
            result = text.lower()
        elif case_type == "title":
            result = text.title()
        elif case_type == "sentence":
            # Convert to sentence case
            sentences = re.split(r'([.!?]+)', text.lower())
            result = ""
            for i, sentence in enumerate(sentences):
                if i % 2 == 0 and sentence.strip():  # Every other element is actual text
                    sentence = sentence.strip()
                    if sentence:
                        sentence = sentence[0].upper() + sentence[1:]
                result += sentence
        else:
            return jsonify({"error": "Invalid case type"}), 400
            
        return jsonify({"result": result})
    except Exception as e:
        logging.error(f"Error in convert_case: {str(e)}")
        return jsonify({"error": "An error occurred during case conversion"}), 500

@app.route("/api/count-text", methods=["POST"])
def count_text():
    """Count words, characters, and calculate reading time"""
    try:
        data = request.get_json()
        text = data.get("text", "")
        
        # Character count (with and without spaces)
        char_count = len(text)
        char_count_no_spaces = len(text.replace(" ", ""))
        
        # Word count
        words = text.split() if text.strip() else []
        word_count = len(words)
        
        # Sentence count
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # Paragraph count
        paragraphs = text.split('\n\n')
        paragraph_count = len([p for p in paragraphs if p.strip()])
        
        # Reading time (average 200 words per minute)
        reading_time_minutes = math.ceil(word_count / 200) if word_count > 0 else 0
        
        return jsonify({
            "characters": char_count,
            "characters_no_spaces": char_count_no_spaces,
            "words": word_count,
            "sentences": sentence_count,
            "paragraphs": paragraph_count,
            "reading_time": reading_time_minutes
        })
    except Exception as e:
        logging.error(f"Error in count_text: {str(e)}")
        return jsonify({"error": "An error occurred during text counting"}), 500

@app.route("/api/find-replace", methods=["POST"])
def find_replace():
    """Find and replace text"""
    try:
        data = request.get_json()
        text = data.get("text", "")
        find_text = data.get("find", "")
        replace_text = data.get("replace", "")
        case_sensitive = data.get("case_sensitive", False)
        use_regex = data.get("use_regex", False)
        
        if not find_text:
            return jsonify({"error": "Find text cannot be empty"}), 400
        
        if use_regex:
            try:
                flags = 0 if case_sensitive else re.IGNORECASE
                result = re.sub(find_text, replace_text, text, flags=flags)
                match_count = len(re.findall(find_text, text, flags=flags))
            except re.error as e:
                return jsonify({"error": f"Invalid regex pattern: {str(e)}"}), 400
        else:
            if case_sensitive:
                result = text.replace(find_text, replace_text)
                match_count = text.count(find_text)
            else:
                # Case insensitive replacement
                pattern = re.escape(find_text)
                result = re.sub(pattern, replace_text, text, flags=re.IGNORECASE)
                match_count = len(re.findall(pattern, text, flags=re.IGNORECASE))
        
        return jsonify({
            "result": result,
            "replacements": match_count
        })
    except Exception as e:
        logging.error(f"Error in find_replace: {str(e)}")
        return jsonify({"error": "An error occurred during find and replace"}), 500

@app.route("/api/clean-text", methods=["POST"])
def clean_text():
    """Clean text by removing extra spaces, line breaks, etc."""
    try:
        data = request.get_json()
        text = data.get("text", "")
        clean_type = data.get("clean_type", "")
        
        if clean_type == "extra_spaces":
            # Remove extra spaces
            result = re.sub(r'\s+', ' ', text).strip()
        elif clean_type == "line_breaks":
            # Remove line breaks
            result = text.replace('\n', ' ').replace('\r', ' ')
            result = re.sub(r'\s+', ' ', result).strip()
        elif clean_type == "special_chars":
            # Remove special characters (keep alphanumeric, spaces, and basic punctuation)
            result = re.sub(r'[^\w\s.!?,:;"-]', '', text)
        elif clean_type == "all":
            # Clean everything
            result = re.sub(r'[^\w\s.!?,:;"-]', '', text)
            result = result.replace('\n', ' ').replace('\r', ' ')
            result = re.sub(r'\s+', ' ', result).strip()
        else:
            return jsonify({"error": "Invalid clean type"}), 400
            
        return jsonify({"result": result})
    except Exception as e:
        logging.error(f"Error in clean_text: {str(e)}")
        return jsonify({"error": "An error occurred during text cleaning"}), 500

@app.route("/api/format-text", methods=["POST"])
def format_text():
    """Format text as bullet points or numbered lists"""
    try:
        data = request.get_json()
        text = data.get("text", "")
        format_type = data.get("format_type", "")
        
        # Split text into lines and filter out empty ones
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if format_type == "bullets":
            result = '\n'.join([f"• {line}" for line in lines])
        elif format_type == "numbers":
            result = '\n'.join([f"{i+1}. {line}" for i, line in enumerate(lines)])
        elif format_type == "remove_formatting":
            # Remove bullet points and numbers
            result = []
            for line in lines:
                # Remove bullets
                line = re.sub(r'^[•·*-]\s*', '', line)
                # Remove numbering
                line = re.sub(r'^\d+\.\s*', '', line)
                if line.strip():
                    result.append(line.strip())
            result = '\n'.join(result)
        else:
            return jsonify({"error": "Invalid format type"}), 400
            
        return jsonify({"result": result})
    except Exception as e:
        logging.error(f"Error in format_text: {str(e)}")
        return jsonify({"error": "An error occurred during text formatting"}), 500

@app.route("/api/seo-analysis", methods=["POST"])
def seo_analysis():
    """Perform basic SEO analysis"""
    try:
        data = request.get_json()
        text = data.get("text", "")
        keyword = data.get("keyword", "").lower()
        
        if not text.strip():
            return jsonify({"error": "Text cannot be empty"}), 400
        
        # Word count and text preparation
        words = text.lower().split()
        word_count = len(words)
        
        # Keyword density
        keyword_density = 0
        if keyword and word_count > 0:
            keyword_count = words.count(keyword)
            keyword_density = round((keyword_count / word_count) * 100, 2)
        
        # Reading score (simplified Flesch Reading Ease approximation)
        sentences = len(re.split(r'[.!?]+', text))
        sentences = max(sentences, 1)  # Avoid division by zero
        avg_sentence_length = word_count / sentences
        
        # Simple syllable counter (rough approximation)
        syllables = 0
        for word in words:
            vowels = re.findall(r'[aeiouAEIOU]', word)
            syllables += max(len(vowels), 1)
        
        avg_syllables_per_word = syllables / max(word_count, 1)
        
        # Simplified readability score
        readability_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        readability_score = max(0, min(100, readability_score))  # Clamp between 0-100
        
        # Readability level
        if readability_score >= 90:
            readability_level = "Very Easy"
        elif readability_score >= 80:
            readability_level = "Easy"
        elif readability_score >= 70:
            readability_level = "Fairly Easy"
        elif readability_score >= 60:
            readability_level = "Standard"
        elif readability_score >= 50:
            readability_level = "Fairly Difficult"
        elif readability_score >= 30:
            readability_level = "Difficult"
        else:
            readability_level = "Very Difficult"
        
        return jsonify({
            "keyword_density": keyword_density,
            "readability_score": round(readability_score, 1),
            "readability_level": readability_level,
            "avg_sentence_length": round(avg_sentence_length, 1),
            "avg_syllables_per_word": round(avg_syllables_per_word, 1)
        })
    except Exception as e:
        logging.error(f"Error in seo_analysis: {str(e)}")
        return jsonify({"error": "An error occurred during SEO analysis"}), 500

@app.route("/api/compare-text", methods=["POST"])
def compare_text():
    """Compare two texts"""
    try:
        data = request.get_json()
        text1 = data.get("text1", "")
        text2 = data.get("text2", "")
        
        # Basic comparison metrics
        words1 = text1.split()
        words2 = text2.split()
        
        char_diff = len(text2) - len(text1)
        word_diff = len(words2) - len(words1)
        
        # Calculate similarity (simple word overlap)
        set1 = set(word.lower() for word in words1)
        set2 = set(word.lower() for word in words2)
        
        if len(set1) == 0 and len(set2) == 0:
            similarity = 100
        elif len(set1) == 0 or len(set2) == 0:
            similarity = 0
        else:
            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            similarity = round((intersection / union) * 100, 1)
        
        return jsonify({
            "char_difference": char_diff,
            "word_difference": word_diff,
            "similarity_percentage": similarity,
            "text1_stats": {
                "characters": len(text1),
                "words": len(words1)
            },
            "text2_stats": {
                "characters": len(text2),
                "words": len(words2)
            }
        })
    except Exception as e:
        logging.error(f"Error in compare_text: {str(e)}")
        return jsonify({"error": "An error occurred during text comparison"}), 500

@app.route("/api/export-text", methods=["POST"])
def export_text():
    """Export processed text as downloadable file"""
    try:
        data = request.get_json()
        text = data.get("text", "")
        filename = data.get("filename", "processed_text.txt")
        
        if not text.strip():
            return jsonify({"error": "Text cannot be empty"}), 400
        
        # Create a file-like object
        text_file = io.BytesIO()
        text_file.write(text.encode('utf-8'))
        text_file.seek(0)
        
        return send_file(
            text_file,
            as_attachment=True,
            download_name=filename,
            mimetype='text/plain'
        )
    except Exception as e:
        logging.error(f"Error in export_text: {str(e)}")
        return jsonify({"error": "An error occurred during text export"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)