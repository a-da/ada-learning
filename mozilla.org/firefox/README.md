# Problem

Firefox bookmarks have limited feature.

Use case:

1. When search for youtube bookmarks it will provide a flat list.
2. It is hard to understand in which folder is located the item.

# Solution

Connect to storages of the bookmarks and apply fulfill the goals programatically.
To make it with a script in Rust or Python.

# Documentation resources

1. Find the location of the sqlite database: https://en.wikiversity.org/wiki/Firefox#Profiles. 
2. Relational schema for places.sqlite: https://wiki.mozilla.org/images/d/d5/Places.sqlite.schema3.pdf
