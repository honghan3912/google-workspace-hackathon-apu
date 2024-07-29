import webbrowser
import streamlit as st
import pandas as pd
from pymongo import MongoClient
from io import BytesIO
import fitz  # PyMuPDF
from docx import Document
from PIL import Image

# Google Apps Script URL
SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbxfKM-cjUvtzzbgA5pu18zQ8Di8hNRvhtO_WFcpld1i/dev'  # Replace with your actual URL

# MongoDB connection
client = MongoClient('mongodb+srv://teohkailiang03:mongod85a67be3f@freecluster.avglmsx.mongodb.net/?retryWrites=true&w=majority&appName=FreeCluster')
db = client['ResumeDatabase']
collection = db['ResumeCollection']

def insert_document(document):
    result = collection.insert_one(document)
    st.write(f"Inserted document ID: {result.inserted_id}")

def process_txt(file):
    text = file.read().decode("utf-8")
    document = {"content": text}
    insert_document(document)

def process_md(file):
    text = file.read().decode("utf-8")
    document = {"content": text}
    insert_document(document)

def process_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    document = {"content": text}
    insert_document(document)

def process_docx(file):
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    document = {"content": text}
    insert_document(document)

def process_image(file):
    img = Image.open(file)
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format=img.format)
    img_byte_arr = img_byte_arr.getvalue()
    document = {"image": img_byte_arr}
    insert_document(document)

def handle_file_upload(file):
    file_extension = file.name.split('.')[-1].lower()
    
    if file_extension == 'txt':
        process_txt(file)
    elif file_extension == 'md':
        process_md(file)
    elif file_extension == 'pdf':
        process_pdf(file)
    elif file_extension == 'docx':
        process_docx(file)
    else:
        st.error("Unsupported file type")

def display_data():
    documents = list(collection.find())
    if documents:
        for doc in documents:
            st.write(f"Document ID: {doc['_id']}")
            if 'image' in doc:
                st.image(doc['image'])
            else:
                st.json(doc)
    else:
        st.write("No documents found in the collection.")


def send_mail(): 
    webbrowser.open(SCRIPT_URL)

