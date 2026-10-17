#!/bin/bash
set -euo pipefail

: "${VECTOR_SIZE:?VECTOR_SIZE must be set}"

case "$VECTOR_SIZE" in
  1536|4096) ;;
  *) echo "Unsupported VECTOR_SIZE: $VECTOR_SIZE" >&2; exit 1 ;;
esac

sed "s/\${VECTOR_SIZE}/$VECTOR_SIZE/g" /tmp/schema.sql \
  | psql -v ON_ERROR_STOP=1 \
      --username "$POSTGRES_USER" \
      --dbname "$POSTGRES_DB"