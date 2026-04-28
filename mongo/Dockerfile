FROM mongo:4.4

USER root

RUN mkdir -p /data/db /data/configdb && chown -R 1001:0 /data/db /data/configdb && chmod -R g+w /data/db /data/configdb

COPY --chown=1001:0 init-db.js /docker-entrypoint-initdb.d/


USER 1001

EXPOSE 27017
