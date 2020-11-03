HOST=`hostname`
sed -i -e "s/hostname/$HOST/g" /app/gunicorn.conf.py
gunicorn -c /app/gunicorn.conf.py app:server
