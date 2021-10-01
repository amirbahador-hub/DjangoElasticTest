from elasticsearch_dsl import analyzer, analysis, tokenizer


shingle_filter = analysis.token_filter('shingle_filter', type="shingle",
                                       min_shingle_size=2, max_shingle_size=3, )
# edge_ngram_filter = analysis.token_filter('edge_ngram_filter', type="edgeNGram", side="front",
#                                                      min_gram=1, max_gram=15,)

completion_filter = analysis.token_filter('edge_ngram_filter', type="edgeNGram",
                                          min_gram=1, max_gram=15, )

auto_token = tokenizer('autocomplete', type="edgeNGram", token_chars="letter",
                       min_gram=2, max_gram=10, )

auto_complete = analysis.analyzer(
    'auto_complete',
    tokenizer=auto_token,
    filter=["lowercase"],
)
reverse = analyzer(
    'reverse',
    type="custom",
    tokenizer="standard",
    filter=["lowercase", "reverse"],
)
shingle = analyzer(
    'shingle',
    type="custom",
    tokenizer="standard",
    filter=["lowercase", shingle_filter, ],
)

whitespace_analyzer = analysis.analyzer(
    'whitespace_analyzer',
    tokenizer="keyword",
)
autocomplete_search = analyzer(
    'autocomplete_search',
    tokenizer="whitespace",
)

html_strip = analyzer('html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)