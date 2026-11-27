import chromadb
import hashlib
from intelligence.agents.rag.embeddings import embed_texts


client = chromadb.PersistentClient(
    path="intelligence/rag/chroma_db"
)

collection = client.get_or_create_collection(
    name="crypto_news",
    metadata={"hnsw:space": "cosine"},
)


def store_articles(articles: list[dict]):
    if not articles:
        return

    documents = [
        article["title"] + ". " + article["summary"]
        for article in articles
    ]

    embeddings = embed_texts(documents)

    ids = [
        hashlib.sha256(article["link"].encode()).hexdigest()
        for article in articles
    ]

    metadatas = [
        {
            "title": article["title"],
            "link": article["link"],
            "published": article["published"],
        }
        for article in articles
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def retrieve_articles(query: str, top_k: int = 5) -> list[dict]:
    count = collection.count()

    if count == 0:
        return []

    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, count),
    )

    articles = []

    for i, document in enumerate(results["documents"][0]):
        articles.append({
            "content": document,
            "metadata": results["metadatas"][0][i],
            "similarity": 1 - results["distances"][0][i],
        })

    return articles


