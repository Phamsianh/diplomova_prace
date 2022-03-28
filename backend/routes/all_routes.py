import importlib
from typing import List

from fastapi import APIRouter, Depends, status

from routes.dependencies import oauth2_scheme as oa2s
from routes.pof_generator import POFGenerator
from routes.resource_registry import resource_registry

router = APIRouter(
    dependencies=[Depends(oa2s.oauth2_scheme)],
    # tags=["all resources"]
)

for resource_name, controller_name in resource_registry.items():
    pof_generator = POFGenerator(controller_name)
    router.get(
        f"/{resource_name}",
        response_model=List[pof_generator.response_schema],
        tags=[
            resource_name,
            # "Get Resource Collection"
        ]
    )(pof_generator.grc_generator())

    router.get(
        "/" + resource_name + "/{rsc_id}",
        response_model=pof_generator.response_schema,
        tags=[
            resource_name,
            # "Get Resource Instance"
        ]
    )(pof_generator.gri_generator())

    Controller_module = importlib.import_module(f'controller.{controller_name}')
    resource_controller = getattr(Controller_module, controller_name)()
    for related_resource in resource_controller.related_resource:
        router.get(
            "/" + resource_name + "/{rsc_id}/" + related_resource,
            tags=[
                resource_name,
                # "Get Related Resource"
            ]
        )(pof_generator.grr_generator(related_resource))

    router.post(
        f"/{resource_name}",
        response_model=pof_generator.response_schema,
        tags=[
            resource_name,
            # "Post Resource Collection"
        ],
        status_code=status.HTTP_201_CREATED
    )(pof_generator.prc_generator())

    router.patch(
        "/" + resource_name + "/{rsc_id}",
        response_model=pof_generator.response_schema,
        tags=[
            resource_name,
            # "Patch Resource Instance"
        ]
    )(pof_generator.pri_generator())

    router.delete(
        "/" + resource_name + "/{rsc_id}",
        status_code=status.HTTP_410_GONE,
        tags=[
            resource_name,
            # "Delete Resource Instance"
        ]
    )(pof_generator.dri_generator())
