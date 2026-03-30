from config import db

class Veiculos(db.Model):

    __tablename__ = "Veiculos"   
     
    id = db.Column(db.Integer, primary_key=True ,)
    placa = db.Column(db.String(7), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    renavan = db.Column(db.String(11), nullable=False)
    chassi = db.Column(db.String(17), nullable=False)
    cor = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    peso_maximo_kg = db.Column(db.Integer, nullable=False)
    ano_modelo = db.Column(db.String(4), nullable=False)
    ano_fabricacao = db.Column(db.String(4), nullable=False)

    # chaves estrangeiras
    usuario_id = db.Column(db.Integer, db.ForeignKey("Usuarios.id"), nullable=False)
    usuario  = db.relationship("Usuarios", back_populates="veiculo")
    manifestos = db.relationship("ManifestoCarga", back_populates="veiculo")

    def to_dict(self): 
        return {
                "id": self.id,
                "placa": self.placa ,
                "modelo": self.modelo, 
                "marca" : self.marca,  
                "renavan" : self.renavan, 
                "chassi": self.chassi,
                "cor" : self.cor, 
                "tipo" : self.tipo, 
                "peso_maximo_kg" : self.peso_maximo_kg ,
                "ano_modelo" : self.ano_modelo , 
                "ano_fabricacao" : self.ano_fabricacao,
                "usuario_id": self.usuario_id } 


class VeiculoNaoEncontrado(Exception):
    pass



def getVeiculosId(id_veiculo):
    veiculo = Veiculos.query.get(id_veiculo)
    if veiculo:
        return veiculo.to_dict()
    return {"message": "Veículo não encontrado"}, None


def getVeiculosPorPeso(peso):
    if peso <= 0:
        veiculos = Veiculos.query.all()
    else:
        veiculos = Veiculos.query.filter(Veiculos.peso_maximo_kg >= peso).all()
    return [v.to_dict() for v in veiculos], None


def postVeiculos(dados):
    novo_veiculo = Veiculos(
        placa=dados.get("placa"),
        modelo=dados.get("modelo"),
        marca=dados.get("marca"),
        renavan=dados.get("renavan"),
        chassi=dados.get("chassi"),
        cor=dados.get("cor"),
        tipo=dados.get("tipo"),
        peso_maximo_kg=dados.get("peso_maximo_kg"),
        ano_modelo=dados.get("ano_modelo"),
        ano_fabricacao=dados.get("ano_fabricacao"),
        usuario_id=dados.get("usuario_id")
    )
    
    db.session.add(novo_veiculo)
    db.session.commit()
    
    return f"Veículo {novo_veiculo.modelo} cadastrado com sucesso."


def putVeiculoPorId(id_veiculo, dados):
    veiculo = Veiculos.query.get(id_veiculo)
    
    if veiculo:
        veiculo.placa = dados.get("placa", veiculo.placa)
        veiculo.modelo = dados.get("modelo", veiculo.modelo)
        veiculo.marca = dados.get("marca", veiculo.marca)
        veiculo.renavan = dados.get("renavan", veiculo.renavan)
        veiculo.chassi = dados.get("chassi", veiculo.chassi)
        veiculo.cor = dados.get("cor", veiculo.cor)
        veiculo.tipo = dados.get("tipo", veiculo.tipo)
        veiculo.peso_maximo_kg = dados.get("peso_maximo_kg", veiculo.peso_maximo_kg)
        veiculo.ano_modelo = dados.get("ano_modelo", veiculo.ano_modelo)
        veiculo.ano_fabricacao = dados.get("ano_fabricacao", veiculo.ano_fabricacao)
        veiculo.usuario_id = dados.get("usuario_id", veiculo.usuario_id)

        
        db.session.commit()
        return f"Veículo com ID {id_veiculo} atualizado com sucesso."
    
    return f"Veículo com ID {id_veiculo} não encontrado."


def deleteVeiculoPorId(id_veiculo):
    veiculo = Veiculos.query.get(id_veiculo)
    
    if veiculo:
        db.session.delete(veiculo)
        db.session.commit()
        return f"veículo com ID {id_veiculo} deletado com sucesso."
    
    return f"Veículo com ID {id_veiculo} não encontrado."

