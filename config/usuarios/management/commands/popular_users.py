import csv
import random
import unicodedata
from django.core.management.base import BaseCommand
from usuarios.models import Usuario

class Command(BaseCommand):
    help = 'Importa usuários a partir de um arquivo CSV'

    def add_arguments(self, parser):
        # Define que o comando recebe um argumento (o caminho do arquivo)
        parser.add_argument('arquivo_csv', type=str, help='Caminho completo para o arquivo CSV')

    def handle(self, *args, **options):
        from django.db import transaction
        
        arquivo = options['arquivo_csv']
        
        def normalizar_chave(chave):
            # Remove acentos, converte para minúsculas e troca espaços por underscores
            nfkd = unicodedata.normalize('NFKD', chave)
            sem_acentos = ''.join([c for c in nfkd if not unicodedata.combining(c)])
            return sem_acentos.lower().strip().replace(' ', '_')

        try:
            with open(arquivo, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                with transaction.atomic():
                    cont_criados = 0
                    for row in reader:
                        # Normaliza todas as chaves da linha para facilitar o acesso
                        row_norm = {normalizar_chave(k): v for k, v in row.items()}
                        
                        cpf = row_norm.get('cpf')
                        
                        # Se não houver CPF, gera um valor aleatório único
                        if not cpf:
                            import uuid
                            cpf = str(uuid.uuid4().int)[:11]
                        
                        # Remove caracteres não numéricos do CPF se existirem
                        cpf = ''.join(filter(str.isdigit, str(cpf)))
                        
                        if not Usuario.objects.filter(cpf=cpf).exists():
                            # Se não houver matrícula, usa o CPF como fallback
                            matricula = row_norm.get('matricula') or cpf
                            
                            # Define um username: matrícula se disponível, senão user_<cpf>
                            username = str(matricula) if matricula else f"user_{cpf}"
                            
                            # Garante que o username é único
                            if Usuario.objects.filter(username=username).exists():
                                username = f"{username}_{random.randint(100, 999)}"

                            nome = row_norm.get('nome') or username
                            email = row_norm.get('email') or f"{username}@gfrota.com"

                            Usuario.objects.create_user(
                                username=username,
                                email=email,
                                password=cpf, # CPF inicial como senha
                                first_name=nome[:30], # Limita tamanho do primeiro nome
                                last_name=row_norm.get('sobrenome', ''),
                                cpf=cpf,
                                nome_completo=row_norm.get('nome_completo') or nome,
                                matricula=matricula,
                                nome_guerra=row_norm.get('nome_guerra') or nome.split()[0]
                            )
                            cont_criados += 1
                    
            self.stdout.write(self.style.SUCCESS(f'Sucesso! {cont_criados} usuários importados.'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Arquivo não encontrado: {arquivo}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro durante a importação: {str(e)}'))