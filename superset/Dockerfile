FROM apache/superset:3.0.2

USER root

COPY --chmod=777 superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

RUN pip install trino

USER superset
ENTRYPOINT [ "/usr/bin/run-server.sh" ]