from lab import run, save, result
from progress import set_status

query = "USE minicloud; SHOW TABLES; SELECT * FROM notes;"
output = run("docker", "compose", "exec", "-T", "relational-database-server", "sh", "-c",
             'MYSQL_PWD="$MARIADB_ROOT_PASSWORD" mariadb -uroot -e "$1"', "sh", query)
assert "notes" in output and "Hello from MariaDB!" in output, output
evidence = save("R04-database.json", result("R04", {"query": query, "output": output}))
set_status("R04", "DAT", evidence)
print("PASS: minicloud.notes contains initial seed; " + evidence)
