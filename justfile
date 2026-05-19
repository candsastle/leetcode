run:
    uv run src/main.py

publish msg:
    git add . && git commit -m "{{msg}}" && git push
