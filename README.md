# Subtitle Finder 

Main credit for [SubSource](https://subsource.net/)

Create venv
```sh
python -m venv venv
```

Activate
```sh
source venv/bin/activate
```

Install requirements
```sh
pip install -r requirements.txt
```

Run on port 8004
```sh
uvicorn main:app --reload --port 8004
```


TODOS;
- [ ] Fit for TVSeries
- [ ] Download subtitle without releaseYear
- [ ] Docker
