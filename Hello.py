import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome 👋")

col1, col2 = st.columns(2, gap="large", border=True)
col1.subheader("Voice annotations")
col2.subheader("Abreviations used")

with col1:
    st.markdown("""
    |annotation|corresponding voice|
    |:----:|:---:|
    |$x$|note with voice annotation|
    |$.$|rest|
    |$u$|upper voice|
    |$b$|bass voice|
    |$B$|opposite stems-notes : bass voice|
    |$m$|middle voice|
 """)


with col2:
        st.markdown("""
    |abbreviations|meaning|
    |:----:|:---:|
    |BM|binary meter|
    |TM|ternary meter|
    |♪♪|group of two 8th within a same beat in binary|
    |♬♬|group of four 16th within a same beat in binary|
    |♪♪♪|group of three 8th within a same beat in ternary|
    """)

st.markdown("""
            <style>
                .fancy-link {
                    font-size: 20px;
                    color: #1a73e8;
                    text-decoration: none;
                    transition: color 0.3s ease, transform 0.3s ease;
                }

                .fancy-link:hover {
                    color: #d93025;
                    transform: scale(1.05);
                }
                </style>
                
             <div style="text-align: center ;margin-top: 20px;"">
                <a href="https://www.dezrann.net/explore/telemann-flute-fantaisies" target="_blank" class="fancy-link"> 
                🔗 Annotated corpus on <strong title="Interacting with Annotated and Synchronized Music Corpora 
                on the Dezrann Web Platform, C. Ballester and al., TISMIR, 2025">Dezrann</strong></a>
             </div>
             """, unsafe_allow_html=True)
