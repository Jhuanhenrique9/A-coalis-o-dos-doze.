"""Cenário original de The Battle. Dados narrativos, sem regras de atributos."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Distrito:
    signo: str
    nome: str
    povo: str
    regiao: str
    npc: str
    arquivo: str
    local: str
    oficina: str
    lore: str
    cena: str
    prova: str
    categoria: str
    material: str
    inimigo: str
    classe_inimigo: str
    luta: str
    acordo: str
    custo: str
    classe_forte: str
    classe_fraca: str
    atalho: str
    retorno: str

DISTRITOS = [
Distrito('Áries','Bastião Rubro','Orcs','Portões do norte','Capitã Raska','Memorial das Lanças','Pátio da Guarda','Ferraria da Brasa',
'Os clãs orcs ergueram a muralha durante a Guerra das Cinzas, quando os nobres abandonaram os bairros externos. Hoje a guarda é eleita por famílias e veteranos. Os nomes dos civis mortos estão gravados antes dos generais. O Bastião importa grãos de Touro e fornece escolta às caravanas.',
'Raska mostra um mandado com seu selo falsificado. Um oficial pretende levar três recrutas para o subterrâneo antes do amanhecer. “Se eu o prender sem testemunhas, o Conselho dirá que fui eu quem assinou.”',
'Mandado de transferência com selo duplicado','ordens','Ferro','Oficial Varek','Guerreiro',
'Interpor-se entre Varek e os recrutas; ele desembainha a espada para impedir a revista.',
'Entregar o mandado à assembleia dos veteranos, aceitando que o oficial permaneça livre até o julgamento.','assembleia', 'Guerreiro','Ladino','Invocar o direito de revista de um companheiro de armas; Raska convoca duas testemunhas.','Os recrutas retornam ao quartel. Raska promete lembrar quem colocou a palavra deles acima de uma ordem.'),
Distrito('Touro','Vale dos Sinos','Anões','Terraços agrícolas do oeste','Mestre Doran','Casa das Medidas','Celeiro Comum','Forja dos Sete Sinos',
'Os anões trocaram mineração profunda por canais e lavouras quando o veio de prata desabou. As guildas medem riqueza em reservas de inverno, não em moedas. Cada sino marca uma etapa da irrigação. Os moinhos dependem das águas de Câncer.',
'Doran encontra sacos vazios apesar de ter recebido recibos de entrega. Um cobrador armado guarda o livro de pesagens. “Não quero vingança. Quero saber por que nossas crianças estão passando fome.”',
'Livro de pesagens de grão desviado','suprimentos','Madeira','Cobrador Brann','Guerreiro',
'Exigir o livro do cobrador; ele fecha a porta e ataca para destruir os recibos.',
'Pagar a cópia autenticada e permitir que Doran organize uma auditoria pública.','cópia','Paladino','Mago','Garantir a auditoria sob juramento diante dos trabalhadores.','O celeiro volta a distribuir rações, mas os recibos revelam que os desvios começaram meses antes.'),
Distrito('Gêmeos','Ponte dos Ecos','Gnomos','Pontes sobre o canal central','Iria e Nilo','Gabinete dos Cartógrafos','Correio das Duas Portas','Oficina de Molas',
'Gnomos fundaram um correio neutro durante a guerra. As duas torres da ponte usam relógios independentes para impedir que uma única autoridade adultere horários. Mensagens cifradas sustentam tanto comerciantes honestos quanto dissidentes.',
'Iria recebe uma mensagem de Nilo, embora ele esteja sentado ao seu lado. Um mensageiro de máscara espera pela resposta; a carta manda lacrar as saídas da cidade na noite da conjunção.',
'Carta cifrada sobre o bloqueio dos portões','ordens','Cristal','Mensageiro de Vidro','Ladino',
'Seguir o mensageiro até o arquivo e impedir que ele queime o original; ele reage com uma adaga.',
'Decifrar uma cópia com os cartógrafos e deixar o mensageiro partir sob vigilância.','decifração','Ladino','Guerreiro','Usar os sinais dos correios clandestinos para interceptar a carta sem alertar o mensageiro.','Iria pendura a mensagem falsa no quadro de avisos. Nilo começa a mapear quem lucra com portões fechados.'),
Distrito('Câncer','Concha de Nácar','Tritões','Doca e canais do sul','Neris','Arquivo das Marés','Casa das Comportas','Estaleiro de Nácar',
'Os tritões negociaram cidadania em troca da manutenção dos canais. A arquitetura mistura rampas secas e câmaras inundadas, acessíveis por guias. Uma antiga lei impede a abertura simultânea das comportas, pois a pressão destruiria bairros inteiros.',
'Neris viu um engenheiro comprar chaves proibidas. O vigia que a acompanhava sumiu; outro homem ocupa a guarita e ameaça inundar o arquivo.',
'Depoimento de Neris sobre as chaves das comportas','testemunhos','Madeira','Vigia substituto','Paladino',
'Salvar Neris e impedir a abertura da comporta; o vigia parte para o combate.',
'Evacuar o arquivo e chamar a cooperativa de barqueiros, sacrificando a captura imediata do vigia.','barqueiros','Mago','Paladino','Identificar o encantamento nas chaves e desativar o mecanismo sem entrar na guarita.','Os canais permanecem abertos para a população. Neris envia seu relato por uma embarcação neutra.'),
Distrito('Leão','Coroa Solar','Leoninos','Praça alta do centro','Arahan','Galeria dos Regentes','Salão das Petições','Arsenal Dourado',
'Os leoninos guardam a tradição de proclamar leis em praça pública para que ninguém possa alegar ignorância. A casa regente perdeu poder após a guerra, mas conserva a presidência do Conselho. Bailes e petições são campos de disputa política.',
'Arahan, herdeiro sem assento, apresenta a lista de convidados de uma reunião que oficialmente nunca ocorreu. Um duelista contratado bloqueia a saída até que o documento seja devolvido.',
'Lista dos financiadores da sessão secreta','suprimentos','Ferro','Duelista Saren','Guerreiro',
'Aceitar o desafio do duelista para garantir a saída de Arahan com a lista.',
'Publicar os nomes na praça por intermédio de um arauto, expondo também Arahan.','arauto','Guerreiro','Ladino','Invocar o código dos duelos: exigir uma testemunha pública e fazer o duelista recuar.','A praça passa a discutir os contratos, não a linhagem do herdeiro. Arahan perde convites, mas ganha aliados.'),
Distrito('Virgem','Jardins de Alva','Elfos','Jardins do nordeste','Curandeira Eline','Herbário das Estações','Enfermaria da Alva','Ateliê de Resinas',
'Os elfos cultivam árvores enxertadas em memória dos mortos e mantêm a maior enfermaria da cidade. A ordem de curadores disputa com mercadores o direito de produzir remédios. Suas portas nunca fecham por linhagem, embora o Conselho pressione por prioridades.',
'Eline descobre que remédios foram substituídos por sedativos. Um guarda privado pretende retirar a última paciente consciente antes que ela possa testemunhar.',
'Relato da paciente sobre transporte ao observatório','testemunhos','Couro','Guarda da botica','Ladino',
'Impedir a remoção da paciente; o guarda decide cumprir o contrato pela força.',
'Levar a paciente por uma saída de serviço e pagar a escolta dos jardineiros.','escolta','Paladino','Guerreiro','Reivindicar o santuário da enfermaria e chamar a ordem de curadores para testemunhar.','Eline registra a paciente com seu nome verdadeiro. A enfermaria prepara um relatório para as outras ordens.'),
Distrito('Libra','Átrio do Equilíbrio','Aasimar','Colina dos tribunais','Juíza Maelis','Arquivo das Sentenças','Tribunal das Balanças','Oficina de Selos',
'Os aasimar que fundaram o tribunal rejeitaram o direito divino de governar. Seus magistrados juram que uma sentença vale apenas quando pode ser contestada. As leis antigas protegem os distritos, mas decretos emergenciais oferecem brechas perigosas.',
'Maelis encontra uma ordem de emergência já assinada, datada de amanhã. Seu escrivão foi comprado e um executor ameaça confiscar a folha.',
'Decreto de emergência pré-datado','ordens','Cristal','Executor do selo','Paladino',
'Defender o arquivo contra o executor enquanto Maelis autentica a ordem.',
'Registrar a ordem como prova lacrada em cartório independente, preservando a cadeia de custódia.','cartório','Paladino','Ladino','Invocar a audiência de urgência sob juramento e obter a proteção formal da juíza.','Maelis suspende o decreto em primeira instância. A decisão ainda pode ser revertida pelo Conselho.'),
Distrito('Escorpião','Véu de Ônix','Tieflings','Ruelas e cisternas do sudoeste','Vesper','Casa das Memórias','Mercado da Meia-Noite','Ateliê de Lâminas',
'Famílias tieflings transformaram antigas cisternas em moradias e redes de ajuda. A reputação sombria do bairro serve a quem vende medo; seus comerciantes também mantêm cozinhas comunitárias. A informação é valiosa porque a polícia nem sempre os escuta.',
'Vesper admite ter transportado caixas sem perguntar seu conteúdo. Agora um intermediário exige que ela desapareça. Ele conhece o caminho das caixas até o observatório.',
'Confissão de Vesper e rota das caixas','testemunhos','Couro','Intermediário Kesh','Ladino',
'Enfrentar Kesh quando ele tenta levar Vesper à força pela viela.',
'Comprar a saída segura de Vesper e entregar seu relato sem divulgar o endereço.','refúgio','Ladino','Paladino','Negociar com a rede de mensageiros e expor Kesh aos próprios contratantes.','Vesper entrega os nomes das transportadoras. O mercado protege sua família enquanto o caso avança.'),
Distrito('Sagitário','Horizonte de Freixo','Centauros','Estrada e bosques orientais','Talan','Posto das Rotas','Estábulo das Caravanas','Casa dos Arqueiros',
'Os centauros mantêm estradas livres por pacto entre viajantes. Prédios têm corredores amplos e pátios abertos. A madeira dos freixos é cortada por rotação, e seus batedores levam correspondências a lugares que a guarda não alcança.',
'Talan perdeu uma caravana depois que marcos de pedra foram deslocados. Um mercenário controla o cruzamento, cobrando passagem e recolhendo cargas para um comprador oculto.',
'Romaneio das caravanas desviadas','suprimentos','Madeira','Mercenário da estrada','Guerreiro',
'Desafiar o mercenário no cruzamento para devolver a carga aos viajantes.',
'Contratar batedores para contornar a cobrança e recuperar uma cópia do romaneio.','batedores','Guerreiro','Mago','Organizar a escolta dos viajantes e obrigar o mercenário a abandonar o posto diante da caravana.','Os marcos voltam aos lugares certos. Talan oferece a rota como testemunho da rede de desvio.'),
Distrito('Capricórnio','Escarpa de Basalto','Goliaths','Pedreiras e encostas do noroeste','Odran','Torre dos Marcos','Mina do Contrapeso','Fundição de Basalto',
'Comunidades goliaths construíram os elevadores de pedra que sustentam o terraço superior. O trabalho se divide por turnos, com direito de recusa quando a rocha ameaça ruir. A guilda vende metal e contrapesos para os doze distritos.',
'Odran interrompe a extração ao descobrir uma ordem que removeu os contrapesos de segurança. Um capataz armado tenta reabrir a mina e ocultar a remessa.',
'Inventário de contrapesos e metais retirados','suprimentos','Ferro','Capataz Harg','Guerreiro',
'Impedir o acionamento do elevador; o capataz o enfrenta no patamar.',
'Custear a inspeção externa e manter a mina fechada até a guilda decidir.','inspeção','Mago','Ladino','Ler as marcas de tensão rúnica e provar o risco técnico diante dos mineiros.','A mina permanece fechada para reparos. Odran envia o inventário e o nome do comprador.'),
Distrito('Aquário','Cúpula das Chuvas','Genasi','Reservatórios do leste','Mestra Suri','Biblioteca dos Ventos','Torre da Condensação','Laboratório de Cristais',
'Os genasi mantêm torres que condensam água e desviam tempestades. A escola local ensina magia como ofício público, com licenças contestadas por acadêmicos independentes. Sua principal controvérsia é quem possui os projetos financiados por todos.',
'Suri identifica uma cópia de seu projeto dentro de um cristal roubado. Um aprendiz radical alega que a cidade precisa de um único controlador, e tenta fugir levando o cristal.',
'Projeto de redirecionamento da energia das torres','ordens','Cristal','Aprendiz Kair','Mago',
'Bloquear a fuga do aprendiz antes que ele acione a descarga de proteção.',
'Isolar o laboratório e divulgar uma cópia autenticada aos acadêmicos independentes.','publicação','Mago','Guerreiro','Desfazer o selo de proteção e demonstrar que o projeto pode ser usado para cortar água dos bairros.','Suri retira as licenças do projeto e solicita que os reservatórios sejam administrados por equipes de bairros distintos.'),
Distrito('Peixes','Ilhas do Sonho','Halflings','Ilhotas do delta','Mira','Casa dos Relatos','Hospedaria das Lanternas','Oficina de Velas',
'Os halflings acolheram refugiados em casas sobre estacas. A tradição local preserva histórias em livros de hóspedes; nenhuma pessoa precisa oferecer sobrenome para obter comida. Barcos pequenos ligam as ilhas ao restante da cidade.',
'Mira abriga um antigo operador do observatório, que viu o regente aprovar testes em bairros habitados. Um caçador de recompensas acaba de chegar com uma ordem de captura sem assinatura.',
'Depoimento do operador sobre o teste da conjunção','testemunhos','Couro','Caçador Iven','Ladino',
'Proteger a hospedaria quando Iven tenta arrastar o operador para o barco.',
'Pagar a viagem do operador para um abrigo neutro e gravar o relato diante de hóspedes.','barco','Ladino','Paladino','Identificar a ordem falsa e usar a rede de hospedeiros para despistar Iven.','O operador finalmente dorme sem manter a porta trancada. Mira guarda o depoimento em duas cópias.'),
]
POR_SIGNO = {d.signo:d for d in DISTRITOS}
CLASSES_MUNDO = {
'Guerreiro':('Autoridade marcial; soluções diretas em quartéis, duelos e estradas.','Em Gêmeos? Não: em Virgem e Aquário, demonstrações de força despertam desconfiança; a rota técnica custa mais.'),
'Mago':('Interpreta runas, mecanismos e projetos; favorecido em Câncer, Capricórnio e Aquário.','Em Touro e Sagitário, é preciso pagar pela validação local de uma solução técnica.'),
'Paladino':('Juramentos e proteção de civis; favorecido em Touro, Virgem e Libra.','Em Câncer, Escorpião e Peixes, instituições oficiais inspiram desconfiança; é necessário um intermediário.'),
'Ladino':('Redes de informação e rotas discretas; favorecido em Gêmeos, Escorpião e Peixes.','Em Áries, Leão, Libra e Capricórnio, sua atuação exige credenciais extras.'),
}
CLASSES_MUNDO['Guerreiro'] = ('Autoridade marcial; favorecido em Áries, Leão e Sagitário.','Em Gêmeos, Virgem e Aquário, é necessário pagar pela mediação local.')
RECEITAS = {
'Florete de freixo':({'Ferro':2,'Madeira':2},'D20','Uma nova rolagem de D20 preparado por combate.'),
'Martelo de basalto':({'Ferro':3,'Couro':1},'D6','Uma nova rolagem de D6 preparado por combate.'),
'Cajado de maré':({'Cristal':2,'Madeira':2},'D20','Uma nova rolagem de D20 preparado por combate.'),
'Adaga do véu':({'Ferro':1,'Couro':2,'Cristal':1},'D6','Uma nova rolagem de D6 preparado por combate.'),
}
FACCOES = {'Câmara do Meridiano':'Concentra recursos e promete proteção rápida; seus contratos ocultos ameaçam a autonomia local.', 'Liga dos Doze':'Defende assembleias distritais, mas sua lentidão pode deixar bairros expostos.', 'Pacto dos Faróis':'Curadores, barqueiros e mensageiros que exigem serviço público verificável, sem lealdade hereditária.'}

# Perguntas opcionais: o interlocutor tem uma voz e interesses próprios.
DIALOGOS = {
'Áries': ('“Varek recebeu ordens de alguém que pode pagar pensões. Tenho medo de que meus veteranos acreditem nele antes de me ouvir.”','“Compare o selo do mandado com o do memorial. Há uma lasca no brasão verdadeiro. O outro é perfeito demais.”','“Uma guarda só serve à cidade enquanto a cidade puder contestar suas ordens.”'),
'Touro': ('“Se o celeiro fechar, os nobres comprarão farinha de fora. Os trabalhadores não terão essa escolha.”','“Veja as pesagens da entrada e da saída. A mesma carga foi cobrada duas vezes, mas só passou uma.”','“Quero contas abertas. Não me importa se quem as publica tem uma coroa ou um avental.”'),
'Gêmeos': ('“Se nos obrigarem a revelar todo remetente, o correio acabará. Se não fizermos nada, ele será usado para prender gente.”','“O relógio da torre oeste estava adiantado onze minutos. Só alguém dentro da rede conheceria a diferença.”','“Uma cidade precisa de mais de uma maneira de dizer a verdade.”'),
'Câncer': ('“Meu companheiro de turno não voltou. Não vou arriscar a vida de outros barqueiros sem um plano.”','“A chave proibida não abre uma comporta: ela abre todas. Foi fabricada para emergências que nunca deveriam acontecer.”','“Quando um reservatório seca, não é o sobrenome do governante que importa. É quem possui a chave.”'),
'Leão': ('“Minha família me ensinou a confundir prestígio com dever. Estou tentando aprender a diferença antes que seja tarde.”','“Os nomes da lista aparecem também nos contratos do arsenal. Eles financiam as torres e esperam concessões depois da votação.”','“Uma coroa pode unir a cidade, mas não deve ficar acima da lei. Se isso me custar o salão, que custe.”'),
'Virgem': ('“A paciente não é uma peça de evidência. Antes de conversar com ela, vou pedir que concorde.”','“Os sedativos tinham a etiqueta da enfermaria, mas o lacre vinha de um fornecedor de fora. Alguém pagou pela substituição.”','“Os curadores não juraram obediência a uma casa. Juraram cuidar de quem chega à porta.”'),
'Libra': ('“O decreto me daria autoridade para prender opositores. É precisamente por isso que preciso impedir que entre em vigor.”','“A sessão que supostamente o aprovou só acontecerá amanhã. O registro público do tribunal confirma a data.”','“Uma lei não é justa só porque saiu de um tribunal. Também precisa admitir recurso.”'),
'Escorpião': ('“Aceitei o dinheiro para pagar o remédio da minha irmã. Não quero que usem isso para dizer que todo o bairro é culpado.”','“As caixas tinham as marcas de três transportadoras. Kesh apagava as etiquetas assim que entravam no túnel.”','“O bairro precisa de proteção, não de um protetor que decida quem merece existir aqui.”'),
'Sagitário': ('“Meus batedores voltaram sem uma caravana inteira. Não é uma taxa ilegal qualquer: alguém está escolhendo o que chega à cidade.”','“Cada marco tem um entalhe voltado para o nascer do sol. Alguém girou dois deles na noite da lua nova.”','“Uma estrada é livre quando até quem não tem montaria consegue atravessá-la.”'),
'Capricórnio': ('“O capataz diz que o metal é para a defesa. Se for verdade, por que as famílias dos mineiros não podem ver os contratos?”','“Os contrapesos foram enviados sem substituição. O elevador funcionaria por algumas horas antes de falhar.”','“Nenhum conselho deveria poder ordenar trabalho que seus próprios filhos não aceitariam.”'),
'Aquário': ('“Eu desenhei as torres para dividir a água. Transformar minha invenção em instrumento de coerção não era parte do projeto.”','“O cristal possui uma matriz invertida. Em vez de distribuir energia, toda a rede alimentaria um único ponto.”','“Ciência financiada pelo povo precisa de fiscalização do povo, não apenas de mestres.”'),
'Peixes': ('“O homem que abrigo não é inocente de tudo. Mas se o entregarmos antes de ouvi-lo, nunca saberemos o que fez nem quem mandou.”','“Ele descreveu o mesmo clarão que vimos na festa. O primeiro teste foi em uma ilha que ficou três dias sem água.”','“Prefiro uma porta que se abre a uma promessa de segurança feita do outro lado de uma muralha.”'),
}
