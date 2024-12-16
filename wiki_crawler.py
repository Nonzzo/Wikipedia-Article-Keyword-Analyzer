import os
import sys
import time
import random
import wikipedia
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from urllib.parse import quote_plus

# Database Configuration
DB_HOST = os.getenv('DATABASE_HOST', 'localhost')
DB_PORT = os.getenv('DATABASE_PORT', '5432')
DB_NAME = os.getenv('DATABASE_NAME', 'wikipedia')
DB_USER = os.getenv('DATABASE_USER', 'postgres')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD', 'mysecretpassword')

# Keyword to analyze (can be set via environment variable)
KEYWORD = os.getenv('ANALYSIS_KEYWORD', 'default')

# Construct the database URL
DB_URL = f'postgresql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# SQLAlchemy Setup
Base = declarative_base()

def wait_for_database():
    """Wait for database to be ready."""
    max_attempts = 30
    delay_between_attempts = 2
    
    for attempt in range(max_attempts):
        try:
            engine = create_engine(DB_URL, connect_args={'connect_timeout': 3})
            # Attempt to connect
            with engine.connect() as connection:
                print("Database connection successful!")
                return True
        except OperationalError:
            print(f"Waiting for database (attempt {attempt + 1}/{max_attempts})...")
            time.sleep(delay_between_attempts)
    
    print("Could not connect to the database.")
    return False

def create_tables(engine):
    """Create database tables."""
    Base.metadata.create_all(engine)
    print("Database tables created successfully.")

class WikiArticle(Base):
    __tablename__ = 'wiki_articles'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    content = Column(Text)

def fetch_random_articles(num_articles=10):
    """Fetch random Wikipedia articles."""
    articles = []
    for _ in range(num_articles):
        try:
            # Get a random Wikipedia page
            random_page = wikipedia.random(pages=1)
            page = wikipedia.page(random_page)
            articles.append({
                'title': page.title,
                'content': page.content
            })
        except Exception as e:
            print(f"Error fetching article: {e}")
    return articles

def store_articles(articles):
    """Store articles in the database."""
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        for article in articles:
            # Check if article already exists
            existing = session.query(WikiArticle).filter_by(title=article['title']).first()
            if not existing:
                wiki_article = WikiArticle(
                    title=article['title'],
                    content=article['content']
                )
                session.add(wiki_article)
        session.commit()
        print(f"Stored {len(articles)} articles in the database.")
    except Exception as e:
        session.rollback()
        print(f"Error storing articles: {e}")
    finally:
        session.close()

def analyze_keyword_frequency(keyword):
    """Analyze keyword frequency across stored articles."""
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        articles = session.query(WikiArticle).all()
        total_occurrences = sum(
            article.content.lower().count(keyword.lower()) 
            for article in articles
        )
        
        print(f"\nKeyword Analysis Results:")
        print(f"Keyword '{keyword}' appears {total_occurrences} times across {len(articles)} articles.")
        
        # Detailed breakdown
        print("\nDetailed Breakdown:")
        for article in articles:
            count = article.content.lower().count(keyword.lower())
            if count > 0:
                print(f"- {article.title}: {count} occurrences")
        
    except Exception as e:
        print(f"Error analyzing keyword: {e}")
    finally:
        session.close()

def main():
    """Main function to orchestrate the Wikipedia crawling and analysis process."""
    # Wait for database connection
    if not wait_for_database():
        return

    # Create engine and tables
    engine = create_engine(DB_URL)
    create_tables(engine)

    # Fetch and store random articles
    print("Fetching 10 random Wikipedia articles...")
    articles = fetch_random_articles()
    store_articles(articles)

    # Analyze keyword
    print(f"\nAnalyzing keyword: {KEYWORD}")
    analyze_keyword_frequency(KEYWORD)

if __name__ == "__main__":
    main()