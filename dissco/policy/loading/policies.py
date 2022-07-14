from pathlib import Path

from policy.loading.utils import upsert_object, load_yaml
from policy.models import PolicyCategory, PolicyArea, PolicyComponent, PolicyComponentOption


def load_policies(root: Path):
    if not root.exists():
        return

    category_defs_path = root / 'categories.yml'
    area_defs_path = root / 'areas'

    if category_defs_path.exists():
        category_defs: list[dict] = load_yaml(category_defs_path)
        for category_def in category_defs:
            result = upsert_object(PolicyCategory, category_def)
            yield result.result

    if area_defs_path.exists():
        for policy_def_path in area_defs_path.iterdir():
            policy_def: dict = load_yaml(policy_def_path)

            # convert the category id into a category object
            category_id = policy_def.pop('category')
            category = PolicyCategory.objects.get(id=category_id)

            policy_area, result = upsert_object(PolicyArea, policy_def, ignore={'components'},
                                                category=category)
            yield result
            if 'components' in policy_def:
                yield from load_policy_components(policy_area, policy_def['components'])


def load_policy_components(policy_area: PolicyArea, policy_component_defs: list[dict]):
    id_start = (policy_area.id * 1000) + 1
    for pc_id, component_def in enumerate(policy_component_defs, start=id_start):
        policy_component, result = upsert_object(PolicyComponent, component_def, ignore={'options'},
                                                 object_id=pc_id, policy_area=policy_area)
        yield result

        if policy_component.is_option_based() and 'options' in component_def:
            yield from load_policy_component_options(policy_component, component_def['options'])


def load_policy_component_options(policy_component: PolicyComponent, options: list[str]):
    option_id_start = (policy_component.id * 1000) + 1
    for pco_id, option_def in enumerate(options, start=option_id_start):
        result = upsert_object(PolicyComponentOption, object_id=pco_id, value=option_def,
                               policy_component=policy_component)
        yield result.result
