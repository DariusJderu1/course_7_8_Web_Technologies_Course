# Student Directory

Exercitiu pentru cursurile 7 si 8 de Tehnologii Web, anul 2026-2027.
Aplicatia Django ofera un API pentru citirea datelor despre studenti.
Datele sunt fictive si sunt pastrate in lista `STUDENTS` din `students/views.py`, nu in baza de date.

## Instalare si rulare

Este necesar Python 3.10 sau mai nou, compatibil cu versiunea Django instalata.
Dependentele sunt in `requirements.txt`.

Pe Linux / macOS, din folderul proiectului:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py test students
python manage.py runserver
```

Pe Windows PowerShell, din folderul proiectului:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py test students
python manage.py runserver
```

Daca PowerShell blocheaza activarea, foloseste `.\.venv\Scripts\python.exe` in loc de `python`, fara pasul de activare.

Deschide http://127.0.0.1:8000/api/students/ in browser. Opreste serverul cu Ctrl+C.
Ruta `/` nu este definita, deci afiseaza 404.
Comanda `migrate` creeaza tabelele standard Django; nu salveaza lista `STUDENTS` in baza de date.
Configuratia si cheia demonstrativa `SECRET_KEY` sunt doar pentru rulare locala.

## E1 - Structura proiectului

| Fisier | Rol |
| --- | --- |
| `config/settings.py` | Contine setarile proiectului: aplicatii, baza de date, limba si alte optiuni. |
| `config/urls.py` | Defineste rutele principale. Trimite cererile cu prefixul `api/` catre rutele din aplicatia `students`. |
| `students/urls.py` | Leaga adresele API-ului de functiile care le raspund. |
| `students/views.py` | Contine lista de studenti si functiile care primesc cereri si returneaza raspunsuri. |
| `students/tests.py` | Contine testele automate pentru verificarea API-ului. |

Cand primeste o cerere HTTP, Django creeaza un obiect cu datele cererii.
Cererea trece prin componentele middleware, care pot face verificari, cum ar fi protectia CSRF.
Django cauta adresa in `config/urls.py`. Pentru prefixul `api/`, continua cautarea in `students/urls.py`.
Apoi apeleaza functia asociata rutei, cu obiectul cererii si eventualele valori din URL.
De exemplu, pentru `/api/students/2/`, functia `student_detail` primeste identificatorul 2 ca numar intreg.
Functia creeaza raspunsul JSON si codul HTTP. Raspunsul trece prin middleware si este trimis clientului.

## E2 - Completarea serviciului REST

- `student_list` returneaza lista studentilor. Decoratorul `require_GET` permite numai GET; POST primeste 405.
- `student_detail` cauta identificatorul in `STUDENTS`. Returneaza studentul in format JSON cu 200 sau un mesaj cu 404 daca nu exista.
- `health` returneaza 200 si `{"status": "ok"}`.
- In `students/urls.py` sunt definite rutele pentru lista, detalii si starea serviciului.

| Cerere | Rezultat asteptat |
| --- | --- |
| GET `/api/students/` | 200 si lista studentilor |
| GET `/api/students/2/` | 200 si datele lui Radu Ionescu |
| GET `/api/students/999/` | 404, student inexistent |
| GET `/api/health/` | 200 si `{"status": "ok"}` |
| POST `/api/students/` | 405, metoda nepermisa |

## E3 - Testarea serviciului REST

Verificarea a fost facuta cu Python 3.14.4 si Django 5.2.19.
Comanda `python manage.py check` a returnat:

```text
System check identified no issues (0 silenced).
```

### Testele automate

In `students/tests.py` sunt cinci teste: lista studentilor, datele studentului 2, studentul inexistent, starea serviciului si respingerea POST.
Testul pentru health verifica atat codul 200, cat si intregul obiect JSON.

Comanda:

```sh
python manage.py test students
```

Rezultatul executarii:

```text
Creating test database for alias 'default'...
.....
----------------------------------------------------------------------
Ran 5 tests in 0.005s

OK
Destroying test database for alias 'default'...
Found 5 test(s).
System check identified no issues (0 silenced).
```

### Dovezi pentru cererile GET

Cu serverul pornit, intr-un alt terminal se pot rula aceste comenzi.
Pe Windows foloseste `curl.exe` in loc de `curl`.

```sh
curl -sS -w '\nHTTP %{http_code}\n' http://127.0.0.1:8000/api/students/
curl -sS -w '\nHTTP %{http_code}\n' http://127.0.0.1:8000/api/students/2/
curl -sS -w '\nHTTP %{http_code}\n' http://127.0.0.1:8000/api/students/999/
curl -sS -w '\nHTTP %{http_code}\n' http://127.0.0.1:8000/api/health/
```

Raspunsurile obtinute, in aceeasi ordine:

```text
{"items": [{"id": 1, "name": "Ana Popescu", "year": 3}, {"id": 2, "name": "Radu Ionescu", "year": 3}]}
HTTP 200
{"id": 2, "name": "Radu Ionescu", "year": 3}
HTTP 200
{"detail": "Studentul nu exista."}
HTTP 404
{"status": "ok"}
HTTP 200
```

### Dovada pentru POST

Pentru POST se foloseste Django Test Client, care nu verifica implicit protectia CSRF.
O cerere POST prin curl poate primi 403 de la protectia CSRF, inainte sa ajunga la functie.

Cu mediul virtual activ, deschide consola:

```sh
python manage.py shell
```

Executa:

```python
from django.test import Client, override_settings

with override_settings(ALLOWED_HOSTS=["testserver"]):
    response = Client().post("/api/students/")
    print("POST /api/students/ ->", response.status_code)
```

Apasa Enter pe o linie goala pentru a executa blocul. Rezultatul verificat:

```text
POST /api/students/ -> 405
```

Iesi din consola cu `exit()`.

## E4 - Explicarea solutiei

1. De ce este utilizata metoda HTTP GET pentru obtinerea informatiilor despre studenti?

   GET este folosita pentru citirea datelor. Cererea nu adauga, nu modifica si nu sterge studenti.

2. Care este diferenta dintre HttpResponse si JsonResponse in Django?

   HttpResponse este un raspuns general, caruia ii putem da text sau HTML. JsonResponse transforma datele Python in JSON si seteaza tipul continutului la `application/json`.

3. Cum identifica Django functia care trebuie executata pentru un anumit URL?

   Django verifica rutele din `urlpatterns`, in ordine, si foloseste prima ruta care se potriveste. Prin `include`, poate continua cautarea in alt fisier de rute. Ruta gasita indica functia de apelat.

4. De ce este potrivit codul HTTP 404 atunci cand studentul solicitat nu exista?

   404 arata ca resursa ceruta nu a fost gasita. Adresa are un format valid, dar nu exista un student cu acel identificator in lista.

## Declararea utilizarii instrumentelor de inteligenta artificiala
Declar ca am folosit instrumente de inteligenta artificiala (ChatGPT, GPT-6 Astra) pentru suport la exercitii. De exemplu intelegerea notiunilor de Django.