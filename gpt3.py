import os

import openai

openai.api_key = os.getenv("OPENAI_KEY")


def main(prompt: str, max_tokens: int = 5):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.8,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1,
        stop=["\nHuman:", "\n"]
    )
    return response


def parties(parties_clause: str):
    """Finds parties information (PAR, DEF)"""
    few_shots = [
        'This is a party extraction task. The AI extracts every party and their respective definition from the clause.',

        'Parties Clause: DATE"), by and between Integral LifeSciences Corporation, a corporation organized under the '
        'laws of the State of Delaware, having a business office at 105 Morgan Lane, Plainsboro, New Jersey 08536 '
        '(hereinafter referred to as "INTEGRA"), and REVA Medical, Inc., a corporation duly organized and existing '
        'under the laws of California, having its principal office at 5751 Copley Drive, Suite B, San Diego, CA 92111 '
        '(hereinafter referred to as "REVA").',
        'Extracted:\n',
        '1. Integral LifeSciences Corporation, defined as "INTEGRA".',
        '2. REVA Medical, Inc., defined as "REVA".',
        '###',

        'Parties Clause: effective as of the Closing Date, by and between Bottomline Technologies (de), Inc., a '
        'Delaware corporation ("Tech"), and Bank of America, N.A., a national banking association ("Bank").',
        'Extracted:\n'
        '1. Bottomline Technologies (de), Inc., defined as "Tech',
        '2. Bank of America, N.A., defined as "Bank".',
        '###',

        'Parties Clause: December 7, 2010 between Conrad J. Hunter (the “Executive"), NTELOS Inc., a Virginia '
        'corporation, and NTELOS Holdings Corp., a Delaware corporation (“Holdings") (and collectively with '
        'NTELOS, Inc., the “Company") recites and provides as follows:',
        'Extracted:\n',
        '1. Conrad J. Hunter, defined as "Executive"',
        '2. NTELOS Inc., defined as "Company" (collectively with NTELOS, Holdings Corp.)',
        '3. NTELOS Holdings Corp., defined as "Company" (collectively with NTELOS, Inc.)',
        '###',

        'Parties Clause: GUARANTEE AGREEMENT, dated as of February 12, 2010, made by GMAC Inc., a Delaware corporation '
        '(the "Company", which term includes any successor under the Indenture hereinafter referred to) and each of the '
        'parties hereto designated on the signature pages hereof as a Guarantor (including each Person that '
        'becomes a party hereto pursuant to Section 3.12, each a "Guarantor"), by and between '
        'the Company and The Bank of New York Mellon, as trustee (in such capacity, the "Trustee").',
        'Extracted:\n',
        '1. GMAC Inc., defined as "Company"',
        '2. The Bank of New York Mellon, defined as "Trustee"',
        '###',
    ]

    prompt = "\n".join(few_shots) + "\nParties Clause: " + parties_clause + "\nExtracted:\n1."
    # print(prompt)
    response = openai.Completion.create(
        engine="curie",
        prompt=prompt,
        temperature=1,
        top_p=0.5,
        max_tokens=200,
        frequency_penalty=1,
        presence_penalty=1,
        stop=["\nParties Clause:"]
    )
    return response


if __name__ == "__main__":


    # TEST ONE
    # prompt = [
    #     "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.",
    #     "Human: Hello, who are you?",
    #     "AI: I am an AI created by OpenAI. How can I help you today?",
    #     "Human:If it is raining outside, what should I wear?",
    #     "AI:",
    #     ]
    # max_tokens = 20
    # response = main("\n".join(prompt), max_tokens)
    # print(response)


    # PARTIES EXTRACTION
    prompt = 'as of the date of the last signature below, effective May 17, 2010 by and between ' \
             'Elsinore Services, Inc., a Delaware corporation ("Client"), and FaceTime Strategy LLC, a ' \
             'Virginia limited liability company ("FaceTime"), and provides as follows:'
    response = parties(prompt)
    print('Parties Clause: {}'.format(prompt))
    print('What GPT3 thinks:')
    print('1.{}'.format(response["choices"][0]["text"]))
    print('Finish Reason: [{}]'.format(response["choices"][0]["finish_reason"]))
