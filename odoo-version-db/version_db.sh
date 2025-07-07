#!/bin/bash

# Automates the building and initialization of Odoo databases across multiple versions with selected modules.
# Handles both Community and Enterprise code, along with additional demo data modules.
# These scripts aim to reduce module run time.
# Run them once, and later, when needed, simply restore the corresponding version’s database and upgrade the related module.


# Define Odoo versions you want to build
VERSIONS=("18.0" "saas-18.1" "saas-18.2" "saas-18.3" "master")
VERSIONS_WITH_DEMO_TAG=("saas-18.3" "master")

# Define your workspace (where the code is)
WORKSPACE="$HOME/odoo-sec"
PG_USER="odoo"  # Adjust if needed

# Define odoo run command 
MODULES_TO_INSTALL="pos_restaurant,l10n_in"
ADDONS_PATH="addons,../enterprise,../x"

# Community and enterprise path
ODOO_DIR="$WORKSPACE/community"
ENT_DIR="$WORKSPACE/enterprise"

echo "🗂️  Updating existing community repo..."
cd "$ODOO_DIR"
git checkout .
git remote update

echo "🗂️  Updating existing community repo..."
cd "$ENT_DIR"
git checkout .
git remote update

LOADED_DBS=()

for version in "${VERSIONS[@]}"; do
    echo "🚀 Processing version: $version"

    # enterprise
    echo "🔄  Updating enterprise repo for version: $version..."
    cd "$ENT_DIR"
    git checkout "$version"
    git pull --rebase

    # community
    echo "🔄  Updating community repo for version: $version..."
    cd "$ODOO_DIR"
    git checkout "$version"
    git pull --rebase

    # Create a PostgreSQL database
    DBNAME="testdb-${version}"  # e.g. testsb-saas-18.3

    if psql -lqt | cut -d \| -f 1 | grep -qw "$DBNAME"; then
        echo "⚠️  Dropping existing database: $DBNAME"
        dropdb "$DBNAME"
    fi

    echo "📦 Creating database: $DBNAME"
    createdb -U "$PG_USER" "$DBNAME"

    # Initialize Odoo database
    echo "🔧  Initializing Odoo database: $DBNAME..."
    cd "$ODOO_DIR"

    if printf '%s\n' "${VERSIONS_WITH_DEMO_TAG[@]}" | grep -q "^$version$"; then
        # Version with --with-demo tag required
        python3 odoo-bin --addons="$ADDONS_PATH" -d "$DBNAME" -i "$MODULES_TO_INSTALL" --with-demo --stop-after-init \
            || echo "🚨  Initialization failed for $DBNAME"
    else
        python3 odoo-bin --addons="$ADDONS_PATH" -d "$DBNAME" -i "$MODULES_TO_INSTALL" --stop-after-init \
            || echo "🚨  Initialization failed for $DBNAME"
    fi


    LOADED_DBS+=("$DBNAME")

    echo "✅ Done with version: $version"
    echo "-------------------------"
done

echo ""
echo "🎉 All databases created successfully! 🚀"
echo "📝 Database Info Summary:"
echo "-----------------------------------------------"
printf "%-20s | %-10s | %-15s\n" "Database" "Size" "Tables"
echo "-----------------------------------------------"

for db in "${LOADED_DBS[@]}"; do
    DB_SIZE=$(psql -U "$PG_USER" -d "$db" -c "SELECT pg_size_pretty(pg_database_size('$db'));" -t | xargs)
    TABLE_COUNT=$(psql -U "$PG_USER" -d "$db" -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';" -t | xargs)
    printf "%-20s | %-10s | %-15s\n" "$db" "$DB_SIZE" "$TABLE_COUNT"
done

echo "-----------------------------------------------"


echo "✅ Script completed successfully! 🎉"
