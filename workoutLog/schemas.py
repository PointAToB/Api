from typing import List, Optional, Literal, Union
from ninja import Schema


class GenreOut(Schema):
    id: int
    name: str
    slug: str


class ExerciseMediaOut(Schema):
    media_type: Literal["IMAGE", "VIDEO"]
    url: str
    order: int
    alt_text: str


class ExerciseOut(Schema):
    id: int
    name: str
    slug: str
    summary: str
    instructions_md: str
    unit_type: str
    default_sets: int
    default_reps_or_seconds: int
    default_rest_sec: int
    equipment: str
    media: List[ExerciseMediaOut] = []


class WorkoutCardOut(Schema):
    id: int
    title: str
    slug: str
    short_description: str
    hero_image: str
    difficulty: str
    genres: List[GenreOut]
    percent_complete: int


class StepExerciseOut(Schema):
    kind: Literal["EXERCISE"]
    id: int
    order: int
    exercise: ExerciseOut
    sets: int
    reps_or_seconds: int
    rest_between_sets_sec: Optional[int]
    tempo: str
    camera_required: bool


class StepRestOut(Schema):
    kind: Literal["REST"]
    id: int
    order: int
    rest_duration_sec: int
    rest_message: str


class StepNoteOut(Schema):
    kind: Literal["NOTE"]
    id: int
    order: int
    note_title: str
    note_body_md: str


StepOut = Union[StepExerciseOut, StepRestOut, StepNoteOut]


class WorkoutDetailOut(Schema):
    id: int
    title: str
    slug: str
    short_description: str
    hero_image: str
    difficulty: str
    genres: List[GenreOut]
    steps: List[StepOut]
    percent_complete: int


class SessionOut(Schema):
    id: int
    workout_id: int
    status: str
    current_step_order: int
    current_set_index: int
    percent_complete: int


class SessionEventIn(Schema):
    type: Literal["complete_set", "start_rest", "end_rest", "skip_step"]
    workout_step_id: Optional[int] = None
    set_index: Optional[int] = None
    reps_done: Optional[int] = None
    seconds_done: Optional[int] = None

