"""Doze expedições opcionais, cada uma ligada à história do distrito."""
from dataclasses import dataclass
from mundo import POR_SIGNO

@dataclass(frozen=True)
class Masmorra:
    nome: str
    historia: str
    inimigos: tuple
    chefe: str
    revelacao: str
    tema: str

# Cada lista contém nove adversários distintos, em ordem crescente.
MASMORRAS={
'Áries': Masmorra('Fortim das Ordens Perdidas','Uma passagem sob o quartel abriga armaduras animadas por ordens militares adulteradas. A Vigília solicita a recuperação do selo que comanda a guarnição.',('Sentinela de bronze','Escudeiro vazio','Cão de guerra rúnico','Lanceiro de cinzas','Batedor desertor','Carrasco de ferro','Porta-estandarte espectral','Centurião quebrado','Guardião do selo'),'Kharzug, o Marechal Oco','O selo confirma que a guarnição recebeu ordens falsas antes da crise.','armor'),
'Touro': Masmorra('Celeiro das Raízes Famintas','Os canais abandonados do primeiro moinho alimentam um crescimento subterrâneo. Doran pede que a reserva de sementes seja recuperada.',('Rato do silo','Broto voraz','Besouro de grão','Espantalho animado','Javali de raízes','Fungo do moinho','Trepa-pedra','Golem de argila','Touro de palha'),'Bramor, a Raiz do Inverno','As raízes cresceram sobre um conduto de água desviado clandestinamente.','plant'),
'Gêmeos': Masmorra('Labirinto dos Relógios Gêmeos','Um antigo correio mecânico começou a repetir mensagens que ninguém enviou. Iria encontra uma entrada de manutenção.',('Autômato carteiro','Aranha de latão','Sentinela de mola','Eco duplicado','Esfera de engrenagens','Relógio ambulante','Copista mecânico','Gêmeo de vidro','Executor cronológico'),'Os Dois Ponteiros','O mecanismo conservou uma cópia das mensagens anteriores ao bloqueio dos portões.','machine'),
'Câncer': Masmorra('Cripta da Maré Presa','Neris descobre uma câmara antiga atrás de uma comporta selada. Uma criatura atrai para lá as correntes que deveriam abastecer o bairro.',('Caranguejo de pedra','Enguia luminosa','Afogado espectral','Polvo de lodo','Guardião de coral','Serpente do canal','Tritão de espuma','Tubarão rúnico','Colosso de nácar'),'Thalassa, a Maré Cativa','O conduto que aprisionou Thalassa havia sido instalado sem autorização dos barqueiros.','aquatic'),
'Leão': Masmorra('Mausoléu da Coroa Partida','Sob a galeria dos regentes, antigos juramentos de proteção despertam com a ruptura do astrolábio. Arahan pede que o arquivo funerário seja preservado.',('Leão de pedra','Pajem espectral','Duelista de ouro','Escudo animado','Arauto sem rosto','Gárgula solar','Campeão do pátio','Guardião do trono','Leão coroado'),'Aurelion, o Rei de Bronze','Os juramentos antigos exigiam que o Conselho prestasse contas aos cidadãos.','beast'),
'Virgem': Masmorra('Herbário da Flor Noturna','Eline perdeu acesso a um jardim de pesquisa contaminado por resíduos arcanos. Há espécimes que podem curar os moradores, se forem recolhidos com cuidado.',('Esporo errante','Mariposa de vidro','Liana viva','Mandrágora','Vespa de seiva','Flor carnívora','Ent de Alva','Alquimista de musgo','Guardião das pétalas'),'Selyne, a Rosa da Vigília','Os resíduos chegaram de uma oficina externa, não do trabalho dos curandeiros.','plant'),
'Libra': Masmorra('Câmara das Sentenças Seladas','Decretos antigos deram vida aos mecanismos de uma prisão desativada. Maelis pede acesso aos nomes de prisioneiros esquecidos.',('Corrente animada','Escriba vazio','Vigia de mármore','Livro de sentenças','Balança espectral','Carcereiro de prata','Magistrado ilusório','Executor da cela','Guardião do tribunal'),'Justicar, a Balança Cega','A lista recuperada permite solicitar revisão das detenções sem julgamento.','armor'),
'Escorpião': Masmorra('Catacumbas da Lanterna Negra','A rede subterrânea perdeu uma rota de fuga para um grupo de criaturas atraídas por cristais clandestinos. Vesper conhece a entrada.',('Escorpião de ônix','Rato de sombra','Aranha da lanterna','Vulto encapuzado','Serpente de obsidiana','Caçador de ecos','Mímico do cofre','Assombração do túnel','Escorpião cristalino'),'Nox, o Ferrão de Vidro','As cavernas revelam uma antiga saída civil que pode ser reaberta sem expor a rede.','shadow'),
'Sagitário': Masmorra('Ruínas da Última Caravana','Um posto de estrada soterrado impede a passagem de comboios. Exploradores ouvem cascos e flechas sob as pedras.',('Lobo de freixo','Corvo de tempestade','Batedor espectral','Arqueiro das ruínas','Urso de espinhos','Cervo rúnico','Cavaleiro sem montaria','Grifo de cinzas','Centauro de pedra'),'Orion, o Caçador Sem Norte','O posto guardava mapas de desvios seguros para as caravanas durante a guerra.','beast'),
'Capricórnio': Masmorra('Fundição do Eco Profundo','Mineiros abandonaram uma galeria onde a rocha começou a andar. O sindicato pede a recuperação dos registros de segurança.',('Golem de carvão','Besouro de escória','Mineiro de pedra','Lagarto de magma','Martelo animado','Elemental de minério','Sentinela de basalto','Gigante de escória','Guardião da fornalha'),'Varkun, o Coração da Montanha','Os registros provam que os avisos de instabilidade foram ignorados por administradores.','stone'),
'Aquário': Masmorra('Cisterna das Estrelas Afogadas','Uma instalação experimental começou a condensar luz em criaturas instáveis. Os pesquisadores solicitam o desligamento do núcleo auxiliar.',('Centelha errante','Gota de éter','Esfera de chuva','Elemental de vento','Vórtice azul','Constructo de gelo','Nuvem de relâmpagos','Arauto do prisma','Golem atmosférico'),'Astrael, o Núcleo da Tempestade','O núcleo registrou uma transferência clandestina de energia ao observatório.','machine'),
'Peixes': Masmorra('Gruta dos Sonhos Náufragos','Pescadores ouviram vozes familiares sob as ilhas. Uma caverna de maré guarda pertences de refugiados e ilusões de suas lembranças.',('Peixe-lanterna','Caranguejo onírico','Sombra de pescador','Medusa de névoa','Mímico do baú','Enguia dos sonhos','Barqueiro ilusório','Serpente lunar','Guardião da lembrança'),'Myr, o Devorador de Sonhos','As lembranças são libertadas e os pertences podem retornar às famílias.','aquatic'),
}
CLASSES_ONDA=('Ladino','Guerreiro','Mago','Paladino','Guerreiro','Ladino','Mago','Guerreiro','Paladino','Guerreiro')

def inimigo_onda(signo,onda):
    m=MASMORRAS[signo]
    return m.chefe if onda==10 else m.inimigos[onda-1]

# Nome, ações alternadas usando as habilidades originais e uma descrição telegráfica.
# Não altera os dados de combate, os custos ou as fórmulas do protagonista.
PADROES_CHEFE={
'Áries': ('Ordem de execução',('Golpe Poderoso','Ataque Rápido'),'Kharzug ergue o estandarte antes de ordenar uma investida.'),
'Touro': ('Colheita de espinhos',('Ataque Rápido','Golpe Poderoso'),'Bramor estende raízes sob o chão antes de golpear.'),
'Gêmeos': ('Pêndulo reverso',('Bola de Fogo','Ataque Rápido'),'Os ponteiros alternam descargas arcanas e movimentos rápidos.'),
'Câncer': ('Maré crescente',('Bola de Fogo','Golpe Poderoso'),'A água se acumula ao redor de Thalassa, anunciando o próximo ataque.'),
'Leão': ('Decreto solar',('Golpe Poderoso','Bola de Fogo'),'A coroa de bronze incandesce antes da ofensiva.'),
'Virgem': ('Pólen da vigília',('Ataque Rápido','Bola de Fogo'),'Selyne dispersa pólen cintilante entre chicotadas de pétalas.'),
'Libra': ('Veredito de prata',('Golpe Poderoso','Golpe Poderoso'),'A balança se inclina; Justicar ergue a arma para executar a sentença.'),
'Escorpião': ('Ferrão de vidro',('Ataque Rápido','Ataque Rápido'),'Nox baixa o corpo e aponta o ferrão antes de atacar.'),
'Sagitário': ('Flechas sem norte',('Ataque Rápido','Golpe Poderoso','Ataque Rápido'),'Orion alterna disparos rápidos com uma flecha pesada.'),
'Capricórnio': ('Ruptura da fornalha',('Golpe Poderoso','Bola de Fogo','Golpe Poderoso'),'As fissuras de Varkun brilham quando a fornalha se prepara para romper.'),
'Aquário': ('Prisma atmosférico',('Bola de Fogo','Bola de Fogo'),'Astrael condensa duas descargas sucessivas de energia.'),
'Peixes': ('Pesadelo recorrente',('Bola de Fogo','Ataque Rápido','Bola de Fogo'),'As ilusões de Myr alternam ondas de luz e ataques súbitos.'),
}

def acao_chefe(signo,turno):
    nome,acoes,_=PADROES_CHEFE[signo]
    return nome,acoes[(turno-1)%len(acoes)]
