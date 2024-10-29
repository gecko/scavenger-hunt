# Run with
# streamlit run Welcome.py --theme.base="dark" --theme.primaryColor="#ea0a8e"

from utils import get_named_page_renderer, render_admin_page
import yaml
import re
import streamlit as st


with open("ressources/config.yaml", "r", encoding="utf-8") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


# Go through the config and create for each ``page*`` section a page in the website
game_pages = []
for key in config.keys():
    if re.match(r"^page\d+", key):
        # Get page rendering funktion
        render_page = get_named_page_renderer(
            "render_" + key,
            page_num=int(key[4:]),
            is_start=config[key]["is_start"],
            is_end=config[key]["is_end"],
        )
        # Create page
        game_pages.append(
            st.Page(
                render_page,
                title=config[key]["title"],
                icon=":material/arrow_forward_ios:",
            )
        )

# Add a navigation with two sections
pg = st.navigation(
    {
        "Scavenger Hunt": game_pages,
        "Admin": [
            st.Page(render_admin_page, title="Edit Puzzles", icon=":material/settings:")
        ],
    }
)

pg.run()
