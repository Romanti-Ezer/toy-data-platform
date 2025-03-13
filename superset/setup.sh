superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@localhost \
              --password secret

superset db upgrade &&
/usr/bin/run-server.sh