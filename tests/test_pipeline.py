

from unittest.mock import patch

from simple_rag.pipeline import fetch_html_as_raw_text


@patch("httpx.get")
def test_fetch_html_as_docs_default_urls(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html><body><p>Test</p></body></html>"
    fetch_html_as_raw_text()
    assert mock_get.call_count == 3
    assert mock_get.call_args_list[0][0][0] == "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"
    assert mock_get.call_args_list[1][0][0] == "https://en.wikipedia.org/wiki/Vector_database"
    assert mock_get.call_args_list[2][0][0] == "https://en.wikipedia.org/wiki/Information_retrieval"


@patch("httpx.get")
def test_fetch_html_as_docs_custom_urls(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html><body><p>Test</p></body></html>"
    fetch_html_as_raw_text(source_urls=["https://en.wikipedia.org/wiki/Test"])
    assert mock_get.call_count == 1
    assert mock_get.call_args_list[0][0][0] == "https://en.wikipedia.org/wiki/Test"
