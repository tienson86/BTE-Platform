# Log contract (Beta-1)

BTE Python services use stdlib logging (not Logback). This file names the **logical** appenders for ops parity with JVM-style runbooks.

| Appender | Maps to |
|----------|---------|
| APP | uvicorn / applications logger → stdout + `/app/logs` |
| ACCESS | nginx `access.log` |
| ERROR | nginx `error.log` + Python ERROR |
| AUDIT | application logger names containing auth/admin (existing) |

Do not introduce a new logging framework in Beta-1.

---

END
