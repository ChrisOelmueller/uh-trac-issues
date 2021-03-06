STATES = { # translate trac terminology to GH issues
		'new': 'open',
		'assigned': 'open',
		'reopened': 'open',
		'closed': 'closed',
		}

LABELS = {# merge some priority classes and components we only used rarely.
		# Set target label to '' and it will be removed from the label list for GH.
		# Default behavior is to keep all priority, component, type labels and lowercase them.
		'Code:AI': 'gamelogic',
		'Code:Combat': 'gamelogic',
		'SoC: Combat': 'gamelogic',
		'Code:Network': 'gamelogic',
		'Code:Game': 'gamelogic',
		'Code:Editor': 'editor',
		'Gui': 'gui',
		'Code:Interface': 'gui',
		'Engine-related': 'fife',
		'Scenarios / Campaigns': 'scenarios',
		'Sounds / Music': 'audio',
		'Wiki': 'website',
		'Website / Wiki': 'website',

		'blocker': 'blocker!',
		'critical': 'important',
		'important': 'important',
		'milestone feature': 'important',
		'major': '', # none
		'minor': '', # none
		'trivial': '', # none

		'Unspecified': '', # none
		'Management': '', # none
		'meta-ticket': '', # none
		'spam': '', # none
		'task': '', # none

		'opinion': 'enhancement',
		'start': 'starter',
		'defect': 'bug',
		}

MILESTONES = { # assign temporary, unique ID for each milestone
		'Future': 0,
		'2008.0': 1,
		'2008.1': 2,
		'2009.0': 3,
		'2009.1': 4,
		'2009.2': 5,
		'2010.1': 6,
		'2011.1': 7,
		'2011.2': 8,
		'GSoC 2011: Deadline': 9,
		'2011.3':10,
		'Website migration': 11,
		'2012.1':12,
		'2012.2':13,
		'2012.3':14,
		'Organization': 15,
		}

# map reporter and comment author names to either GH account {'login': username}
# or email address {'email': email@ddress) (only if GH account exists for that mail)
DEFAULT_USER = {'login' : 'unknown-horizons'}
USERNAMES = {
		'Andre' : {'login' : 'AndreR'},
		'Andre_Re' : {'login' : 'AndreR'},
		'Beliar' : {'login' : 'Beliaar'}, # yes, two 'a'
		'catpig' : {'login' : 'steffen123'},
		'christoph' : {'login' : 'siccegge'},
		'christoph_debian' : {'login' : 'siccegge'},
		'court-jus' : {'login' : 'court-jus'},
		'desophos' : {'login' : 'desophos'},
		'enno4uh' : {'login' : 'enno4uh'},
		'eoc' : {'login' : 'ChrisOelmueller'},
		'greyghost' : {'login' : 'GreyGhost'},
		'GreyGhost' : {'login' : 'GreyGhost'},
		'Grickit' : {'login' : 'grickit'},
		'gscai' : {'login' : 'otinn'},
		'H0ff1' : {'login' : 'hoffi'},
		'kaschte' : {'login' : 'kaschte'},
		'ketheriel' : {'login' : 'ketheriel'},
		'kili' : {'login' : 'stubb'},
		'kinshuksunil' : {'login' : 'kinshuksunil'},
		'Kiryx' : {'login' : 'kiryx'},
		'knutas' : {'login' : 'kennedyshead'},
		'kozmo' : {'login' : 'k0zmo'},
		'LinuxDonald' : {'login' : 'LinuxDonald'},
		'mage' : {'login' : 'mage666'},
		'manuel' : {'login' : 'manuelm'},
		'manue|' : {'login' : 'manuelm'},
		'MasterofJOKers' : {'login' : 'MasterofJOKers'},
		'mbivol' : {'login' : 'mihaibivol'},
		'mesutcank' : {'login' : 'mesutcank'},
		'mihaibivol' : {'login' : 'mihaibivol'},
		'mssssm' : {'login' : 'mssssm'},
		'MSSSSM' : {'login' : 'mssssm'},
		'mtfk' : {'login' : 'mitfik'},
		'mvBarracuda' : {'login' : 'mvbarracuda'},
		'nightraven' : {'login' : 'tschroefel'},
		'Nightraven' : {'login' : 'tschroefel'},
		'nihathrael' : {'login' : 'nihathrael'},
		'Nihathrael' : {'login' : 'nihathrael'},
		'Nihatrael' : {'login' : 'nihathrael'}, # sic (#273)
		'prock' : {'login' : 'prock-fife'},
		'qubodup' : {'login' : 'qubodup'},
		'RainCT' : {'login' : 'RainCT'},
		'Sharkash' : {'login' : 'Vivek-sagar'},
		'sidi' : {'login' : 'sids-aquarius'},
		'spq' : {'login' : 'spq'},
		'squiddy' : {'login' : 'squiddy'},
		'teraquendya' : {'login' : 'teraquendya'},
		'totycro' : {'login' : 'totycro'},
		'tuempl' : {'login' : 'tuempl'},
		'TunnelWicht' : {'login' : 'TunnelWicht'},
		'UnknownScribe' : {'login' : 'DanielStephens'},
		'wentam' : {'login' : 'wentam'},
		}

UNKNOWN = {
		'Amfidiusz' : {'login' : ''},
		'AyCe' : {'login' : ''},
		'Crendgrim' : {'login' : ''},
		'dario' : {'login' : ''},
		'dauerflucher' : {'login' : ''},
		'deathmaster9' : {'login' : ''},
		'dreimer' : {'login' : ''},
		'Emperor2k3' : {'login' : ''},
		'Fabio Pedretti' : {'login' : ''},
		'Foaly' : {'login' : ''},
		'Iankap99' : {'login' : ''},
		'Illusion' : {'login' : ''},
		'IwfY' : {'login' : ''},
		'janus' : {'login' : ''},
		'josch' : {'login' : ''},
		'Juarrox' : {'login' : ''},
		'LiveWire' : {'login' : ''},
		'lynxis' : {'login' : ''},
		'lynxis_' : {'login' : ''},
		'MadMonk' : {'login' : ''},
		'Manthus' : {'login' : ''},
		'Mastaxlokks' : {'login' : ''},
		'MoXe' : {'login' : ''},
		'Nikolai' : {'login' : ''},
		'o01eg' : {'login' : ''},
		'patty' : {'login' : ''},
		'pkerling' : {'login' : ''},
		'Psycojoker' : {'login' : ''},
		'Quassy' : {'login' : ''},
		'raymond' : {'login' : ''},
		'RealNitro' : {'login' : ''},
		'RM87' : {'login' : ''},
		'ronnie_c' : {'login' : ''},
		'scaabi' : {'login' : ''},
		'seblabel' : {'login' : ''},
		'Soeb' : {'login' : ''},
		'teraquendya' : {'login' : ''},
		'terwarf' : {'login' : ''},
		'Torv' : {'login' : ''},
		'Yeya' : {'login' : ''},
		'yonibear' : {'login' : ''},
		}
