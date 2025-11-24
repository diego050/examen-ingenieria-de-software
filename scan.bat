@echo off
echo Running tests and generating coverage report...

:: 1. Ejecuta pytest dentro del contenedor 'backend' que ya está corriendo.
::    El .coveragerc se encargará de corregir las rutas en el informe.
docker compose exec -T backend pytest tests/ --cov=src --cov-report=xml --junitxml=test-report.xml

:: Copy coverage and test report from the backend container to the host
:: This makes sure SonarScanner (which runs outside the backend container)
:: can read the generated `coverage.xml` and `test-report.xml`.
docker compose exec -T backend sh -c "cat /app/coverage.xml" > coverage.xml || echo coverage.xml not found
docker compose exec -T backend sh -c "cat /app/test-report.xml" > test-report.xml || echo test-report.xml not found

echo.
echo Running SonarQube analysis...

:: 2. Ejecuta el Sonar Scanner.
::    Montamos el proyecto en /usr/src (esto es para el scanner, no afecta al backend).
::    SonarQube verá las rutas corregidas como 'src/...' gracias al .coveragerc
docker run --rm --network examen-ingenieria-de-software_default ^
  -v "%CD%:/usr/src" sonarsource/sonar-scanner-cli ^
  -Dsonar.projectBaseDir=/usr/src ^
  -Dsonar.host.url=http://sonarqube:9000 ^
  -Dsonar.login=sqa_2342df1659c250e7ff531d4147453e8ee2435131 ^
  -Dsonar.sources=src ^
  -Dsonar.python.coverage.reportPaths=coverage.xml ^
  -Dsonar.tests=tests ^
  -Dsonar.python.xunit.reportPath=test-report.xml

echo Analysis complete. Check the results at http://localhost:9000