# AndroidApps
Contains the files for Android App privacy quantification
  

### app details ordered all apps 20230213 wcl.csv
csv table storing the description of the crawled apps; in zip format
|app_link|app_version|CHAR_LENGTH(app_description)|app_description|
|-----:|-----------|--|--|
  
  
### app category ordered all apps 20230213.csv
csv table storing the category of the app (an app may belong to more than one category)
|app_link|category|
|--|--|
  
  
### app name table ordered all apps 20230213.csv
csv table storing the name and creator of an app
|app_link|app_name|app_creator|
|--|--|--|
  
  
### category details ordered all apps 20230213.csv
csv table storing the name of each category
|category|category_description|
|--|--|
  
  
### app permissions ordered all apps 20230213.csv
csv table storing the permission request of an app (with the corresponding version); in zip format
|app_link|app_version|permission|
|--|--|--|
  
  
### permission list ordered 317 20230213.csv
csv table storing the category and description (as on Google Play store) of each permission
|permission|permission_category|permission_description|
|--|--|--|
  
  
### permission list ordered 317 with description highlighted dangerous.xlsx
Manual mapping between permission and the corresponding permission (as in AndroidManifest.xml), together with the more detailed description (from various sources), and decision rationale. 
It also includes the statistics of number of apps requesting each permission.
  
  
### Raw_Dataset.zip
A set of labeled permission requests, grouped by permission ID. 
1 means permission request is justified, 0 means not justified
