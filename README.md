## VenueSignal

# Project: 

The hospitality and restaurant industries face a critical challenge when opening new locations: understanding how operational constraints, such as limited parking, will affect customer satisfaction and reviews. For businesses considering expansion into urban city centers where parking is scarce, there's a significant financial risk, as customer reception is hard to predict. This is especially relevant in existing cities with large surface parking lots where debate over ideal development practices regularly swirls, seeking to weigh the needs of the local economy, business owners, and consumers. 

This project aims to develop a machine learning model to predict Yelp review ratings and sentiment for new businesses opening in city centers with limited parking. By leveraging the Yelp Open Dataset, which contains millions of reviews across various business categories and locations, we can identify patterns that correlate parking constraints with customer feedback.

The model's objective is to provide actionable insights for business owners and investors by forecasting expected review scores and identifying key factors that influence customer satisfaction in parking-constrained environments. This is fundamentally a supervised learning problem—specifically, a regression task if we're predicting star ratings (1-5 scale) or a classification task if we're categorizing sentiment (positive/negative/neutral). Additionally, we may employ natural language processing (NLP) techniques to extract sentiment and themes from review text. Understanding these dynamics will help stakeholders make informed decisions about location selection, pricing strategies, and operational adjustments to mitigate parking-related concerns.

# Data Source

Our data source is the Yelp Open Dataset, sourced directly from Yelp here: https://business.yelp.com/data/resources/open-dataset/ 

Per the Yelp terms:

*The Data is made available by Yelp Inc. (“Yelp”) to enable you to access
valuable local information to develop an academic project as part of an ongoing course
of study or for non-commercial purposes.*


The dataset consists of five JSON files:

## 1. yelp_academic_dataset_business.json

- **Records**: 150,346 businesses
- **Size**: 113 MB
- **Contains**: Business information including name, location, categories, ratings, hours, and attributes
- **Sample fields**: business_id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open, attributes, categories, hours

## 2. yelp_academic_dataset_checkin.json

- **Records**: 131,930 check-ins
- **Size**: 274 MB
- **Contains**: Check-in timestamps for businesses
- **Sample fields**: business_id, date (comma-separated list of check-in timestamps)

## 3. yelp_academic_dataset_review.json

- **Records**: 6,990,280 reviews (largest dataset)
- **Size**: 5.0 GB
- **Contains**: User reviews with ratings and text
- **Sample fields**: review_id, user_id, business_id, stars, useful, funny, cool, text, date

## 4. yelp_academic_dataset_tip.json

- **Records**: 908,915 tips
- **Size**: 172 MB
- **Contains**: Short tips/suggestions from users
- **Sample fields**: user_id, business_id, text, date, compliment_count

## 5. yelp_academic_dataset_user.json

- **Records**: 1,987,897 users (second largest)
- **Size**: 3.1 GB
- **Contains**: User profiles with social network info and compliments
- **Sample fields**: user_id, name, review_count, yelping_since, friends (list), useful, funny, cool, fans, average_stars, compliment_hot/more/profile/etc.

## License Terms

This project is part of the MSAAI program at the University of San Diego.  

## S3 Bucket
The JSON files for this project (as described above) have been loaded into an S3 bucket for processing. The bucket is located at s3://yelp-aai540-group6/yelp-dataset/. 

Additionally, the ARN for the bucket is arn:aws:s3:::yelp-aai540-group6.

Permissions for the bucket have been made public via AWS Learner Labs.

