# Backup policy

- Daily full archive of data + reports (RPO 24h).  
- Weekly config snapshot (compose + nginx + env **examples**).  
- Knowledge: store git tag SHA with each release; do not mutate knowledge in backups as source of truth.  
- Retention: 14 daily, 8 weekly, 6 monthly.  
- Encrypt archives at rest if they leave the host.  
- Verify restore monthly.

---

END
