import re


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def unique_slug(title, existing):
    """Slug for a new post that does not clash with existing slugs."""
    raise NotImplementedError
