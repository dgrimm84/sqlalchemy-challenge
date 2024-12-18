# sqlalchemy-challenge
# Files in this repository and their functions
- <ins>Resources/hawaii.sqlite</ins> - this has data stored in it for which the main code file creates an SQLAcademy server to access and query this information
- <ins>hawaii_measurements.csv</ins> - this is a CSV file that contains data of Station ID Column, Date Column, Precipitation reading column, and temperature reading column
- <ins>hawaii_stations.csv</ins> - this is a CSV file that contains data of Station ID column, name column containing name and location data, latitude column, longitude column, and elevation column
- <ins>climate_starter_ipynb</ins> - this is the 1st of the two main code files for this challgen that executes the following:
> - Creates an engine/server to connect to the hawaii.sqlite file mentioned above, reflects the tables in this file, and displays the main keys (columns) of the file:<br><br>
> ![image](https://github.com/user-attachments/assets/5ff835c5-31e5-4df6-b443-5e642dc628be)<br>

> - Saves python references to each table and creates a link to this session from Python
> - calculates the most recent date of measurement in the dataset:<br><br>
> ![image](https://github.com/user-attachments/assets/0ef2b4fa-32d0-497c-abc6-9c6f13cce9ec)<br>
> - queries the precipitation data over a 12 month period to plot it for ease of interpretation:<br><br>
> ![image](https://github.com/user-attachments/assets/70aa40d9-9a6b-4d9a-9219-f9d3962320b1)
> - calculates summary statistics of this dataset in a table:<br><br>
> ![image](https://github.com/user-attachments/assets/708d2467-14f6-4afe-bf9f-70c7020bcd16)
> - calculates the total number of stations in the dataset:<br><br>
> ![image](https://github.com/user-attachments/assets/e27e7299-7a83-4b84-88f2-5eb04714bce3)
> - calculates the total number of unique measurements for each station, totals them, and then displays them in descending order from most to least:<br><br>
> ![image](https://github.com/user-attachments/assets/540fc49e-bca0-4980-bf39-303e3565572a)
> - uses the above results to find the most active station and then calculating the lowest, highest, and average temperature for that station:<br><br>
> ![image](https://github.com/user-attachments/assets/8defadb0-bc05-485e-9093-c5de4e776032)
> - uses the above data again to display in a plot the temperature readings for this most-active station over the last 12 months:<br><br>
> ![image](https://github.com/user-attachments/assets/67a8b466-f1c8-4739-a1a3-60c78517f60f)<br><br>


- <ins>app.py</ins> - this is the 2nd of the two main code files for this challenge that executes the following:
> - using Flask, generate an API to store data that can be accessed by specific routes.  These routes are accessible by button click and also by the user typing date ranches in the URL Path:<br><br>
  ![image](https://github.com/user-attachments/assets/3c5435c6-e026-442b-9c39-4105ecf3bed9)<br>
> - the /precipitation route displays a jsonified version of the last 12 months of precipitation readings:<br><br>
> ![image](https://github.com/user-attachments/assets/56941795-947b-465a-a366-6baa314eb33d)
> - the /stations route displays the 9 unique station IDs and the number of unique measurements of each:<br><br>
> ![image](https://github.com/user-attachments/assets/bc861804-4a2c-40e7-add5-1d7bf99cc1cb)
> - the /tobs route displays the temperature reading data for the last 12 months of the most active station:<br><br>
> ![image](https://github.com/user-attachments/assets/ddc1336c-dae2-4397-a521-e1fd55a3260b)
> - the /start route allows the user to add a starting date to the end of the API URL as a custom route to display the minimum, maximum, and average temperatures of the most active station from the inputted date to present:<br><br>
> ![image](https://github.com/user-attachments/assets/50ce0c7a-41a1-4eb2-aa89-aa0a9e6b6f1c)<br>
> ![image](https://github.com/user-attachments/assets/5ab59647-990c-4b78-90f0-a40ccc04b9b3)<br>
> - the /start/end route allows the user to add a starting date and ending date to the end of the API URL as a custom route to display the minimum, maximum, and average temperature of the most active station from the inputted start date to the inputted end date:<br><br>
> ![image](https://github.com/user-attachments/assets/1583d356-32bf-43b5-a02c-8661e3339e4d)<br>
> ![image](https://github.com/user-attachments/assets/8f9ccb22-6ac1-476b-8b47-f9854b212b82)<br>



