
# watsonx Code Assistant General Code Demo
An end-to-end full stack web app demo. The user fixes a bug in the Java backend. Once the backend passes all tests, then the user uses WCA to generate a front end in HTML, JS, and CSS. 

## Demo documents:
- [Script](https://ibm.box.com/s/z2zfd4ozft33y4k1p0qmjuadud3aegb0)
- [Instructions](https://ibm.box.com/s/fpdxpyxz7383to85h92vnj4ikebizbu0)
- [Demo recording](https://ibm.seismic.com/app?ContentId=e60211c5-cf0b-4fde-98b1-c722c5194999#/doccenter/861ea1fd-99e0-44d7-9135-85412e5c28d1/doc/%252Fdd3359e5f7-a856-a91b-7688-41024b2ac637%252FdfNTY4NmVhOWItY2RkNS04ZWY3LTZkNzItZTQwZjczMWUyMjk1%252CPT0%253D%252CRGF0YSBQbGF0Zm9ybQ%253D%253D%252FdfNDRmODBlMzMtY2ViMC0zMDI1LTVhNDEtNzg2OTg4MWVmZDBl%252COthers%252FdfOTRiYmU4NTQtNWY4NC03Y2QyLWZjYWUtOGIxYmFmZjkyZThk%252CPT0%253D%252CRGVtbw%253D%253D%252Flf14bdc6a5-40e0-4a56-85f4-353faf9ceca1//?mode=view&parentPath=sessionStorage)
- [TechZone Setup PDF](https://ibm-my.sharepoint.com/:b:/p/oscar_hong1/EWgazL38NkFPiFOZukF3wpcBQzzscHkxZLmw_fW-R7otkQ?e=NAKfU2)
- [TechZone Setup Recording](https://ibm.ent.box.com/s/yfqn401tytaywf3pdus5bpcjqtjocj7i)
- [Owner Contact](https://ibm.enterprise.slack.com/user/@U03GGPKCRBN)


## Set Up Guide
Ensure that the Java version you use in the backend folder is Java 11. If is not, install Java 11 and set it as the current version. 

#### How to use and install Java 11 (mac):
1. cd backend
2. brew install openjdk@11
3. brew link --force --overwrite openjdk@11
4. export JAVA_HOME=$(/usr/libexec/java_home -v 11)

#### How to install Java 11 (FOR TECHZONE)
1. Follow instructions [here](https://ibm-my.sharepoint.com/:b:/p/oscar_hong1/EWgazL38NkFPiFOZukF3wpcBQzzscHkxZLmw_fW-R7otkQ?e=NAKfU2)

#### How to test the backend:
1. cd backend
2. ./gradlew test

#### How to run the backend server:
1. cd backend
2. ./gradlew bootRun
3. It will hover ~83% once active

#### How to run the frontend server:
1. cd frontend
2. npm install -g http-server
3. http-server .
4. Launch available server (for me is http://127.0.0.1:8081)
5. After each change, clear browser cache and reload page


## Source
This was based off of the [open source Article spring boot repo](https://github.com/gothinkster/spring-boot-realworld-example-app).
