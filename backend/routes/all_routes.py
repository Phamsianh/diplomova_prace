from typing import List

from fastapi import APIRouter, Depends, status
from routes.dependencies import oauth2_scheme as oa2s
from routes.resource_registry import resource_registry as rr
from routes.pof_generator import POFGenerator
import importlib

router = APIRouter(
    dependencies=[Depends(oa2s.oauth2_scheme)],
    tags=["all resources"]
)


for r, c in rr.items():
    pof_generator = POFGenerator(c)
    router.get(f"/{r}", response_model=List[pof_generator.response_schema])(pof_generator.grc_generator())
    router.get("/" + r + "/{rsc_id}", response_model=pof_generator.response_schema)(pof_generator.gri_generator())

    RC_module = importlib.import_module(f'controller.{c}')
    rc = getattr(RC_module, c)()
    for r_r in rc.rel_rsc:
        router.get("/" + r + "/{rsc_id}/" + r_r)(pof_generator.grr_generator(r_r))

    router.post(f"/{r}",
                response_model=pof_generator.response_schema)(pof_generator.pr_generator())
    router.patch("/" + r + "/{rsc_id}",
                 response_model=pof_generator.response_schema)(pof_generator.pri_generator())
    router.delete("/" + r + "/{rsc_id}", status_code=status.HTTP_410_GONE)(pof_generator.dri_generator())

