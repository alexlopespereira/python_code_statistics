
body_settings_generic = {
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 2,
    "analysis": {
      "analyzer": {
        "source_analyzer": {
          "type":      "pattern",
          "pattern":   "[\\,%&.()*+<=>?@[\]^:{|}~]|\\s|\\n",
        }
      }
    }
  }
}
