import requests
import consts as c

class GoogleSearchAPI:
    """
    A class representing a custom Google search engine.

    The class contains properties key and engine_id, which represent
    the API key, and custom search engine ID, respectively. The class contains
    methods to generate search queries and to return search results of a 
    query.
    """

    def __init__(self, key, engine_id):
        """
        Creates a new GoogleSearchAPI object.

        Parameter key: The API key used in the Google Search.
        Precondition: key is a String object representing a valid API key.

        Parameter engine_id: The ID of the Custom Google search engine.
        Precondition: engine_id is a String object representing a 
        valid search engine engine ID.
        """
        self.key = key
        self.id = engine_id
                

    def search(self):
        """
        Searches google for terms as per user preferences in consts.py.

        Uses the list of terms from generate urls to search google until
        the daily free API request limit is reached. Records client profiles
        in a pandas DataFrame that includes the page Title, Url, and Snippets.
        After using a search query from terms, it records it so it doesnt get
        used again later. As it compiles the list of clients, the method checks 
        for and removes any previously indexed profiles from the DataFrame. The 
        method stops when it encounters an error from the API, either returning
        the error code, or in the case of the API request limit filling up, it
        returns a message signaling that.

        Returns: A list of length 2 where the first element is a pandas DataFrame
        that contains new profile information, and the second element is an error 
        message, if one occured.
        
        Parameter terms: The list of terms used to search Google.
        Precondition: terms is made up of Strings that represent Google 
        search terms.
        """
        # Set up DataFrame
        brk = False
        er_msg = ""
        num_results = 2
        start = 1
        while num_results > start:
            url = f"https://www.googleapis.com/customsearch/v1?key="
            url = url + f"{self.key}&cx={self.id}&q=site:linkedin.com {c.FIRST_NAME, c. LAST_NAME, c.LOCATION}&start={start}"
            data = requests.get(url).json()
            
            # Look for error
            if data.get("error") is not None:
                brk = True
                error = data.get("error")
                code = error.get("code")
                break

            # Get search result data
            search_info = data.get("searchInformation")
            if search_info is not None:
                total_results = search_info.get("totalResults")
                if total_results is not None:
                    num_results = min(2, int(total_results))
            start +=1

            if data.get("items") is not None:
                links = data.get("items")[0].get("link")

            # Index search query
            if brk:
                if code != 429:
                    er_msg = "Google API Error " + str(code)
                else:
                    er_msg = "API request limit reached."
                break


        lst = [links, er_msg]
        return lst
