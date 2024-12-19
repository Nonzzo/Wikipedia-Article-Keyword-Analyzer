# Wikipedia Article Keyword Analyzer

A Docker-based application that crawls random Wikipedia articles and analyzes keyword frequencies across the collected content. The application stores articles in a PostgreSQL database and provides keyword frequency analysis.

## Features

- Fetches random Wikipedia articles automatically
- Stores article content in a PostgreSQL database
- Analyzes keyword frequency across all stored articles
- Runs in a containerized environment using Docker
- Provides detailed breakdown of keyword occurrences per article

## Prerequisites

- Docker and Docker Compose installed on your system
- Basic knowledge of Docker and Python
- Internet connection for fetching Wikipedia articles

## Project Structure

```
wiki-keyword-analyzer/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
├── wiki_crawler.py
├── wait-for-postgres.sh
└── tests/
    ├── __init__.py
    ├── test_wiki_crawler.py
    └── conftest.py
    ├── requirements.txt
    └── Dockerfile.test
    └── docker-compose.test.yml
```

## Installation & Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd wiki-keyword-analyzer
```

2. Make the wait script executable:
```bash
chmod +x wait-for-postgres.sh
```

3. Build and run the containers:
```bash
docker-compose up --build
```

## Configuration

You can configure the following environment variables in `docker-compose.yml`:

- `DATABASE_HOST`: PostgreSQL host (default: database)
- `DATABASE_PORT`: PostgreSQL port (default: 5432)
- `DATABASE_NAME`: Database name (default: wikipedia)
- `DATABASE_USER`: Database user (default: postgres)
- `DATABASE_PASSWORD`: Database password
- `ANALYSIS_KEYWORD`: Keyword to analyze (default: python)

## Usage

1. The application will automatically:
   - Connect to the database
   - Create necessary tables
   - Fetch 10 random Wikipedia articles
   - Store them in the database
   - Analyze the frequency of the specified keyword

2. To analyze a different keyword:
   - Update the `ANALYSIS_KEYWORD` in docker-compose.yml
   - Rebuild and restart the containers

## Development

### Running Tests

```bash
docker-compose -f docker-compose.test.yml up --build
```

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Write tests for new features
5. Submit a pull request

## Technical Details

- **Python Version**: 3.9
- **Database**: PostgreSQL 13
- **Key Dependencies**:
  - SQLAlchemy for database operations
  - Wikipedia-API for fetching articles
  - Psycopg2 for PostgreSQL connection
  - Requests for HTTP operations

## Troubleshooting

Common issues and solutions:

1. Database Connection Issues:
   - Ensure PostgreSQL container is running
   - Check database credentials
   - Verify network connectivity between containers

2. Wikipedia API Issues:
   - Check internet connectivity
   - Verify API rate limits
   - Ensure proper error handling

## License

MIT License - feel free to use this project for any purpose.