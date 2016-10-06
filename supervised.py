import textrazor

textrazor.api_key = "d62cbd9970ef9077fda7db949108f528810bd5ea6047c832eea33c8c"

client = textrazor.TextRazor(extractors=["words", "entities", "entailments", "relations"])

def process(string):
    final = []
    typeslist = []
    print(string)
    response = client.analyze(string)

    for entity in response.entities():
        print(entity.id, entity.freebase_types)
        for type in entity.freebase_types:
            string_type = str(type).split('/')
            typeslist.append(string_type)
            #print(string_type)


    #print(typeslist)
    flat = sum(typeslist, [])
    flat = [elem for elem in flat if elem]
    typesset = list(set(flat))
    #print(typesset)

    typesstring = " ".join(typesset)
    responseontypes = client.analyze(typesstring)


    return final