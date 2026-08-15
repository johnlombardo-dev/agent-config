# Delivery

Read this after implementation and final verification. This reference owns Git, pull request, CI, and merge mechanics only.

## Prepare the exact result

- Resolve the intended branch, base, exact head, dirty state, remote, required CI, and repository delivery instructions.
- Run the final checks required by the parent skill and repository. Reuse unchanged successful evidence.
- Do not invoke `review-agent`, `$evidence-first-review`, `$verify-repair-seam`, or a hosted code reviewer. SSLG has no code-review phase.

## Apply the selected mode

- **No PR:** stop after final local verification. Do not push, create a pull request, or merge.
- **No merge:** commit and push the exact verified head, create or update the pull request, wait for required CI, and leave it open.
- **Draft PR:** keep the pull request draft during final verification and CI. Mark it ready before merge unless merge is forbidden.
- **Default:** commit and push the exact verified head, create or update the pull request, wait for required CI, then merge.

Do not request code review or wait for an optional reviewer. If repository policy requires approval, or an existing unresolved thread blocks delivery, report that external blocker. Do not start a review-repair loop inside SSLG.

## Finish

Before merge, confirm that required CI and mergeability apply to the exact pushed head. After merge, verify that the resulting commit contains that head. Do not report completion while CI, mergeability, or merge remains pending.
