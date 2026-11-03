from blog.slugs import unique_slug


def test_free():
    assert unique_slug("Hello World", set()) == "hello-world"


def test_first_clash():
    assert unique_slug("Hello World", {"hello-world"}) == "hello-world-2"


def test_second_clash():
    assert unique_slug("Hello World", {"hello-world", "hello-world-2"}) == "hello-world-3"


def test_existing_posts():
    assert unique_slug("Hello, World!", {"hello-world", "hello-world-2", "hello-world-3", "release-notes"}) == "hello-world-4"


def test_other_title():
    assert unique_slug("Release Notes", {"release-notes"}) == "release-notes-2"
