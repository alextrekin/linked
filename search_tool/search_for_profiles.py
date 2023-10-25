from search_tool.google_api import GoogleSearchAPI
import consts as c

def run_search():
    """
    Uses Google's search API to search LinkedIn accounts based on preferences.

    Uses preferences to generate a specific search term based on position,
    location, and experience, then uses the Google API to search for the term.
    
    Returns: A list of length 2 where the fist element is a pandas DataFrame 
    containing search results, and the second element is an error message, if one
    occured. 

    Parameter preferences: A dictionary of user search preferences.
    Precondition: preferences is generated by search_for_profiles.load_preferences()
    and is based on a consts.py configuration which follows the rules
    outlined in that file.
    """
    # Generate search terms
    google = GoogleSearchAPI(c.API_KEY, c.SEARCH_ENGINE_ID)
    # Search for list of terms using Google API
    results = google.search()

    return results
