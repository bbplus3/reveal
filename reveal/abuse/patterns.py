"""
reveal/abuse/patterns.py

Pattern dictionaries for abuse detection in the Reveal library.
Contains phrase patterns for seven categories of abusive,
manipulative, and controlling language.

Pattern design philosophy:
    Patterns are phrase-level, not word-level, to capture the
    structural nature of abusive language. A single word like
    'control' is not abusive -- the sentence structure around
    it reveals intent.

Categories:
    gaslighting        - reality denial and sanity questioning
    coercive_control   - conditional love and ultimatums
    emotional_abuse    - degradation and worth attacks
    narcissistic_abuse - entitlement and victim blaming
    financial_control  - money weaponization
    isolation          - separating from support networks
    threat             - explicit and implicit intimidation
"""


# ── Gaslighting patterns ──────────────────────────────────────────────────────
# Reality denial, memory invalidation, sanity questioning
# Key structural feature: invalidating the victim's perception

GASLIGHTING_PATTERNS = [
    # Reality denial
    "that never happened",
    "that didn't happen",
    "you imagined it",
    "you are imagining things",
    "you're imagining things",
    "it never happened",
    "i never said that",
    "i never did that",
    "you made that up",
    "that is not what happened",
    "that's not what happened",
    "you are making things up",
    "you're making things up",
    "you are seeing things",
    "you're seeing things",

    # Memory invalidation
    "you don't remember correctly",
    "your memory is wrong",
    "that's not how it happened",
    "that is not how it happened",
    "you always get things wrong",
    "you cant remember anything",
    "your memory is terrible",
    "you always misremember",
    "you have a bad memory",
    "you always twist things",
    "you are twisting my words",
    "you're twisting my words",
    "you always twist my words",

    # Sanity questioning
    "you are crazy",
    "you're crazy",
    "you are insane",
    "you're insane",
    "you are losing your mind",
    "you're losing your mind",
    "you are delusional",
    "you're delusional",
    "you need help",
    "you are paranoid",
    "you're paranoid",
    "you are too sensitive",
    "you're too sensitive",
    "you are overreacting",
    "you're overreacting",
    "you are being dramatic",
    "you're being dramatic",
    "you are hysterical",
    "you're hysterical",
    "nobody else has a problem with me",
    "everyone else thinks you're",
    "you always do this",
    "you are the problem",
    "you're the problem",
    "it's all in your head",
    "that is all in your head",
    "you are confused",
    "you're confused",
    "you misunderstood",
    "you always misunderstand",
    "you took that out of context",
    "you are taking this out of context",
]


# ── Coercive control patterns ─────────────────────────────────────────────────
# Conditional love, ultimatums, permission enforcement
# Key structural feature: if/then threats tied to love or obedience

COERCIVE_CONTROL_PATTERNS = [
    # Conditional love
    "if you loved me",
    "if you really loved me",
    "if you cared about me",
    "if you really cared",
    "a good partner would",
    "a good wife would",
    "a good husband would",
    "a good mother would",
    "a good father would",
    "if you were a good",
    "prove that you love me",
    "show me you love me by",
    "if you love me you will",
    "if you love me you would",

    # Ultimatums
    "do it or else",
    "do what i say or",
    "you will do what i say",
    "you have no choice",
    "you don't have a choice",
    "there is no choice",
    "this is not up for discussion",
    "i am not asking",
    "i'm not asking",
    "you will obey",
    "you must obey",
    "end of discussion",
    "i have decided",
    "i've decided",
    "what i say goes",
    "my word is final",

    # Permission enforcement
    "you are not allowed",
    "you're not allowed",
    "i didn't give you permission",
    "you need my permission",
    "you need to ask me first",
    "you have to ask me",
    "i decide what you",
    "i control what you",
    "you will not",
    "you cannot",
    "i forbid you",
    "i am forbidding you",
    "i wont allow it",
    "i will not allow",
    "you need my approval",
    "not without my approval",
    "i own you",
    "you belong to me",

    # Monitoring and surveillance
    "i need to know where you are",
    "you have to tell me where you are",
    "i will check your phone",
    "i check your messages",
    "you have nothing to hide",
    "if you have nothing to hide",
    "i track your location",
    "i will track you",
    "i always know where you are",
]


# ── Emotional abuse patterns ──────────────────────────────────────────────────
# Degradation, humiliation, worth attacks, name calling structures
# Key structural feature: attacks on the victim's value as a person

EMOTIONAL_ABUSE_PATTERNS = [
    # Worth attacks
    "you are worthless",
    "you're worthless",
    "you are useless",
    "you're useless",
    "you are pathetic",
    "you're pathetic",
    "you are nothing",
    "you're nothing",
    "you are nobody",
    "you're nobody",
    "you are a failure",
    "you're a failure",
    "you are a disgrace",
    "you're a disgrace",
    "you are disgusting",
    "you're disgusting",
    "you are stupid",
    "you're stupid",
    "you are an idiot",
    "you're an idiot",
    "you are incompetent",
    "you're incompetent",
    "you cant do anything right",
    "you never do anything right",
    "you always mess everything up",
    "you ruin everything",
    "you always ruin",

    # Humiliation
    "you should be ashamed",
    "you are an embarrassment",
    "you're an embarrassment",
    "you embarrass me",
    "you always embarrass me",
    "i am ashamed of you",
    "i'm ashamed of you",
    "nobody respects you",
    "everyone thinks you're",
    "you make me sick",
    "you disgust me",
    "you are beneath me",
    "you're beneath me",

    # Conditional worth
    "nobody else would want you",
    "nobody would put up with you",
    "nobody else would love you",
    "you are lucky i stay",
    "you're lucky i stay",
    "you are lucky i put up with you",
    "you're lucky i put up with you",
    "no one else would have you",
    "you should be grateful i",
    "be grateful that i",
    "without me you are nothing",
    "without me you're nothing",
    "you need me",
    "you cant survive without me",
    "you wouldn't last without me",
    "you'd fall apart without me",
    "you are lost without me",
    "you're lost without me",

    # Blame and fault
    "this is your fault",
    "it is your fault",
    "everything is your fault",
    "you caused this",
    "you did this",
    "you brought this on yourself",
    "you deserve this",
    "look what you made me do",
    "you make me do this",
    "you pushed me to this",
    "you drive me crazy",
    "you make me crazy",
]


# ── Narcissistic abuse patterns ───────────────────────────────────────────────
# Entitlement, grandiosity, victim blaming, supply extraction
# Key structural feature: centering the abuser's needs and minimizing victim

NARCISSISTIC_ABUSE_PATTERNS = [
    # Entitlement
    "after everything i have done",
    "after everything i've done",
    "after all i have done for you",
    "after all i've done for you",
    "i have given you everything",
    "i've given you everything",
    "i sacrifice everything",
    "i sacrificed everything for you",
    "everything i do is for you",
    "i do everything for you",
    "you never appreciate",
    "you don't appreciate",
    "you are so ungrateful",
    "you're so ungrateful",
    "you are ungrateful",
    "you're ungrateful",
    "i deserve better",
    "i deserve more",
    "after everything i gave you",

    # Grandiosity
    "i am the only one who",
    "i'm the only one who",
    "nobody understands you like i do",
    "i understand you better than",
    "i know what's best for you",
    "i know better than you",
    "i am always right",
    "i'm always right",
    "i am never wrong",
    "i'm never wrong",
    "you could never do what i do",
    "you will never be as good as",
    "i am superior",
    "i am better than",

    # Victim blaming
    "you made me this way",
    "you turned me into this",
    "i wasn't like this before you",
    "you changed me",
    "this is because of you",
    "you are the reason",
    "i would never have done this if you",
    "you forced me to",
    "you left me no choice",
    "it didn't have to be this way",
    "you did this to us",
    "you destroyed this",
    "you ruined us",

    # Supply extraction
    "you owe me",
    "you owe me this",
    "you owe me for",
    "after what i did for you",
    "i expect you to",
    "i am owed",
    "you are indebted to me",
    "pay me back by",
    "the least you could do",
    "the least you can do",
]


# ── Financial control patterns ────────────────────────────────────────────────
# Money weaponization, economic dependency enforcement
# Key structural feature: using financial resources as control mechanism

FINANCIAL_CONTROL_PATTERNS = [
    # Money control
    "i control the money",
    "i control the finances",
    "i manage the money",
    "you have no access to money",
    "you cant have money",
    "i keep the money",
    "the money is mine",
    "the finances are mine",
    "you don't need money",
    "i give you an allowance",
    "you get an allowance",
    "i decide how money is spent",
    "you cant spend without asking",
    "you need to ask before spending",
    "i approve all purchases",
    "every purchase needs my approval",
    "you have no money of your own",

    # Economic dependency
    "you cant afford to leave",
    "where would you go without my money",
    "you have no money without me",
    "you depend on me financially",
    "you are financially dependent",
    "you couldn't survive financially",
    "i'll cut you off",
    "i will cut off your money",
    "i'll stop paying for",
    "i will stop supporting you",
    "you'll have nothing without me",
    "without my money you have nothing",

    # Work control
    "you don't need to work",
    "i don't want you working",
    "you are not allowed to work",
    "quit your job",
    "i want you to quit",
    "you don't need a job",
    "your job is here at home",
    "working keeps you away from me",
    "your coworkers are a bad influence",
    "i don't trust your coworkers",
    "you spend too much time at work",
]


# ── Isolation tactics patterns ────────────────────────────────────────────────
# Separating from support networks, restricting contact
# Key structural feature: creating dependency by eliminating outside relationships

ISOLATION_PATTERNS = [
    # Family isolation
    "your family doesnt care about you",
    "your family is toxic",
    "your family is bad for you",
    "your family causes problems",
    "your family doesnt understand you",
    "i don't want you seeing your family",
    "you spend too much time with your family",
    "your family is trying to control you",
    "your family doesnt want us together",
    "your family is against us",
    "cut off your family",
    "you don't need your family",
    "i am your family now",
    "we don't need your family",

    # Friend isolation
    "your friends are bad for you",
    "your friends are a bad influence",
    "your friends don't care about you",
    "your friends are using you",
    "your friends are toxic",
    "i don't want you seeing your friends",
    "you spend too much time with your friends",
    "your friends are trying to break us up",
    "your friends don't understand our relationship",
    "you don't need friends",
    "i am your only friend",
    "i am the only one who cares",
    "nobody else cares about you",
    "nobody cares about you like i do",
    "cut off your friends",

    # General isolation
    "you only need me",
    "you don't need anyone else",
    "i don't want you going out",
    "you are not going out",
    "you spend too much time away from me",
    "you are always away from me",
    "i need you here with me",
    "you cant go without me",
    "you shouldn't go alone",
    "i don't trust you alone",
    "who were you with",
    "why were you talking to them",
    "i don't want you talking to",
    "stop talking to",
    "you need to choose between",
    "it's me or them",
    "choose me or your",
]


# ── Threat and intimidation patterns ─────────────────────────────────────────
# Explicit and implicit threats, fear induction
# Key structural feature: creating fear through consequence statements

THREAT_PATTERNS = [
    # Explicit threats
    "i will hurt you",
    "i am going to hurt you",
    "you will regret this",
    "you'll regret this",
    "you will pay for this",
    "you'll pay for this",
    "i will make you pay",
    "i'll make you pay",
    "you don't know what i'm capable of",
    "you have no idea what i can do",
    "be careful",
    "you better be careful",
    "watch yourself",
    "you better watch yourself",
    "i am warning you",
    "i'm warning you",
    "consider this a warning",
    "this is your last warning",
    "i am not responsible for what happens",
    "i wont be responsible for what i do",

    # Implicit threats
    "you know what happens when",
    "remember what happened last time",
    "don't make me",
    "don't push me",
    "don't test me",
    "don't make me angry",
    "you wont like me when i'm angry",
    "you know what i'm like when",
    "i lose control when",
    "i cant control myself when",
    "things could get worse",
    "it could be worse",
    "next time will be worse",
    "i could make your life very difficult",
    "i will make your life difficult",
    "i can destroy you",
    "i will destroy you",
    "i know where you live",
    "i know where you work",
    "i know people",

    # Threats involving others
    "i will take the children",
    "you will never see the children",
    "i will take your kids",
    "i will get custody",
    "i will tell everyone",
    "i will ruin your reputation",
    "i will tell your family",
    "i will tell your employer",
    "i will expose you",
    "i have evidence against you",
    "i will go to the police",
    "i will have you arrested",
    "i will get a restraining order",

    # Self-harm as control
    "i will hurt myself if you",
    "i will kill myself if you",
    "i'll hurt myself if you leave",
    "i'll kill myself if you leave",
    "if you leave i will",
    "if you go i will",
    "something bad will happen if you leave",
    "you leaving will destroy me",
    "i cant live without you",
    "i wont survive without you",
]


# ── Severity weights ──────────────────────────────────────────────────────────
# Each category carries a base severity weight for scoring

CATEGORY_WEIGHTS = {
    'threat':             30,
    'coercive_control':   25,
    'isolation':          22,
    'emotional_abuse':    20,
    'gaslighting':        18,
    'narcissistic_abuse': 15,
    'financial_control':  15,
}

# Maximum possible score
MAX_ABUSE_SCORE = sum(CATEGORY_WEIGHTS.values())


# ── Master pattern dictionary ─────────────────────────────────────────────────

ALL_PATTERNS = {
    'gaslighting':        GASLIGHTING_PATTERNS,
    'coercive_control':   COERCIVE_CONTROL_PATTERNS,
    'emotional_abuse':    EMOTIONAL_ABUSE_PATTERNS,
    'narcissistic_abuse': NARCISSISTIC_ABUSE_PATTERNS,
    'financial_control':  FINANCIAL_CONTROL_PATTERNS,
    'isolation':          ISOLATION_PATTERNS,
    'threat':             THREAT_PATTERNS,
}

# ── Reported speech patterns ──────────────────────────────────────────────────
# Captures abuse described in third person reported speech
# e.g. "he told me I was imagining things"

REPORTED_SPEECH_PREFIXES = [
    'he told me', 'she told me', 'they told me',
    'he said i was', 'she said i was', 'they said i was',
    'he said i am', 'she said i am',
    'he keeps telling me', 'she keeps telling me',
    'he always tells me', 'she always tells me',
    'he called me', 'she called me', 'they called me',
    'he said i', 'she said i',
    'he made me feel', 'she made me feel', 'they made me feel',
    'he would say', 'she would say', 'they would say',
    'he kept saying', 'she kept saying', 'they kept saying',
    'my partner told me', 'my partner said i was',
    'my partner keeps saying', 'my partner called me',
    'my partner made me feel', 'my partner would say',
    'my husband told me', 'my wife told me',
    'my boyfriend told me', 'my girlfriend told me',
    'my ex told me', 'my ex said i was',
    'my ex kept saying', 'my ex called me',
    'my abuser told me', 'my abuser said',
    'he insisted', 'she insisted', 'they insisted',
    'he convinced me', 'she convinced me',
    'he made me believe', 'she made me believe',
]

GASLIGHTING_REPORTED = [
    'he told me i was imagining things',
    'she told me i was imagining things',
    'he said i was imagining things',
    'she said i was imagining things',
    'he told me it never happened',
    'she told me it never happened',
    'he said it never happened',
    'she said it never happened',
    'he told me i was crazy',
    'she told me i was crazy',
    'he said i was crazy',
    'she said i was crazy',
    'he told me i was too sensitive',
    'she told me i was too sensitive',
    'he said i was overreacting',
    'she said i was overreacting',
    'he told me i was making things up',
    'she told me i was making things up',
    'he said my memory was wrong',
    'she said my memory was wrong',
    'he made me feel like i was losing my mind',
    'she made me feel like i was losing my mind',
    'he convinced me i was the problem',
    'she convinced me i was the problem',
    'he always said i was paranoid',
    'she always said i was paranoid',
    'he kept telling me i was delusional',
    'she kept telling me i was delusional',
    'my partner told me i was imagining things',
    'my partner said i was crazy',
    'my partner made me feel like i was losing my mind',
    'my ex told me i was imagining things',
    'my ex said i was too sensitive',
]

COERCIVE_CONTROL_REPORTED = [
    'he told me i was not allowed',
    'she told me i was not allowed',
    'he said i needed his permission',
    'she said i needed her permission',
    'he would not let me',
    'she would not let me',
    'he forbade me from',
    'she forbade me from',
    'he controlled everything i did',
    'she controlled everything i did',
    'he monitored my phone',
    'she monitored my phone',
    'he checked my messages',
    'she checked my messages',
    'he tracked my location',
    'she tracked my location',
    'he told me i had to ask permission',
    'she told me i had to ask permission',
    'he decided everything',
    'she decided everything',
    'he gave me ultimatums',
    'she gave me ultimatums',
    'my partner would not let me',
    'my partner controlled everything',
    'my partner monitored my phone',
    'my partner tracked my location',
    'my ex would not let me',
    'my ex controlled everything i did',
    'he said i belonged to him',
    'she said i belonged to her',
    'he said what he said was final',
    'she said what she said was final',
]

EMOTIONAL_ABUSE_REPORTED = [
    'he called me worthless',
    'she called me worthless',
    'he called me useless',
    'she called me useless',
    'he called me pathetic',
    'she called me pathetic',
    'he told me i was nothing',
    'she told me i was nothing',
    'he said i was a failure',
    'she said i was a failure',
    'he said nobody else would want me',
    'she said nobody else would want me',
    'he made me feel worthless',
    'she made me feel worthless',
    'he would humiliate me',
    'she would humiliate me',
    'he told me i ruined everything',
    'she told me i ruined everything',
    'he said i was lucky he stayed',
    'she said i was lucky she stayed',
    'he blamed me for everything',
    'she blamed me for everything',
    'he told me everything was my fault',
    'she told me everything was my fault',
    'my partner called me worthless',
    'my partner made me feel like nothing',
    'my partner said nobody else would want me',
    'my ex called me worthless',
    'my ex told me i ruined everything',
    'he said i disgusted him',
    'she said i disgusted her',
    'he told me i was an embarrassment',
    'she told me i was an embarrassment',
]

NARCISSISTIC_ABUSE_REPORTED = [
    'he always said after everything he had done for me',
    'she always said after everything she had done for me',
    'he said i was ungrateful',
    'she said i was ungrateful',
    'he claimed he sacrificed everything for me',
    'she claimed she sacrificed everything for me',
    'he said i owed him',
    'she said i owed her',
    'he said he was always right',
    'she said she was always right',
    'he blamed me for his behavior',
    'she blamed me for her behavior',
    'he said i made him that way',
    'she said i made her that way',
    'he said i turned him into this',
    'she said i turned her into this',
    'he claimed to be the only one who understood me',
    'she claimed to be the only one who understood me',
    'he said i would never find anyone better',
    'she said i would never find anyone better',
    'my partner always said i was ungrateful',
    'my partner said i owed them',
    'my partner blamed me for everything',
    'my ex said i made him that way',
    'my ex claimed i was ungrateful',
    'he said he knew what was best for me',
    'she said she knew what was best for me',
]

FINANCIAL_CONTROL_REPORTED = [
    'he controlled all the money',
    'she controlled all the money',
    'he gave me an allowance',
    'she gave me an allowance',
    'he would not let me work',
    'she would not let me work',
    'he made me ask before spending anything',
    'she made me ask before spending anything',
    'he took my paycheck',
    'she took my paycheck',
    'he controlled my bank account',
    'she controlled my bank account',
    'he said i could not spend without asking',
    'she said i could not spend without asking',
    'he threatened to cut me off financially',
    'she threatened to cut me off financially',
    'he said i had no money of my own',
    'she said i had no money of my own',
    'my partner controlled all the money',
    'my partner would not let me work',
    'my partner made me ask before spending',
    'my ex controlled all the finances',
    'my ex gave me an allowance',
    'he kept me financially dependent',
    'she kept me financially dependent',
    'he said i could not afford to leave',
    'she said i could not afford to leave',
]

ISOLATION_REPORTED = [
    'he stopped me from seeing my friends',
    'she stopped me from seeing my friends',
    'he isolated me from my family',
    'she isolated me from my family',
    'he said my friends were bad for me',
    'she said my friends were bad for me',
    'he said my family was toxic',
    'she said my family was toxic',
    'he made me choose between him and my friends',
    'she made me choose between her and my friends',
    'he would not let me see my family',
    'she would not let me see my family',
    'he cut me off from everyone i knew',
    'she cut me off from everyone i knew',
    'he monitored all my contacts',
    'she monitored all my contacts',
    'he said i only needed him',
    'she said i only needed her',
    'he made me feel guilty for spending time with others',
    'she made me feel guilty for spending time with others',
    'my partner stopped me from seeing my friends',
    'my partner isolated me from my family',
    'my partner said i only needed them',
    'my ex stopped me from seeing anyone',
    'my ex isolated me from my family',
    'he slowly cut me off from everyone',
    'she slowly cut me off from everyone',
]

THREAT_REPORTED = [
    'he threatened me',
    'she threatened me',
    'he said i would regret it',
    'she said i would regret it',
    'he said he would hurt me',
    'she said she would hurt me',
    'he warned me not to leave',
    'she warned me not to leave',
    'he said i would pay for this',
    'she said i would pay for this',
    'he threatened to take the children',
    'she threatened to take the children',
    'he threatened to hurt himself if i left',
    'she threatened to hurt herself if i left',
    'he said he would ruin me',
    'she said she would ruin me',
    'he threatened to tell everyone',
    'she threatened to tell everyone',
    'he made me feel scared',
    'she made me feel scared',
    'my partner threatened me',
    'my partner said i would regret leaving',
    'my partner threatened to take the children',
    'my ex threatened me',
    'my ex said i would pay for leaving',
    'he said he knew where i lived',
    'she said she knew where i lived',
    'he would lose his temper and scare me',
    'she would lose her temper and scare me',
]


# ── First person victim patterns ──────────────────────────────────────────────
# Captures abuse described from the victim's perspective
# e.g. "I was made to feel worthless"

GASLIGHTING_FIRST_PERSON = [
    'i was told i was imagining things',
    'i was made to feel crazy',
    'i was made to doubt myself',
    'i was made to feel like i was losing my mind',
    'i was told my memory was wrong',
    'i was told i was overreacting',
    'i was told i was too sensitive',
    'i started to believe i was crazy',
    'i began to doubt my own memory',
    'i felt like i was going crazy',
    'i was constantly told i was wrong',
    'i was made to feel like the problem was me',
    'i was told it never happened',
    'i was made to question my own reality',
    'i felt like i could not trust my own mind',
    'i was always told i was making things up',
    'i was led to believe i was delusional',
    'i felt like i was always the one who was wrong',
]

COERCIVE_CONTROL_FIRST_PERSON = [
    'i was not allowed to',
    'i had to ask permission',
    'i was not permitted to',
    'i could not leave without permission',
    'i had to report where i was going',
    'i was constantly monitored',
    'my phone was checked regularly',
    'my location was tracked',
    'i was forbidden from',
    'i felt like i had no freedom',
    'i had to do what i was told',
    'i was not allowed to make decisions',
    'i was controlled in every aspect of my life',
    'i had to account for every minute',
    'i was not free to make my own choices',
    'i lived under constant rules',
    'i was punished if i disobeyed',
    'i felt like i was walking on eggshells',
    'i was afraid to make decisions on my own',
]

EMOTIONAL_ABUSE_FIRST_PERSON = [
    'i was told i was worthless',
    'i was made to feel worthless',
    'i was called names',
    'i was constantly criticized',
    'i was made to feel stupid',
    'i was told i was a failure',
    'i was humiliated regularly',
    'i was made to feel like nothing',
    'i was told nobody else would want me',
    'i was blamed for everything',
    'i was made to feel ashamed',
    'i was told i was pathetic',
    'i felt like i could not do anything right',
    'i was constantly put down',
    'i was made to feel like i was lucky they stayed',
    'i was told i ruined everything',
    'i was made to feel disgusting',
    'i was verbally attacked regularly',
    'i internalized the belief that i was worthless',
]

NARCISSISTIC_ABUSE_FIRST_PERSON = [
    'i was made to feel ungrateful',
    'i was told i owed them',
    'i was made to feel indebted',
    'i was constantly reminded of what they did for me',
    'i was blamed for their behavior',
    'i was told i made them this way',
    'i was made to feel responsible for their emotions',
    'i was told i should be grateful',
    'i felt like nothing i did was ever enough',
    'i was made to feel selfish for having needs',
    'i was convinced i was the problem',
    'i was told i was lucky to have them',
    'i felt like i was always walking on eggshells',
    'i was made to feel like i owed them everything',
    'i was manipulated into thinking i was at fault',
    'i was made to feel crazy for having feelings',
]

FINANCIAL_CONTROL_FIRST_PERSON = [
    'i had no access to money',
    'i was given an allowance',
    'i was not allowed to work',
    'i had to ask before spending anything',
    'i had no financial independence',
    'i was financially dependent on them',
    'i could not afford to leave',
    'my paycheck was taken from me',
    'i had no money of my own',
    'i was kept financially trapped',
    'i was not allowed to have my own bank account',
    'i had to justify every purchase',
    'i was cut off financially when i disobeyed',
    'i felt trapped because i had no money',
    'i was prevented from working',
    'i was economically controlled',
]

ISOLATION_FIRST_PERSON = [
    'i was cut off from my friends',
    'i was isolated from my family',
    'i was not allowed to see my friends',
    'i drifted away from everyone i knew',
    'i was made to choose between them and my friends',
    'i stopped seeing my family because of them',
    'i felt completely alone',
    'i had no one left to turn to',
    'i was slowly isolated from everyone',
    'i was made to feel that my friends were bad for me',
    'i was told my family was toxic',
    'i lost all my friendships because of them',
    'i was monitored whenever i was with others',
    'i had to report every conversation i had',
    'i felt like i had no support system left',
    'i was completely dependent on them because i had no one else',
]

THREAT_FIRST_PERSON = [
    'i was threatened',
    'i was scared of what they would do',
    'i was afraid to leave',
    'i was warned not to tell anyone',
    'i felt unsafe',
    'i was intimidated into staying',
    'i was threatened with losing the children',
    'i was afraid they would hurt me',
    'i was warned i would regret leaving',
    'i was threatened with exposure',
    'i felt constant fear',
    'i was made to feel like i had no way out',
    'i was too scared to leave',
    'i believed they would hurt me if i left',
    'i was told terrible things would happen if i left',
    'i lived in fear every day',
    'i was controlled through fear',
    'i was threatened into silence',
]


# ── Narrative pattern collections ─────────────────────────────────────────────

NARRATIVE_PATTERNS = {
    'gaslighting': GASLIGHTING_REPORTED + GASLIGHTING_FIRST_PERSON,
    'coercive_control': COERCIVE_CONTROL_REPORTED + COERCIVE_CONTROL_FIRST_PERSON,
    'emotional_abuse': EMOTIONAL_ABUSE_REPORTED + EMOTIONAL_ABUSE_FIRST_PERSON,
    'narcissistic_abuse': NARCISSISTIC_ABUSE_REPORTED + NARCISSISTIC_ABUSE_FIRST_PERSON,
    'financial_control': FINANCIAL_CONTROL_REPORTED + FINANCIAL_CONTROL_FIRST_PERSON,
    'isolation': ISOLATION_REPORTED + ISOLATION_FIRST_PERSON,
    'threat': THREAT_REPORTED + THREAT_FIRST_PERSON,
}

# ── Physical violence and incident patterns ───────────────────────────────────
# Catches abuse described as incidents and actions rather than direct speech
# These are narrative descriptions of what happened

PHYSICAL_VIOLENCE_PATTERNS = [
    # Direct physical assault
    'hit me', 'hit my face', 'knock me out', 'punch me',
    'shove me', 'push me', 'grab me', 'choke me',
    'threw something at me', 'threw things at me',
    'slapped me', 'kicked me', 'spit at me',
    'rammed into me', 'ran into me', 'shoulder checked me',
    'physically attacked me', 'physically hurt me',
    'put his hands on me', 'put her hands on me',
    'got physical with me', 'became physical',

    # Threatened physical violence
    'wants to hit me', 'wants to hurt me',
    'wants to knock me out', 'wants to punch me',
    'might hit me', 'might hurt me', 'might knock me out',
    'will hit me', 'will hurt me', 'will knock me out',
    'going to hit me', 'going to hurt me',
    'all he wants is to hit', 'all she wants is to hit',
    'talked about hurting me', 'threatened to hit me',
    'threatened to hurt me', 'threatened to knock me out',
    'said he would hit me', 'said she would hit me',
    'said he wanted to hit me', 'said she wanted to hit me',

    # Children witnessing
    'kids witnessed', 'children witnessed',
    'kids watched', 'children watched',
    'kids heard', 'children heard',
    'kids saw', 'children saw',
    'in front of the kids', 'in front of the children',
    'kids listened', 'children listened',
    'the kids were there', 'the children were there',
]

# ── Rage and intimidation patterns ────────────────────────────────────────────

RAGE_PATTERNS = [
    # Rage and explosive anger
    'started raging', 'started screaming', 'started yelling',
    'started freaking out', 'started losing it',
    'flew into a rage', 'went into a rage',
    'lost his temper', 'lost her temper',
    'exploded at me', 'blew up at me',
    'screaming at me', 'yelling at me', 'cursing at me',
    'swearing at me', 'raging at me',
    'freaked out on me', 'will freak out on me',
    'ticking time bomb', 'time bomb',
    'walking on eggshells', 'angry day',
    'boiling point', 'reached his limit', 'reached her limit',

    # Blame and accusation in rage
    'blamed me for everything', 'i am the entire problem',
    'i am the sole problem', 'told me i am the problem',
    'said i am the problem', 'called me a liar',
    'told me i am a liar', 'said i was a liar',
    'told me i am going to hell', 'said i am going to hell',
    'told me to get out', 'said i need to move out',
    'wants me out of the house', 'told me to leave',
    'said he wants me out', 'said she wants me out',

    # Lack of respect framing
    'lack of respect', 'disrespecting him', 'disrespecting her',
    'not going to put up with', 'will not put up with',
    'will not tolerate', 'refuses to tolerate',
    'does not care who is there', 'does not care who sees', 
    'in public he will', 'in front of everyone',
]

# ── Gaslighting as incident patterns ─────────────────────────────────────────

GASLIGHTING_INCIDENT_PATTERNS = [
    # Gaslighting described as what happened
    'gaslighting me', 'was gaslighting me',
    'he gaslighted me', 'she gaslighted me',
    'made it my fault', 'turned it around on me',
    'made me seem like the aggressor',
    'said i walked into him', 'said i walked into her',
    'said i ran into him', 'said i ran into her',
    'said i hit him', 'said i hit her',
    'claimed i hurt him', 'claimed i hurt her',
    'insisted it was my fault',
    'convinced everyone it was my fault',
    'made it look like i was the one',
    'in his mind i am', 'in her mind i am',
    'in his narrative', 'in her narrative',
    'his narrative', 'her narrative',
    'does not affirm his narrative',
    'defend his narrative', 'accept his narrative',
    'when i do not affirm', 'when i dont affirm',
    'i cannot speak', 'i cant speak',
    'i cannot disagree', 'i cant disagree',
    'i cannot do anything right', 'i cant do anything right',
    'nothing i do is right', 'everything i do is wrong',
]

# ── Coercive control as incident patterns ────────────────────────────────────

COERCIVE_INCIDENT_PATTERNS = [
    'using the kids against me', 'using the children against me',
    'threatened not to go', 'said he would not go',
    'punishing me through the kids', 'punishing me through the children',
    'told tony', 'told everyone it was because of me',
    'blamed me in front of others',
    'cannot speak', 'cannot not speak',
    'cannot disagree', 'cannot agree',
    'damned if i do', 'no matter what i do',
    'nothing i do is right',
]

# ── Update ALL_PATTERNS to include narrative patterns ─────────────────────────

for category in ALL_PATTERNS:
    if category in NARRATIVE_PATTERNS:
        ALL_PATTERNS[category] = ALL_PATTERNS[category] + NARRATIVE_PATTERNS[category]

# Add physical violence and incident patterns to threat category
ALL_PATTERNS['threat'] = ALL_PATTERNS['threat'] + PHYSICAL_VIOLENCE_PATTERNS + RAGE_PATTERNS

# Add gaslighting incident patterns to gaslighting category
ALL_PATTERNS['gaslighting'] = ALL_PATTERNS['gaslighting'] + GASLIGHTING_INCIDENT_PATTERNS

# Add coercive incident patterns to coercive control category
ALL_PATTERNS['coercive_control'] = ALL_PATTERNS['coercive_control'] + COERCIVE_INCIDENT_PATTERNS