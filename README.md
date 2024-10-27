# Scavenger Hunt

A lightweight Python / Streamlit application that let's you easily set up a digital scavenger hunt.

## Description
The app is build as `streamlit` multipage app.
The entry point is `app.py`. 
All other pages are defined in the `ressources.yaml`-file.

The main code is in `utils.py`. Here the function `render_page()` does the work.
It is returned by the function `get_named_page_renderer()`, which configures and renames `render_page()`.
This way, streamlits `st.Pages()` function gets one individual function per page.
Every page (except for the very first one) needs a password. 
The password for each next page is given to the user, if a quizz is solved correctly.

## Configuration
Each page can be configured in the file `ressources/config.yaml`.

The following options are given:
```yaml
page0:
  is_start: True, or False  # True for the first page, else False
  is_end: True, or False  # True for the last page, else False
  title: "A title"  # rendered as st.title()
  text: "Some markdown"   # rendered as st.markdown(unsafe_allow_html=True)
  image: "More markdown (I like to insert an image here)"  # rendered as st.markdown(unsafe_allow_html=True)
  question: "More markdown (I like to put my question here)"  # rendered as st.markdown(unsafe_allow_html=True)
  answer: "Answer"  # a string that is matched excatly, to get the next pages password
  next_page_password: "Secret"  # the next pages password
```

### <span style='color:#ea0a8e'>IMPORTANT</span> - Naming convention in the `yaml`
**Keep in mind** that the pages are **not implemented as linked list**!
When you call `get_named_page_renderer(name, page_num, is_start=False, is_end=False)` for a page, you give it the current page number.
- The script searches for a section called *page\<NUMBER\>:*
- The password for the current page is given in `next_page_password` of the block *page\<NUMBER - 1\>:*
**Just name the pages:** *page0*, *page1*, *page2*, ... in sequential order.


## Install
- create an environment
- activate it
- pip install streamlit pyyaml streamlit_code_editor


## Run locally
`streamlit run app.py --theme.base="dark" --theme.primaryColor="#ea0a8e"`


## Run in `docker`
There is a little hack here.

In order to make the config files persistent, the `src/ressources` folder is deleted from the image and the actual ressources folder is mounted into the container in place.
- **Build:** `docker build -t scavenger-hunt .`
- **Run:** `docker run --detach -v ~/scavenger-hunt/src/ressources:/app/src/ressources:rw -p 8501:8501 --user $(id -u):$(id -g) scavenger-hunt`
- **Access:** `http://localhost:8501`