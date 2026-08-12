# Structures to Avoid

## Binary Contrasts (Negative Parallelism)

The single most commonly identified AI writing tell. Creates false drama by framing everything as a surprising reframe. One in a piece can work; multiple instances per piece is a strong AI signal. Before LLMs, people did not write like this at scale.

| Pattern | Problem |
|---------|---------|
| "Not because X. Because Y." / "Not because X, but because Y." | Telegraphed reversal |
| "[X] isn't the problem. [Y] is." | Formulaic reframe |
| "The answer isn't X. It's Y." | Predictable pivot |
| "It feels like X. It's actually Y." | Setup/reveal cliche |
| "The question isn't X. It's Y." | Rhetorical misdirection |
| "Not X. But Y." / "not X, it's Y" / "isn't X, it's Y" | Mechanical contrast |
| "It's not this. It's that." | Same formula, different words |
| "stops being X and starts being Y" | False transformation arc |
| "doesn't mean X, but actually Y" | Negation-then-assertion crutch |
| "is about X but not Y" | False distinction |
| "not just X but also Y" | Additive hedge |

**Fix:** State Y directly. "The problem is Y." Drop the negation entirely.

## Negation-Then-Reframe Couplet

The two-sentence cousin of the binary contrast, and one of the most reliable AI signatures in otherwise formal prose. Sentence one denies something with a full verb phrase, sentence two opens with a bare pronoun and supplies the "real" answer. Formula is "X does not [verb] Y. It [verb]s Z." The denial exists only to set up the pivot, and the pivot is almost always a restatement dressed as a revelation.

| Pattern | Problem |
|---------|---------|
| "That protection does not eliminate risk. It changes where the risk sits." | Denial exists only to stage the reframe |
| "The tool doesn't replace judgment. It sharpens it." | Pronoun-subject pivot, zero new information |
| "This isn't a fix. It's a workaround." | Two-beat reveal of a single fact |
| "Encryption doesn't solve the problem. It relocates it." | Same verb negated then substituted |
| "The model didn't fail. It did exactly what we asked." | Contrarian pivot as false insight |
| "AI won't take your job. It'll change it." | Headline cadence, no content |

Tells that identify it: the second sentence starts with It/They/That, the two verbs are near-synonyms or antonyms of each other, and deleting the first sentence loses nothing.

**Fix:** Keep the second sentence, drop the first, and make the claim specific. "That protection does not eliminate risk. It changes where the risk sits." becomes "The design moves exposure into records governance and key custody." If the denial carries real information (a reader would genuinely expect the opposite), fold it into a single sentence with a subordinate clause.

## Rather-Than Padding (The Invented Foil)

The third member of the binary-contrast family, and the hardest to notice because each instance looks harmless. A plain statement gets a rejected alternative bolted onto it with "rather than," "instead of," or "as opposed to." The foil was never on the table. It exists so the sentence sounds like the product of a considered choice.

The frequency is the signal. One is ordinary English. A draft where nearly every methodological sentence rejects something is running a reflex. One report reviewed under this skill used "rather than" 20 times, including three restatements of the same patient-versus-epoch contrast.

| Pattern | Problem |
|---------|---------|
| "The six patients were divided by identity rather than by epoch." | The division is the fact. The foil adds nothing |
| "...combined here rather than treated as competitors" | Nobody proposed treating them as competitors |
| "...from expert-annotated clinical EEG rather than from a preprocessed teaching file" | Strawman that flatters the author's choice |
| "That gap is deliberate and is corrected later rather than ignored." | No reader suspected it would be ignored |
| "...survives at a magnitude of roughly 9 log-odds rather than being shrunk toward the rest" | The magnitude is the claim |
| "...should be read as an order of magnitude rather than a specification" | Two ways of saying one thing |

**The deletion test.** Cut the "rather than" clause and read what is left. If the sentence still says what you meant, the clause was padding. "The six patients were divided by identity." Done.

Keep the contrast only when the reader's default assumption genuinely is the rejected alternative *and* you do not explain that contrast anywhere else. In the example above the patient-versus-epoch distinction mattered, but the next paragraph already spent four sentences on it, so the inline foil was the third time the same point was made.

Watch for the repetition sub-tell. When the same opposition appears in three sentences with different nouns ("by identity rather than by epoch," "by patient rather than by epoch," "about seizures rather than about epochs"), the writer is restating a single idea and the "rather than" is what makes it feel new each time.

**Fix:** State the thing. If the alternative genuinely needs rejecting, give it its own sentence and say why it fails.

## Negative Listing

Listing what something is *not* before revealing what it *is*. A dramatic countdown through negation.

| Pattern | Problem |
|---------|---------|
| "Not a X... Not a Y... A Z." | Dramatic buildup through negation |
| "It wasn't X. It wasn't Y. It was Z." | Same structure, past tense |
| "Not ten. Not fifty. Five hundred." | Numerical countdown reveal |
| "not recklessly, not completely, but enough" | Hedging disguised as precision |

**Fix:** State Z. The reader does not need the runway.

## Dramatic Fragmentation

Sentence fragments for emphasis read as manufactured profundity. RLHF training has pushed models toward "writing for readability" aimed at the lowest common denominator: one thought per sentence, no mental state-keeping required. No human writes first drafts this way.

| Pattern | Problem |
|---------|---------|
| "[Noun]. That's it. That's the [thing]." | Performative simplicity |
| "X. And Y. And Z." | Staccato drama |
| "This unlocks something. [Word]." | Artificial revelation |
| "He published this. Openly. In a book." | Fragment stacking for emphasis |
| "Platforms do." | Orphaned fragment as punchline |

**Fix:** Complete sentences. Trust content over presentation.

## Self-Posed Rhetorical Questions

The model asks a question nobody was asking, then answers it for dramatic effect.

| Pattern | Problem |
|---------|---------|
| "The result? Devastating." | Manufactured suspense |
| "The worst part? Nobody saw it coming." | Same formula |
| "What if [reframe]?" | Socratic posturing |
| "Here's what I mean:" | Redundant preview |
| "Think about it:" | Condescending prompt |
| "And that's okay." | Unnecessary permission |

**Fix:** Make the point. Let readers draw conclusions.

## Anaphora Abuse

Repeating the same sentence opening multiple times in quick succession.

| Pattern | Problem |
|---------|---------|
| "They assume that... They assume that... They assume that..." | Mechanical repetition |
| "They could expose... They could offer... They could provide..." | List disguised as prose |
| "They have built X, but not Y. They have built A, but not B." | Parallel structure stacking |

**Fix:** Vary sentence openings. Combine related points into single sentences.

## Tricolon Abuse

Overuse of the rule-of-three pattern. A single tricolon is fine; multiple back-to-back tricolons are an AI pattern.

| Pattern | Problem |
|---------|---------|
| "Products impress; platforms empower. Products solve; platforms create." | Parallel tricolon stacking |
| "identity, payments, compute, distribution" | Extended lists masquerading as analysis |
| "workflows, decisions, and interactions" | Three-item groupings everywhere |

**Fix:** Use two items or one. Break the three-item habit.

## False Agency

Giving inanimate things human verbs. AI loves this because it avoids naming the actor.

| Pattern | Problem |
|---------|---------|
| "a complaint becomes a fix" | Someone fixed it. |
| "a bet lives or dies in days" | Someone kills or ships the project. |
| "the decision emerges" | Someone decides. |
| "the culture shifts" | People change behavior. |
| "the conversation moves toward" | Someone steers. |
| "the data tells us" | Someone reads it and draws a conclusion. |
| "the market rewards" | Buyers pay for things. |

**Fix:** Name the human. "The team fixed it that week" beats "the complaint becomes a fix." If no specific person fits, use "you" to put the reader in the seat.

## Narrator-from-a-Distance

Floating above the scene instead of putting the reader in it.

| Pattern | Problem |
|---------|---------|
| "Nobody designed this." | Disembodied observation |
| "This happens because..." | Lecturer voice |
| "This is why..." | Same |
| "People tend to..." | Armchair sociologist |

**Fix:** Put the reader in the room. "You don't sit down one day and decide to..." beats "Nobody designed this."

## Passive Voice

Every sentence needs a subject doing something. Passive voice hides the actor and drains energy.

| Pattern | Fix |
|---------|-----|
| "X was created" | Name who created it |
| "It is believed that" | Name who believes it |
| "Mistakes were made" | Name who made them |
| "The decision was reached" | Name who decided |

**Fix:** Find the actor. Put them at the front of the sentence.

## Listicle in a Trench Coat

Numbered or labeled points dressed up as continuous prose. The model writes a listicle but wraps each point in a paragraph starting with "The first... The second... The third..." to disguise the format.

| Pattern | Problem |
|---------|---------|
| "The first wall is... The second wall is... The third wall is..." | Numbered list pretending to be prose |
| "The second takeaway is... The third takeaway is..." | Same |

**Fix:** If the content is a list, present it as a list. If it should be prose, weave the points together without numbering.

## Announced-Count Preamble

A topic sentence that names a number and withholds the content, followed by the items themselves. Formula is "[Subject] [verb]s in X ways. The first is..." The count tells the reader nothing they need before the items, and the sentence exists only to promise that items are coming. The tell is that the preamble cannot stand alone. Delete the sentences after it and it says nothing.

This is the parent of Listicle in a Trench Coat, not a synonym for it. The listicle tell is the ordinals in the body; this tell is the number in the preamble. Stripping "First / Second / Third" out of the body does not fix it, because the announcement is still doing the same stalling work.

| Pattern | Problem |
|---------|---------|
| "Prior medical knowledge entered the analysis at two points. The first is the population base rate." | Count announced, content deferred a full sentence |
| "There are three reasons for this. First..." | The canonical form |
| "The problem has two dimensions. One is cost, the other is time." | Same stall without ordinals |
| "Two things stand out here." | Withholds both of them |
| "This section makes four arguments." | Count with no content at all |
| "The priors earned their place in two distinct ways." | "distinct" padding a bare count |

Counting is legitimate when the number is the point, as in "Only two of the nine sites reported a failure." The number there is a finding. In the pattern above it is scaffolding.

**Fix:** Lead with the first item and let the rest follow. "Prior medical knowledge entered the analysis at two points. The first is the population base rate." becomes "The population base rate is the first place prior medical knowledge enters the analysis." Better still, drop the count and join the items directly: "Prior medical knowledge enters through the population base rate and through the priors on the regression coefficients." A reader who wants the count can see it.

## Superficial Participle Analyses

Tacking a present participle phrase onto the end of a sentence to inject shallow analysis.

| Pattern | Problem |
|---------|---------|
| "contributing to the region's rich cultural heritage" | Hollow significance-signaling |
| "highlighting its enduring legacy" | Same |
| "underscoring its role as a dynamic hub" | Same |
| "reflecting broader trends in..." | Same |

**Fix:** Either make a specific analytical claim or delete the participle phrase.

## False Ranges

"From X to Y" constructions where X and Y are not on any real scale. In legitimate use, "from X to Y" implies a spectrum with a meaningful middle. AI uses it to list two loosely related things.

| Pattern | Problem |
|---------|---------|
| "From innovation to implementation to cultural transformation." | No real spectrum |
| "From the singularity of the Big Bang to the grand cosmic web." | Grandiose range with nothing in between |
| "From problem-solving to scientific discovery to artistic expression." | Fancy list, not a range |

**Fix:** If the items are a list, list them. If there is a real spectrum, describe it.

## Historical Analogy Stacking

Rapid-fire listing of historical companies or tech revolutions to build false authority. Common in technical writing.

| Pattern | Problem |
|---------|---------|
| "Apple didn't build Uber. Facebook didn't build Spotify." | Shotgun historical references |
| "Every major shift -- the web, mobile, social, cloud -- followed..." | Revolution-listing |
| "Take Spotify... Or consider Uber... Airbnb followed... Shopify is another..." | Sequential name-dropping |

**Fix:** Use one example, examine it in depth. One well-analyzed case beats five name-drops.

## "Despite Its Challenges..."

AI acknowledges problems only to immediately dismiss them. Always follows the same beat.

| Pattern | Problem |
|---------|---------|
| "Despite these challenges, the initiative continues to thrive." | Formulaic optimism |
| "Despite its prosperity, [X] faces challenges typical of..." | Structured dismiss-and-pivot |

**Fix:** If challenges are worth mentioning, analyze them. If they are not, skip them.

## Sentence Starters to Avoid

| Pattern | Fix |
|---------|-----|
| Sentences starting with What, When, Where, Which, Who, Why, How | Restructure. Lead with the subject or the verb. |
| Paragraphs starting with "So" | Start with content |
| Sentences starting with "Look," | Remove |

Wh- openers become a crutch. "What makes this hard is..." becomes "The constraint is..." or better, name the specific constraint.

## Formulaic Constructions

| Pattern | Problem |
|---------|---------|
| "By the time X, I was Y." | Narrative template |
| "X that isn't Y" | Indirect. Say "X is broken" |

## Rhythm Patterns

| Pattern | Fix |
|---------|-----|
| Three-item lists | Use two items or one |
| Questions answered immediately | Let questions breathe or cut them |
| Every paragraph ends punchily | Vary endings |
| Em dashes | Remove. Use commas or periods. |
| Staccato fragmentation | Do not stack short punchy sentences |
| "Not always. Not perfectly." | Hedging disguised as reassurance |

## Formatting Tells

| Pattern | Problem |
|---------|---------|
| Bold-first bullets | Every list item starting with a bolded keyword is an AI signal |
| Unicode arrows (→) | Use -> or => or plain text instead |
| Smart/curly quotes | Use straight quotes |
| Signposted conclusions ("In conclusion...") | Let the writing conclude naturally |
| Fractal summaries | Do not summarize what you are about to say, say it, then summarize what you said |

## One-Point Dilution

Making a single argument and restating it in ten different ways. The model pads a simple thesis to feel comprehensive by rephrasing the same idea with different metaphors, examples, and framings.

**Fix:** State the point once, support it, move on. If the piece circles back to the same claim more than twice, cut the repetitions.

## The Dead Metaphor

Latching onto a single metaphor and using it in every paragraph. A human writer introduces a metaphor, uses it, and moves on. AI repeats the same metaphor 5-10 times.

**Fix:** Use a metaphor once or twice. Then drop it.

## Invented Concept Labels

AI clusters invented compound labels that sound analytical without being grounded. It appends abstract problem-nouns (paradox, trap, creep, divide, vacuum, inversion) to domain words and uses them as if they are established terms.

| Pattern | Problem |
|---------|---------|
| "the supervision paradox" | Invented term treated as established |
| "the acceleration trap" | Same |
| "workload creep" | Same |

**Fix:** If the concept needs a name, define it. If it does not need a name, describe it in plain language.

## Word Patterns

| Pattern | Problem |
|---------|---------|
| Lazy extremes (every, always, never, everyone, everybody, nobody) | False authority. Use specifics instead of sweeping claims. |
| All adverbs (-ly words, "really," "just," "literally," "genuinely," "honestly," "simply," "actually") | Empty emphasis. See phrases.md for full list. |
