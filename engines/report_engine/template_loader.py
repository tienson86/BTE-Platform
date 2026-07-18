class TemplateLoader:
    def load(self, template_name="default"):
        return {"name": template_name, "content": "BTE Report"}

    def list(self):
        return ["default"]
