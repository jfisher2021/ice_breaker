from langchain_tavily import TavilySearch

def get_profile_url_tavily(name: str):
    """Searches for Linkedin or Twitter Profile Page."""
    search = TavilySearch()
    
    # Usar invoke en lugar de __call__
    res = search.invoke({"query": f"Buscame el perfil de linkedin de {name}"})
    return res