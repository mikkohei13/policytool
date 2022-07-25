from itertools import count
from pathlib import Path

from django.core.management.base import OutputWrapper
from django.db import transaction

from common.loading_utils import UpsertManager, load_yaml, gen_offset_id
from maturity.models import Category, Question, Period


@transaction.atomic
def load(data_dir: Path, stdout: OutputWrapper, stderr: OutputWrapper):
    upsert_manager = UpsertManager()

    for category_def_path in data_dir.iterdir():
        load_category(category_def_path, upsert_manager)

    upsert_manager.delete_old()

    stdout.write(f'Load complete:')
    upsert_manager.report(stdout)


def load_category(source: Path, upsert_manager: UpsertManager):
    category_def = load_yaml(source)

    category = upsert_manager.upsert(Category, object_id=category_def['id'],
                                     name=category_def['name'])

    gen_question_id = count(gen_offset_id(category.id, 0))

    for subcategory, questions in category_def['questions'].items():
        for order, question in enumerate(questions):
            for period in [Period.CURRENT, Period.FUTURE_12]:
                question_id = next(gen_question_id)
                upsert_manager.upsert(Question, object_id=question_id,
                                      prompt=f'{subcategory}: {question}', order=order,
                                      period=period, category=category)
