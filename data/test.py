from requests import get, delete

print(get('http://localhost:5000/api/trans').json())
print(get('http://localhost:5000/api/trans/2').json())
print(get('http://localhost:5000/api/trans/999').json())
print(get('http://localhost:5000/api/trans/6').json())
print(get('http://localhost:5000/api/trans/q').json())
print(delete('http://localhost:5000/api/trans/999').json())
print(delete('http://localhost:5000/api/trans/10').json())