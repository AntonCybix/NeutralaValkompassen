"""
Bygger distilled.json från valkompass_riksdagspartier_2026.json.

Frågebanken nedan är REDAKTIONELLT KODAD: varje partiposition är härledd direkt
ur partiets egna formuleringar i policy_areas (position_summary + main_proposals)
i källfilen. Skala:
   1.0  = tydligt för        0.5 = delvis/lutar för
   0.0  = uttalad mittenposition
  -0.5  = delvis/lutar emot  -1.0 = tydligt emot
   None = ingen tydlig position i källan  -> UTESLUTS ur matchningen (inget straff)

Parties: S, M, SD, V, C, KD, MP, L
"""
import json

src = json.load(open('valkompass_riksdagspartier_2026.json'))
PARTY_ORDER = src['metadata']['parties_included']
party_full = {p['id']: p['name'] for p in src['parties']}

# fyll ut: alla partier som inte nämns -> None
def pos(**kw):
    return {p: kw.get(p, None) for p in PARTY_ORDER}

# ---------------- PÅSTÅENDEN (likert: instämmer / tar avstånd) ----------------
LIKERT = [
 ("tax_work", "Skatten på arbete och pension bör sänkas.",
    pos(S=-0.5, M=1, SD=1, V=-1, KD=1, L=1), "economy_tax"),
 ("food_vat", "Matmomsen bör sänkas, åtminstone tillfälligt.",
    pos(M=1, KD=1, L=1), "economy_tax"),
 ("child_benefit", "Barnbidrag och studiestöd bör höjas.",
    pos(S=1, V=1, MP=1, KD=0.5), "economy_tax"),
 ("wealth_tax", "Höga inkomster och förmögenheter bör beskattas hårdare.",
    pos(V=1, S=0.5), "economy_tax"),
 ("bank_tax", "Banker bör beskattas extra för att finansiera välfärd.",
    pos(S=1, V=1), "economy_tax"),
 ("isk_taxfree", "Sparande på ISK bör vara skattefritt upp till 300 000 kr.",
    pos(SD=1, L=1), "economy_tax"),
 ("el_tax", "Elskatten bör sänkas.",
    pos(M=1, KD=1, L=1, SD=0.5, S=0.5), "transport_infrastructure"),
 ("profit_school", "Vinstuttag i skolan bör förbjudas eller fasas ut.",
    pos(S=1, V=1, MP=1, L=1), "school_education"),
 ("state_school", "Staten bör ta över ansvaret för skolan från kommunerna.",
    pos(L=1), "school_education"),
 ("small_classes", "Klasserna bör bli mindre och lärartätheten högre.",
    pos(L=1, S=1), "school_education"),
 ("screen_free", "Mobiler och skärmar bör begränsas kraftigt i skolan.",
    pos(L=1, KD=1), "school_education"),
 ("benefit_requirements", "Bidrag bör villkoras med tydliga krav och motprestation.",
    pos(SD=1, L=1, S=0.5, M=0.5), "migration_integration"),
 ("swedish_culture", "Svensk kultur och det svenska språket bör ges en starkare roll i politiken.",
    pos(SD=1, KD=0.5, L=0.5, S=0.5), "democracy_culture"),
 ("police_everywhere", "Det bör finnas synlig polis i alla kommuner.",
    pos(C=1, SD=1), "crime_security"),
 ("islamism_plan", "Sverige bör ha en nationell handlingsplan mot islamism.",
    pos(KD=1, SD=1), "crime_security"),
 ("abolish_regions", "Regionerna bör avskaffas och sjukvården styras mer nationellt.",
    pos(KD=1, V=0.5), "welfare_healthcare"),
 ("welfare_resources", "Vård och välfärd bör få mer resurser, även om det kräver höjda anslag.",
    pos(V=1, S=1, MP=1, C=0.5, KD=0.5, SD=0.5), "welfare_healthcare"),
 ("transit_card", "Staten bör införa ett billigt nationellt kollektivtrafikkort.",
    pos(MP=1, V=1, S=0.5), "transport_infrastructure"),
 ("railway", "Stora satsningar bör göras på järnväg och infrastruktur.",
    pos(V=1, L=1, C=1, MP=0.5, S=0.5), "transport_infrastructure"),
 ("rural_money", "Mer pengar bör gå till landsbygden och hela landet.",
    pos(C=1, V=0.5, SD=0.5), "rural_housing"),
 ("moving_tax", "Skatten vid bostadsförsäljning (flyttskatten) bör sänkas eller avskaffas.",
    pos(KD=1), "rural_housing"),
 ("preschool_fees", "Avgifterna för förskola och fritids bör sänkas.",
    pos(M=1, KD=1), "family_social"),
 ("shorter_workweek", "Arbetstiden bör kortas med bibehållen lön.",
    pos(V=1), "jobs_business"),
 ("raise_pensions", "Pensionerna bör höjas.",
    pos(S=1, V=1), "family_social"),
 ("public_service", "Public service bör värnas och stärkas.",
    pos(L=1, S=0.5), "democracy_culture"),
 ("culture_support", "Kultur och civilsamhälle bör få mer offentligt stöd.",
    pos(MP=1, V=0.5), "democracy_culture"),
 ("employer_fees", "Det bör bli billigare för företag att anställa (lägre arbetsgivaravgifter).",
    pos(C=1, L=1, KD=1, M=0.5, S=0.5), "jobs_business"),
 ("fuel_prices", "Drivmedelspriserna bör hållas nere och klimatkraven på drivmedel sänkas.",
    pos(SD=1, MP=-1, C=-0.5), "climate_energy"),
 ("nature_protection", "Naturskydd som strandskyddet och skyddet av skog bör stärkas.",
    pos(MP=1), "climate_energy"),
 ("renewables", "Sverige bör kraftigt bygga ut förnybar energi som sol och vind.",
    pos(MP=1, V=1, C=1, L=0.5, SD=-0.5), "climate_energy"),
]

# ---------------- VÄLJ ALTERNATIV (avsluta meningen / välj sida) ----------------
# options: lista av (label, value)  värde på samma -1..1-axel som positionerna
CHOOSE = [
 ("c_religious_school", "Religiösa friskolor bör …", "school_education",
    [("få finnas kvar och behandlas som andra friskolor", 1),
     ("tillåtas men med betydligt hårdare krav och granskning", 0),
     ("avvecklas eller förbjudas", -1)],
    pos(S=-1, L=-1)),
 ("c_crime", "I kampen mot brott bör tyngdpunkten ligga på …", "crime_security",
    [("hårdare straff och mer polis", 1),
     ("lika delar straff och förebyggande", 0),
     ("förebyggande arbete och sociala insatser", -1)],
    pos(SD=1, M=1, KD=0.5, L=0.5, S=0, C=0, MP=-1)),
 ("c_energy", "Elproduktionen bör byggas ut främst med …", "climate_energy",
    [("ny kärnkraft", 1),
     ("både kärnkraft och förnybart", 0),
     ("förnybart som sol och vind", -1)],
    pos(L=0.5, M=0.5, SD=0.5, C=-1, V=-1, MP=-1)),
 ("c_climate", "Klimat kontra ekonomi – vad bör väga tyngst?", "climate_energy",
    [("skärpta klimatmål, även om det kostar", 1),
     ("en balans mellan klimat och ekonomi", 0),
     ("jobb och låga kostnader främst", -1)],
    pos(MP=1, V=1, C=0.5, L=0, M=0, KD=0, S=0, SD=-1)),
 ("c_euro", "Sverige bör när det gäller euron …", "defense_security",
    [("hålla folkomröstning och närma sig euron", 1),
     ("inte ändra något nu", 0),
     ("behålla kronan och stå utanför euron", -1)],
    pos(L=1, SD=-1, V=-0.5)),
 ("c_migration", "Migrationspolitiken bör framöver …", "migration_integration",
    [("bli stramare", 1),
     ("ligga kvar ungefär som idag", 0),
     ("bli mer öppen och human", -1)],
    pos(SD=1, M=1, S=0.5, L=0.5, C=-0.5, V=-1, MP=-1)),
 ("c_welfare_private", "Privata vinstdrivna företag i vård, skola och omsorg bör …", "welfare_healthcare",
    [("få större utrymme och fler valmöjligheter", 1),
     ("vara kvar ungefär som idag", 0),
     ("begränsas till förmån för offentlig regi", -1)],
    pos(V=-1, S=-0.5, MP=-0.5)),
 ("c_taxes", "Skatterna i stort bör …", "economy_tax",
    [("sänkas", 1),
     ("ligga kvar på dagens nivå", 0),
     ("höjas för att finansiera välfärden", -1)],
    pos(M=1, L=1, SD=1, KD=1, C=0.5, S=-0.5, V=-1)),
 ("c_citizenship", "Kraven för medborgarskap och integration bör …", "migration_integration",
    [("skärpas tydligt", 1),
     ("vara ungefär som idag", 0),
     ("lättas, med mer fokus på rättigheter", -1)],
    pos(SD=1, M=0.5, L=0.5, KD=0.5, S=0.5, C=-0.5, MP=-0.5, V=-1)),
 ("c_welfare_money", "Pengar till välfärden kontra lägre skatt – vad väljer du?", "economy_tax",
    [("mer pengar till välfärden", 1),
     ("en balans", 0),
     ("lägre skatt framför nya satsningar", -1)],
    pos(V=1, S=1, MP=1, C=0.5, M=-0.5, L=-0.5, SD=0, KD=0)),
]

questions = []
for qid, text, positions, issue in LIKERT:
    questions.append({"id": qid, "fmt": "likert", "text": text, "issue": issue, "positions": positions})
for qid, stem, issue, opts, positions in CHOOSE:
    questions.append({"id": qid, "fmt": "choose", "text": stem, "issue": issue,
                      "options": [{"label": l, "val": v} for l, v in opts], "positions": positions})

# ---------------- kanoniska politikområden (budgetspelet) ----------------
PRIO = {'mycket hög': 3, 'hög': 2, 'medel': 1, 'låg': 0.5}
issue_label = {k: v['label'] for k, v in src['issue_index'].items()}
issue_desc = {k: v.get('description', '') for k, v in src['issue_index'].items()}
areas = {}
for p in src['parties']:
    pid = p['id']
    for pa in p['policy_areas']:
        par = pa.get('parent_issue_id') or pa['issue_id']
        if par not in areas:
            areas[par] = {'id': par, 'label': issue_label.get(par, pa.get('label', par)),
                          'desc': issue_desc.get(par, ''), 'parties': {}}
        prio_str = pa.get('priority_in_2026_material', '').lower()
        w = PRIO.get(prio_str, 0)
        prev = areas[par]['parties'].get(pid)
        if not prev or w > prev['weight']:   # behåll högsta prioriteten per parent-område
            areas[par]['parties'][pid] = {
                'prio': prio_str, 'weight': w,
                'summary': pa.get('position_summary', ''),
                'proposals': pa.get('main_proposals', []),
            }
areas_list = sorted(areas.values(), key=lambda a: -len(a['parties']))

parties = []
for p in src['parties']:
    parties.append({
        'id': p['id'], 'name': p['name'],
        'priorities': p.get('headline_priorities', []),
        'sources': [{'id': s.get('id'), 'title': s.get('title', ''), 'url': s.get('url', '')}
                    for s in p.get('sources', []) if s.get('url')][:5],
    })

out = {
    'meta': {'title': src['metadata']['title'], 'retrieved': src['metadata']['retrieved_date'],
             'limitations': src['metadata']['important_limitations']},
    'party_order': PARTY_ORDER, 'party_full': party_full,
    'parties': parties, 'questions': questions, 'areas': areas_list,
}
json.dump(out, open('distilled.json', 'w'), ensure_ascii=False)

nlik = sum(1 for q in questions if q['fmt'] == 'likert')
ncho = sum(1 for q in questions if q['fmt'] == 'choose')
print(f"questions: {len(questions)}  (likert {nlik}, choose {ncho})  areas: {len(areas_list)}")
for q in questions:
    n = sum(1 for v in q['positions'].values() if v is not None)
    print(f"  {q['fmt'][:3]} {n}/8  {q['text'][:58]}")
