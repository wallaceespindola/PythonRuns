"""
Summary of Python's pickle Module

The pickle module in Python is used for serializing and deserializing Python objects.
Serialization refers to converting a Python object into a byte stream, and deserialization is the reverse process of converting the byte stream back into a Python object. Here are the key points about the pickle module:

# Purpose:

Serialization: Convert Python objects into a format that can be stored on disk or transmitted over a network.
Deserialization: Reconstruct the Python objects from the stored or transmitted format.

# Usage:

Dumping (Serialization): Use pickle.dump(obj, file) to serialize obj and write it to file.
Loading (Deserialization): Use pickle.load(file) to read the serialized object from file and deserialize it.

# Functions:

pickle.dump(obj, file, protocol=None, *, fix_imports=True): Serializes obj and writes it to file.
pickle.load(file, *, fix_imports=True, encoding="ASCII", errors="strict"): Reads a pickled object from file and returns it.
pickle.dumps(obj, protocol=None, *, fix_imports=True): Returns the pickled representation of obj as a bytes object.
pickle.loads(bytes_object, *, fix_imports=True, encoding="ASCII", errors="strict"): Deserializes bytes_object and returns the corresponding object.

# Protocols:

Protocol 0: Original ASCII protocol, backwards compatible with earlier versions of Python.
Protocol 1: Older binary format.
Protocol 2: Introduced in Python 2.3; provides more efficient pickling of new-style classes.
Protocol 3: Added in Python 3.0; supports bytes objects.
Protocol 4: Added in Python 3.4; allows for very large objects and more types.
Protocol 5: Added in Python 3.8; offers improvements for out-of-band data.

# Security Considerations:

The pickle module is not secure against erroneous or maliciously constructed data. Only unpickle data you trust.
Use safer alternatives like json for serializing data if security is a concern.

#Common Use Cases:

Saving program state or configuration.
Sending data between processes or over the network.
Storing complex data structures like lists, dictionaries, or custom objects.

# Examples:

1) Serialize to a file:

import pickle

data = {'key': 'value'}
with open('data.pkl', 'wb') as f:
    pickle.dump(data, f)

2) Deserialize from a file:

with open('data.pkl', 'rb') as f:
    data = pickle.load(f)
print(data)
"""
import pickle


def save_text_to_pickle(file_name, text_data):
    """
    Save the given text data to a pickle file.

    :param file_name: The name of the file to save the text data to.
    :param text_data: The text data to be saved.
    """
    with open(file_name, 'wb') as file:
        pickle.dump(text_data, file)
    print(f"Text data has been pickled and saved to '{file_name}'.")


def load_text_from_pickle(file_name):
    """
    Load text data from a pickle file.

    :param file_name: The name of the file to load the text data from.
    :return: The loaded text data.
    """
    with open(file_name, 'rb') as file:
        text_data = pickle.load(file)
    print(f"Loaded text data from '{file_name}': {text_data}")
    return text_data


# Example usage
if __name__ == "__main__":
    text_to_save = "Hello, this is some text that will be pickled."
    pickle_file_name = 'text_data.pkl'

    # Save the text data to a pickle file
    save_text_to_pickle(pickle_file_name, text_to_save)

    # Load the text data from the pickle file
    loaded_text = load_text_from_pickle(pickle_file_name)
