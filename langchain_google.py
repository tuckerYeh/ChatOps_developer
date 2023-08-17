from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper

GOOGLE_CSE_ID = "516d8ea8163e2469f"
GOOGLE_API_KEY = "AIzaSyAqwCRgdwm9_5xbAAjHBR5yr2fniZVZNKM"

class GoogleSearchWeb:
    search = GoogleSearchAPIWrapper(google_api_key=GOOGLE_API_KEY, google_cse_id=GOOGLE_CSE_ID)

    def __init__(self):
        self.search_tool = Tool(
            name="Google Search",
            description="Search Google for recent results.",
            func=self.search.run
        )

if __name__ == '__main__':
    google_search = GoogleSearchWeb()
    results = google_search.search_tool.run("誰是中華開發金控董事長")
    print(results)
