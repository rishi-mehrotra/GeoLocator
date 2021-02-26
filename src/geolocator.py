import googlemaps
import json
from datetime import datetime
import psycopg2
import sys
from flask import Flask, request
import logging


app = Flask(__name__)
app.config["DEBUG"] = True

logFileName= "query.log"
logging.basicConfig(filename=logFileName, level=logging.DEBUG, format='%(levelname)s: [%(asctime)s]: [%(name)s]: %(message)s')
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

@app.route('/getstate', methods=['GET'])
def getStateByAddress():
    log.debug('Received request')
    query_parameters = request.args
    address = query_parameters.get('address')
    log.debug(address)
    ##gmaps = googlemaps.Client(key='AIzaSyCDdz12SqBuiK8h9MmmgyGuSFlBDiTfQJY')
    gmaps = googlemaps.Client(key='<your-key>')

    # Geocoding an address
    geocode_result = gmaps.geocode(address)
    #print(geocode_result)
    location=geocode_result[0]['geometry']['location']
    log.debug(location)
    latitude=location['lat']
    longitude=location['lng']
    log.debug(latitude)
    log.debug(longitude)

    con = None

    try:
        con = psycopg2.connect(host='192.168.171.33', database='postgres', user='postgres',password='rishi', port=5432)
        cur = con.cursor()
        sql=f"""select name from public.config_usstates
where ST_CONTAINS(geom, ST_SetSRID( ST_Point({longitude} ,{latitude}), 2263)::geometry  ) is True;"""
        log.debug(sql)
        cur.execute(sql)
        state = cur.fetchone()[0]
        log.debug(state)

    except psycopg2.DatabaseError as e:
        log.debug(f'Error {e}')
        sys.exit(1)

    finally:
        if con:
            con.close()
    return state

if __name__ == "__main__":    
    app.run(host='0.0.0.0', debug=False, threaded=True, port='9000')
    ##app.run(host='localhost', debug=False, threaded=True, port='8000')