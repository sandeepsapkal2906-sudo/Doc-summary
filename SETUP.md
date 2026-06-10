# Document Summarizer - Installation & Usage Guide

## Quick Start (Local Development)

### Step 1: Install Dependencies

**Backend (Python)**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend (Node.js)**
```bash
cd frontend
npm install
```

### Step 2: Start the Services

**Terminal 1 - Backend**
```bash
cd backend
source venv/bin/activate
python app/main.py
```
Backend runs on: http://localhost:8080

**Terminal 2 - Frontend**
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:3030

### Step 3: Open the Application
Visit http://localhost:3030 in your browser

---

## Features

### ✅ What It Does
- Upload PDF and DOCX documents
- Generates intelligent summaries
- Extracts key topics and insights
- Analyzes sentiment and complexity
- Provides reading time estimates
- Shows named entities in documents

### ✅ Privacy & Security
- **100% Local Processing** - No data sent to cloud
- **No External APIs** - Everything runs on your machine
- **Automatic Cleanup** - Temporary files are deleted after processing
- **No Storage** - Summaries only kept in browser session unless downloaded

---

## How It Works

### Upload Process
1. Select a PDF or DOCX file
2. File is sent to backend API
3. Text is extracted from document
4. NLP models analyze the content locally
5. Summary and insights are generated
6. Results sent back to frontend
7. Temporary file is deleted

### Summarization
- Uses extractive summarization (picks important sentences)
- Based on word frequency analysis
- Removes stopwords for better results
- Maintains document context

### Insights Extraction
- **Key Topics**: Most frequent important words
- **Entities**: Names and proper nouns
- **Sentiment**: Positive, negative, or neutral tone
- **Statistics**: Word count, sentences, reading time
- **Complexity**: Simple, moderate, or complex

---

## API Endpoints

### POST /api/upload
Upload and process a document

**Request:**
```
Content-Type: multipart/form-data
File: PDF or DOCX file
```

**Response:**
```json
{
  "filename": "document.pdf",
  "original_text_length": 5000,
  "summary": "This is a summary of the document...",
  "insights": {
    "key_topics": ["topic1", "topic2"],
    "entities": ["Entity1", "Entity2"],
    "sentiment": "positive",
    "word_count": 5000,
    "reading_time_minutes": 20,
    "document_complexity": "moderate"
  },
  "processed_at": "2024-01-10T12:34:56"
}
```

### GET /api/health
Health check endpoint

### GET /api/supported-formats
Get supported file formats

---

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (needs 3.8+)
- Ensure virtual environment is activated
- Try reinstalling dependencies: `pip install -r requirements.txt --force-reinstall`

### Frontend won't start
- Check Node.js version: `node --version` (needs 16+)
- Delete `node_modules`: `rm -rf node_modules`
- Reinstall: `npm install`
- Clear Next.js cache: `rm -rf .next`

### Port already in use
- Backend (8080): `lsof -i :8080` then `kill -9 <PID>`
- Frontend (3030): `lsof -i :3030` then `kill -9 <PID>`

### File upload fails
- Check file format (PDF or DOCX only)
- Verify file size is under 50MB
- Ensure file isn't corrupted

### Processing takes too long
- Large documents (>100 pages) will take longer
- First run downloads NLP models (slower)
- Subsequent runs are faster with cached models

---

## Using Docker (Optional)

### Prerequisites
- Docker and Docker Compose installed

### Start with Docker
```bash
docker-compose up
```

This will:
- Build and start backend on port 8080
- Build and start frontend on port 3030

### Stop Services
```bash
docker-compose down
```

---

## Performance Tips

1. **Smaller Documents**: Process faster
2. **Close Other Applications**: Frees up system resources
3. **First Run**: Slower due to NLP model downloads
4. **SSD vs HDD**: Faster on SSD

---

## System Requirements

- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB free (for NLP models)
- **CPU**: Modern multi-core processor
- **OS**: Windows, macOS, or Linux

---

## Security & Privacy

All processing happens locally:
- ✅ Files don't leave your computer
- ✅ No internet required for processing
- ✅ No accounts or logins needed
- ✅ No tracking or analytics
- ✅ No data collection

Your documents are completely private!

---

## Support

For issues or questions, check:
1. Logs in terminal for error messages
2. Browser console (F12) for frontend errors
3. Backend error responses in API responses

---

## License

MIT License - See LICENSE file for details
