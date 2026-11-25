"""Dados originais de Mercadores da Conjunção."""
ITENS = {
 'Tônico rubro': ('vida', 30, 7, 'Restaura até 30 HP. Em combate consome o turno.'),
 'Essência lunar': ('mana', 22, 7, 'Restaura até 22 MP. Em combate consome o turno.'),
 'Elixir da aurora': ('ambos', 20, 12, 'Restaura até 20 HP e 20 MP. Em combate consome o turno.'),
 'Ração de viagem': ('vida', 15, 3, 'Recupera até 15 HP, somente fora de combate.'),
 'Selo de passagem': ('selo', 0, 5, 'Usado em eventos de bloqueio; evita pagar pedágio.'),
}
# Each district has two stalls, and each stall restocks from the saved day counter.
MERCADOS = {
 'Áries': ('Arsenal da Vigília','Botica dos Veteranos'), 'Touro': ('Feira do Celeiro','Empório dos Sinos'),
 'Gêmeos': ('Bazar das Engrenagens','Loja dos Mensageiros'), 'Câncer': ('Cais das Pérolas','Botica das Marés'),
 'Leão': ('Galeria Dourada','Mercado dos Arautos'), 'Virgem': ('Feira das Ervas','Botica de Alva'),
 'Libra': ('Empório dos Selos','Pavilhão das Balanças'), 'Escorpião': ('Bazar das Lanternas','Cozinha do Véu'),
 'Sagitário': ('Feira das Caravanas','Posto de Mantimentos'), 'Capricórnio': ('Mercado dos Mineiros','Armazém da Escarpa'),
 'Aquário': ('Empório das Runas','Loja da Condensação'), 'Peixes': ('Feira Flutuante','Hospedaria do Anzol'),
}
# Local stories, each with two decisions and distinct effects. One occurrence per save.
# Effects: gold, reputation, material, item, damage, seal (automatic if held).
EVENTOS = {
 'Áries': [('Uma ordem sem brasão','Uma recruta encontra uma convocação sem assinatura. O oficial exige que ela marche mesmo assim.','Acompanhar a recruta ao posto de Raska.',{'rep':2,'xp':12},'Entregar a folha ao mensageiro por uma gratificação.',{'ouro':5,'rep':-1}),('A muralha fria','Uma vigia deixou cair o lampião; a chuva ameaça apagar as tochas.','Comprar óleo e ajudar.',{'ouro':-3,'rep':2,'xp':10},'Prosseguir e recolher metal abandonado.',{'material':1})],
 'Touro': [('O pão de amanhã','Uma família de moleiros não consegue pagar a taxa de entrada da farinha.','Pagar parte da taxa.',{'ouro':-3,'rep':2,'xp':12},'Ajudar a descarregar sacas por pagamento.',{'ouro':4,'xp':7}),('O selo de cera','Uma saca de farinha tem o brasão do observatório.','Levar a informação à guilda.',{'rep':1,'xp':15},'Trocar a saca vazia por mantimentos.',{'item':'Ração de viagem'})],
 'Gêmeos': [('A carta trocada','Uma mensageira segura duas cartas com endereços idênticos.','Conferir os registros com ela.',{'rep':2,'xp':12},'Aceitar pagamento por entregar a segunda.',{'ouro':5}),('Relógio parado','Um aprendiz perde uma peça de latão na sarjeta.','Devolver a peça.',{'rep':1,'xp':10},'Comprar a peça do aprendiz.',{'ouro':-2,'material':2})],
 'Câncer': [('Água entre as pedras','A comporta lateral começa a vazar sobre uma banca.','Ajudar Neris a fechar a comporta.',{'rep':2,'xp':12,'dano':5},'Afastar clientes e receber uma ração.',{'item':'Ração de viagem','xp':7}),('O pedágio da ponte','Um fiscal improvisado cobra a travessia dos carregadores.','Mostrar um selo ou pagar 4 moedas.',{'selo':True,'rep':1,'xp':10},'Usar a ponte pública mais distante.',{'xp':5})],
 'Leão': [('O convite rasgado','Uma criada é acusada de furtar uma lista de convidados.','Pedir que um arauto ouça sua versão.',{'rep':2,'xp':12},'Aceitar o favor de um nobre e não intervir.',{'ouro':6,'rep':-1}),('A estátua velada','Um restaurador precisa de ajuda para cobrir uma estátua vandalizada.','Ajudar a restaurar a praça.',{'xp':10,'rep':1},'Fazer a entrega de ferramentas por pagamento.',{'ouro':4})],
 'Virgem': [('A estufa fechada','Uma criança precisa de ervas cultivadas numa estufa sob embargo.','Pagar a dose e registrá-la com Eline.',{'ouro':-3,'rep':2,'xp':12},'Buscar uma substituta na horta pública.',{'xp':8,'item':'Tônico rubro'}),('A colheita noturna','Os jardineiros recolhem flores antes que o orvalho seque.','Trabalhar com a equipe.',{'ouro':3,'xp':10},'Trocar informações por uma essência.',{'item':'Essência lunar'})],
 'Libra': [('Uma testemunha sem nome','Uma testemunha teme que seu endereço apareça no processo.','Pedir proteção formal a Maelis.',{'rep':2,'xp':12},'Encaminhar anonimamente o relato.',{'xp':8}),('O fiscal itinerante','Um fiscal exige autorização para transportar ferramentas.','Mostrar selo ou pagar 4 moedas.',{'selo':True,'rep':1,'xp':10},'Guardar as ferramentas e seguir pela rua pública.',{'xp':5})],
 'Escorpião': [('A lanterna apagada','Um comerciante esconde uma família perseguida por credores.','Levar comida sem revelar o endereço.',{'ouro':-3,'rep':2,'xp':12},'Trabalhar como vigia por uma moeda.',{'ouro':4,'xp':7}),('A dívida de Vesper','Um cobrador oferece dinheiro por informações sobre Vesper.','Avisar Vesper sem aceitar o pagamento.',{'rep':2,'xp':15},'Vender apenas o horário público do mercado.',{'ouro':5,'rep':-1})],
 'Sagitário': [('A roda quebrada','Uma caravana não consegue mover a carroça.','Ajudar a erguer o eixo.',{'rep':2,'xp':12,'dano':5},'Buscar um carpinteiro e receber madeira.',{'material':2,'xp':7}),('Marcos na neblina','Dois viajantes discutem a direção da estrada.','Conferir o mapa de Talan.',{'rep':1,'xp':10},'Guiá-los até a hospedaria.',{'ouro':4})],
 'Capricórnio': [('O turno interrompido','Uma sineta avisa sobre uma rocha instável.','Ajudar a evacuar o patamar.',{'rep':2,'xp':12,'dano':5},'Transportar ferramentas para a superfície.',{'material':2,'xp':7}),('O minério marcado','Um lote traz marcas de propriedade raspadas.','Informar Odran.',{'rep':2,'xp':12},'Comprar sucata de um lote autorizado.',{'ouro':-2,'material':2})],
 'Aquário': [('A chuva dentro da torre','Um condensador libera névoa sobre os aprendizes.','Desligar a válvula com Suri.',{'rep':2,'xp':12,'dano':5},'Ajudar a carregar cristais intactos.',{'material':2,'xp':7}),('A fórmula omitida','Uma bolsista descobre que seu nome sumiu do relatório.','Testemunhar a autoria.',{'rep':2,'xp':12},'Organizar as cópias por pagamento.',{'ouro':4,'xp':7})],
 'Peixes': [('A balsa atrasada','Uma balsa leva refugiados, mas falta corda para atracar.','Ajudar a puxar o barco.',{'rep':2,'xp':12},'Comprar mantimentos para os viajantes.',{'ouro':-3,'rep':2,'xp':15}),('A canção antiga','Mira reconhece uma canção da Guerra das Cinzas.','Ouvir a história e registrá-la.',{'rep':1,'xp':15},'Ajudar os músicos a montar a feira.',{'ouro':4,'xp':7})],
}
NPCS = {
 'Ione': ('Arquivista itinerante', ['Peixes','Gêmeos','Libra'], [
 ('O fragmento do sino','Ione mostra a borda quebrada do astrolábio. “A data gravada é anterior à votação. Alguém autorizou a obra em segredo.”','Prometer proteger suas fontes.','Pedir que toda fonte seja publicada.'),
 ('O arquivo duplicado','Com os primeiros casos reunidos, Ione revela que fez cópias em três depósitos. Um deles foi lacrado por ordem de Cassian.','Deixar as cópias sob guarda comunitária.','Concentrar as cópias no tribunal.'),
 ('Depois do testemunho','Ione questiona se a verdade servirá às pessoas ou apenas a outro governo.','Abrir o arquivo à população.','Manter acesso restrito às fontes sensíveis.')]),
 'Raska': ('Capitã da Vigília', ['Áries','Leão','Sagitário'], [
 ('O juramento da guarda','Raska diz que o juramento é com a cidade, não com um regente. Pede que você não trate todos os soldados como cúmplices.','Garantir julgamento individual.','Exigir suspensão imediata dos oficiais suspeitos.'),
 ('Ordens contraditórias','Raska recebe duas ordens: fechar as pontes ou escoltar civis. Ela suspeita que uma tenha sido forjada.','Priorizar os civis.','Preservar a cadeia de comando e documentar a ordem.'),
 ('A última vigília','Raska prepara guardas para impedir represálias após a audiência.','Defender patrulhas comunitárias.','Defender uma guarda central fiscalizada.')]),
 'Vesper': ('Informante do Véu', ['Escorpião','Câncer','Gêmeos'], [
 ('O preço de um nome','Vesper oferece um mapa das entregas e teme que sua família seja exposta.','Prometer anonimato.','Pedir um depoimento nominal.'),
 ('Uma rota apagada','Uma rota foi retirada dos registros; Vesper reconhece o nome de um intermediário do Conselho.','Proteger a rede de mensageiros.','Entregar os registros ao magistrado.'),
 ('A cidade que escuta','Vesper quer que o mercado tenha representação, não imunidade.','Apoiar uma associação pública.','Exigir auditoria antes da representação.')]),
 'Maelis': ('Juíza do Equilíbrio', ['Libra','Virgem','Leão'], [
 ('O limite da lei','Maelis admite que a lei de emergência permite abusos, mesmo quando a ameaça é real.','Defender limites e revisão pública.','Defender medidas temporárias sob sigilo.'),
 ('A ata perdida','A juíza encontra uma votação sem ata. Ela quer impedir que a próxima audiência repita o erro.','Exigir sessão pública.','Proteger testemunhas em sessão reservada.'),
 ('A sentença futura','Maelis pergunta como impedir que a próxima crise seja usada para concentrar poder.','Garantir recurso aos distritos.','Criar auditoria independente.')]),
}
