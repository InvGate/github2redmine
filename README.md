# github2redmine

Es una aplicacion para migrar los issues de Github a Redmine.

## Proceso

Primero debemos exportar los issues y sus correspondientes comentarios 
desde Github (en formato json) usando la web api de Github

curl "https://api.github.com/repos/<repo-owner>/<repo-name>/issues&per_page=1000" -u "<user-name>" 

Luego se textrae la información que necesitamos para crear los issues en Redmine y la guardamos en formato csv

Finalmente los issues se importan desde Redmine usando el archivo csv

http://www.redmine.org/projects/redmine/wiki/HowTo_import_issues

