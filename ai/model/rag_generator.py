from optimum.rbln import RBLNLlamaForCausalLM

class GenerationModel(RBLNLlamaForCausalLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model_id = "./ai/model/EEVE-Korean-Instruct-10.8B-v1.0-AIF-QA"
        self.name_or_path =  model_id