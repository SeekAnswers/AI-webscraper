import streamlit as st
from scrape import (
    scrape_website, 
    split_dom_content, 
    clean_body_content, 
    extract_body_content,
)
from parse import parse_with_ollama

# Setting Up Streamlit Interface
st.title('SeekAnswers AI Web Scraper')
url = st.text_input('Enter a Website URL:')

# Scraping Website Content
if st.button('Scrape Site'):
    if url:
        # Automatically add 'https://' if it's not included
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        
        st.write('Scraping the website')

        result = scrape_website(url)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)

        st.session_state.dom_content = cleaned_content

        with st.expander('View DOM Content'):
            st.text_area('DOM content', cleaned_content, height=300)

# Parsing DOM Content    
if 'dom_content' in st.session_state:
    parse_description = st.text_area('Describe what you want to parse?')

    if st.button('Parse Content'):
        if parse_description:
            st.write('Parsing the content')

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)
