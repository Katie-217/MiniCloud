FROM eclipse-temurin:21-jre-jammy AS java
FROM node:22-bookworm-slim
COPY --from=java /opt/java/openjdk /opt/java/openjdk
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH="/opt/java/openjdk/bin:${PATH}"
ENV CI=true FIREBASE_CLI_DISABLE_UPDATE_CHECK=true
RUN npm install --global firebase-tools@14.18.0 && npm cache clean --force
WORKDIR /app
COPY firebase.json firestore.rules storage.rules ./
RUN firebase setup:emulators:firestore && firebase setup:emulators:storage
COPY start.sh healthcheck.js ./
EXPOSE 9099 8180 9199 4400
STOPSIGNAL SIGTERM
ENTRYPOINT ["sh", "/app/start.sh"]
