```bash
~/Library/Application Support/Firefox/Profiles/d5250dys.default-release
> sqlite3 places.sqlite
sqlite> SELECT * FROM moz_places WHERE url LIKE "%youtube%" LIMIT 2;
35|https://www.youtube.com/watch?app=desktop&v=4IuE324VBBQ|Trevor Noah Calls Out Media Racism with Ukraine War - YouTube|moc.ebutuoy.www.|3|0|0|19|1655496236458083|pNiHm80Lm6mI|0|47356423415096|CBS News Reporter: "This isn't a place, with all due respect, like Iraq, Afghanistan... You know, this is a relatively civilized, relatively European city, I...|https://i.ytimg.com/vi/4IuE324VBBQ/maxresdefault.jpg||18|0||0
36|https://www.youtube.com/watch?v=ouHVkMo3gwE|How to create documentation with sphinx - YouTube|moc.ebutuoy.www.|1|0|0|-1|1713337980964732|LRFh2jo5IXKO|0|47359957631786|Sphinx is a tool that makes it easy to create intelligent and beautiful documentation.Sphinx uses reStructuredText as its markup language, and many of its st...|https://i.ytimg.com/vi/ouHVkMo3gwE/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGFsgWyhbMA8=&rs=AOn4CLDy1PgDTFhZGvXTAT8Ekk1GKPTp1A||18|0||1
```
