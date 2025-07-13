import requests
import os

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def search_duckduckgo(query):
    """
    Uses DuckDuckGo Instant Answer API for quick facts and related topics.
    """
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        abstract = data.get("AbstractText")
        if abstract:
            return abstract
        elif data.get("RelatedTopics"):
            return ", ".join([topic.get("Text", "") for topic in data["RelatedTopics"][:3]])
        else:
            return "No relevant results found on DuckDuckGo."
    except Exception as e:
        return f"DuckDuckGo search error: {str(e)}"


def search_tavily(query):
    """
    Uses Tavily Web Search API for in-depth search results.
    """
    url = "https://api.tavily.com/search"
    headers = {"Authorization": f"Bearer {TAVILY_API_KEY}"}
    data = {
        "query": query,
        "search_depth": "advanced"
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        results = response.json().get("results", [])
        if not results:
            return "No search results found from Tavily."
        return "\n\n".join([f"🔗 {r['title']}\n{r['url']}\n{r['content']}" for r in results[:3]])
    except Exception as e:
        return f"Tavily search error: {str(e)}"


# Example usage for testing
if __name__ == "__main__":
    print("DuckDuckGo:")
    print(search_duckduckgo("force majeure clause meaning"))

    print("\nTavily:")
    print(search_tavily("non-compete clause enforceability India"))
