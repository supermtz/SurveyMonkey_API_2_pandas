# Import the API2Pandas class
from src.api_2_pandas import API2Pandas
from pandas import DataFrame

# Import API token from .env file
# Note: The .env file should be in the top of the project directory
#       and should contain a line like this (without the quotes):
#       "API_TOKEN=your_api_token"
#       After the API_TOKEN is set, rerun ´pipenv shell´ to import it. 
#       The .env file should not be committed to the repository.
import os
API_TOKEN = os.environ['API_TOKEN']

# Create an instance of the API2Pandas class with the API token
pm = API2Pandas(API_TOKEN)

# Search for surveys (you can use the search_str parameter to search for a specific survey)
# This method saves the results within the class instance,
# however it also returns it as a list that you can use in your code.
surveys = pm.search_surveys()

# This command runs the actual API call to get the data
# from the survey into a pandas dataframe
# Like the one above, this method saves the results within the class instance,
# however it also returns it as a pandas dataframe that you can use in your code.
dfs = pm.run()

# dfs is a dictionary with the survey ids as keys and the dataframes as values
# You can access the dataframes like this:
first_survey: DataFrame = dfs[surveys[0]]

# Let's print the first survey
print(first_survey)