import requests
from bs4 import BeautifulSoup

def scrape_courses(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # List to hold course data
    courses = []

    # Find all course cards (you may need to adjust the selector based on the actual HTML structure)
    for course in soup.find_all('div', class_='course-card'):
        title = course.find('h3').text.strip() if course.find('h3') else 'No Title'
        description = course.find('p').text.strip() if course.find('p') else 'No Description'
        
        # Append the course data to the list
        courses.append({'title': title, 'description': description})

    return courses

# URL of the Analytics Vidhya free courses page
url = 'https://www.analyticsvidhya.com/courses/free-courses/'

# Scrape the courses
course_data = scrape_courses(url)

# Print the scraped course data
for index, course in enumerate(course_data, start=1):
    print(f"Course {index}:")
    print(f"Title: {course['title']}")
    print(f"Description: {course['description']}")
    print("-" * 40)