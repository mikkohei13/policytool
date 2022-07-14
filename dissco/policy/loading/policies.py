from pathlib import Path

from policy.loading.utils import upsert_object, load_yaml
from policy.models import PolicyCategory, PolicyArea, PolicyComponent, PolicyComponentOption


def load_policies(root: Path):
    if not root.exists():
        return

    category_defs_path = root / 'categories.yml'
    if category_defs_path.exists():
        category_defs: list[dict] = load_yaml(category_defs_path)
        for category_def in category_defs:
            upsert_object(PolicyCategory, category_def)

    for policy_def_path in root.iterdir():
        if policy_def_path == category_defs_path:
            continue

        policy_def: dict = load_yaml(policy_def_path)
        policy_component_defs: list[dict] = policy_def.pop('components', [])
        category_id = policy_def.pop('category')
        category = PolicyCategory.objects.get(id=category_id)
        policy_area = upsert_object(PolicyArea, policy_def, category=category)
        if policy_component_defs:
            load_policy_components(policy_area, policy_component_defs)


def load_policy_components(policy_area: PolicyArea, policy_component_defs: list[dict]):
    id_start = (policy_area.id * 1000) + 1
    for pc_id, policy_component_def in enumerate(policy_component_defs, start=id_start):
        options = policy_component_def.pop('options', [])
        policy_component = upsert_object(PolicyComponent, policy_component_def, object_id=pc_id,
                                         policy_area=policy_area)
        if policy_component_def['type'] == 'options' and options:
            load_policy_component_options(policy_component, options)


def load_policy_component_options(policy_component: PolicyComponent, options: list[str]):
    option_id_start = (policy_component.id * 1000) + 1
    for pco_id, option_def in enumerate(options, start=option_id_start):
        upsert_object(PolicyComponentOption, object_id=pco_id, value=option_def,
                      policy_component=policy_component)
