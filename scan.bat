@echo off
echo Running tests and generating coverage report...

:: -T es para evitar un warning de "pseudo-TTY".
:: El --cov-config ya no es necesario pasarlo como argumento, pytest lo encuentra solo.
docker compose exec -T backend pytest tests/ --cov=src --cov-report=xml

echo.
echo Running SonarQube analysis...

docker run --rm --network examen-ingenieria-de-software_default \
  -v "$PWD:/usr/src" \
  -v "$PWD/.git:/usr/src/.git" \
  sonarsource/sonar-scanner-cli \
  -Dsonar.projectBaseDir=/usr/src \
  -Dsonar.host.url=http://sonarqube:9000 \
  -Dsonar.login=%SONAR_TOKEN% \
  -Dsonar.sources=src \
  -Dsonar.python.coverage.reportPaths=coverage.xml \
  -Dsonar.python.version=3

echo Analysis complete. Check the results at http://localhost:9000