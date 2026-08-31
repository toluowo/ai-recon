from __future__ import annotations

import argparse

from ai_recon.models import Target, TargetType
from ai_recon.services import AssessmentService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-recon",
        description=(
            "AI-assisted reconnaissance and exposure analysis "
            "for authorized security assessments."
        ),
    )

    parser.add_argument(
        "--target",
        required=True,
        help="Target identifier to assess.",
    )

    parser.add_argument(
        "--authorized",
        action="store_true",
        help=(
            "Acknowledge that you are authorized to assess "
            "the specified target."
        ),
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.authorized:
        parser.error(
            "You must provide --authorized to acknowledge "
            "authorization for the target."
        )

    target = Target(
        identifier=args.target,
        target_type=TargetType.DOMAIN,
    )

    service = AssessmentService()
    assessment = service.create_assessment(target)

    print(
        f"Assessment initialized for "
        f"{assessment.target.identifier}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
