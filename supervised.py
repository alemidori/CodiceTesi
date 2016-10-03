import textrazor

textrazor.api_key = "d62cbd9970ef9077fda7db949108f528810bd5ea6047c832eea33c8c"

client = textrazor.TextRazor(extractors=["entities", "topics"])
response = client.analyze_url("http://www.bbc.co.uk/news/uk-politics-18640916")

for entity in response.entities():
    print(entity.id, entity.relevance_score, entity.confidence_score, entity.freebase_types)

