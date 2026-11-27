from intelligence.agents.rag.ingestion import ingest_news
from intelligence.agents.rag.vector_store import retrieve_articles

count = ingest_news()
print(f"Indexed {count} articles")

results = retrieve_articles(
    "Bitcoin institutional adoption and market risks",
    top_k=5,
)

for article in results:
    print("\n", article["metadata"]["title"])
    print("Similarity:", article["similarity"])
    print("Link:", article["metadata"]["link"])