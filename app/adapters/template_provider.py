from app.application.result import Result


class TemplateProvider:
    def generate(self, briefing: str, **kwargs) -> Result:
        try:
            lines = []
            lines.append("Cena 1: " + briefing[:50])
            lines.append("Cena 2: Continuação da história")

            script = "\n".join(lines)

            return Result.success(
                data={
                    "script": script,
                    "provider": "TemplateProvider",
                    "time": 0.01,
                    "quality": "template"
                }
            )
        except Exception as e:
            return Result.failure(error=str(e))
