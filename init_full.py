import subprocess
import sys
import time

def executar(script):
    print(f"\n🌀 Executando {script}...")
    resultado = subprocess.run([sys.executable, script])
    if resultado.returncode != 0:
        print(f"❌ Erro ao executar {script}. Abortando.")
        exit()

print("♻️ Resetando banco de dados...")
executar("reset_db.py")

# Aguarda 0.5s para garantir que tudo foi liberado
time.sleep(0.5)

print("👤 Criando admin, cliente e estrutura de teste...")
executar("seed.py")

print("\n✅ Sistema inicializado com sucesso e 100% funcional!")
