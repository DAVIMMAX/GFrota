from django.test import TestCase
from .models import Usuario, Orgao, Cargo, Role, Funcao

# Create your tests here.

class CargoTestCase(TestCase):  
    def setUp(self):
        self.orgao = Orgao.objects.create(nome='testorgao')
        self.cargo = Cargo.objects.create(nome='testcargo', orgao_id=self.orgao)

    def test_cargo_creation(self):
        self.assertEqual(self.cargo.nome, 'testcargo')
        self.assertEqual(self.cargo.orgao_id.nome, 'testorgao')

class OrgaoTestCase(TestCase):
    def setUp(self):
        self.orgao = Orgao.objects.create(nome='testorgao')

    def test_orgao_creation(self):
        self.assertEqual(self.orgao.nome, 'testorgao')

class RoleTestCase(TestCase):
    def setUp(self):
        self.role = Role.objects.create(nome='testrole')

    def test_role_creation(self):
        self.assertEqual(self.role.nome, 'testrole')

class FuncaoTestCase(TestCase):
    def setUp(self):
        self.funcao = Funcao.objects.create(nome='testfuncao')

    def test_funcao_creation(self):
        self.role = Role.objects.create(nome='testrole')
        self.funcao.roles.add(self.role)
        self.assertEqual(self.funcao.nome, 'testfuncao')
        self.assertEqual(self.funcao.usuarios.count(), 0)

class UsuarioTestCase(TestCase):
    def setUp(self):
        self.orgao = Orgao.objects.create(nome='testorgao')
        self.cargo = Cargo.objects.create(nome='testcargo', orgao_id=self.orgao)
        self.role = Role.objects.create(nome='testrole')
        self.funcao = Funcao.objects.create(nome='testfuncao')
        self.funcao.roles.add(self.role)
        self.usuario = Usuario.objects.create_user(
            username='testuser', 
            password='password', 
            cpf='12345678901', 
            nome_completo='testuser', 
            email='test@example.com', 
            matricula='123456', 
            nome_guerra='test',
            orgao_id=self.orgao, 
            cargo=self.cargo, 
            funcao=self.funcao
        )

    def test_usuario_creation(self):
        self.assertEqual(self.usuario.username, 'testuser')
        self.assertTrue(self.usuario.check_password('password'))
        self.assertEqual(self.usuario.cpf, '12345678901')
