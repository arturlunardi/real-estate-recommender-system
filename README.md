# Real Estate Recommender System
Access the application [here](http://real-estate-recommender-system.herokuapp.com/).

## About:
This project was built to generate recommendations of real estate rent properties based on their characteristics or atributes. It was an end-end project, that means that passes through all the steps since collect to deploy the project.

## Steps:
- Definition of the problem
- Collect
- Data Wrangling
- Modelling
- Deploy

## Model:
Recommender systems aim to sugest relevant items to the user. To build this model, the Content-based recommender system was chosen.\
Content Based Filtering are a type of recommender system that uses item features to recommend other items similar to what the user likes, based on their previous actions or explicit feedback.\
One of the advantages of these system it is that it is possible to generate recommendations without have a historic of the behavior of another users.

## Tools:
- Python for programming language
- HTML and CSS for front-end
- Docker for containerization
- Heroku for cloud hosting

## Project structure:
1. Definition of the problem
The main purpose of a recommender system it is to suggest relevant items to the user. It saves time, increase the user experience and increase the profit from a company. Imagine that you are on a website that have thousands of products, you wouldn't have the time to go through every product to find the one you are searching for. To improve your experience and help you to find your product, the recommender system it's gonna suggest products that matches your searches.

Therefore, to solve this problem it was defined a simple structure:

Problem to be solved: a system that recommends me the most similar properties based on what I've searched.
How can I solve this problem: create a content based recommender system that will return me the n similar properties based on the features of the item the user select.

2. Data Collect
The data collect was made through an API that was provided by [Órion](https://orionsm.com.br/), a real estate company.

3. Data Wrangling
In this step we had to clean and transform the data. It was necessary to select only the columns that we want to feed our model from. The data had some missing values, so it was necessary to fill this values. Some of the data were categorical, so we had to transform these in numbers so our model could read those. Since we had some numerical values that have some very different scales, it was performed a standardization in order to normalize the data. Some of the columns were textual data, so we chose to work with TfidfVectorize from Scikit-Learn to perform the transformation.

4. Modelling
There are a lot of ways to develop a content based filter. We chose to work with the cosine similarity, it is a metric that measure the distance between two vectors of n dimensional spaces. It is measured by the cosine of the angle between these vectors. The model itself it is simple. It is important to say that we are not predicting anything, we are measuring the similarity between vectors, that represent our items.

5. Deploy
The system was released through this [application](http://real-estate-recommender-system.herokuapp.com/), made in Flask. The application collect the data through the API every n minutes and perform all the steps above to deliver the top n recommendations for the item that the user selected.

## Additional information:
Author - Artur Lunardi Di Fante | Contacts: [LinkedIn](https://www.linkedin.com/in/artur-lunardi-di-fante-393611194/)