from django.core.exceptions import ObjectDoesNotExist

from common.models import Institution
from policy.models import PolicyComponent, InstitutionPolicyComponent


def calculate_alignment(policy_component: PolicyComponent, institution: Institution) -> bool:
    # TODO: this actually needs to check the rules but for now it just returns whether the
    #       institution has a response to the policy component
    try:
        answer = InstitutionPolicyComponent.objects.get(policy_component=policy_component,
                                                        institution=institution)
        return True
    except ObjectDoesNotExist:
        return False
