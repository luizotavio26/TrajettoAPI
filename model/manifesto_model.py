from config import db
from model.cliente_model import Clientes
from model.veiculos_model import Veiculos
from model.motorista_model import Motoristas

FAIXAS_KM = [40, 60, 100, 130, 160, 200, 280, 400, 480, 550, 620, 700]

PRECOS = {
    "seca": {
        # 
        "van":   [441, 470, 613, 656, 713, 850, 911, 1032, 1195, 1636, 1808, 1908],
        # 
        "leve":  [583, 625, 740, 797, 869, 999, 1073, 1179, 1404, 1987, 2144, 2273],
        # 
        "toco":  [780, 838, 894, 1010, 1082, 1235, 1311, 1447, 1597, 2377, 2491, 2679],
        # 
        "truck": [971, 1044, 1197, 1280, 1400, 1571, 1662, 1863, 2171, 3142, 3215, 3571]
    },
    "refrigerada": {
        # 
        "van":   [509, 542, 678, 787, 854, 911, 1049, 1204, 1388, 1897, 2066, 2242],
        # 
        "leve":  [604, 658, 800, 948, 1044, 1148, 1247, 1374, 1544, 2148, 2344, 2588],
        # 
        "toco":  [854, 918, 989, 1200, 1301, 1417, 1516, 1657, 1856, 2710, 2845, 2957],
        # 
        "truck": [1065, 1141, 1280, 1410, 1628, 1862, 1920, 2153, 2328, 3393, 3608, 3956]
    }
}

def get_tipo_veiculo(peso):
    # 
    if peso <= 1600:
        return "van"
    # 
    elif peso <= 2500:
        return "leve"
    # 
    elif peso <= 6800:
        return "toco"
    # 
    elif peso <= 12000:
        return "truck"
    else:
        return None


def get_distancia_api(origem, destino):
    """
    *** FUNÇÃO DE SIMULAÇÃO ***
    Aqui você deve implementar a chamada real a uma API como Google Maps Distance Matrix.
    
    PARA TESTE: Vamos simular uma distância com base no tamanho dos nomes das cidades
    para forçar o uso de diferentes faixas da tabela.
    """
    print(f"SIMULANDO DISTÂNCIA para {origem} -> {destino}")
    distancia_simulada = (len(origem) + len(destino)) * 5.3
    
    if distancia_simulada > 700:
        distancia_simulada = 650 
    
    return round(distancia_simulada, 2)


def get_valor_frete_tabelado(tipo_carga, tipo_veiculo, distancia):
    if tipo_carga not in PRECOS or tipo_veiculo not in PRECOS[tipo_carga]:
        return None

    for index, limite_km in enumerate(FAIXAS_KM):
        if distancia <= limite_km:
            return PRECOS[tipo_carga][tipo_veiculo][index]
    
    return None



class ManifestoCarga(db.Model):
    __tablename__ = "manifesto_carga"

    id = db.Column(db.Integer, primary_key=True)
    tipo_carga = db.Column(db.String(50), nullable=False)
    peso_carga = db.Column(db.Float, nullable=False)

    motorista_id = db.Column(db.Integer, db.ForeignKey("Motoristas.id"), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("Clientes.id"), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey("Veiculos.id"), nullable=False)

    origem_carga = db.Column(db.String(200), nullable=False)
    destino_carga = db.Column(db.String(200), nullable=False)
    valor_frete = db.Column(db.Float, nullable=False)
    valor_km = db.Column(db.Float, nullable=False)
    distancia = db.Column(db.Float, nullable=False)

    
    motorista = db.relationship("Motoristas", back_populates="manifestos")
    cliente = db.relationship("Clientes", back_populates="manifestos")
    veiculo = db.relationship("Veiculos", back_populates="manifestos")
    usuario_id = db.Column(db.Integer, db.ForeignKey("Usuarios.id"), nullable=False)
    usuario  = db.relationship("Usuarios", back_populates="manifestos")



    def __init__(self, tipo_carga, peso_carga, motorista_id, cliente_id, veiculo_id, origem_carga,
                 destino_carga, valor_km, distancia, valor_frete, usuario_id):
        self.tipo_carga = tipo_carga
        self.peso_carga = peso_carga
        self.cliente_id = cliente_id
        self.motorista_id = motorista_id
        self.veiculo_id = veiculo_id
        self.origem_carga = origem_carga
        self.destino_carga = destino_carga
        self.valor_km = valor_km
        self.distancia = distancia
        self.valor_frete = valor_frete
        self.usuario_id = usuario_id


    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,

            "tipo_carga": self.tipo_carga,
            "peso_carga": self.peso_carga,

            "cliente_id": self.cliente_id,
            "cliente": self.cliente.razao_social if self.cliente else None,

            "motorista_id": self.motorista_id,
            "motorista": self.motorista.nome if self.motorista else None,

            "veiculo_id": self.veiculo_id,
            "veiculo": self.veiculo.placa if self.veiculo else None,

            "origem_carga": self.origem_carga,
            "destino_carga": self.destino_carga,

            "valor_frete": self.valor_frete,
            "valor_km": self.valor_km,
            "distancia": self.distancia
        }



class CargaNaoEncontrada(Exception):
    pass


def create_carga(carga):
    try:
        tipo_carga = carga["tipo_carga"] 
        origem = carga["origem_carga"]
        destino = carga["destino_carga"]
        usuario_id = carga["usuario_id"]
        
        peso_carga_str = carga.get("peso_carga", 0) 
        peso_carga = float(peso_carga_str)

        distancia_calculada = get_distancia_api(origem, destino) 
        
        if distancia_calculada <= 0:
             return None, f"Não foi possível calcular a distância entre {origem} e {destino}."

        tipo_veiculo = get_tipo_veiculo(peso_carga)
        if tipo_veiculo is None:
            return None, f"Peso da carga ({peso_carga}kg) excede o limite da tabela (12000kg)."

        valor_frete_tabelado = get_valor_frete_tabelado(tipo_carga, tipo_veiculo, distancia_calculada)
        
        if valor_frete_tabelado is None:
            msg_erro = f"Valor não encontrado na tabela para: Carga {tipo_carga}, Veículo {tipo_veiculo} (peso {peso_carga}kg), Distância {distancia_calculada}km."
            return None, msg_erro

        valor_km_calculado = valor_frete_tabelado / distancia_calculada

        nova_carga = ManifestoCarga(
            tipo_carga = tipo_carga,
            peso_carga = peso_carga,
            usuario_id = carga["usuario_id"],
            cliente_id = carga["cliente_id"],
            motorista_id = carga["motorista_id"],
            veiculo_id= carga["veiculo_id"],
            origem_carga = origem,
            destino_carga = destino,
            valor_km = round(valor_km_calculado, 2),  
            distancia = round(distancia_calculada, 2), 
            valor_frete = float(valor_frete_tabelado) 
        )

        db.session.add(nova_carga)
        db.session.commit()
        return nova_carga.to_dict(), None

    except KeyError as e:
        db.session.rollback()
        return None, f"Dado obrigatório faltando: {str(e)}. Verifique o JSON enviado pelo frontend."
    except Exception as e:
        db.session.rollback()
        return None, str(e)


def read_cargas_id(id_carga):
    carga = ManifestoCarga.query.get(id_carga)

    if not carga:
        return {'message':'Nenhuma carga encontrada.'}
    else:
        return carga.to_dict()


def update_carga(id_carga, dados_atualizados):
    carga = ManifestoCarga.query.get(id_carga)
    if not carga:
        return {'message':'Nenhuma carga encontrada.'}
    
    carga.tipo_carga = dados_atualizados["tipo_carga"]
    carga.peso_carga = dados_atualizados["peso_carga"]
    carga.cliente_id = dados_atualizados["cliente_id"]
    carga.motorista_id = dados_atualizados["motorista_id"]
    carga.veiculo_id = dados_atualizados["veiculo_id"]
    carga.origem_carga = dados_atualizados["origem_carga"]
    carga.destino_carga = dados_atualizados["destino_carga"]
    carga.usuario_id = dados_atualizados["usuario_id"]

    distancia_calculada = get_distancia_api(carga.origem_carga, carga.destino_carga)
    tipo_veiculo = get_tipo_veiculo(carga.peso_carga)
    valor_frete_tabelado = get_valor_frete_tabelado(carga.tipo_carga, tipo_veiculo, distancia_calculada)
    carga.valor_frete = float(valor_frete_tabelado)
    carga.valor_km = round(valor_frete_tabelado / distancia_calculada, 2)
    carga.distancia = round(distancia_calculada, 2)

    db.session.commit()

    return {'message': "Informações sobre a carga atualizada com sucesso!"}, None


def delete_carga_id(id_carga):
    carga = ManifestoCarga.query.get(id_carga)
    if not carga:
        raise CargaNaoEncontrada(f'Informação sobre a carga não encontrada.')
    db.session.delete(carga)
    db.session.commit()
    return {"message":"Cargas deletadas com sucesso!"}, None


def delete_todas_cargas():
    cargas = ManifestoCarga.query.all()
    for carga in cargas:
        db.session.delete(carga)
    db.session.commit()
    return {'message':"Cargas deletadas com sucesso!"}, None


def cargasCadastradas(usuario_id):
    cargas = ManifestoCarga.query.filter_by(usuario_id=usuario_id).all()

    lista_cargas = [
        {
            "id": c.id,
            "usuario_id": c.usuario_id,

            "tipo_carga": c.tipo_carga,
            "peso_carga": c.peso_carga,

            "cliente_id": c.cliente_id,
            "cliente": c.cliente.razao_social if c.cliente else None,

            "motorista_id": c.motorista_id,
            "motorista": c.motorista.nome if c.motorista else None,

            "veiculo_id": c.veiculo_id,
            "veiculo": c.veiculo.placa if c.veiculo else None,

            "origem_carga": c.origem_carga,
            "destino_carga": c.destino_carga,

            "valor_frete": c.valor_frete,
            "valor_km": c.valor_km,
            "distancia": c.distancia,
        }
        for c in cargas
    ]

    return {"Cargas": lista_cargas}


def motoristasCadastrados(usuario_id):
    motoristas = Motoristas.query.filter_by(usuario_id=usuario_id).all()

    lista_motoristas = [
        {
            "id": m.id,
            "usuario_id": m.usuario_id,
            "nome": m.nome,
            "cpf": m.cpf,
            "rg": m.rg,
            "salario": m.salario,
            "data_nascimento": m.data_nascimento,
            "numero_cnh": m.numero_cnh,
            "categoria_cnh": m.categoria_cnh,
            "validade_cnh": m.validade_cnh,
            "telefone": m.telefone,
            "email": m.email,
            "cep": m.cep,
            "logradouro": m.logradouro,
            "numero": m.numero,
            "complemento": m.complemento,
            "bairro": m.bairro,
            "cidade": m.cidade,
            "estado": m.estado
        }
        for m in motoristas
    ]

    return lista_motoristas


def clientesCadastrados(usuario_id):
    clientes = Clientes.query.filter_by(usuario_id=usuario_id).all()


    lista_clientes = [
        {
            "id": c.id,
            "usuario_id": c.usuario_id,
            "cnpj": c.cnpj,
            "razao_social": c.razao_social,
            "email": c.email,
            "telefone": c.telefone,
            "cep": c.cep,
            "logradouro": c.logradouro,
            "numero": c.numero,
            "complemento": c.complemento,
            "bairro": c.bairro,
            "cidade": c.cidade,
            "estado": c.estado
        }
        for c in clientes
    ]

    return lista_clientes


def veiculosCadastrados(usuario_id):
    veiculos = Veiculos.query.filter_by(usuario_id=usuario_id).all()


    lista_veiculos = [
        {
            "id": v.id,
            "usuario_id": v.usuario_id,
            "placa": v.placa,
            "modelo": v.modelo,
            "marca": v.marca,
            "renavan": v.renavan,
            "chassi": v.chassi,
            "cor": v.cor,
            "tipo": v.tipo,
            "peso_maximo_kg": v.peso_maximo_kg,
            "ano_modelo": v.ano_modelo,
            "ano_fabricacao": v.ano_fabricacao
        }
        for v in veiculos
    ]

    return lista_veiculos


