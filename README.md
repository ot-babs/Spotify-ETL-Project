# Spotify-ETL-Project
Using Apache Airflow to schedule our ETL process

Pre Requisite to run
1. Download Docker
2. Ensure that WSL 2 is active on the docker
3. Recommend using dbeaver to access the database

Setting Up the Docker
1. In VScode - Setup the Terminal to be n the folder where the docker is located
2. Creating the directorys needed: In the terminal write mkdir ./dags ./plugins ./logs
3. Next in the terminal: Type echo -e "AIRFLOW_UID=$(id -u)\AIRFLOW_GID=0" > .env
4. Now to initiate our airflow in the terminal: Type docker-compose up airflow-init
5. Finally to run the airflow, type in the terminal:docker-compose up
6. To check health of our docker we type: docker ps

Running the ETL
1. Ensure all zipped files/folders are decomposed all together and saved in the same location
2. Open up VScode - and have a terminal open
3. In the folder where docker-compose file is, in the terminal type docker-compose up then press enter
	- This will initiate the airflow on localhost:8081
4. On a browser type the localhost:8081 - Look for spotify_dag and then activate the DAG
5. Once this is active you can now run the dag or wait for it to run when it's scheduled

Notes:
- Necessary ETL files are found in the dags folder
- Within the spotify_dag.py (located in the dags folder) we you can change the schedule_interval to either minutes/ hours /days 
- Also Note that in order for the scheduler to work your computer cannot switch off similar to the cloud.
- Note that this is going to be my spotify played songs, to use your own you will need to remove the Refresh part of the spotify_etl and manually insert your played 
  tracks token
