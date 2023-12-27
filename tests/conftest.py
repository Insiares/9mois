import pytest
from modules.build_corpus import init_api, concatenate_row_values
from modules.build_corpus import load_stop_words
from modules.search import search, load_corpus, load_vect
from modules.db import process_table, connect_db
import os


@pytest.fixture
def database_connection():
    engine, metadata = connect_db()
    yield engine, metadata


def test_connect_db(database_connection):
    engine, metadata = database_connection

    try:
        # Ensure the engine is valid
        assert engine.connect()
    except Exception as e:
        pytest.fail(f"Failed to connect to the database: {e}")


def test_process_table(database_connection):
    engine, metadata = database_connection
    table_name = "recipes"

    result_set = process_table(engine, metadata, table_name)

    assert isinstance(result_set, list)
    assert len(result_set) > 0  # Ensure that the result set is not empty


@pytest.fixture
def test_list():
    mock_list = ["ai", "des", "nausées", "et", "je", "manque", "de", "fer"]
    yield mock_list


def test_concat(test_list):
    result = concatenate_row_values(test_list)
    assert result == "aidesnauséesetjemanquedefer"


@pytest.fixture
def stop_words():
    stop_list = load_stop_words("./data/stop_words_french.json")
    yield stop_list


def test_stop_words(stop_words):
    words = stop_words
    assert len(words) > 0
    assert words[-3] == "voient"


@pytest.fixture
def ini_data():
    data = init_api()
    yield data


def test_init(ini_data):
    data = ini_data

    assert len(data) == 4
    assert isinstance(data, dict)


def test_file_exists():
    file_path1 = "./data/questions.npy"
    file_path2 = "./ML/articles.sav"
    assert os.path.exists(file_path1)
    assert os.path.exists(file_path2)


def test_vect_load():
    vect = load_vect()
    assert len(vect) == 4
    assert isinstance(vect, dict)


def test_corpus_load():
    corpus = load_corpus()
    assert len(corpus) == 4
    assert isinstance(corpus, dict)


@pytest.fixture
def recherche():
    data = init_api()
    corpus = load_corpus()
    vect = load_vect()
    result = search("crevette", data, corpus, vect, "food")
    yield result


def test_search(recherche):
    res = recherche

    assert isinstance(res, list)
    assert res[0] == (
        0.5424475628741318,
        (
            "25584",
            "Nem aux crevettes ou crabe",
            0,
            "/images/food/25584_nem_crevettes.png",
            4,
            "1207",
        ),
    )
