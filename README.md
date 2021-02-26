# GeoLocator How to run

1. I am using postgresql 13 on Local machine.Install using below link https://www.enterprisedb.com/postgresql-tutorial-resources-training?cid=437. Select PostGIS extension and install it with Application builder.
2. Downloaded the zip file from link https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_20m.zip and extract the zip.
3. Run below command from the location of file cb_2018_us_state_20m.shp. This will import shapefile in postgresql config_usstates table.
"C:\Program Files\PostgreSQL\13\bin\shp2pgsql.exe" -I -s 2263 cb_2018_us_state_20m.shp public.config_usstates | "C:\Program Files\PostgreSQL\13\bin\psql.exe" -U postgres -d postgres
5. Install Docker on windows. git pull https://github.com/rishi-mehrotra/GeoLocator.git.
6. Run command-  docker build -t geolocator . to create image.
7. Run command -  docker run -it --add-host=host:host-ip -p 9000:9000 geolocator:latest bash and replace host-ip with local laptop ip.
8.  This will open linux shell. Run commmand to start server -  python3 geolocator.py. This will start server on port 9000.
9.  Edit C:\Program Files\PostgreSQL\13\data\pg_hba.conf and add below entry.(replace host-ip with local ip address)


                   host	all	            all	            host-ip/16	        md5
                   host	all	            all	            192.168.171.33/16	        md5
  
10. Open browser and hit the link http://localhost:9000/getstate?address=1%20Hacker%20Way,%20Menlo%20Park,%20CA. This will hit the server running on container and return output California.
