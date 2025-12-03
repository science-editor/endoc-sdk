from gql import gql

DOCUMENT_SEARCH_QUERY = gql("""
query documentSearch(
    $ranking_variable: String
    $keywords: [String]
    $paper_list: [MetadataInput]
    $ranking_collection: String
    $ranking_id_field: String
    $ranking_id_value: String
    $ranking_id_type: String
) {
    documentSearch(
    ranking_variable: $ranking_variable
    keywords: $keywords
    paper_list: $paper_list
    ranking_collection: $ranking_collection
    ranking_id_field: $ranking_id_field
    ranking_id_value: $ranking_id_value
    ranking_id_type: $ranking_id_type
    ) {
    status
    message
    response {
        search_stats {
        DurationTotalSearch
        nMatchingDocuments
        }
        paper_list {
        collection
        id_field
        id_type
        id_value
        }
        reranking_scores
        prefetching_scores
    }
    }
}
""")

PAGINATED_SEARCH_QUERY = gql("""
query paginatedSearch($paper_list: [MetadataInput]!, $keywords: [String]) {
    paginatedSearch(paper_list: $paper_list, keywords: $keywords) {
        status
        message
        response {
            _id
            DOI
            Title
            Content {
                Abstract
                Abstract_Parsed {
                    section_id
                    section_title
                    section_text {
                        paragraph_id
                        paragraph_text {
                            sentence_id
                            sentence_text
                            sentence_similarity
                            cite_spans {
                                start
                                end
                                text
                                ref_id
                            }
                        }
                    }
                }
            }
            Author {
                FamilyName
                GivenName
            }
            Venue
            PublicationDate {
                Year
                Month
                Day
                Name
            }
            id_int
            relevant_sentences
        }
    }
}
""")

SUMMARIZE_PAPER_QUERY = gql("""
query summarizePaper($paper_id: MetadataInput!) {
    summarizePaper(paper_id: $paper_id) {
        status
        message
        response {
        paragraph_id
        section_id
        sentence_id
        sentence_text
        tag
        }
    }
}
""")

SINGLE_PAPER_QUERY = gql("""
query singlePaper($paper_id: MetadataInput!) {
    singlePaper(paper_id: $paper_id) {
        status
        message
        response {
            _id
            id_int
            DOI
            Title
            Content {
                Abstract
                Abstract_Parsed {
                    section_id
                    section_title
                    section_text {
                        paragraph_id
                        paragraph_text {
                            sentence_id
                            sentence_text
                            sentence_similarity
                            cite_spans {
                                start
                                end
                                text
                                ref_id
                            }
                        }
                    }
                }
                Fullbody_Parsed {
                    section_id
                    section_title
                    section_text {
                        paragraph_id
                        paragraph_text {
                            sentence_id
                            sentence_text
                            sentence_similarity
                            cite_spans {
                                start
                                end
                                text
                                ref_id
                            }
                        }
                    }
                }
                Fullbody
            }
            Author {
                FamilyName
                GivenName
            }
            Venue
            PublicationDate {
                Year
                Month
                Day
                Name
            }
            Reference {
                Title
                Author {
                    FamilyName
                    GivenName
                }
                Venue
                PublicationDate {
                    Year
                    Month
                    Day
                    Name
                }
                ReferenceText
                PaperID {
                    collection
                    id_field
                    id_type
                    id_value
                }
            }
        }
    }
}
""")

GET_NOTE_LIBRARY_QUERY = gql("""
query getNoteLibrary($doc_id: String!) {
    getNoteLibrary(doc_id: $doc_id) {
        status
        message
        response {
            _id
            id_value
            id_field
            id_type
            id_collection
        }
    }
}
""")

TITLE_SEARCH_QUERY = gql("""
query titleSearch($titles: [String]!) {
  titleSearch(titles: $titles) {
    status
    message
    response {
      Title
      collection
      found
      id_field
      id_type
      id_value
      Author {
        FamilyName
        GivenName
      }
    }
  }
}
""")