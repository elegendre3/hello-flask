from typing import List, Tuple

import spacy


nlp = spacy.load("en_core_web_sm")  # 13MB
# nlp = spacy.load("en_core_web_trf")  # 438MB


def predict(texts: str) -> str:
    out = ner([texts])
    return make_html(out)


def ner(texts: List[str]) -> List[Tuple[str, str]]:
    out = []
    for doc in nlp.pipe(texts, disable=["tagger", "parser"]):
        doc_ents = []
        for ent in doc:
            doc_ents.append((ent.text, ent.ent_type_, ent.ent_iob_))
        out.append(doc_ents)
    return out


def make_html(tagged_entities: List[Tuple[str, str]]):
    s = ''
    for doc in tagged_entities:
        for ent in doc:
            # print(ent)
            if ent[1] is '':
                s += f'<mark class={ent[2]}>{ent[0]} </mark>'
                # s += f'"{ent[0]}" - {ent[2]}<br>'
            else:
                s += f'<mark class={ent[1]}>{ent[0]} </mark>'
                # s += f'"{ent[0]}" - {ent[1]}<br>'
        s += '<br>'
    return s
