# Grammy Awards Poll 

**Owners:** Nicole Amenta (Nicole.Amenta@ibm.com), Tanmay Bakshi (tanmay@ibm.com)

## Demo Videos

- IBM Canada Townhall (December 10th, 2024): [Recording](https://secure.video.ibm.com/channel/23940224/video/134139902)
- WCA@IBM Office Hours (January 16th, 2025): [Recording (skip to 19:58)](https://ibm-my.sharepoint.com/:v:/r/personal/bedi_ca_ibm_com/Documents/Recordings/WCA@IBM%20-%20Monthly%20Office%20Hours-20250116_110029-Meeting%20Recording.mp4?csf=1&web=1&e=ASMvtj&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)

## Development Setup

1. Deploy a Postgres database and set the following environment variables:
   ```bash
   export DB_NAME=
   export DB_USER=
   export DB_PASSWORD=
   export DB_HOST=
   export DB_PORT=
   ```
2. Execute the following SQL within the deployed database:
    ```sql
    -- Create the categories table
    CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
    );

    -- Create the choices table
    CREATE TABLE choices (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    name VARCHAR(255) NOT NULL
    );

    -- Create the votes table
    CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    choice_id INTEGER NOT NULL REFERENCES choices(id),
    vote_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Insert category data
    INSERT INTO `categories` (`id`, `name`) VALUES (1, 'Best New Artist');
    INSERT INTO `categories` (`id`, `name`) VALUES (2, 'Song of the Year');
    INSERT INTO `categories` (`id`, `name`) VALUES (3, 'Album of the Year');

    -- Insert nominee data
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (1, 1, 'Benson Boone');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (2, 1, 'Sabrina Carpenter');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (3, 1, 'Doechii');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (4, 1, 'Khruangbin');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (5, 1, 'Raye');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (6, 1, 'Chappell Roan');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (7, 1, 'Shaboozey');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (8, 1, 'Teddy Swims');

    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (9, 2, 'Beyoncé — "Texas Hold ''Em"');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (10, 2, 'Sabrina Carpenter — "Please Please Please"');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (11, 2, 'Billie Eilish — "Birds Of A Feather"');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (12, 2, 'Lady Gaga & Bruno Mars — "Die With a Smile"');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (13, 2, 'Kendrick Lamar — "Not Like Us"');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (14, 2, 'Chappell Roan — "Good Luck, Babe!"');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (15, 2, 'Shaboozey — "A Bar Song (Tipsy)"');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (16, 2, 'Taylor Swift ft. Post Malone — "Fortnight"');

    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (17, 3, 'André 3000 — New Blue Sun');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (18, 3, 'Beyoncé — Cowboy Carter');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (19, 3, 'Sabrina Carpenter — Short n'' Sweet');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (20, 3, 'Charli XCX — Brat');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (21, 3, 'Jacob Collier — Djesse Vol 4');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (22, 3, 'Billie Eilish — Hit Me Hard and Soft');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (23, 3, 'Chappell Roan — The Rise and Fall of a Midwest Princess');
    INSERT INTO `choices` (`id`, `category_id`, `name`) VALUES (24, 3, 'Taylor Swift — The Tortured Poets Department');
    ```
3. Create a new Code Engine project in IBM Cloud named `grammy-poll`.
4. In your terminal, authenticate against the IBM Cloud CLI:
    ```bash
    ibmcloud login --sso
    ibmcloud target -g default
    ibmcloud cr login
    ibmcloud ce project select -n grammy-poll
    ```
   
## Running the Demo

1. Navigate to the `clean_state` directory and follow the instructions in the video to create the app!
   - _A reference to what the final code **should** look like can be found in the `working_state` directory._
2. Once development is complete, run the app using the following command:
   ```bash
   python app.py
   ```
3. Dockerize the application and deploy it to IBM Code Engine by running the commands below:
   ```bash
   docker build --platform linux/amd64 -t grammy-poll .
   
   docker tag grammy-poll us.icr.io/grammy-poll/grammy-poll
   
   docker push us.icr.io/grammy-poll/grammy-poll
   
   ibmcloud ce app create \
      --name grammy-poll \
      --image us.icr.io/grammy-poll/grammy-poll \
      --port 4321 \
      --registry-secret icr-secret \
      --env DB_NAME=$DB_NAME \
      --env DB_USER=$DB_USER \
      --env DB_PASSWORD=$DB_PASSWORD \
      --env DB_HOST=$DB_HOST \
      --env DB_PORT=$DB_PORT \
      --cpu 1 \
      --memory 4G
   ```
