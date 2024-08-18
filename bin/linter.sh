set -e

main() {
    export TOP_DIR=$(git rev-parse --show-toplevel)

    if [ -d "${TOP_DIR}/etl/app" ]; then
        echo "Linting Python code with black..."
        black "${TOP_DIR}/etl/app"
    else
        echo "Python source directory not found, skipping Python linting."
    fi

    echo "Installing dbt dependencies..."
    dbt deps --project-dir "${TOP_DIR}/dbt/DBTdec"

    echo "Linting SQL files with sqlfluff..."
    sqlfluff fix -f "${TOP_DIR}/dbt/DBTdec" --verbose || true

    if [ -z "$(git status --porcelain)" ]; then 
        echo "Working directory clean, linting passed."
        exit 0
    else
        echo "Linting found issues. Please review and commit these changes:"
        git --no-pager diff HEAD
        exit 1
    fi
}

main

