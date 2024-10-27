import streamlit as st
from code_editor import code_editor
from glob import glob


st.title("Admin Area")
st.markdown("**This is not part of the game**")
st.markdown("# ")

password = st.text_input("Password", type="password")
if password == "ei123":

    config_selection = st.selectbox("Select Config:", options=glob("ressources/*.yaml"))

    with open(config_selection, "r", encoding="utf8") as f:
        config = f.read()
    response_dict = code_editor(
        config,
        lang="yaml",
        height="700px",
        buttons=[
            {
                "name": "Accept edited text",
                "feather": "Save",
                "hasText": True,
                "alwaysOn": True,
                "commands": ["save-state", ["response", "saved"]],
                "response": "saved",
                "style": {"bottom": "0.46rem", "right": "0.4rem"},
            }
        ],
    )

    st.write("Save as:")
    col1, col2 = st.columns([10, 1])
    file_name = col1.text_input(
        "Save as", value=config_selection, label_visibility="collapsed"
    )
    if col2.button("OK"):
        if response_dict["text"] != "":
            with open(file_name, "w", encoding="utf8") as f:
                f.write(response_dict["text"])
        else:
            st.warning(
                "You need to **accept the text** from the editor first, before saving it."
            )
