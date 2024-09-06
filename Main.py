# import streamlit as st
# from streamlitimage import findimgae
# from page1 import page1
# from page2 import page2
# from page3 import page3

# def main():
#     # Initialize session state if not already present
#     if 'logged_in' not in st.session_state:
#         st.session_state.logged_in = False

#     if not st.session_state.logged_in:
#         login()
#     else:
#         st.sidebar.title("Navigation")
#         page = st.sidebar.radio("Go to", ["Page 1", "Page 2", "Page 3"])
        
#         if page == "Page 1":
#             page1()
#         elif page == "Page 2":
#             page2()
#         elif page == "Page 3":
#             page3()

# if __name__ == "__main__":
#     main()
