#!/usr/bin/env bash
set -eu

main() {
    export TOP_DIR=$(git rev-parse --show-toplevel)

    # Lint Python code with black
    if [ -d "${TOP_DIR}/etl/app" ]; then
        echo "Linting Python code with black..."
        black "${TOP_DIR}/etl/app"
    else
        echo "Python source directory not found, skipping Python linting."
    fi

    # Install dbt dependencies
    echo "Installing dbt dependencies..."
    dbt deps --project-dir "${TOP_DIR}/dbt/DBTdec"

    # Lint and fix SQL files with sqlfluff
    echo "Linting SQL files with sqlfluff..."
    sqlfluff fix -f "${TOP_DIR}/dbt/DBTdec"

    # Check for uncommitted changes
    if [ -z "$(git status --porcelain)" ]; then 
        echo "Working directory clean, linting passed."
        exit 0
    else
        echo "Linting failed. Please commit these changes:"
        git --no-pager diff HEAD
        exit 1
    fi
}

main

