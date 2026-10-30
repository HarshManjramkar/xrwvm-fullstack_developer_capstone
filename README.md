# Cars Dealership - Full Stack Cloud Development Capstone Project

## Project Overview
**Cars Dealership** is a comprehensive, responsive national car retailer web application deployed across microservices in the United States. The platform enables users to search for dealership branches across all 50 states, filter dealerships by location, view real customer reviews accompanied by AI-powered sentiment analysis (positive, neutral, negative), and submit vehicle reviews for visited dealerships.

## Technology Stack & Architecture
- **Frontend**: React.js SPA, HTML5, CSS3, Bootstrap 5, Vite/Webpack
- **Backend Framework**: Python Django 4.2 Web Framework
- **Microservices**:
  - **Dealership & Reviews Service**: Node.js & Express REST API with MongoDB/Mongoose
  - **Sentiment Analyzer Service**: Python Flask microservice utilizing NLTK SentimentIntensityAnalyzer
  - **Vehicle Database**: Django Models & SQLite database storing Car Make and Car Model records
- **DevOps, CI/CD & Deployment**:
  - **Containers**: Docker & Docker Compose
  - **CI/CD**: GitHub Actions linting, unit testing, and automated deployment pipelines
  - **Cloud Hosting**: IBM Cloud Code Engine (serverless containers) & Kubernetes

## Key Features
1. **Dealership Management**: Interactive list of dealerships across all US states with state-level filtering.
2. **Review & Sentiment Analysis**: Real-time customer reviews annotated with NLTK sentiment polarity tags.
3. **User Authentication**: Secure user registration, session login, and logout.
4. **Post Review Experience**: Authenticated customer review submission with car make, model, purchase date, and rating.
5. **Static Pages**: Informative "About Us" and "Contact Us" pages with responsive layouts.

## Author
- **Harsh Manjramkar**
