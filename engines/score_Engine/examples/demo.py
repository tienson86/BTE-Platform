from engines.score_engine.service import ScoreService

service = ScoreService("database/13_score_engine")

print(
    "Score Engine Demo"
)

print(
    "Database:",
    service.loader.database_path
)
