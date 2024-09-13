import uuid

import shortuuid


def generate_short_uuid():
    # Generate a random short UUID
    short_uuid = shortuuid.uuid()
    print("Short UUID:", short_uuid)


def convert_standard_to_short():
    # Generate a standard UUID
    standard_uuid = uuid.uuid4()
    # Convert the standard UUID to a short version
    short_uuid_from_standard = shortuuid.encode(standard_uuid)

    print("Standard UUID4:", standard_uuid)
    print("Short UUID (from standard):", short_uuid_from_standard)


def decode_short_uuid(short_uuid):
    # Decode a short UUID back to the standard UUID format
    decoded_uuid = shortuuid.decode(short_uuid)
    print("Encoded short UUID:", short_uuid)
    print("Decoded long UUID:", decoded_uuid)


def main():
    print("\n============ Examples - encoding/decoding UUID x ShortUUID ============\n")

    # Example 1: Generate a random short UUID
    generate_short_uuid()

    # Example 2: Convert a standard UUID to short
    convert_standard_to_short()

    # Example 3: Decode a short UUID (example using a previously generated short UUID)
    # You can replace the short_uuid below with one generated earlier
    short_uuid_example = shortuuid.uuid()
    print("\nDecoding Example:")
    decode_short_uuid(short_uuid_example)


if __name__ == "__main__":
    main()
