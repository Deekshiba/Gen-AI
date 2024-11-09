import numpy as np
import gradio as gr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SmartSearch:
    def __init__(self, courses):
        self.courses = courses
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform([course['description'] for course in self.courses])

    def search(self, user_query):
        # Transform the user query into the same TF-IDF space
        query_vector = self.vectorizer.transform([user_query])
        
        # Calculate cosine similarity between the query and course descriptions
        cosine_similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get the indices of the top 5 most similar courses
        relevant_indices = np.argsort(cosine_similarities)[-5:][::-1]
        
        # Return the top 5 relevant courses
        return [(self.courses[i]['title'], cosine_similarities[i]) for i in relevant_indices]

# Example course data (replace this with your scraped data)
courses = [
    {'title': 'Data Science for Beginners', 'description': 'Learn the basics of data science, including data analysis and visualization.'},
    {'title': 'Machine Learning Basics', 'description': 'Introduction to machine learning concepts and algorithms.'},
    {'title': 'Deep Learning with Python', 'description': 'Explore deep learning techniques using Python and TensorFlow.'},
    {'title': 'Statistics for Data Science', 'description': 'Understand statistical methods and their applications in data science.'},
    {'title': 'Data Visualization Techniques', 'description': 'Learn how to visualize data effectively using various tools.'},
]

# Create an instance of the SmartSearch class
smart_search = SmartSearch(courses)

# Define the Gradio interface function
def search_courses(user_query):
    results = smart_search.search(user_query)
    return [f"Title: {course[0]}, Score: {course[1]:.4f}" for course in results]

# Create a Gradio interface
iface = gr.Interface(
    fn=search_courses,
    inputs="text",
    outputs="list",
    title="Smart Course Search",
    description="Enter a query to find relevant free courses on Analytics Vidhya."
)

# Launch the Gradio app
iface.launch()