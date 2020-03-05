
body_settings_sourcecode = {
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 2,
    "analysis": {
      "char_filter": {
          "number_filter": {
             "type": "pattern_replace",
             "pattern": "\\d+",
             "replacement": ""
          },
          "one_char_filter": {
             "type": "pattern_replace",
             "pattern": "(^|\\s+)\\w(?=\\s+|$)",
             "replacement": " "
          }
       },
      "tokenizer": {
        "source_tokenizer": {
          "type":       "pattern",
          "pattern":    "[\\-\\!\\,\\%\\&\\(\\)\\*\\+\\<\\=\\>\\?\\@\\[\\]\\^\\;\\:\\{\\|\\}\\~]|\\s|\\n"
        }
      },
      "analyzer": {
        "source_analyzer": {
          "type":      "custom",
          "tokenizer": "source_tokenizer",
          "lowercase": False,
          "char_filter": [
                  "number_filter", "one_char_filter"
           ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
        "date_modified": {
            "type": "date"
        },
        "sourcecode": {
          "type": "text",
          "analyzer": "source_analyzer",
        "fielddata": True
        },
        "filename": {
          "type": "keyword"
        },
        "path": {
          "type": "keyword"
        }
    }
  }
}
