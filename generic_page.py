import streamlit as st
import yaml


def read_in_config(page_num: int) -> dict:
    """Load all details for the pages from yaml file and return them as dict"""
    with open("ressources/config.yaml", "r", encoding="utf-8") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    conf = {}
    conf["help_menu"] = config["help_menu"]
    conf["page_title"] = config["page_title"]
    conf["page_icon"] = config["page_icon"]
    conf["title"] = config[f"page{page_num}"]["title"]
    conf["text"] = config[f"page{page_num}"]["text"]
    conf["image"] = config[f"page{page_num}"]["image"]
    conf["question"] = config[f"page{page_num}"]["question"]
    conf["solution"] = config[f"page{page_num}"]["answer"]
    try:
        conf["current_page_password"] = config[f"page{page_num - 1}"][
            "next_page_password"
        ]
    except:
        conf["current_page_password"] = ""
    conf["next_page_password"] = config[f"page{page_num}"]["next_page_password"]
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

    return (
        st.session_state[f"page{page_num}_access"],
        st.session_state[f"page{page_num}_solved"],
    )


def check_access_right(config: dict, page_num: int) -> bool:
    """Ask for a password and return if it is correct"""
    password = st.text_input("Enter password", type="password")
    if password == config["current_page_password"]:
        st.session_state[f"page{page_num}_access"] = True
        return True
    else:
        return False


def show_content(config: dict):
    """Render the main part of the page"""
    st.title(config["title"])
    st.markdown(config["text"], unsafe_allow_html=True)
    st.markdown(config["image"], unsafe_allow_html=True)
    st.markdown(config["question"], unsafe_allow_html=True)


def check_for_solution(config: dict, page_num: int) -> bool:
    """Check if the proposed solutionis correct and return if it is correct"""
    proposed_solution = st.text_input(" ")
    if proposed_solution == config["solution"]:
        st.session_state[f"page{page_num}_solved"] = True
        return True
    else:
        return False


def show_solved_part(config: dict, page_num: int):
    """Shows the solution and the password for the next page"""
    st.markdown(
        f"""
        ---

        <span style='color:#ea0a8e'>{config["solution"]}</span> is correct, the password to the next side is:
        <br>
        <span style='color:#ea0a8e'>**{config["next_page_password"]}**</span>
        """,
        unsafe_allow_html=True,
    )


@st.dialog("Some helpful explanations")
def show_help_menu(config: dict):
    """Add the helping explanations from the config.yaml to the sidebar"""
    st.markdown(config["help_menu"], unsafe_allow_html=True)


def render_page(page_num, is_start=False, is_end=False):
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
        has_access = check_access_right(config, page_num)

    if has_access:
        show_content(config)

    if is_end:  # The last page doesn't have a quizz and a solution
        if has_access:
            st.balloons()
            st.snow()
    else:
        if (has_access) and (not is_solved):
            is_solved = check_for_solution(config, page_num)
        if (has_access) and (is_solved):
            show_solved_part(config, page_num)

    if st.sidebar.button("Help"):
        show_help_menu(config)
