import pandas as pd
import unidecode


def fix_accented_characters(text):
    """
    Function to fix accented characters in a string.
    It first tries to decode the text using utf-8 and then transliterates
    to replace non-ASCII characters with their closest ASCII equivalent.
    """
    try:
        # Attempt to decode using utf-8
        text = text.encode('latin1').decode('utf-8')
    except UnicodeError:
        pass  # If the encoding is not latin1, proceed with the original text
    
    # Transliterate to replace non-ASCII characters
    return unidecode.unidecode(text)

import streamlit as st
import pandas as pd

# Set page configuration to wide layout
st.set_page_config(layout="wide")


# Function to load the data
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Streamlit app layout
def main():


    st.image("static/logo.png", width=200) 

    


    st.title("Player Feelings")

    # Load the data
    data = load_data("DATA/Corrected.csv")
    unique_teams = sorted(data['Team'].dropna().unique())


    # Search by team or player name
    search_type = st.radio("Search by", ('Team', 'Player Name'))

    if search_type == 'Team':
        # Add a default option to your list of teams
        team_options = ["Select a Team"] + unique_teams
        team_name = st.selectbox("Select Team", team_options)

        # Check if the user has selected a team other than the default
        if team_name != "Select a Team":
            results = data[data['Team'] == team_name]
            st.write(results)



    elif search_type == 'Player Name':
        player_name = st.text_input("Enter Player Name")
        if player_name:
            results = data[data['Nome'].str.contains(player_name, case=False, na=False)]
            st.write(results)


# Load the file to examine its contents
file_path = 'RAW/Admin Page.csv'
data = pd.read_csv(file_path)

# Apply the function to all string columns in the dataframe
for col in data.select_dtypes(include=['object']).columns:
    data[col] = data[col].apply(fix_accented_characters)

# Save the corrected file
corrected_file_path = 'DATA/Corrected.csv'
data.to_csv(corrected_file_path, index=False)


if __name__ == "__main__":
    main()
