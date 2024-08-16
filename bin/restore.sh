#!/usr/bin/env bash
set -eu

main() {
    export TOP_DIR=$(git rev-parse --show-toplevel)
    createdb "${PGDATABASE}"
    pg_restore --clean --if-exists -d "${PGDATABASE}" -1 "${TOP_DIR}/adv_works_oltp_postgres.backup"
}

main
