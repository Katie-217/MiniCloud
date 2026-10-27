"""Apply the additive student migration and verify schema/data/idempotency."""
from lab import ROOT, run, save, result
from progress import set_status
import requests

def sql(query):
    return run("docker", "compose", "exec", "-T", "relational-database-server", "sh", "-c",
        'MYSQL_PWD="$MARIADB_ROOT_PASSWORD" mariadb --default-character-set=utf8mb4 -uroot -e "$1"', "sh", query)

migration = (ROOT / "relational-database-server/init/002_students.sql").read_text(encoding="utf-8")
before = sql("SELECT COUNT(*) FROM minicloud.notes;")
sql(migration)
first = sql("SELECT COUNT(*) FROM studentdb.students;")
sql(migration)
assert sql("SELECT COUNT(*) FROM studentdb.students;") == first
assert sql("SELECT COUNT(*) FROM minicloud.notes;") == before
schema = sql("DESCRIBE studentdb.students;")
for definition in ("student_id\tvarchar(10)", "fullname\tvarchar(100)", "dob\tdate", "major\tvarchar(50)", "auto_increment"):
    assert definition in schema, schema
assert int(first.splitlines()[-1]) >= 3
rows = sql("SELECT * FROM studentdb.students ORDER BY id;")
# Grant only SELECT to the existing application user; no hardcoded password/user in SQL source.
run("docker", "compose", "exec", "-T", "relational-database-server", "sh", "-c",
    'MYSQL_PWD="$MARIADB_ROOT_PASSWORD" mariadb -uroot -e "GRANT SELECT ON studentdb.* TO \'$MARIADB_USER\'@\'%\';"')
api = requests.get("http://localhost/api/students-db", timeout=10)
assert api.status_code == 200 and len(api.json()) >= 3
assert {"id", "student_id", "fullname", "dob", "major"} == set(api.json()[0])
path = save("E03-student-database.json", result("E03", {
    "schema": schema, "rows": rows, "migration_idempotent": True,
    "existing_notes_preserved": True, "synthetic_data": True, "api_response": api.json(),
}))
set_status("E03", "DAT", path + "; feat/student-sql-database; python scripts/check_student_database.py")
print("PASS E03: required schema, 3+ records, additive repeatable migration.")
