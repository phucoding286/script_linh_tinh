from freegpt_modules.__llmApiGpt import GPT
from freegpt_modules.__sessionCookies import api, headers, payloads


class ModuleGPT(GPT):
    def __init__(self, top_p=0.9, temperature=0.7, presence_penalty=0, frequency_penalty=0,
        model_name='gpt-3.5-turbo', instructor="", payloads=payloads, api=api, headers=headers):

        super().__init__(top_p=top_p, temperature=temperature, presence_penalty=presence_penalty,
                         frequency_penalty=frequency_penalty, model_name=model_name, 
                         instructor=instructor, payloads=payloads, api=api, headers=headers)