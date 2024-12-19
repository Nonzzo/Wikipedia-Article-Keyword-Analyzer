# Using fixtures from conftest.py in test_wiki_crawler.py

def test_store_articles(db_session, sample_articles):
    # db_session and sample_articles come from conftest.py
    store_articles(sample_articles)
    stored = db_session.query(WikiArticle).all()
    assert len(stored) == len(sample_articles)

def test_with_mocked_wikipedia(mock_wikipedia):
    # mock_wikipedia comes from conftest.py
    articles = fetch_random_articles()
    assert articles[0]['title'] == "Mock Article Title"