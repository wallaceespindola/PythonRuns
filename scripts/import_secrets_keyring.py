# Before starting, pip install secretstorage

import secretstorage

def get_collection_by_label(bus, label):
    for collection in secretstorage.get_all_collections(bus):
        if collection.get_label() == label:
            return collection
    raise ValueError(f"Collection '{label}' not found")

def migrate_items(source_label, destination_label):
    bus = secretstorage.dbus_init()

    # Find source and destination collections
    source = get_collection_by_label(bus, source_label)
    destination = get_collection_by_label(bus, destination_label)

    # Unlock collections if needed
    if source.is_locked():
        source.unlock()
    if destination.is_locked():
        destination.unlock()

    for item in source.get_all_items():
        label = item.get_label()
        attrs = item.get_attributes()
        secret = item.get_secret()

        print(f"Migrating: {label}")
        destination.create_item(label, attrs, secret, replace=True)

    print("Migration complete.")

if __name__ == "__main__":
    migrate_items("Default keyring", "Login")
