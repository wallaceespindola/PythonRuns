for process in `ps ax | grep python | awk '{print $1}'`; do kill -9 "$process"; done 2>/dev/null

# Hello world app running on python flask directly
cd ~/flask_app && nohup flask run --host=0.0.0.0 -p 3000 > flask_app_nohup.out 2>&1 &

# Flask Web App configured and running on apache, port 3100 (not here)
#cd /var/www/flask_apache && nohup flask run --host=0.0.0.0 -p 3100 > flask_apache_nohup.out 2>&1 &

# Web App skp.io moved to apache
#cd ~/skp_io_app && nohup flask run --host=0.0.0.0 -p 4000 > skp_io_nohup.out 2>&1 &
# Option that also works: python3 /var/www/skp_io/app.py ==> on http://195.31.150.176:4000/

# ConstaNosAutos
cd ~/ibm-web && nohup flask run --host=0.0.0.0 -p 5000 > ibm_web_nohup.out 2>&1 &


# Web App qjump_api (findforme.bc/api) moved to apache
#cd ~/qjump-api && nohup python3 app.py > qjump_api_nohup.out 2>&1 &
cd ~/qjump-api && nohup flask run --host=0.0.0.0 -p 7000 > qjump_api_nohup.out 2>&1 & # findforme.bc/api
# Option that also works: python3 /var/www/qjump_api/app.py ==> run on http://195.31.150.176:7000/
#cd ~/qjump-api && nohup python3 app.py > qjump_api_nohup.out 2>&1 & 


cd ~/findma && nohup flask run --host=0.0.0.0 -p 9000 > findma_nohup.out 2>&1 &

cd ~

echo "==================================================================================================="
echo "Started flask_app:3000, app_io:4000, ibm-web-CNA:5000, qjump-api(findforme):7000, findma:9000"
echo "==================================================================================================="
