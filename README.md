# StyleDNA AI - Fashion Image Processor & Outfit Recommender

An AI-powered system for processing clothing images and providing personalized outfit recommendations.

## Features

- Image upload and processing
- AI-powered clothing analysis using computer vision
- Automatic color extraction and clothing type detection
- Cloud storage integration
- Smart outfit recommendations based on weather and occasion

## Tech Stack

- Backend:
  - FastAPI
  - OpenCV
  - scikit-learn
  - AWS S3
  - PostgreSQL
  - SQLAlchemy

## Project Structure

```
/styledna-ai
│
├── backend/
│   ├── api/
│   │   └── upload_image.py
│   ├── services/
│   │   ├── processor.py
│   │   ├── storage.py
│   │   └── recommender.py
│   ├── models/
│   │   └── image_metadata.py
│   └── main.py
│
├── requirements.txt
└── README.md
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export DATABASE_URL=postgresql://user:password@localhost:5432/styledna
```

3. Run the application:
```bash
cd backend
uvicorn main:app --reload
```

## API Endpoints

- `POST /upload-image`: Upload and process clothing images
- `GET /recommend`: Get outfit recommendations
- `GET /wardrobe`: List user's wardrobe items

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 