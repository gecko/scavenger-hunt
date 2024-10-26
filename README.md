# Scavenger Hunt

A lightweight Python / Streamlit application that let's you easily set up a digital scavenger hunt.

## Description
The app is build as `streamlit` multipage app.
The entry point is `Welcome.py`. 
All other pages are placed in the `pages` folder.

The main code is in `generic_page.py`. Here the function `render_page()` does the work.
Every page (except for the very first one) needs a password. 
The password for each next page is given to the user, if a quizz is solved correctly.

## Configuration
Each page can be configured in the file `ressources/config.yaml`.

The following options are given:
```yaml
page0:
  title: "A title"  # rendered as st.title()
  text: "Some markdown"   # rendered as st.markdown(unsafe_allow_html=True)
  image: "More markdown (I like to insert an image here)"  # rendered as st.markdown(unsafe_allow_html=True)
  question: "More markdown (I like to put my question here)"  # rendered as st.markdown(unsafe_allow_html=True)
  answer: "Answer"  # a string that is matched excatly, to get the next pages password
  next_page_password: "Secret"  # the next pages password
```

### <span style='color:#ea0a8e'>IMPORTANT</span> - Naming convention in the `yaml`
**Keep in mind** that the pages are **not implemented as linked list**!
When you call `render_page(page_num, is_start=False, is_end=False)` for a page, you give it the current page number.
- The script searches for a section called *page\<NUMBER\>:*
- The password for the current page is given in `next_page_password` of the block *page\<NUMBER - 1\>:*


## ToDo
- Admin area to edit the `yaml` template.
- Do not store the password, but a hash of it.
- Add "hash my password" functionality to the admin area.


## Install
- create an environment
- activate it
- pip install streamlit pyyaml


## Run locally
`streamlit run Welcome.py --theme.base="dark" --theme.primaryColor="#ea0a8e"`


## Run in `docker`
- **Build:** `docker build -t scavenger-hunt .`
- **Run:** `docker run --detach -v /path/on/host:/app/ressources -p 8501:8501 scavenger-hunt`
- **Access:** `http://localhost:8501`