import json

from IPython.core.interactiveshell import InteractiveShell

from version_information.version_information import VersionInformation


def make_version_information():
    shell = InteractiveShell.instance()
    result = VersionInformation(shell=shell)
    result.packages = [
        ("Python", "3.14.4"),
        ("example", "1.2.3"),
    ]
    return result


def test_html_is_the_automatic_notebook_representation():
    result = make_version_information()
    formatted, metadata = (
        InteractiveShell.instance().display_formatter.format(result)
    )

    assert "text/html" in formatted
    assert "application/json" not in formatted
    assert "<table>" in formatted["text/html"]


def test_html_escapes_names_and_versions():
    result = make_version_information()
    result.packages = [
        ("A & <B>", '<script>alert("x")</script>'),
    ]

    rendered = result._repr_html_()

    assert "A &amp; &lt;B&gt;" in rendered
    assert "&lt;script&gt;" in rendered
    assert "<script>" not in rendered
    assert "&quot;x&quot;" in rendered


def test_to_dict_preserves_json_structure():
    result = make_version_information()

    assert result.to_dict() == {
        "Software versions": [
            {"module": "Python", "version": "3.14.4"},
            {"module": "example", "version": "1.2.3"},
        ]
    }


def test_to_json_is_serializable():
    result = make_version_information()

    assert json.loads(result.to_json(indent=2)) == result.to_dict()


def test_json_is_not_an_automatic_display_hook():
    assert not hasattr(VersionInformation, "_repr_json_")
