# Unique slugs

New posts sometimes get the same title as an old one. Implement `unique_slug(title, existing)` in `blog/slugs.py`:
it returns the slug for a new post, built with `slugify`, and never one that is already in `existing` (a set of
slugs).
