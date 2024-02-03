if __name__=="__main__":
    doc_number = input("Give the document number for an entire act from IndianKanoon ")
    df_condition = input("Press 1 if you want the first 10 provisions, as a trial, or 2 if you want to parse the whole statute ")
    openai_key = input("Enter you openai key ")
    ik_key = input("Enter your IndianKanoon API key ")
    filename = input("Give the name you want for txt file containing the LegalRuleML code ")

    ik_key_encoded = "ik_key=" +'"' + str(ik_key)+ '"'
    openai_key_encoded = "openai_key="+'"' + str(openai_key)+ '"'

    combined_keys = ik_key_encoded + '\n' + openai_key_encoded
    
    with open("secret_key.py", "w") as file:
        file.write(combined_keys)

    import lrml_generator

    combined_output=lrml_generator.law_parser(doc_number, df_condition)

    with open(f"{filename}.txt", "w") as file2:
        file2.write(combined_output)
    
