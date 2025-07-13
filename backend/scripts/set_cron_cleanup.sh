#!/bin/bash
set -f # flag is required - otherwise shell will interpret '*' as glob expansion (will return all files from the folder)

PSQL_COMMAND="
SELECT cron.schedule(
    'clean-old-logs',
    '0 1 * * *',
    \$\$DELETE FROM logs WHERE timestamp < NOW() - INTERVAL '7 days' \$\$
);
"
echo $PSQL_COMMAND

docker exec -it -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD genai-agentos-postgres-1 psql -U $POSTGRES_USER -d postgres -c "$PSQL_COMMAND"
