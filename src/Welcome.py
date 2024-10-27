# Run with
# streamlit run Welcome.py --theme.base="dark" --theme.primaryColor="#ea0a8e"

from generic_page import render_page
from streamlit.source_util import get_pages, _on_pages_changed

render_page(page_num=0, is_start=True)

# Add an icon to the admin area
current_pages = get_pages("Welcome.py")
for key, value in current_pages.items():
    if value["page_name"] == "Admin_Area":
        current_pages[key]["icon"] = "🛇"
        _on_pages_changed.send()
