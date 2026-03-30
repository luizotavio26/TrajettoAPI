from config import db
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
import secrets
import jwt
import datetime
from model.manifesto_model import ManifestoCarga
from model.motorista_model import Motoristas
from model.cliente_model import Clientes
from model.veiculos_model import Veiculos
from math import floor

#Classe admin
class Administradores(db.Model):

    __tablename__ = "Administradores"   
     
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(50), nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False)

    '''
    motorista = db.relationship("Motoristas", back_populates="usuario")
    veiculo = db.relationship("Veiculos", back_populates="usuario")
    cliente = db.relationship("Clientes", back_populates="usuario")
    manifestos = db.relationship("ManifestoCarga", back_populates="usuario")
    '''
    
    
    def __init__(self, nome_usuario, email, senha):
        self.nome_usuario = nome_usuario
        self.email = email
        self.senha = senha


    def to_dict(self): 
        return {
                "id": self.id,
                "nome_usuario": self.nome_usuario ,
                "email" : self.email,
                "senha" : self.senha}

class AdminNaoEncontrado(Exception):
    pass

class ErroValidacao(Exception):
    pass

#-------------------------
# ROTAS DA ENTIDADE ADMIN
#-------------------------
def getAdmin():
    admin  = Administradores.query.all()   
    return [admin.to_dict() for admin in admins]

def getAdminId(admin):
    admin = Administradores.query.get(admin)
    if not admin:
        raise AdminNaoEncontrado
    
    return admin.to_dict()

def putAdminPorId(adminId, dados):
    admin = Administradores.query.get(adminId)

    if not admin:
        raise AdminoNaoEncontrado
    
    admin.nome_usuario = dados.get("nome_usuario", admin.nome_usuario)
    admin.email = dados.get("email", admin.email)
    admin.senha = dados.get("senha", admin.senha)
    
    
    db.session.commit()
    return {"message": "admin com ID {adminId} atualizado com sucesso."}

def deleteAdminPorId(adminId):
    admin = Administradores.query.get(adminId)
    
    if admin:
        db.session.delete(admin)
        db.session.commit()
        return {"message":"admin com ID {adminId} deletado com sucesso."}
    
    return {"message":"admin com ID {adminId} não encontrado."}

# CADASTRO E LOGIN DE ADMIN COM TOKEN
def postAdmin(dados):
    try:
        if Administradores.query.filter_by(email=dados.get('email')).first():
            return None, "E-mail já cadastrado no sistema."
        
        if Administradores.query.filter_by(nome_usuario=dados.get('nome_usuario')).first():
            return None, "Nome de admin não disponível"

        novo_admin = Administradores(
            email = dados["email"],
            senha = dados["senha"],
            nome_usuario = dados["nome_usuario"],
        )
        
        db.session.add(novo_admin)
        db.session.commit()
        
        return novo_admin.id, None
    
    except IntegrityError as e:
        db.session.rollback()
        
        if 'usuarios_email_key' in str(e):
            return None, "Erro: E-mail já cadastrado no sistema."

        if "usuarios_nome_usuario_key" in str(e):
            return None, "Erro: Nome de admin ja existe no sistema."

        return None, "Erro de integridade dos dados."
        
    except Exception as e:
        db.session.rollback()
        return None, f"Erro interno ao cadastrar: {str(e)}"

def verificaSenhaEmail(dados):
    admin = Administradores.query.filter_by(email=dados["email"]).first()

    # SECRET_KEY
    SECRET_KEY = "ytskryo"

    if admin.email is None:
        return {"message": "registro não encontrado, faça seu cadastro"}

    elif admin.nome_usuario is None:
        return {"message": "registro não encontrado"}
    
    else:
        if dados["senha"] != admin.senha:
            return {"message": "senha invalida"}

        else:
            token = jwt.encode(
            {"email": admin.email, 
            "nome_usuario": admin.nome_usuario,
            "id_usuario": admin.id,
            "isAdmin":True,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256"
            )
            
            return ({"message": "Login realizado com sucesso", "token": token,"success": True})

def esqueciSenha(dados):
    admin = Administradores.query.filter_by(email=dados["email"]).first()

    if not admin:
        raise AdminNaoEncontrado

    admin.senha = dados.get("senha", admin.senha)
    db.session.commit()

    return {"success": True, "message": "Senha alterada com sucesso"}

#------------------------------------------------------------------------
# ROTAS PARA ACESSAR OUTRAS ENTIDADES
#------------------------------------------------------------------------
def getClientes():
    clientes  = Clientes.query.all()   
    return [cliente.to_dict() for cliente in clientes]

def read_todas_cargas():
    cargas = ManifestoCarga.query.all()
    print(cargas)
    return [carga.to_dict() for carga in cargas], None

def read_todos_motorista():
    motoristas  = Motoristas.query.all()   
    return [motorista.to_dict() for motorista in motoristas], None

def getUsuarios():
    usuarios  = Usuarios.query.all()   
    return [usuario.to_dict() for usuario in usuarios]

def getVeiculos():
    veiculos  = Veiculos.query.all()   
    return [v.to_dict() for v in veiculos], None 


# -------------------------
# ROTAS PARA O DASHBOARD
# -------------------------

def cargasCadastradas():
    quantidade_cargas = ManifestoCarga.query.filter_by().count()
    return ({"Cargas Totais": quantidade_cargas})

def motoristasCadastrados():
    quantidade_motoristas = Motoristas.query.filter_by().count()
    return ({"Motoristas Totais": quantidade_motoristas})

def clientesCadastrados():
    quantidade_clientes = Clientes.query.filter_by().count()
    return ({"Clientes Totais": quantidade_clientes})

def veiculosCadastrados():
    quantidade_veiculos = Veiculos.query.filter_by().count()
    return ({"Veiculos Totais": quantidade_veiculos})

"""
#Acho que isso pode ser visto depois, para pedir o valor cobrado por todos os fretes

def totaisCargas():
    cargas = ManifestoCarga.query.filter_by().all()

    total_frete = 0
    total_km = 0

    for c in cargas:
        # Tratando valor_frete
        if c.valor_frete:
            if isinstance(c.valor_frete, str):
                valor = c.valor_frete.replace("R$ ", "").replace(".", "").replace(",", ".")
                total_frete += float(valor)
            else:  # já é float ou int
                total_frete += c.valor_frete

        # Tratando distancia
        if c.distancia:
            if isinstance(c.distancia, str):
                valor = c.distancia.replace(" km", "").replace(",", ".")
                total_km += float(valor)
            else:  # já é float ou int
                total_km += c.distancia

    return {"TotalFrete": total_frete, "TotalKM": total_km}


#funções pro calculo de faturamento
valor_diesel = 6.06
consumo_medio = 2.5
pedagio_base = 3.5


def parse_moeda(valor):
    if isinstance(valor, str):
        valor = (
            valor.replace("R$ ", "")
            .replace(".", "")
            .replace(",", ".")
        )
    return float(valor)


def parse_km(valor):
    if isinstance(valor, str):
        valor = (
            valor.replace(" km", "")
            .replace(",", ".")
        )
    return float(valor)


def calcular_pedagio(km):
    if km <= 60:
        return 0.0
    extra = km - 60
    return floor(extra / 15) * pedagio_base

def faturamento(usuario_id):
    cargas = ManifestoCarga.query.filter_by(usuario_id=usuario_id).all()
    motoristas = Motoristas.query.filter_by(usuario_id=usuario_id).all()

    total_km = 0.0
    total_combustivel = 0.0
    total_pedagios = 0.0
    total_bruto = 0.0
    total_salarios = 0.0

    # ------------------------------------------------------
    # SOMATÓRIO DE SALÁRIOS (equivalente ao reduce JS)
    # ------------------------------------------------------
    for m in motoristas:
        if m.salario:
            try:
                salario = parse_moeda(m.salario)
                total_salarios += salario
            except:
                pass

    # ------------------------------------------------------
    # PROCESSAMENTO DAS CARGAS (equivalente ao map/filter JS)
    # ------------------------------------------------------
    dados_faturamento = []

    for c in cargas:
        # validar existencia dos campos
        if not (c.valor_frete and c.distancia):
            continue

        km = parse_km(c.distancia)
        valor_frete = parse_moeda(c.valor_frete)

        # cálculos equivalentes ao JavaScript
        litros = km / consumo_medio
        combustivel = litros * valor_diesel
        pedagios = calcular_pedagio(km)

        liquido_sem_salario = valor_frete - combustivel - pedagios

        # acumula totais globais
        total_km += km
        total_combustivel += combustivel
        total_pedagios += pedagios
        total_bruto += valor_frete

        dados_faturamento.append({
            "nome": c.destino_carga,
            "bruto": valor_frete,
            "liquido": liquido_sem_salario
        })

    # ------------------------------------------------------
    # TOTAL LÍQUIDO FINAL (igual ao JS)
    # ------------------------------------------------------
    total_liquido = total_bruto - total_combustivel - total_pedagios - total_salarios

    return {
        "total_km": total_km,
        "total_combustivel": total_combustivel,
        "total_pedagios": total_pedagios,
        "total_bruto": total_bruto,
        "total_salarios": total_salarios,
        "total_liquido": total_liquido,
        "detalhado": dados_faturamento
    }

"""



