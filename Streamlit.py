import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Library Management", layout="wide")
st.title("📚 Library Management System (SQLite)")

menu = ["View Books", "Add Book", "Delete Book"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "View Books":
    st.subheader("Book Catalog")
    try:
        response = requests.get(f"{API_URL}/books")
        if response.status_code == 200:
            books = response.json()
            if books:
                st.dataframe(books, use_container_width=True)
            else:
                st.info("No books found in the database.")
        else:
            st.error("Failed to fetch books.")
    except Exception as e:
        st.error(f"Error connecting to backend API: {e}")

elif choice == "Add Book":
    st.subheader("Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Sci-Fi", "Biography", "Technology"])
        available = st.checkbox("Available", value=True)
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            payload = {
                "title": title,
                "author": author,
                "genre": genre,
                "available": available
            }
            res = requests.post(f"{API_URL}/books", json=payload)
            if res.status_code == 200:
                st.success(f"Book '{title}' added to database!")
            else:
                st.error("Could not add book.")

elif choice == "Delete Book":
    st.subheader("Delete a Book")
    book_id_to_delete = st.number_input("Enter Book ID to Delete", min_value=1, step=1)
    if st.button("Delete"):
        res = requests.delete(f"{API_URL}/books/{book_id_to_delete}")
        if res.status_code == 200:
            st.success(f"Book ID {book_id_to_delete} removed successfully!")
        else:
            st.error(f"Error: {res.json().get('detail', 'Could not delete book')}")
