import streamlit as st
import yaml
from code_editor import code_editor
from glob import glob
from PIL import Image
import os


def read_in_config(page_num: int) -> dict:
    """Load all details for the pages from yaml file and return them as dict"""
    with open("ressources/config.yaml", "r", encoding="utf-8") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    conf = {}
    conf["help_menu"] = config["help_menu"]
    conf["page_title"] = config["page_title"]
    conf["page_icon"] = config["page_icon"]
    conf["greeting"] = config[f"page{page_num}"]["greeting"]
    conf["title"] = config[f"page{page_num}"]["title"]
    conf["text"] = config[f"page{page_num}"]["text"]
    conf["image"] = config[f"page{page_num}"]["image"]
    try:
        conf["audio"] = config[f"page{page_num}"]["audio"]
    except:
        conf["audio"] = ""
    conf["question"] = config[f"page{page_num}"]["question"]
    try:
        conf["current_page_password"] = config[f"page{page_num - 1}"]["answer"].lower()
    except:
        conf["current_page_password"] = ""
    return conf


def setup_page(config: dict):
    """Page styling"""
    st.set_page_config(
        page_title=config["page_title"],
        page_icon=config["page_icon"],
    )
    st.markdown(
        r"""
        <style>
        .stAppDeployButton {
                visibility: hidden;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def setup_session_states(page_num: int, is_start: bool):
    """Initialize the session states and return if `has_access` and `is_solved`"""
    if f"page{page_num}_access" not in st.session_state:
        if is_start:  # the first page has no password and is always accessible
            st.session_state[f"page{page_num}_access"] = True
        else:
            st.session_state[f"page{page_num}_access"] = False

    if f"page{page_num}_solved" not in st.session_state:
        st.session_state[f"page{page_num}_solved"] = False

    if "is_greeted" not in st.session_state:
        st.session_state["is_greeted"] = False

    return (
        st.session_state[f"page{page_num}_access"],
        st.session_state[f"page{page_num}_solved"],
    )


def check_access_right(config: dict, page_num: int) -> bool:
    """Ask for a password and return if it is correct"""
    password = st.text_input("Enter password", type="password").lower()
    if password == config["current_page_password"]:
        st.session_state[f"page{page_num}_access"] = True
        return True
    else:
        return False


def show_content(config: dict):
    """Render the main part of the page"""
    st.title(config["title"])
    st.markdown(config["text"], unsafe_allow_html=True)
    if os.path.exists(config["image"]):
        st.image(Image.open(config["image"]), width=500)
    else:
        st.markdown(config["image"], unsafe_allow_html=True)
    if config["audio"] != "":
        audio_file = open(config["audio"], "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/ogg")
    st.markdown(config["question"], unsafe_allow_html=True)


@st.dialog("Some helpful explanations")
def show_help_menu(config: dict):
    """Add the helping explanations from the config.yaml to the sidebar"""
    st.markdown(config["help_menu"], unsafe_allow_html=True)


@st.dialog("Herzlich willkommen")
def greetings():
    """A pop up dialog that greets the users"""
    st.image(Image.open("ressources/cover.png"), width=450)
    st.markdown("## 🎄 Data Analytics @ Technik 🎅")
    st.markdown(
        "## 🎁 <span style='color:red'>Weihnachts</span><span style='color:green'>special</span> <span style='color:red'>2024</span> 🍬",
        unsafe_allow_html=True,
    )


def get_named_page_renderer(name, page_num, is_start, is_end):
    """
    Configures the main page rendering function and renames it.
    For st.Pages() to work with functions, each page needs an individual function.
    Using this hacky factory-like construct lets us define all pages purely in the config.yaml
    and generate an individual function per page dynamically.
    """

    def render_page():
        """
        The main function.

        It
        - checks for a password (and doesn't if it was correctly given)
        - displays the content
        - checks the proposed solution (and doesn't if the correct solution was already given)
        - displays the solution and the password for the next page if the quizz was solved
        """

        config = read_in_config(page_num)

        setup_page(config)

        has_access, is_solved = setup_session_states(page_num, is_start)

        if not has_access:
            st.markdown(config["greeting"], unsafe_allow_html=True)
            has_access = check_access_right(config, page_num)

        if has_access:
            show_content(config)

        if is_start:  # Display a greeting dialog
            if not st.session_state["is_greeted"]:
                greetings()
                st.session_state["is_greeted"] = True

        if is_end:  # The last page doesn't have a quizz and a solution
            if has_access:
                st.balloons()
                st.snow()

        if st.sidebar.button("Help"):
            show_help_menu(config)

    render_page.__name__ = name
    render_page.__qualname__ = name
    return render_page


def render_admin_page():
    st.title("Admin Area")
    st.markdown("**This is not part of the game**")
    st.markdown("# ")

    password = st.text_input("Password", type="password")
    if password == "ei123":

        config_selection = st.selectbox(
            "Select Config:", options=glob("ressources/*.yaml")
        )

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
