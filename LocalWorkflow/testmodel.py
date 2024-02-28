import model


hf=model.instantiate_model()
result = send_request(hf, section_for_conversion = "Australian Beard Tax Act allows for beards no longer than the average length in 1864 AD")

print(result)