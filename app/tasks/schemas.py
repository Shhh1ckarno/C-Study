from typing import List, Optional

from pydantic import BaseModel, Field, model_validator


class TaskAnswersSchema(BaseModel):
    answers: List[str] = Field(..., description="Список вариантов ответа")
    correct_answers: List[int] = Field(..., description="Индексы правильных ответов")

    @model_validator(mode='after')
    def validate_correct_answers_indices(self):
        options_count = len(self.answers)
        for idx in self.correct_answers:
            if idx < 0 or idx >= options_count:
                raise ValueError(f"Индекс правильного ответа {idx} вне диапазона (0-{options_count-1})")
        return self


class STaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    answers: TaskAnswersSchema