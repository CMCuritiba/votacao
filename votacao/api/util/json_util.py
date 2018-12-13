import json
 
class JsonConvert(object):
    mappings = {}
     
    @classmethod
    def class_mapper(clsself, d):
        for keys, cls in clsself.mappings.items():
            if keys.issuperset(d.keys()):   # are all required arguments present?
                return cls(**d)
        else:
            # Raise exception instead of silently returning None
            raise ValueError('Unable to find a matching class for object: {!s}'.format(d))
     
    @classmethod
    def complex_handler(clsself, Obj):
        if hasattr(Obj, '__dict__'):
            return Obj.__dict__
        else:
            raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj)))
 
    @classmethod
    def register(clsself, cls):
        clsself.mappings[frozenset(tuple([attr for attr,val in cls().__dict__.items()]))] = cls
        return cls
 
    @classmethod
    def ToJSON(clsself, obj):
        return json.dumps(obj.__dict__, default=clsself.complex_handler, indent=4)
 
    @classmethod
    def FromJSON(clsself, json_str):
        return json.loads(json_str, object_hook=clsself.class_mapper)
     
    @classmethod
    def ToFile(clsself, obj, path):
        with open(path, 'w') as jfile:
            jfile.writelines([clsself.ToJSON(obj)])
        return path
 
    @classmethod
    def FromFile(clsself, filepath):
        result = None
        with open(filepath, 'r') as jfile:
            result = clsself.FromJSON(jfile.read())
        return result

@JsonConvert.register
class VotoJSON(object):
    def __init__(self, vereador:str=None, voto:str=None, restricao:str=None):
        self.vereador = vereador
        self.voto = voto
        self.restricao = restricao
        return                        

@JsonConvert.register
class TotalJSON(object):
    def __init__(self, contrario:int=None, favoravel:int=None, favoravel_restricoes:int=None, abstencao:int=None, vista:int=None):
        self.contrario = contrario
        self.favoravel = favoravel
        self.favoravel_restricoes = favoravel_restricoes
        self.abstencao = abstencao
        self.vista = vista
        return                        

@JsonConvert.register
class VotacaoJSON(object):
    def __init__(self, con_id:int=None, codigo_proposicao:str=None, relator:str=None, iniciativa:str=None, VotoJSONs:[VotoJSON]=None, TotalJSONs:[TotalJSON]=None):
        self.con_id = con_id
        self.codigo_proposicao = codigo_proposicao
        self.relator = relator
        self.iniciativa = iniciativa
        self.VotoJSONs = [] if VotoJSONs is None else VotoJSONs
        self.TotalJSONs = [] if TotalJSONs is None else TotalJSONs
        return        

@JsonConvert.register
class ReuniaoJSON(object):
    def __init__(self, rec_id:int=None, rec_tipo_reuniao:str=None, rec_numero:str=None, ini_nome:str=None, rec_data:str=None, VotacaoJSONs:[VotacaoJSON]=None):
        self.rec_id = rec_id
        self.rec_tipo_reuniao = rec_tipo_reuniao
        self.rec_numero = rec_numero
        self.ini_nome = ini_nome
        self.rec_data = rec_data
        self.VotacaoJSONs = [] if VotacaoJSONs is None else VotacaoJSONs


@JsonConvert.register
class PainelVotacaoJSON(object):
    def __init__(self, codigo_proposicao:str=None, relator:str=None, iniciativa:str=None, sumula:str=None, conclusao:str=None, status: str=None, comissao:str=None, VotoJSONs:[VotoJSON]=None, TotalJSONs:[TotalJSON]=None):
        self.codigo_proposicao = codigo_proposicao
        self.relator = relator
        self.iniciativa = iniciativa
        self.sumula = sumula
        self.conclusao = conclusao
        self.status = status
        self.comissao = comissao
        self.VotoJSONs = [] if VotoJSONs is None else VotoJSONs
        self.TotalJSONs = [] if TotalJSONs is None else TotalJSONs
        return        
'''
def montaJSONVotacao(voto, rec_id, con_id, rec_tipo_reuniao, rec_numero, ini_nome):
    linha_json = {}
    linha_json['rec_id'] = rec_id
    linha_json['con_id'] = con_id
    linha_json['rec_tipo_reuniao'] = rec_tipo_reuniao
    linha_json['rec_numero'] = rec_numero
    linha_json['ini_nome'] = ini_nome
    linha_json['pac_id'] = voto.votacao.pac_id
    linha_json['proposicao'] = voto.votacao.codigo_proposicao
    linha_json['id_pessoa'] = voto.vereador.pessoa
    linha_json['vereador'] = voto.vereador.get_full_name()
    linha_json['voto'] = voto.voto
    return linha_json

def montaJSONVoto(voto, rec_id, con_id, rec_tipo_reuniao, rec_numero, ini_nome):

def montaJSONTotal(voto, rec_id, con_id, rec_tipo_reuniao, rec_numero, ini_nome):   
'''    