# BookKeeperAI

## Overview
BookKeeperAI is a state-of-the-art application designed to mimic the behavior of a librarian using artificial intelligence. The app leverages LangChain, LangGraph, and Azure OpenAI's GPT-4 (o-mini model) to provide users with an interactive and intelligent library management experience. The app is hosted on a Gradio interface for an easy-to-use and visually appealing interface.

## Key Features
- **Search Books:** Users can query the library dataset to search for books by title, category, or other attributes.
- **Rent Books:** Users can rent books directly through the interface. The app checks the availability of the book before completing the rental process.
- **Markdown Responses:** Search results are displayed in an elegant markdown table format for better readability.

--- 

## Tech Stack

**1. LangChain**
LangChain serves as the core framework for building conversational AI agents. It provides the tools and structure to integrate language models, tools, and memory into a single seamless application.

**2. LangGraph**
LangGraph is used to design and manage the application flow, ensuring a modular and scalable architecture for the AI librarian.

**3. Azure OpenAI GPT-4 o-mini**
The AI model behind the app is the powerful Azure OpenAI GPT-4 (o-mini model). This model enables advanced natural language understanding and generation, making interactions with the AI librarian intuitive and human-like.

**4. Gradio**
Gradio is used to create the user interface for the app. It provides a web-based platform where users can interact with the librarian, search books, and manage rentals.

---

## Prerequisites
Before you can run this project, ensure you have the following installed on your system:
- Docker
- Docker Compose
You will also need an Azure OpenAI API Key and a valid library dataset to set up the application.

---

**Getting Started**
Follow the steps below to set up and run the project:

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Set Up Environment Variables
Create a .env file in the root of the project based on the keys provided in the .env-example file.

### 3. Start the Application
Run the following command to start the application using Docker Compose:
```bash
docker-compose up
```
This will build the Docker image, start the container, and host the Gradio interface on http://localhost:9000.

---

## Usage Instructions
1. **Access the Gradio Interface:** Open your web browser and navigate to http://localhost:9000.

2. **Search for Books:**
- Enter a query to search for books. For example:
    - "Show me all fantasy books."
    - "Find books with the title 'Harry Potter'."
- Rent a Book:
    - Once a book is selected, the librarian checks its availability. If available, the book can be rented directly.

---

## API Integration
The app uses the following APIs:

1. **Azure OpenAI API:**
- Handles language model interactions.
- Requires an API key and endpoint configured in the .env file.

2. **Database (SQLite):**
- Manages the library dataset, including books, rentals, and customers.
- Queries are handled dynamically by LangChain tools.

---

## Known Issues & Limitations
- Book Availability: The app assumes each book is a single-copy entity. Multi-copy support is not currently implemented.
- Model Latency: The response time depends on the Azure OpenAI API and may vary.

---

## Future Enhancements
- Add support for creating new customers.
- Extend the librarian's functionality to recommend books based on user preferences.
- Implement user authentication for a personalized library experience.

---

## License
This project is licensed under the MIT License.

---

Enjoy your AI-powered library experience! 📚
