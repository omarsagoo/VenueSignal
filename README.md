# VenueSignal

## Overview 

The hospitality and restaurant industries face a critical challenge when opening new locations: understanding how operational constraints, such as limited parking, will affect customer satisfaction and reviews. For businesses considering expansion into urban city centers where parking is scarce, there's a significant financial risk, as customer reception is hard to predict. This is especially relevant in existing cities with large surface parking lots where debate over ideal development practices regularly swirls, seeking to weigh the needs of the local economy, business owners, and consumers. 

This project aims to develop a machine learning model to predict Yelp review ratings and sentiment for new businesses opening in city centers with limited parking. By leveraging the Yelp Open Dataset, which contains millions of reviews across various business categories and locations, we can identify patterns that correlate parking constraints with customer feedback.

The model's objective is to provide actionable insights for business owners and investors by forecasting expected review scores and identifying key factors that influence customer satisfaction in parking-constrained environments. This is fundamentally a supervised learning problem—specifically, a regression task if we're predicting star ratings (1-5 scale) or a classification task if we're categorizing sentiment (positive/negative/neutral). Additionally, we may employ natural language processing (NLP) techniques to extract sentiment and themes from review text. Understanding these dynamics will help stakeholders make informed decisions about location selection, pricing strategies, and operational adjustments to mitigate parking-related concerns.

## Data Source

Our data source is the Yelp Open Dataset, sourced directly from Yelp here: https://business.yelp.com/data/resources/open-dataset/ 

Per the Yelp terms:

*The Data is made available by Yelp Inc. (“Yelp”) to enable you to access
valuable local information to develop an academic project as part of an ongoing course
of study or for non-commercial purposes.*


The dataset consists of five JSON files:

### 1. yelp_academic_dataset_business.json

- **Records**: 150,346 businesses
- **Size**: 113 MB
- **Contains**: Business information including name, location, categories, ratings, hours, and attributes
- **Sample fields**: business_id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open, attributes, categories, hours

### 2. yelp_academic_dataset_checkin.json

- **Records**: 131,930 check-ins
- **Size**: 274 MB
- **Contains**: Check-in timestamps for businesses
- **Sample fields**: business_id, date (comma-separated list of check-in timestamps)

### 3. yelp_academic_dataset_review.json

- **Records**: 6,990,280 reviews (largest dataset)
- **Size**: 5.0 GB
- **Contains**: User reviews with ratings and text
- **Sample fields**: review_id, user_id, business_id, stars, useful, funny, cool, text, date

### 4. yelp_academic_dataset_tip.json

- **Records**: 908,915 tips
- **Size**: 172 MB
- **Contains**: Short tips/suggestions from users
- **Sample fields**: user_id, business_id, text, date, compliment_count

### 5. yelp_academic_dataset_user.json

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

## Table Documentation

### yelp.business
| Field Name   | Data Type          | Description                                                                |
| ------------ | ------------------ | -------------------------------------------------------------------------- |
| business_id  | string             | Unique Yelp identifier for the business                                    |
| name         | string             | Business name                                                              |
| address      | string             | Street address                                                             |
| city         | string             | City where the business is located                                         |
| state        | string             | State or province code                                                     |
| postal_code  | string             | ZIP or postal code                                                         |
| latitude     | double             | Latitude coordinate                                                        |
| longitude    | double             | Longitude coordinate                                                       |
| stars        | double             | Average Yelp star rating                                                   |
| review_count | int                | Total number of reviews                                                    |
| is_open      | int                | Business open status (1 = open, 0 = closed)                                |                               
| attributes   | map<string,string> | Raw semi-structured business attributes. Utilize `yelp.business_attributes`|
| categories   | string             | Comma-separated business categories                                        |
| hours        | map<string,string> | Mapping of day → opening hours. Utilize `yelp.business_attributes`         |

### yelp.review
| Field Name  | Data Type | Description                                 |
| ----------- | --------- | ------------------------------------------- |
| review_id   | string    | Unique Yelp identifier for the review       |
| user_id     | string    | Identifier of the user who wrote the review |
| business_id | string    | Identifier of the reviewed business         |
| stars       | double    | Star rating given in the review             |
| useful      | int       | Number of “useful” votes                    |
| funny       | int       | Number of “funny” votes                     |
| cool        | int       | Number of “cool” votes                      |
| text        | string    | Full review text                            |
| date        | string    | Date the review was posted                  |

### yelp.user
| Field Name         | Data Type     | Description                                |
| ------------------ | ------------- | ------------------------------------------ |
| user_id            | string        | Unique Yelp identifier for the user        |
| name               | string        | User display name                          |
| review_count       | int           | Total number of reviews written            |
| yelping_since      | string        | Date the user joined Yelp                  |
| friends            | array<string> | List of Yelp user IDs representing friends |
| useful             | int           | Total “useful” votes received              |
| funny              | int           | Total “funny” votes received               |
| cool               | int           | Total “cool” votes received                |
| fans               | int           | Number of fans                             |
| elite              | array<string> | Years the user was an Elite member         |
| average_stars      | double        | Average rating given by the user           |
| compliment_hot     | int           | Count of “hot” compliments                 |
| compliment_more    | int           | Count of “more” compliments                |
| compliment_profile | int           | Profile compliments                        |
| compliment_cute    | int           | Cute compliments                           |
| compliment_list    | int           | List compliments                           |
| compliment_note    | int           | Note compliments                           |
| compliment_plain   | int           | Plain compliments                          |
| compliment_cool    | int           | Cool compliments                           |
| compliment_funny   | int           | Funny compliments                          |
| compliment_writer  | int           | Writer compliments                         |
| compliment_photos  | int           | Photo compliments                          |

### yelp.checkin
| Field Name  | Data Type | Description                                   |
| ----------- | --------- | --------------------------------------------- |
| business_id | string    | Identifier of the business being checked into |
| date        | string    | Comma-separated list of check-in timestamps   |

### yelp.tip
| Field Name       | Data Type | Description                              |
| ---------------- | --------- | ---------------------------------------- |
| user_id          | string    | Identifier of the user who wrote the tip |
| business_id      | string    | Identifier of the business               |
| text             | string    | Tip text                                 |
| date             | string    | Date the tip was posted                  |
| compliment_count | int       | Number of compliments received           |

### yelp.business_attributes
| Field Name                 | Data Type | Description                             |
| -------------------------- | --------- | --------------------------------------- |
| business_id                | string    | Unique Yelp business identifier         |
| acceptsinsurance           | string    | Indicates whether insurance is accepted |
| agesallowed                | string    | Age restrictions for the business       |
| alcohol                    | string    | Alcohol service type                    |
| bikeparking                | string    | Bike parking availability               |
| businessacceptsbitcoin     | string    | Bitcoin acceptance indicator            |
| businessacceptscreditcards | string    | Credit card acceptance indicator        |
| byappointmentonly          | string    | Appointment-only business               |
| byob                       | string    | Bring-your-own-beverage allowed         |
| byobcorkage                | string    | Corkage policy                          |
| caters                     | string    | Catering availability                   |
| coatcheck                  | string    | Coat check availability                 |
| corkage                    | string    | Corkage details                         |
| dogsallowed                | string    | Dogs allowed                            |
| drivethru                  | string    | Drive-thru availability                 |
| goodfordancing             | string    | Suitable for dancing                    |
| goodforkids                | string    | Suitable for kids                       |
| happyhour                  | string    | Happy hour availability                 |
| hastv                      | string    | TV availability                         |
| music                      | string    | Music options                           |
| noiselevel                 | string    | Noise level category                    |
| open24hours                | string    | Open 24 hours                           |
| outdoorseating             | string    | Outdoor seating availability            |
| restaurantsattire          | string    | Dress code                              |
| restaurantscounterservice  | string    | Counter service availability            |
| restaurantsdelivery        | string    | Delivery availability                   |
| restaurantsgoodforgroups   | string    | Suitable for groups                     |
| restaurantspricerange2     | string    | Price range (1–4)                       |
| restaurantsreservations    | string    | Reservations accepted                   |
| restaurantstableservice    | string    | Table service availability              |
| restaurantstakeout         | string    | Takeout availability                    |
| smoking                    | string    | Smoking policy                          |
| wheelchairaccessible       | string    | Wheelchair accessibility                |
| wifi                       | string    | WiFi availability/type                  |
| parking_garage             | boolean   | Garage parking available                |
| parking_street             | boolean   | Street parking available                |
| parking_validated          | boolean   | Validated parking available             |
| parking_lot                | boolean   | Parking lot available                   |
| parking_valet              | boolean   | Valet parking available                 |
| ambience_divey             | boolean   | Divey atmosphere                        |
| ambience_hipster           | boolean   | Hipster atmosphere                      |
| ambience_casual            | boolean   | Casual atmosphere                       |
| ambience_touristy          | boolean   | Touristy atmosphere                     |
| ambience_trendy            | boolean   | Trendy atmosphere                       |
| ambience_intimate          | boolean   | Intimate atmosphere                     |
| ambience_romantic          | boolean   | Romantic atmosphere                     |
| ambience_classy            | boolean   | Classy atmosphere                       |
| ambience_upscale           | boolean   | Upscale atmosphere                      |
| good_for_dessert           | boolean   | Good for dessert                        |
| good_for_latenight         | boolean   | Good for late night                     |
| good_for_lunch             | boolean   | Good for lunch                          |
| good_for_dinner            | boolean   | Good for dinner                         |
| good_for_brunch            | boolean   | Good for brunch                         |
| good_for_breakfast         | boolean   | Good for breakfast                      |
| bestnight_monday           | boolean   | Best night: Monday                      |
| bestnight_tuesday          | boolean   | Best night: Tuesday                     |
| bestnight_wednesday        | boolean   | Best night: Wednesday                   |
| bestnight_thursday         | boolean   | Best night: Thursday                    |
| bestnight_friday           | boolean   | Best night: Friday                      |
| bestnight_saturday         | boolean   | Best night: Saturday                    |
| bestnight_sunday           | boolean   | Best night: Sunday                      |
| hair_africanamerican       | boolean   | African-American hair specialization    |
| hair_asian                 | boolean   | Asian hair specialization               |
| hair_coloring              | boolean   | Hair coloring services                  |
| hair_curly                 | boolean   | Curly hair services                     |
| hair_extensions            | boolean   | Hair extensions services                |
| hair_kids                  | boolean   | Kids hair services                      |
| hair_perms                 | boolean   | Perm services                           |
| hair_straightperms         | boolean   | Straight perm services                  |
| dairy_free                 | boolean   | Dairy-free options                      |
| gluten_free                | boolean   | Gluten-free options                     |
| vegan                      | boolean   | Vegan options                           |
| kosher                     | boolean   | Kosher options                          |
| halal                      | boolean   | Halal options                           |
| soy_free                   | boolean   | Soy-free options                        |
| vegetarian                 | boolean   | Vegetarian options                      |
| hours_monday               | string    | Monday operating hours                  |
| hours_tuesday              | string    | Tuesday operating hours                 |
| hours_wednesday            | string    | Wednesday operating hours               |
| hours_thursday             | string    | Thursday operating hours                |
| hours_friday               | string    | Friday operating hours                  |
| hours_saturday             | string    | Saturday operating hours                |
| hours_sunday               | string    | Sunday operating hours                  |
| open_days_count            | int       | Number of days with defined hours       |
| open_on_weekend            | boolean   | Indicates weekend availability          |

## Order of Notebooks in this Project.

EDA
AthenaTables
DataLake
FeatureStore
BENCHMARK
XGBoost
ModelDeployment
8 - ModelComparison

## Contributors
<table>
  <tr>
    <td>
        <a href="https://github.com/littlecl42.png">
          <img src="https://github.com/littlecl42.png" width="100" height="100" alt="Carrie Little"/><br />
          <sub><b>Carrie Little</b></sub>
        </a>
      </td>
      <td>
        <a href="https://github.com/mojodean.png">
          <img src="https://github.com/mojodean.png" width="100" height="100" alt="Dean P. Simmer"/><br />
          <sub><b>Dean P. Simmer </b></sub>
        </a>
      </td>
     <td>
      <a href="https://github.com/omarsagoo.png">
        <img src="https://github.com/omarsagoo.png" width="100" height="100" alt="Omar Sagoo"/><br />
        <sub><b>Omar Sagoo</b></sub>
      </a>
    </td>
  </tr>
</table>
