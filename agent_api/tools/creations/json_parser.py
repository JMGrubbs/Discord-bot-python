def print_json_key_values(json_obj):
    for key, value in json_obj.items():
        print(f"Key: {key}, Value: {value}")


# Sample JSON data for testing
sample_json = {"name": "John", "age": 30, "city": "New York"}

# Testing the function
print_json_key_values(sample_json)
