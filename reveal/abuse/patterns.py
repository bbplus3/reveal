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
    "you can't remember anything",
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
    "i won't allow it",
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
    "you can't do anything right",
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
    "you can't survive without me",
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
    "you can't have money",
    "i keep the money",
    "the money is mine",
    "the finances are mine",
    "you don't need money",
    "i give you an allowance",
    "you get an allowance",
    "i decide how money is spent",
    "you can't spend without asking",
    "you need to ask before spending",
    "i approve all purchases",
    "every purchase needs my approval",
    "you have no money of your own",

    # Economic dependency
    "you can't afford to leave",
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
    "your family doesn't care about you",
    "your family is toxic",
    "your family is bad for you",
    "your family causes problems",
    "your family doesn't understand you",
    "i don't want you seeing your family",
    "you spend too much time with your family",
    "your family is trying to control you",
    "your family doesn't want us together",
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
    "you can't go without me",
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
    "i won't be responsible for what i do",

    # Implicit threats
    "you know what happens when",
    "remember what happened last time",
    "don't make me",
    "don't push me",
    "don't test me",
    "don't make me angry",
    "you won't like me when i'm angry",
    "you know what i'm like when",
    "i lose control when",
    "i can't control myself when",
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
    "i can't live without you",
    "i won't survive without you",
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