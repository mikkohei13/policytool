from pathlib import Path

from common.loading_utils import load_yaml, gen_offset_id, UpsertManager
from policy.models import PolicyCategory, PolicyArea, PolicyComponent, PolicyComponentOption


def load_policies(root: Path, upsert_manager: UpsertManager):
    if not root.exists():
        return

    category_defs_path = root / 'categories.yml'
    area_defs_path = root / 'areas'

    if category_defs_path.exists():
        category_defs: list[dict] = load_yaml(category_defs_path)
        for category_def in category_defs:
            upsert_manager.upsert(PolicyCategory, category_def)

    if area_defs_path.exists():
        for policy_def_path in area_defs_path.iterdir():
            policy_def: dict = load_yaml(policy_def_path)

            # convert the category id into a category object
            category_id = policy_def.pop('category')
            category = PolicyCategory.objects.get(id=category_id)

            policy_area = upsert_manager.upsert(PolicyArea, policy_def, ignore={'components'},
                                                category=category)
            if 'components' in policy_def:
                load_policy_components(policy_area, policy_def['components'], upsert_manager)


def load_policy_components(policy_area: PolicyArea, policy_component_defs: list[dict],
                           upsert_manager: UpsertManager):
    for component_def in policy_component_defs:
        pc_id = gen_offset_id(policy_area.id, component_def.pop('ref'))
        policy_component = upsert_manager.upsert(PolicyComponent, component_def, ignore={'options'},
                                                 object_id=pc_id, policy_area=policy_area)
        if policy_component.is_option_based() and 'options' in component_def:
            load_policy_component_options(policy_component, component_def['options'],
                                          upsert_manager)


def load_policy_component_options(policy_component: PolicyComponent, options: list[dict],
                                  upsert_manager: UpsertManager):
    for order, option_def in enumerate(options, start=1):
        pco_id = gen_offset_id(policy_component.id, option_def.pop('ref'))
        upsert_manager.upsert(PolicyComponentOption, option_def, object_id=pco_id,
                              policy_component=policy_component, order=order)
