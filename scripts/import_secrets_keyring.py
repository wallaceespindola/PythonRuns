# Before starting, pip install secretstorage

import sys

import secretstorage


def list_all_collections(bus):
    """List all available keyring collections."""
    print("\n=== Available Keyrings ===")
    collections = []
    try:
        for collection in secretstorage.get_all_collections(bus):
            label = collection.get_label()
            locked = "🔒 Locked" if collection.is_locked() else "🔓 Unlocked"
            try:
                item_count = len(list(collection.get_all_items()))
                print(f"{len(collections) + 1}. {label} - {locked} ({item_count} items)")
            except:
                print(f"{len(collections) + 1}. {label} - {locked}")
            collections.append(label)
    except Exception as e:
        print(f"Error listing collections: {e}")

    if not collections:
        print("No keyrings found.")

    return collections


def get_collection_by_label(bus, label):
    """Get a collection by its label."""
    try:
        for collection in secretstorage.get_all_collections(bus):
            if collection.get_label() == label:
                return collection
        return None
    except Exception as e:
        print(f"Error finding collection '{label}': {e}")
        return None


def unlock_collection_once(collection, collection_name):
    """Unlock a collection only if it's locked, with user prompt."""
    if collection.is_locked():
        print(f"Collection '{collection_name}' is locked.")
        response = input(f"Unlock '{collection_name}'? (y/n): ").lower()
        if response == "y":
            try:
                collection.unlock()
                print(f"Collection '{collection_name}' unlocked successfully.")
                return True
            except Exception as e:
                print(f"Failed to unlock '{collection_name}': {e}")
                return False
        else:
            print(f"Skipping unlock for '{collection_name}'.")
            return False
    else:
        print(f"Collection '{collection_name}' is already unlocked.")
        return True


def migrate_items(source_label, destination_label):
    """Migrate items from source keyring to destination keyring."""
    try:
        bus = secretstorage.dbus_init()
    except Exception as e:
        print(f"Error initializing D-Bus connection: {e}")
        print("Make sure you're running in a session with D-Bus access.")
        sys.exit(1)

    # Find source and destination collections
    source = get_collection_by_label(bus, source_label)
    destination = get_collection_by_label(bus, destination_label)

    if not source:
        print(f"Error: Source collection '{source_label}' not found.")
        print("\nAvailable keyrings:")
        available = list_all_collections(bus)
        if available:
            print("\nPlease use one of the available keyring names above.")
        sys.exit(1)

    if not destination:
        print(f"Error: Destination collection '{destination_label}' not found.")
        print("\nAvailable keyrings:")
        available = list_all_collections(bus)
        if available:
            print("\nPlease use one of the available keyring names above.")
        sys.exit(1)

    # Unlock collections only if needed and with user confirmation
    print("\nChecking collection lock status...")
    if not unlock_collection_once(source, source_label):
        print(f"Cannot proceed without unlocking source collection '{source_label}'.")
        sys.exit(1)

    if not unlock_collection_once(destination, destination_label):
        print(f"Cannot proceed without unlocking destination collection '{destination_label}'.")
        sys.exit(1)

    # Migrate items
    print(f"\nMigrating items from '{source_label}' to '{destination_label}'...")
    migrated_count = 0
    failed_count = 0

    for item in source.get_all_items():
        try:
            label = item.get_label()
            attrs = item.get_attributes()
            secret = item.get_secret()

            print(f"Migrating: {label}")
            destination.create_item(label, attrs, secret, replace=True)
            migrated_count += 1
        except Exception as e:
            print(f"Failed to migrate '{label}': {e}")
            failed_count += 1

    print(f"\nMigration complete.")
    print(f"Successfully migrated: {migrated_count} items")
    if failed_count > 0:
        print(f"Failed to migrate: {failed_count} items")


def interactive_mode():
    """Interactive mode to select keyrings."""
    print("=== Keyring Migration Tool ===")
    print("This tool migrates secrets from one keyring to another.\n")

    try:
        bus = secretstorage.dbus_init()
    except Exception as e:
        print(f"Error initializing D-Bus connection: {e}")
        print("Make sure you're running in a session with D-Bus access.")
        sys.exit(1)

    # List available keyrings
    available = list_all_collections(bus)

    if len(available) < 2:
        print("\nError: You need at least 2 keyrings to perform migration.")
        sys.exit(1)

    # Select source
    print("\nSelect source keyring (number):")
    try:
        source_idx = int(input("Source: ")) - 1
        if source_idx < 0 or source_idx >= len(available):
            print("Invalid selection.")
            sys.exit(1)
        source_label = available[source_idx]
    except ValueError:
        print("Invalid input.")
        sys.exit(1)

    # Select destination
    print("\nSelect destination keyring (number):")
    try:
        dest_idx = int(input("Destination: ")) - 1
        if dest_idx < 0 or dest_idx >= len(available):
            print("Invalid selection.")
            sys.exit(1)
        destination_label = available[dest_idx]
    except ValueError:
        print("Invalid input.")
        sys.exit(1)

    if source_label == destination_label:
        print("\nError: Source and destination cannot be the same.")
        sys.exit(1)

    print(f"\nMigrating from '{source_label}' to '{destination_label}'")
    confirm = input("Continue? (y/n): ").lower()
    if confirm == "y":
        migrate_items(source_label, destination_label)
    else:
        print("Migration cancelled.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == "--list":
            # List mode
            print("=== Available Keyrings ===\n")
            try:
                bus = secretstorage.dbus_init()
                list_all_collections(bus)
            except Exception as e:
                print(f"Error: {e}")
            sys.exit(0)

        # Migration with specified keyrings
        source_label = sys.argv[1]
        destination_label = sys.argv[2] if len(sys.argv) > 2 else "Login"

        print("=== Keyring Migration Tool ===")
        print(f"Source: {source_label}")
        print(f"Destination: {destination_label}\n")

        confirm = input("Continue with migration? (y/n): ").lower()
        if confirm == "y":
            migrate_items(source_label, destination_label)
        else:
            print("Migration cancelled.")
    else:
        # Interactive mode
        interactive_mode()
