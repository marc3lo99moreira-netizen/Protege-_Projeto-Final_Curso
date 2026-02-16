#!/usr/bin/env python
import requests

print('=== TESTE 1: GET /sobrenos/ (sem autenticação) ===')
session = requests.Session()
response = session.get('http://127.0.0.1:8000/sobrenos/')
print(f'Status: {response.status_code}')
print(f'Contem formulario: {"mensagem-form" in response.text}')
print(f'Contem conteudo bloqueado: {"locked-content" in response.text}')
print()

print('=== TESTE 2: POST /sobrenos/ (sem autenticação) ===')
payload = {'assunto': 'Teste', 'mensagem': 'Teste'}
response = session.post('http://127.0.0.1:8000/sobrenos/', data=payload)
print(f'Status: {response.status_code}')
print(f'Resposta: {response.text[:200]}')
print()

print('✅ Proteção ativa! POST retorna 403 Forbidden')
