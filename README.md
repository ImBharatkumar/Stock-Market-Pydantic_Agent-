# AI Stock Market Research Agent

## Project Overview

This project is an AI-powered stock market research tool that leverages FastAPI, SQLAlchemy, and an AI agent to fetch and analyze stock market information. The application allows users to retrieve real-time stock prices, company information, and save competitor data to a PostgreSQL database.

## Features

- Fetch real-time stock prices using Yfinance
- AI-powered stock information retrieval
- Persistent storage of competitor data
- RESTful API endpoints for stock research
- Database integration with SQLAlchemy

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ImBharatkumar/Stock-Market-Pydantic_Agent-.git
```

### 2. Create a Virtual Environment

```bash
conda create -n venv
conda activate venv  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

1. Create a PostgreSQL database:
```sql
CREATE DATABASE mydatabase;
```

2. Update database credentials in `database.py`:
```python
DATABASE_URL = "postgresql://username:password@localhost/mydatabase"
```

### 5. Initialize Database

```bash
# This will create necessary tables
python -c "from database import engine, Base; Base.metadata.create_all(bind=engine)"
```

## Environment Variables

Create a `.env` file in the project root and add:

GROQ_API_KEY=<your_groq_api_key>

## Running the Application

```bash
uvicorn app:app --reload
```

The application will be available at `http://localhost:8000`

## API Endpoints

### 1. Get Stock Price

- **URL**: `/get_result/`
- **Method**: POST
- **Parameters**:
  - `symbol`: Stock ticker symbol (e.g., 'AAPL' or Apple)
- **Response**:
  - Stock information including symbol, current stock price, sector, market cap
  - Saved competitor ID

### 2. Get Competitor Details

- **URL**: `/competitor/{id}`
- **Method**: GET
- **Parameters**:
  - `id`: Competitor database ID
- **Response**: Detailed competitor information

### OR

- run cli command `uvicorn app:app --reload`
- route to `http://127.0.0.1:8000/docs` #u will get interactive FastAPI dashboard for querying and errors.

## Technology Stack

- **Backend**: FastAPI
- **AI Agent**: Groq LLaMA 3 70B
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Stock Data**: yfinance

## Key Dependencies

- fastapi
- pydantic
- sqlalchemy
- yfinance
- nest_asyncio
- groq

## Error Handling

The application includes robust error handling:

- Catches stock price retrieval errors
- Handles database insertion exceptions
- Provides clear HTTP error responses

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

email - `bharatkumargkori@gmail.com`

LinkedIn -`https://www.linkedin.com/in/bharatkumarkori/`