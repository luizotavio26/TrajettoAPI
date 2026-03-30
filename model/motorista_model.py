from config import db

class Motoristas(db.Model):
    __tablename__ = "Motoristas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(15), nullable=False)
    rg = db.Column(db.String(15), nullable=False)
    salario = db.Column(db.Float, nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    numero_cnh = db.Column(db.String(20), nullable=False)
    categoria_cnh = db.Column(db.String(10), nullable=False)
    validade_cnh = db.Column(db.String(10), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    cep = db.Column(db.String(9), nullable=False)
    logradouro = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    complemento = db.Column(db.String(50), nullable=True)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    
    # chaves estrangeiras
    usuario_id = db.Column(db.Integer, db.ForeignKey("Usuarios.id"), nullable=False)

    usuario = db.relationship("Usuarios", back_populates="motorista")
    manifestos = db.relationship("ManifestoCarga", back_populates="motorista")
    
    def __init__(self,nome, cpf, rg, salario, data_nascimento, numero_cnh, categoria_cnh, validade_cnh, telefone, email, cep, logradouro, numero, complemento, bairro, cidade, estado, usuario_id):
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        self.salario = salario
        self.data_nascimento = data_nascimento
        self.numero_cnh = numero_cnh
        self.categoria_cnh = categoria_cnh
        self.validade_cnh = validade_cnh
        self.telefone = telefone
        self.email = email
        self.cep = cep
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.usuario_id = usuario_id

    def to_dict(self): 
        return {
                "id": self.id,
                "nome": self.nome,
                "cpf": self.cpf, 
                "rg" : self.rg,
                "salario": self.salario,
                "data_nascimento": self.data_nascimento,
                "numero_cnh" : self.numero_cnh,
                "categoria_cnh": self.categoria_cnh,
                "validade_cnh": self.validade_cnh,
                "telefone" : self.telefone, 
                "email": self.email,
                "cep" : self.cep ,
                "logradouro" : self.logradouro,
                "numero" : self.numero,
                "complemento" : self.complemento,
                "bairro" : self.bairro,
                "cidade" : self.cidade,
                "estado" : self.estado,
                "usuario_id": self.usuario_id} 


class MotoristaNaoEncontrado(Exception):
    pass


def create_motorista(motorista):
    novo_motorista = Motoristas(
        nome = motorista["nome"],
        cpf = motorista["cpf"], 
        rg = motorista["rg"],
        salario = motorista["salario"],
        data_nascimento = motorista['data_nascimento'],
        numero_cnh = motorista["numero_cnh"],
        categoria_cnh = motorista["categoria_cnh"],
        validade_cnh = motorista["validade_cnh"], 
        telefone = motorista["telefone"],
        email = motorista["email"],
        cep = motorista["cep"],
        logradouro = motorista["logradouro"],
        numero = motorista["numero"],
        complemento = motorista["complemento"],
        bairro = motorista["bairro"],
        cidade = motorista["cidade"],
        estado = motorista["estado"],
        usuario_id = motorista["usuario_id"]
    )

    db.session.add(novo_motorista)
    db.session.commit()
    return novo_motorista.to_dict(), None



def read_motorista_id(id_motorista):
    motorista = Motoristas.query.get(id_motorista)
    if not motorista:
        return {"message": "Nenhum motorista encontrado"}
    else:
        return motorista.to_dict()


def update_motorista(id_motorista, dados_atualizados):
    motorista = Motoristas.query.get(id_motorista)
    if not motorista:
        return {"message": "Nenhum motorista encontrado"}
    else:
        motorista.nome = dados_atualizados["nome"]
        motorista.cpf = dados_atualizados["cpf"]
        motorista.rg = dados_atualizados["rg"]
        motorista.salario = dados_atualizados["salario"]
        motorista.data_nascimento = dados_atualizados["data_nascimento"]
        motorista.numero_cnh = dados_atualizados["numero_cnh"]
        motorista.categoria_cnh = dados_atualizados["categoria_cnh"]
        motorista.validade_cnh = dados_atualizados["validade_cnh"]
        motorista.telefone = dados_atualizados["telefone"]
        motorista.email = dados_atualizados["email"]
        motorista.cep = dados_atualizados["cep"]
        motorista.logradouro =  dados_atualizados["logradouro"]
        motorista.numero = dados_atualizados["numero"]
        motorista.complemento = dados_atualizados["complemento"]
        motorista.bairro = dados_atualizados["bairro"]
        motorista.cidade = dados_atualizados["cidade"]
        motorista.estado = dados_atualizados["estado"]
        motorista.usuario_id = dados_atualizados["usuario_id"]

        db.session.commit()
        return {"message": "Informações atualizadas com sucesso"}


def delete_motorista_id(id_motorista):
    motorista = Motoristas.query.get(id_motorista)
    if not motorista:
        return MotoristaNaoEncontrado(f"Motorista não encontrado")
    else:
        db.session.delete(motorista)
        db.session.commit()
        return {"message": "Motorista deletado com sucesso"}, None


def delete_todos_motoristas():
    db.session.query(Motoristas).delete()
    db.session.commit()
    return {"message": "Todos os motoristas deletados com sucesso"}, None

