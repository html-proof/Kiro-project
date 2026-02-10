def build_youtube_search_query(query: str, language: str = None, type_filter: str = None) -> str:
    search_query = query
    
    if type_filter:
        type_keywords = {
            "romantic": "romantic love songs",
            "party": "party dance songs",
            "chill": "chill relaxing music",
            "workout": "workout gym music",
            "sleep": "sleep calm music",
            "sad": "sad emotional songs",
            "devotional": "devotional spiritual songs",
            "motivational": "motivational inspiring songs"
        }
        search_query = f"{type_keywords.get(type_filter, query)} {query}"
    
    if language:
        search_query = f"{search_query} {language}"
    
    return search_query
