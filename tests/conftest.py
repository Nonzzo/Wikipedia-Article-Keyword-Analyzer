# tests/conftest.py

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool
from wiki_crawler import Base, WikiArticle

@pytest.fixture(scope="session")
def engine():
    """Create a test database engine that will be used for all tests."""
    # Use in-memory SQLite for testing
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="function")
def db_session(engine):
    """Create a new database session for a test."""
    connection = engine.connect()
    transaction = connection.begin()
    session_factory = sessionmaker(bind=connection)
    session = scoped_session(session_factory)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def sample_articles():
    """Provide sample article data for testing."""
    return [
        {
            'title': 'Test Article 1',
            'content': 'This is a test article about python programming.',
            'expected_python_count': 1,
            'expected_test_count': 1
        },
        {
            'title': 'Test Article 2',
            'content': 'Another article mentioning python twice. Python is great!',
            'expected_python_count': 2,
            'expected_test_count': 0
        },
        {
            'title': 'Test Article 3',
            'content': 'This article has no relevant keywords.',
            'expected_python_count': 0,
            'expected_test_count': 0
        }
    ]

@pytest.fixture
def populated_db(db_session, sample_articles):
    """Create a database populated with sample articles."""
    for article_data in sample_articles:
        article = WikiArticle(
            title=article_data['title'],
            content=article_data['content']
        )
        db_session.add(article)
    db_session.commit()
    return db_session

@pytest.fixture
def mock_wikipedia(monkeypatch):
    """Mock Wikipedia API responses."""
    class MockWikipediaPage:
        def __init__(self, title, content):
            self.title = title
            self.content = content

    def mock_random(*args, **kwargs):
        return "Mock Article Title"

    def mock_page(*args, **kwargs):
        return MockWikipediaPage(
            title="Mock Article Title",
            content="This is mock content for testing purposes."
        )

    monkeypatch.setattr('wikipedia.random', mock_random)
    monkeypatch.setattr('wikipedia.page', mock_page)

@pytest.fixture
def env_setup():
    """Setup environment variables for testing."""
    original_env = dict(os.environ)
    os.environ.update({
        'DATABASE_HOST': 'localhost',
        'DATABASE_PORT': '5432',
        'DATABASE_NAME': 'test_wikipedia',
        'DATABASE_USER': 'test_user',
        'DATABASE_PASSWORD': 'test_password',
        'ANALYSIS_KEYWORD': 'test'
    })
    
    yield
    
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture(autouse=True)
def cleanup_after_test(db_session):
    """Clean up the database after each test."""
    yield
    db_session.query(WikiArticle).delete()
    db_session.commit()